## PoringHydraulic class
Class for hydraulic calculation

Usage:
```
import prghydraulic
h1=prghydraulic.PoringHydraulic(g=0.015, d=0.03, ksi=1.75)
print (h1.lodrop, h1.re) # Pressure drop at the local resistances (Pa), Reynolds number

In:

- d - Inner diameter, m
- k_r - Absolute roughness, m
- ksi - Local resistance coefficient
- g   - Flow, m3/s
- nu  - Kinematic viscosity, m2/s
- ro  - Density, kg/m3

Out:

- w - Speed in section, m/s
- re - Reynolds number
- lmd - Friction coefficient
- lidrop - Specific linear pressure drop, Pa/m
- lodrop - Pressure drop at the local resistances, Pa
```


## PipeExtension class

Usage:
```
import prghydraulic
d1=PipeExtension(pipe=PipeExtension.PP_PN20, outer_diameter='40')
print (d1.d) # inner diameter
```
