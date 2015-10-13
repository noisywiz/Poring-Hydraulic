# coding: utf8

"""Class for hydraulic calculation."""
# Author: noisywiz

class PoringHydraulic:
    """
    In:
        Tube:
            d - Inner diameter, m
            k_r - Absolute roughness, m
            ksi - Local resistance coefficient

        Pumped medium:
            g   - Flow, m3/s
            nu  - Kinematic viscosity, m2/s
            ro  - Density, kg/m3

    Out:
        w - Speed in section, m/s
        re - Reynolds number
        lmd - Friction coefficient
        lidrop - Specific linear pressure drop, Pa/m
        lodrop - Pressure drop at the local resistances, Pa

    """

    def __init__(
            self, k_r=0.00001, nu=0.000001787, ro=1000,
            d=0.0, g=0.0, w=False, re=False, lmd=False, ksi=False
    ):

        self.k_r = k_r
        self.nu = nu
        self.ro = ro
        self.d = d
        self.g = g
        self.w = w
        self.re = re
        self.lmd = lmd
        self.ksi = ksi
        self.lidrop = False
        self.lodrop = False

        # Getting all of the other attributes: w, re, lmd, lidrop, lodrop.
        self.local_drop()

    def speed(self):

        """ Speed in cross sectional area, m/s. """

        try:
            self.w = 4 * self.g / (3.1415 * pow(self.d, 2))

        except ZeroDivisionError:
            self.w = 0.0

        return self.w


    def reynolds(self):

        """ Reynolds number """

        if not self.w:
            self.w = self.speed()

        self.re = self.w * self.d / self.nu

        return self.re


    def lambda_(self):

        """ Friction coefficient """

        wtf = 0.0
        base = 0.0
        lm = 0.0

        try:
            if not self.re:
                self.re = self.reynolds()

            wtf = 568 * self.d / self.k_r  # it's just a book...

            if (self.re < wtf and self.re > 2300):
                base = (self.k_r / self.d + 68 / self.re)
                lm = 0.11 * pow(base, 0.25)

            elif (self.re < 2300):
                lm = 64 / self.re

            else:
                lm = 0.11 * pow(self.k_r / self.d, 0.25)

        except ZeroDivisionError:
            lm = 0.0

        self.lmd = lm
        return lm


    def linear_drop(self):

        """ Specific linear pressure drop, Pa/m. """

        if not self.w:
            self.w = self.speed()

        if not self.lmd:
            self.lmd = self.lambda_()

        try:
            self.lidrop = self.lmd * pow(self.w, 2) * self.ro / (2 * self.d)

        except ZeroDivisionError:
            self.lidrop = 0.0

        return self.lidrop


    def local_drop(self):

        """ Pressure drop at the local resistances, Pa. """

        if not self.lidrop:
            self.lidrop = self.linear_drop()

        if not self.ksi:
            self.lodrop = 0.0
            return 0.0

        else:
            try:
                l_eq = self.ksi * self.d / self.lmd  # m
                self.lodrop = l_eq * self.lidrop

            except ZeroDivisionError:
                self.lodrop = 0.0

            return self.lodrop


class PipeExtension:

    """ Not yet. """

    MM_TO_M = 0.001
    M3H_TO_M3S = 0.000277778
    LS_TO_M3S = 0.001

    # Standard dimension:
    X_DMN = {
        0: False,  # PoringHydraulic dimension
        1: MM_TO_M,  # mm -> m
        2: M3H_TO_M3S,  # m3/h -> m3/s
        3: LS_TO_M3S  # l/s -> m3/s
    }

    # Outer diameter of some types of pipe:
    PP_PN20 = {
        '20': 14.4,  # 20x2.8
        '25': 18.0,  # 25x3.5
        '32': 23.2,  # 32x4.4
        '40': 29.0,  # 40x5.5
        '50': 36.2,  # 50x6.9
        '63': 45.8  # 63x8.6
    }
    VGP_GOST_3262_75 = {
        '15': 9.4,  # 15x2.8
        '20': 14.4,  # 20x2.8
        '25': 18.6,  # 25x3.2
        '32': 25.6,  # 32x3.2
        '40': 33.0,  # 40x3.5
        '50': 43.0,  # 50x3.5
        '65': 57.0,  # 65x4.0
        '80': 72.0,  # 80x4.0
        '100': 91.0  # 100x4.5
    }

    #Absolute roughness, m
    ABS_ROUGHNESS = {
        'PP_PN20': 0.00001,
        'VGP_GOST_3262_75': 0.0005
    }


    def __init__(self, d=0.0, d_dmn=X_DMN[0], g=0.0, g_dmn=X_DMN[0], pipe=False, outer_diameter=False):

        self.d_dmn = d_dmn
        self.g_dmn = g_dmn
        self.g = self.convert(g, g_dmn)
        self.pipe = pipe
        self.outer_diameter = outer_diameter

        if not pipe:
            self.d = self.convert(d, d_dmn)
        else:
            self.d = self.pipe_to_inner_d()


    def convert(cls, x, x_dmn):

        if not x_dmn:
            return x
        return x * x_dmn


    def pipe_to_inner_d(self):

        return self.pipe[self.outer_diameter]


