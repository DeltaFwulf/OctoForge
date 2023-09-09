# given innerWallTemp, wallThickness, Tambient, find heat loss through the furnace walls
# SI units unless specified

# TODO instead of just printing "nusselt calcualation may be less accurate", tag the result with an approval or rejection of final result
# TODO we could linearly blend between different Nusselt correlations to remove discontinuities

from math import sqrt, pi, exp, log
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from random import uniform

def main():

    innerWallTemp = 1373
    Tambient = 273.15 + 15
    pAmbient = 101325
    Cp = 1005
    gasConstant = 287

    chamberRadius = 0.035
    lidThickness = 0.076
    baseThickness = 0.076

    hCyl = 0.145
    kBrick = 0.4
    kRockWool = 0.2
    kWood = 0.3

    brickThickness = 0.076
    rockWoolThickness = 0.2
    casingThickness = 0.012

    conductivities = [kBrick, kRockWool, kWood]
    thicknesses = [brickThickness, rockWoolThickness, casingThickness]

    outerRadius = chamberRadius + brickThickness + rockWoolThickness + casingThickness
    rCyl = rWall(chamberRadius, hCyl, conductivities, thicknesses)

    outerWallTemp, Qwall = wallHeatLoss(innerWallTemp, outerRadius, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)
    
    # assume the lid and base are the width of the furnace (slightly conservative)
    perimiter = 2 * pi * (chamberRadius + sum(thicknesses))
    area = pi * (chamberRadius + sum(thicknesses))**2

    outerLidTemp, Qlid = planarWallHeatLoss(area, perimiter, lidThickness, Tambient, Cp, gasConstant, pAmbient, kBrick, "top")
    outerBaseTemp, Qbase = planarWallHeatLoss(area, perimiter, baseThickness, Tambient, Cp, gasConstant, pAmbient, kBrick, "bottom")

    print("Heat loss from wall = " + str(Qwall) + " W for outer temp = " + str(outerWallTemp - 273.15) + " C")
    print("Heat loss from lid = " + str(Qlid) + " W for outer temp = " + str(outerLidTemp - 273.15) + " C")
    print("Heat loss from base = " + str(Qbase) + " W for outer temp = " + str(outerBaseTemp - 273.15) + " C")

    QvsWallThickness(innerWallTemp, chamberRadius, hCyl, casingThickness, conductivities, Tambient, pAmbient, Cp, gasConstant)
    QvsRockWoolThickness(innerWallTemp, chamberRadius, hCyl, casingThickness, conductivities, Tambient, pAmbient, Cp, gasConstant)
    #QvsChamberTemp(chamberRadius, wallThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)
    plt.show()



# FIXME the general solution produces a different result to the manual solution; resolve this
def rWall(chamberRadius, hCyl, conductivities, thicknesses):

    """General Solution"""
    rWall = 0

    for i in range(len(conductivities)):

        if(i == 0):
            innerRadius = chamberRadius
        else:
            innerRadius = chamberRadius + sum(thicknesses[:i])
        
        outerRadius = innerRadius + thicknesses[i]

        rWall += log(outerRadius / innerRadius) / (2 * pi * hCyl * conductivities[i])

    return rWall



def calcViscosity(Tfilm):
    
    kBoltzmann = 1.380649e-23
    mass = 4.809e-26
    sigma = 3.617e-10

    TStar = Tfilm / 97
    collisionIntegral = 1.16145 * (TStar**-0.14874) + 0.52487 * exp(-0.77320*TStar) + 2.16178 * exp(-2.43787*TStar)
    return (5 / (16 * sqrt(pi))) * ((mass * kBoltzmann * Tfilm)**0.5) / ((sigma**2) * collisionIntegral)



def calcDensity(pressure, gasConstant, temp):
    return pressure / (gasConstant * temp)



def calcGrashof(Tsurf, Tfluid, length, density, viscosity):
    return (density**2) * 9.81 * (2 / (Tsurf + Tfluid)) * abs(Tsurf - Tfluid) * (length**3) / (viscosity**2)


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



