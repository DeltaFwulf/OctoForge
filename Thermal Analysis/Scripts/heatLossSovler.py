# given innerWallTemp, wallThickness, Tambient, find heat loss through the furnace walls
# SI units unless specified

# XXX: we could linearly blend between different Nusselt correlations to remove discontinuities

from math import sqrt, pi, exp, log, ceil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def main():

    innerWallTemp = 1373
    Tambient = 288
    pAmbient = 101325

    # this is air
    Cp = 1005
    gasConstant = 287

    chamberRadius = 0.035
    lidThickness = 0.076
    baseThickness = 0.076

    chamberHeight = 0.145
    kBrick = 0.4
    kRockWool = 0.2
    kSteel = 54

    brickThickness = 76e-3
    rockWoolThickness = 100e-3
    casingThickness = 2e-3

    conductivities = [kBrick, kRockWool, kSteel]
    thicknesses = [brickThickness, rockWoolThickness, casingThickness]

    outerRadius = chamberRadius + brickThickness + rockWoolThickness + casingThickness
    wallResistance = getLayerResistances(chamberRadius, chamberHeight, conductivities, thicknesses)

    outerWallTemp, Qwall = cylinderQSolver(innerWallTemp, outerRadius, chamberHeight, wallResistance, Tambient, pAmbient, Cp, gasConstant)
    
    # assume the lid and base are the width of the furnace (slightly conservative)
    perimiter = 2 * pi * (chamberRadius + sum(thicknesses))
    area = pi * (chamberRadius + sum(thicknesses))**2

    outerLidTemp, Qlid = planeQSolver(area, perimiter, lidThickness, Tambient, Cp, gasConstant, pAmbient, kBrick, "top")
    outerBaseTemp, Qbase = planeQSolver(area, perimiter, baseThickness, Tambient, Cp, gasConstant, pAmbient, kBrick, "bottom")

    print("Heat loss from wall = " + str(Qwall) + " W for outer temp = " + str(outerWallTemp - 273.15) + " C")
    print("Heat loss from lid = " + str(Qlid) + " W for outer temp = " + str(outerLidTemp - 273.15) + " C")
    print("Heat loss from base = " + str(Qbase) + " W for outer temp = " + str(outerBaseTemp - 273.15) + " C")

    QvsChamberTemp(chamberRadius, thicknesses, chamberHeight, wallResistance, Tambient, pAmbient, Cp, gasConstant)
    wallTemperatureDistribution(innerWallTemp, chamberRadius, thicknesses, conductivities, chamberHeight, Qwall)
    plt.show()




# calculate the total thermal resistance of a multilayer cylindrical wall
def getLayerResistances(chamberRadius, chamberHeight, conductivities, thicknesses):

    """General Solution"""
    rWall = 0

    for i in range(len(conductivities)):

        if(i == 0):
            innerRadius = chamberRadius
        else:
            innerRadius = chamberRadius + sum(thicknesses[:i])
        
        outerRadius = innerRadius + thicknesses[i]

        rWall += log(outerRadius / innerRadius) / (2 * pi * chamberHeight * conductivities[i])

    return rWall



def calcViscosity(fluidTemp):
    
    boltzmannConst = 1.380649e-23
    mass = 4.809e-26
    sigma = 3.617e-10

    TStar = fluidTemp / 97
    collisionIntegral = 1.16145 * (TStar**-0.14874) + 0.52487 * exp(-0.77320*TStar) + 2.16178 * exp(-2.43787*TStar)
    return (5 / (16 * sqrt(pi))) * ((mass * boltzmannConst * fluidTemp)**0.5) / ((sigma**2) * collisionIntegral)



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



def calcConvectiveResistance(diameter, L, Tsurf, Tair, Cp, area, pressure, gasConstant):

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



# The steady state condition is satisfied when the heat loss through the wall is equal to the heat loss from the wall to the surrounding air via convection.
def cylinderQSolver(innerWallTemp, outerRadius, hCyl, wallResistance, Tambient, pAmbient, Cp, gasConstant) -> tuple[float, float]:
    
    guess1 = Tambient + 100
    guess2 = innerWallTemp - 100

    tol = 1e-4
    e1 = 2 * tol
    Qcond2 = 0

    outerArea = 2 * pi * outerRadius * hCyl

    while(abs(e1) > tol):

        # conductive heat loss through wall
        Qcond1 = (innerWallTemp - guess1) / wallResistance
        Qcond2 = (innerWallTemp - guess2) / wallResistance

        # heat loss via convection at outer wall
        Qconv1 = (guess1 - Tambient) / calcConvectiveResistance(2 * outerRadius, hCyl, guess1, Tambient, Cp, outerArea, pAmbient, gasConstant)
        Qconv2 = (guess2 - Tambient) / calcConvectiveResistance(2 * outerRadius, hCyl, guess2, Tambient, Cp, outerArea, pAmbient, gasConstant)

        e1 = Qcond1 - Qconv1
        e2 = Qcond2 - Qconv2

        if(e1 == e2 and abs(e2) < tol):
            break

        guess3 = guess1 + ((e1 / (e1 - e2)) * (guess2 - guess1))
        guess1 = guess2
        guess2 = guess3
    
    return guess2, Qcond2



