# Calculates the heat loss from a cylinder using a resistance network

# units (unless specified)
# SI units unless specified
from math import exp, sqrt, pi

def calculateQ():

    Cp = 1005
    R = 287
    
    # ambient air parameters
    tAmbient = 287
    pAmbient = 101325
    densityAmbient = calcDensity(pAmbient, R, tAmbient)

    # chamber air parameters
    tChamber = 1100
    pChamber = pAmbient
    densityChamber = calcDensity(pChamber, R, tChamber)

    # chamber parameters
    wallThickness = 0 # Plot a surface for power_loss(thickness, temperature)
    innerRadius = 0.14
    outerRadius = innerRadius + wallThickness
    cylHeight = 0

    

def calcViscosity(Tfilm):
    
    kBoltzmann = 1.380649e-23
    mass = 4.809e-26
    sigma = 3.617e-10

    TStar = Tfilm / 97
    collisionIntegral = 1.16145 * (TStar**-0.14874) + 0.52487 * exp(-0.77320*TStar) + 2.16178 * exp(-2.43787*TStar)
    return (5 / (16 * sqrt(pi))) * ((mass * kBoltzmann * Tfilm)**0.5) / (sigma * collisionIntegral)


def calcDensity(pressure, R, temp):
    return pressure / (R * temp)


def calcConductivity(TFilm, density):
    
    Tcrit = 132.52
    densityCrit = 313
    kCrit = 4.358e-3

    densityR = density / densityCrit
    Tr = TFilm / Tcrit

    C1 = 33.9729025
    C2 = -164.702679
    C3 = 262.108546
    C4 = -21.5346955
    C5 = -443.455815
    C6 = 607.339582
    C7 = -368.790121
    C8 = 111.296674
    C9 = -13.4122465

    k0 = ((C1*Tcrit**-1)\
        + (C2 * Tcrit**(-2/3))\
        + (C3 * Tcrit**(-1/3))\
        + C4\
        + (C5 * Tcrit**(1/3))\
        + (C6 * Tcrit**(2/3))\
        + (C7 * Tcrit)\
        + (C8 * Tcrit**(4/3))\
        + (C9 * Tcrit**(5/3)))
    
    D1 = 3.120130125
    D2 = -23.0762400
    D3 = 1.65049430
    D4 = -0.191148175
    
    dk =  D1 * densityR\
        + D2 * densityR**2\
        + D3 * densityR**3\
        + D4 * densityR**4
    
    return kCrit * (k0 + dk)


def rConv(diameter, L, Tsurf, Tair, Cp, density):

    Tfilm = (Tsurf + Tair) / 2
    viscosity = calcViscosity(Tfilm)
    k = calcConductivity(Tfilm)

    prandtl = Cp * viscosity / k
    grashof = (density**2) * 9.81 * (2 / (Tsurf + Tair)) * abs(Tsurf - Tair) * (L**3) / (viscosity**2)
    raleigh = grashof * prandtl

    # can we treat the cylinder as a vertical flat plate?
    if(diameter > 35 * L / (grashof**0.25)):
        Nusselt = 0.825 + ((0.387 * raleigh**(1/6)) / ((1 + (0.492 / prandtl)**(9/16))**(8/27)))**2
    else:
        print("Nusselt conditions are not met")
        Nusselt = 0

    # Calculate the convection resistance from these values