def rConvCyl(diameter, L, Tsurf, Tair, Cp, area, pressure, gasConstant):

    Tfilm = (Tsurf + Tair) / 2
    viscosity = calcViscosity(Tfilm)
    density = calcDensity(pressure, gasConstant, Tfilm)
    k = calcConductivity(Tfilm, density)

    prandtl = Cp * viscosity / k
    grashof = calcGrashof(Tsurf, Tair, L, density, viscosity)
    raleigh = grashof * prandtl

    # can we treat the cylinder as a vertical flat plate?
    if(diameter < 35 * L / (grashof**0.25)):
        print("Nusselt calculation may be less accurate")

    Nusselt = 0.825 + ((0.387 * raleigh**(1/6)) / ((1 + (0.492 / prandtl)**(9/16))**(8/27)))**2
    hMean = Nusselt * k / L

    return 1 / (hMean * area)



# use shooting method to find the value of Ts2 that satisfies conservation of energy
def wallHeatLoss(innerWallTemp, outerRadius, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant):
    guess1 = Tambient + 100
    guess2 = innerWallTemp - 100

    tol = 1e-4
    e1 = 2 * tol
    Qcond2 = 0

    outerArea = 2 * pi * outerRadius * hCyl

    while(abs(e1) > tol):

        # wall heat loss
        Qcond1 = (innerWallTemp - guess1) / rCyl
        Qcond2 = (innerWallTemp - guess2) / rCyl

        # convection heat loss
        Qconv1 = (guess1 - Tambient) / rConvCyl(2 * outerRadius, hCyl, guess1, Tambient, Cp, outerArea, pAmbient, gasConstant)
        Qconv2 = (guess2 - Tambient) / rConvCyl(2 * outerRadius, hCyl, guess2, Tambient, Cp, outerArea, pAmbient, gasConstant)

        e1 = Qcond1 - Qconv1
        e2 = Qcond2 - Qconv2

        if(e1 == e2 and abs(e2) < tol):
            break

        guess3 = guess1 + ((e1 / (e1 - e2)) * (guess2 - guess1))
        guess1 = guess2
        guess2 = guess3
    
    return guess2, Qcond2



def rConvPlane(hotSide, Tsurface, Tfluid, L, Cp, gasConstant, pressure, area):

    Tfilm = (Tsurface + Tfluid) / 2
    density = calcDensity(pressure, gasConstant, Tfilm)
    viscosity = calcViscosity(Tfilm)
    filmConductivity = calcConductivity(Tfilm, density)

    prandtl = Cp * viscosity / filmConductivity
    grashof = calcGrashof(Tsurface, Tfluid, L, density, viscosity)
    raleigh = grashof * prandtl
    nusselt = 1

    if((hotSide == "top" and Tsurface > Tfluid) or (hotSide == "bottom" and Tsurface < Tfluid)):
        
        if(raleigh >= 1e4 and raleigh <= 1e7):
            nusselt = 0.54 * (raleigh**0.25)

        elif(raleigh > 1e7 and raleigh <= 1e11):
            nusselt = 0.15 * (raleigh**(1/3))
        
    elif(raleigh >= 1e5 and raleigh <= 1e11):
        nusselt = 0.27 * (raleigh**0.25)

    elif(raleigh > 5e3 and raleigh < 1e5):
        nusselt = 1.611 * (raleigh**0.145)

    hMean = nusselt * filmConductivity / L
    return 1 / (hMean * area)




def planarWallHeatLoss(area, perimiter, thickness, Tambient, Cp, gasConstant, pAmbient, kWall, side):

    L = area / perimiter
    rCond = thickness / (kWall * area)

    guess1 = Tambient + 50
    guess2 = Tambient * 2    

    tol = 1e-4
    e1 = 2 * tol
    Qcond2 = 0

    kRelaxation = 0.1

    while(abs(e1) > tol):

        Qconv1 = (guess1 - Tambient) / rConvPlane(side, guess1, Tambient, L, Cp, gasConstant, pAmbient, area)
        Qconv2 = (guess2 - Tambient) / rConvPlane(side, guess2, Tambient, L, Cp, gasConstant, pAmbient, area)

        Qcond1 = (guess1 - Tambient) / rCond
        Qcond2 = (guess2 - Tambient) / rCond

        e1 = Qcond1 - Qconv1
        e2 = Qcond2 - Qconv2

        if(e1 == e2 and abs(e2) < tol):
            break

        guess3 = guess1 + ((e1 / (e1 - e2)) * (guess2 - guess1))
        guess1 = guess1 + (kRelaxation * (guess2 - guess1))
        guess2 = guess2 + (kRelaxation * (guess3 - guess2))

    return guess2, Qcond2



