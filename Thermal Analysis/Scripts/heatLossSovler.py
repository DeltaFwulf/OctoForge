# given innerWallTemp, wallThickness, Tambient, find heat loss through the furnace walls

# SI units unless specified

from math import sqrt, pi, exp, log

def main():

    innerWallTemp = 1373
    Tambient = 287 # see the effects of a cold winter's day

    pAmbient = 101325
    pChamber = pAmbient

    # This assumes the chamber gas mix is equal to ambient air: if you want to play with this, specify a chamber gas
    Cp = 1005
    gasConstant = 287

    innerRadius = 0.07
    wallThickness = 0.114
    outerRadius = innerRadius + wallThickness
    hCyl = 0.2
    kWall = 0.4

    # use shooting method to find the value of Ts2 that satisfies conservation of energy
    guess1 = Tambient + 100
    guess2 = innerWallTemp - 100

    tol = 1e-4
    e1 = 2 * tol

    rCyl = rWall(outerRadius, innerRadius, hCyl, kWall)
    outerArea = 2 * pi * outerRadius * hCyl

    Qcond2 = 0

    while(abs(e1) > tol):

        # wall heat loss
        Qcond1 = (innerWallTemp - guess1) / rCyl
        Qcond2 = (innerWallTemp - guess2) / rCyl

        # convection heat loss
        Qconv1 = (guess1 - Tambient) / rConv(2 * outerRadius, hCyl, guess1, Tambient, Cp, outerArea, pAmbient, gasConstant)
        Qconv2 = (guess2 - Tambient) / rConv(2 * outerRadius, hCyl, guess2, Tambient, Cp, outerArea, pAmbient, gasConstant)

        e1 = Qcond1 - Qconv1
        e2 = Qcond2 - Qconv2

        guess3 = guess1 + ((e1 / (e1 - e2)) * (guess2 - guess1))
        guess1 = guess2
        guess2 = guess3
      
    Ts2 = guess2
    Qwall = Qcond2
    print("Heat loss from wall = " + str(Qwall) + " W for Ts2 = " + str(Ts2))


def calcViscosity(Tfilm):
    
    kBoltzmann = 1.380649e-23
    mass = 4.809e-26
    sigma = 3.617e-10

    TStar = Tfilm / 97
    collisionIntegral = 1.16145 * (TStar**-0.14874) + 0.52487 * exp(-0.77320*TStar) + 2.16178 * exp(-2.43787*TStar)
    return (5 / (16 * sqrt(pi))) * ((mass * kBoltzmann * Tfilm)**0.5) / ((sigma**2) * collisionIntegral)



def calcDensity(pressure, gasConstant, temp):
    return pressure / (gasConstant * temp)



def calcConductivity(Tfilm, density):
    
    Tcrit = 132.52
    densityCrit = 313
    kCrit = 4.358e-3

    densityR = density / densityCrit
    Tr = Tfilm / Tcrit

    C1 = 33.9729025
    C2 = -164.702679
    C3 = 262.108546
    C4 = -21.5346955
    C5 = -443.455815
    C6 = 607.339582
    C7 = -368.790121
    C8 = 111.296674
    C9 = -13.4122465

    k0 = ((C1 * Tr**-1)\
        + (C2 * Tr**(-2/3))\
        + (C3 * Tr**(-1/3))\
        + C4\
        + (C5 * Tr**(1/3))\
        + (C6 * Tr**(2/3))\
        + (C7 * Tr)\
        + (C8 * Tr**(4/3))\
        + (C9 * Tr**(5/3)))
    
    D1 = 3.120130125
    D2 = -23.0762400
    D3 = 1.65049430
    D4 = -0.191148175
    
    dk =  D1 * densityR\
        + D2 * densityR**2\
        + D3 * densityR**3\
        + D4 * densityR**4
    
    return kCrit * (k0 + dk)



def rConv(diameter, L, Tsurf, Tair, Cp, area, pressure, gasConstant):

    Tfilm = (Tsurf + Tair) / 2
    viscosity = calcViscosity(Tfilm)
    density = calcDensity(pressure, gasConstant, Tfilm)
    k = calcConductivity(Tfilm, density)

    prandtl = Cp * viscosity / k
    grashof = (density**2) * 9.81 * (2 / (Tsurf + Tair)) * abs(Tsurf - Tair) * (L**3) / (viscosity**2)
    raleigh = grashof * prandtl

    # can we treat the cylinder as a vertical flat plate?
    if(diameter < 35 * L / (grashof**0.25)):
        print("Nusselt calculation may be less accurate")

    Nusselt = 0.825 + ((0.387 * raleigh**(1/6)) / ((1 + (0.492 / prandtl)**(9/16))**(8/27)))**2
    hMean = Nusselt * k / L

    return 1 / (hMean * area)



def rWall(outerRadius, innerRadius, L, kCyl):

    rWall = log(outerRadius/innerRadius) / (2 * pi * L* kCyl)
    return rWall



main()