# get the mean convective thermal resistance of a horizontal planar wall
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



# calculates the heat loss from, and outer surface temperature of, a horizontal planar wall
def planeQSolver(area, perimiter, thickness, Tambient, Cp, gasConstant, pAmbient, kWall, side) -> tuple[float, float]:

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



"""PLOTTING FUNCTIONS"""



def QvsWallThickness(innerWallTemp, chamberRadius, hCyl, casingThickness, conductivities, Tambient, pAmbient, Cp, gasConstant):

    brickThickness = np.linspace(0.001, 1, 100)
    rockWoolThickness = np.linspace(0.001, 1, 100)
    heatLoss = np.zeros((brickThickness.size, rockWoolThickness.size))
    TouterWall = np.zeros((brickThickness.size, rockWoolThickness.size))

    for i in range(brickThickness.size):
        for j in range(rockWoolThickness.size):

            rCyl = getLayerResistances(chamberRadius, hCyl, conductivities, [brickThickness[i], rockWoolThickness[j], casingThickness])
            heatLoss[i, j] = cylinderQSolver(innerWallTemp, chamberRadius + brickThickness[i] + rockWoolThickness[j] + casingThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)[1]
        
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

        rCyl = getLayerResistances(chamberRadius, hCyl, conductivities, [brickThickness, rockWoolThickness[i], casingThickness])
        outerWallTemp[i], heatLoss[i] = cylinderQSolver(innerWallTemp, chamberRadius + brickThickness + rockWoolThickness[i] + casingThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)

    plt.figure(10)
    plt.plot(rockWoolThickness * 1000, heatLoss, '-')
    plt.plot([0, 1000], [200, 200], '--r')
    plt.plot([0, 1000], [150, 150], '--g')
    plt.xlabel("rockwool thickness (mm)")
    plt.ylabel("heat loss (W)")

    plt.figure(11)
    plt.plot(rockWoolThickness * 1000, outerWallTemp - 273, '-r')
    plt.xlabel("rockwool thickness (mm)")
    plt.ylabel("outer wall temperature (C)")



def QvsChamberTemp(chamberRadius, thicknesses, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant):

    Tchamber = np.linspace(500, 1373, 100)
    heatLoss = np.zeros(Tchamber.size)
    outerWallTemp = np.zeros(Tchamber.size)

    for i in range(0, Tchamber.size):
        outerWallTemp[i], heatLoss[i] = cylinderQSolver(Tchamber[i], chamberRadius + thicknesses[0] + thicknesses[1] + thicknesses[2], hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)
        
    TchamberC = Tchamber - 273
    outerWallTempC = outerWallTemp - 273

    plt.figure(20)
    plt.plot(TchamberC, outerWallTempC, '-')
    #plt.plot([TchamberC[0], TchamberC[heatLoss.size - 1]], [outerWallTempC[0], outerWallTempC[heatLoss.size - 1]], '--r')
    plt.xlabel("chamber temperature (C)")
    plt.ylabel("outer wall temp (C)")
    plt.title("Ts3 vs Tchamber")

    plt.figure(21)
    plt.plot(TchamberC, heatLoss, 'b-')
    plt.xlabel("chamber temperature (C)")
    plt.ylabel("heat loss (W)")
    plt.title("Q vs Tchamber")
    


# takes the heat loss through the material to work out temperature distribution through all wall layers of a multilayer cylinder
def wallTemperatureDistribution(chamberTemp, chamberRadius, layerThicknesses, layerConductivities, chamberHeight, Q):

    targetResolution = 1e-4

    # for each layer, calculate the inner temperature distribution
    tempDistribution = np.array([], dtype=float)
    radii = np.array([], dtype=float)
    
    for i in range(len(layerThicknesses)):

        r0 = chamberRadius if i == 0 else chamberRadius + sum(layerThicknesses[:i])
        T0 = chamberTemp if i == 0 else tempDistribution[tempDistribution.size - 1]

        layerPoints = np.linspace(r0, r0 + layerThicknesses[i], num=ceil(layerThicknesses[i] / targetResolution))
        radii = np.append(radii, layerPoints)
        
        # solve for temperature at each layerPoint
        layerTemps = np.empty((layerPoints.size), dtype=float)
        for j in range(layerPoints.size):
            layerTemps[j] = T0 - (Q * log(layerPoints[j] / layerPoints[0]) / (2 * pi * chamberHeight * layerConductivities[i]))

        tempDistribution = np.append(tempDistribution, layerTemps)

    # plot the temperature distribution, denoting layer boundaries
    tempDistributionC = tempDistribution - 273

    plt.figure(30)
    plt.plot(radii, tempDistributionC, '-r')
    
    for i in range(len(layerThicknesses)):
        plt.plot([chamberRadius + sum(layerThicknesses[:i]), chamberRadius + sum(layerThicknesses[:i])], [tempDistributionC[0], tempDistributionC[tempDistributionC.size - 1]], '--k')

    plt.title("Wall Temperature Distribution")  
    plt.xlabel("radius, mm")
    plt.ylabel("temperature, C")
     


main()