# TODO: this needs to be a surface plot against both brick and rockwool thicknesses
def QvsWallThickness(innerWallTemp, chamberRadius, hCyl, casingThickness, conductivities, Tambient, pAmbient, Cp, gasConstant):

    brickThickness = np.linspace(0.001, 1, 100)
    rockWoolThickness = np.linspace(0.001, 1, 100)
    heatLoss = np.zeros((brickThickness.size, rockWoolThickness.size))
    TouterWall = np.zeros((brickThickness.size, rockWoolThickness.size))

    for i in range(brickThickness.size):
        for j in range(rockWoolThickness.size):

            rCyl = rWall(chamberRadius, hCyl, conductivities, [brickThickness[i], rockWoolThickness[j], casingThickness])
            heatLoss[i, j] = wallHeatLoss(innerWallTemp, chamberRadius + brickThickness[i] + rockWoolThickness[j] + casingThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)[1]
        
    fig = plt.figure(0)    
    # surface plot against both wall thicknesses

    brickThickness, rockWoolThickness = np.meshgrid(brickThickness, rockWoolThickness)

    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(brickThickness * 1000, rockWoolThickness * 1000, heatLoss, cmap=cm.inferno)
    ax.set_xlabel("brick thickness (mm)")
    ax.set_ylabel("rockwool thickness (mm)")
    ax.set_zlabel("heat loss (W)")



def QvsRockWoolThickness(innerWallTemp, chamberRadius, hCyl, casingThickness, conductivities, Tambient, pAmbient, Cp, gasConstant):

    brickThickness = 0.076
    rockWoolThickness = np.linspace(0.001, 1, 100)
    heatLoss = np.empty(rockWoolThickness.size)
    outerWallTemp = np.empty(rockWoolThickness.size)

    for i in range(0, rockWoolThickness.size):

        rCyl = rWall(chamberRadius, hCyl, conductivities, [brickThickness, rockWoolThickness[i], casingThickness])
        outerWallTemp[i], heatLoss[i] = wallHeatLoss(innerWallTemp, chamberRadius + brickThickness + rockWoolThickness[i] + casingThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)

    plt.figure(3)
    plt.plot(rockWoolThickness * 1000, heatLoss, '-')
    plt.plot([0, 1000], [200, 200], '--r')
    plt.plot([0, 1000], [150, 150], '--g')
    plt.xlabel("rockwool thickness (mm)")
    plt.ylabel("heat loss (W)")

    plt.figure(4)
    plt.plot(rockWoolThickness * 1000, outerWallTemp - 273, '-r')
    plt.xlabel("rockwool thickness (mm)")
    plt.ylabel("outer wall temperature (C)")



def QvsChamberTemp(innerRadius, wallThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant):

    Tchamber = np.linspace(500, 1373, 100)
    heatLoss = np.zeros(Tchamber.size)
    outerWallTemp = np.zeros(Tchamber.size)

    for i in range(0, Tchamber.size):
        outerWallTemp[i], heatLoss[i] = wallHeatLoss(Tchamber[i], innerRadius + wallThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)
        
    plt.figure(1)
    plt.plot(Tchamber - 273.15, outerWallTemp - 273.15, '-')
    plt.plot([Tchamber[0] - 273, Tchamber[Tchamber.size - 1] - 273], [outerWallTemp[0] - 273, outerWallTemp[heatLoss.size - 1] - 273], '--r')
    plt.xlabel("chamber temperature (C)")
    plt.ylabel("outer wall temp (C)")
    plt.title("Ts3 vs Tchamber")

    plt.figure(2)
    plt.plot(Tchamber - 273.15, heatLoss, 'b-')
    plt.xlabel("chamber temperature (C)")
    plt.ylabel("heat loss (W)")
    plt.title("Q vs Tchamber")
    


main()