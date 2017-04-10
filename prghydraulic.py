# coding: utf8

"""Class for hydraulic calculation."""
# Author: noisywiz


class PipeExtension:
    PIPE_LIST = [
        "PP_PN20",
        "VGP_GOST_3262_75"
    ]
    NAME = ""
    ABS_ROUGHNESS = 0.0
    INNER_DIAMETER = 0.0
    OUTER_DIAMETER = 0.0

    def get_in_d(self):
        return self.INNER_DIAMETER

    def get_out_d(self):
        return self.OUTER_DIAMETER

    def get_abs_roughness(self):
        return self.ABS_ROUGHNESS


class PipeCreator:
    def factory_method(index):
        if index == 0:
            return PP_PN20()
        else:
            if index == 1:
                return VGP_GOST_3262_75()
            else:
                return VGP_GOST_3262_75()


class PP_PN20(PipeExtension):
    NAME = "PP_PN20"
    ABS_ROUGHNESS = 0.00001
    INNER_DIAMETER = [
        14.4,  # 20x2.8
        18.0,  # 25x3.5
        23.2,  # 32x4.4
        29.0,  # 40x5.5
        36.2,  # 50x6.9
        45.8   # 63x8.6
    ]
    OUTER_DIAMETER = [
        "20x2.8",
        "25x3.5",
        "32x4.4",
        "40x5.5",
        "50x6.9",
        "63x8.6"
    ]


class VGP_GOST_3262_75(PipeExtension):
    NAME = "VGP_GOST_3262_75"
    ABS_ROUGHNESS = 0.0005
    INNER_DIAMETER = [
        15.0,  # 15x2.8
        20.0,  # 20x2.8
        25.0,  # 25x3.2
        32.0,  # 32x3.2
        40.0,  # 40x3.5
        50.0,  # 50x3.5
        65.0,  # 65x4.0
        80.0,  # 80x4.0
        100.0, # 100x4.5
        125.0, # "125x4.5"
        150.0 # "150x4.5"
    ]
    OUTER_DIAMETER = [
        "15x2.8",
        "20x2.8",
        "25x3.2",
        "32x3.2",
        "40x3.5",
        "50x3.5",
        "65x4.0",
        "80x4.0",
        "100x4.5",
        "125x4.5",
        "150x4.5"
    ]


# Dimension extension
class DimensionExtension:
    MM_TO_M = 0.001
    M3H_TO_M3S = 0.000277778
    LS_TO_M3S = 0.001
    # Standard dimension:
    X_DMN = [
        MM_TO_M,  # * mm -> m
        1,  # nope
    ]
    G_DMN = [
        M3H_TO_M3S,
        LS_TO_M3S,
        1,  # nope
    ]

    def convert(cls, x, x_dmn, atr=1.0):
        return x*x_dmn*atr


class PoringHydraulic:

    def __init__(self, k_r_src, nu_src, ro_src, d_src, g_src, ksi_src):
        self.w = 0.0
        self.k_r = k_r_src  # m
        self.nu = nu_src
        self.ro = ro_src  # kg/m3
        self.d = d_src  # m
        self.g = g_src  # m3/s
        self.re = 0.0
        self.lmd = 0.0
        self.ksi = ksi_src
        self.lidrop = 0.0  # Pa/m
        self.lodrop = 0.0  # Pa
        self.local_drop()

    def speed(self):
        try:
            self.w = 4*self.g / (3.1415*pow(self.d, 2))
        except ZeroDivisionError:
            self.w = 0
        return self.w

    def reynolds(self):
        if self.w == 0:
            self.w = self.speed()
        self.re = self.w*self.d/self.nu
        return self.re

    def _lambda(self):
        wtf = 0.0
        poring_base = 0.0
        lm = 0.0

        try:
            if self.re == 0:
                self.re = self.reynolds()
            wtf = 568*self.d/self.k_r
            if self.re < wtf and self.re > 2300:
                poring_base = (self.k_r/self.d + 68/self.re)
                lm = 0.11*pow(poring_base, 0.25)

            elif self.re < 2300:
                lm = 64/self.re
            else:
                lm = 0.11*pow(self.k_r/self.d, 0.25)

        except ZeroDivisionError:
            lm = 0.0

        self.lmd = lm
        return self.lmd

    def linear_drop(self):

        if self.w == 0:
            self.w = self.speed()
        if self.lmd == 0:
            self.lmd = self._lambda()
        try:
            self.lidrop = self.lmd * pow(self.w, 2) * self.ro / (2 * self.d)

        except ZeroDivisionError:
            self.lidrop = 0.0

        return self.lidrop

    def local_drop(self):

        if self.lidrop == 0:
            self.lidrop = self.linear_drop()
        if self.ksi == 0:
            self.lodrop = 0.0
            return 0.0
        else:
            try:
                l_eq = self.ksi * self.d / self.lmd
                self.lodrop = l_eq * self.lidrop
            except ZeroDivisionError:
                self.lodrop = 0.0
            return self.lodrop
