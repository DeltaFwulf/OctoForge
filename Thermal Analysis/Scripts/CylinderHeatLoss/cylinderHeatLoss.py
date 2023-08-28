# Calculates the heat loss from a cylinder using a resistance network

# SI units unless specified
from math import exp, sqrt, pi, log
import numpy as np
import matplotlib.pyplot as plt

def main():

    # ambient conditions
    Tambient = 287
    pAmbient = 101325
    Cp = 1005 # TODO: change Cp and R for chamber gas if using a different mix
    gasConstant = 287

    # chamber conditions
    pChamber = pAmbient

    # fixed furnace parameters
    rInner = 0.07 # TODO: get this from the crucible size (need to order a crucible)
    hCyl = 0.2
    kWall = 0.4 # W/m*K

    # Solve the furnace design condition:
    Tchamber = 1373

    rOuter, QWall = calcWallThickness(Tchamber, rInner, 373, hCyl, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall)
    print("wall thickness: " + str((rOuter - rInner) * 1000) + " mm, heat loss: " + str(QWall) + " W for Tchamber = " + str(Tchamber) + " K")



def calcViscosity(Tfilm):
    
    kBoltzmann = 1.380649e-23
    mass = 4.809e-26
    sigma = 3.617e-10

    TStar = Tfilm / 97
    collisionIntegral = 1.16145 * (TStar**-0.14874) + 0.52487 * exp(-0.77320*TStar) + 2.16178 * exp(-2.43787*TStar)
    return (5 / (16 * sqrt(pi))) * ((mass * kBoltzmann * Tfilm)**0.5) / ((sigma**2) * collisionIntegral)



def calcDensity(pressure, gasConstant, temp):
    return pressure / (gasConstant * temp)



# this is returning negative for some reason
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

    #print("Tfilm: " + str(Tfilm))
    #print("viscosity: " + str(viscosity))
    #print("density: " + str(density))
    #print("conductivity: " + str(k))

    prandtl = Cp * viscosity / k
    grashof = (density**2) * 9.81 * (2 / (Tsurf + Tair)) * abs(Tsurf - Tair) * (L**3) / (viscosity**2)
    raleigh = grashof * prandtl

    # can we treat the cylinder as a vertical flat plate?
    #if(diameter > 35 * L / (grashof**0.25)):
    Nusselt = 0.825 + ((0.387 * raleigh**(1/6)) / ((1 + (0.492 / prandtl)**(9/16))**(8/27)))**2
    hMean = Nusselt * k / L

    return 1 / (hMean * area)



def rCond(outerRadius, innerRadius, L, kCyl):

    rCond = log(outerRadius/innerRadius) / (2 * pi * L* kCyl)
    return rCond



def calcTs1(Rcyl, Ts2, Q):

    tol = 1e-5
    e1 = 2 * tol

    # use a shooting method to obtain Ts1
    g1 = 2 * Ts2
    g2 = Ts2 + 10

    # get heat flow errors for both 
    while(abs(e1) > tol):

        e1 = Q - ((g1 - Ts2) / Rcyl)
        e2 = Q - ((g2 - Ts2) / Rcyl)

        if(e1 == e2 and abs(e1) < tol):
            return g2
        else:
            g3 = g1 + ((e1 / (e1 - e2)) * (g2 - g1))
            g1 = g2
            g2 = g3
        
    return g2 # TODO: should this actually be g3?



def calcTchamber(rInner, rOuter, hCyl, Ts2, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall):
    
    As1 = pi * (rInner**2) * hCyl
    As2 = pi * (rOuter**2) * hCyl

    # Calculate heat flow through the outer wall
    rConv2 = rConv(2 * rOuter, hCyl, Ts2, Tambient, Cp, As2, pAmbient, gasConstant)
    Q = (Ts2 - Tambient) / rConv2
    print("calcTchamber: heat loss at outer wall = " + str(Q))

    # calculate Ts1
    rCyl = rCond(rOuter, rInner, hCyl, kWall)
    Ts1 = calcTs1(rCyl, Ts2, Q)
    
    print("Ts1: " + str(Ts1))   

    tol = 1e-5
    e1 = 2 * tol
    Q2 = -1 # use for error checking

    g1 = Ts1 * 1.5
    g2 = Ts1 + 1

    while(abs(e1) > tol):

        # Calculate heat loss from the wall
        Q1 = (g1 - Ts1) / rConv(2 * rInner, hCyl, Ts1, g1, Cp, As1, pChamber, gasConstant)
        Q2 = (g2 - Ts1) / rConv(2 * rInner, hCyl, Ts1, g2, Cp, As1, pChamber, gasConstant) # you little shit

        e1 = Q - Q1
        e2 = Q - Q2

        #print("g1: " + str(g1) + ", g2: " + str(g2))
        #print("e1: " + str(e1) + ", e2: " + str(e2))

        g3 = g1 + ((e1 / (e1 - e2)) * (g2 - g1))

        g1 = g2
        g2 = g3

    print("calcTchamber: Tchamber = " + str(g2) + ", Q(W) = " + str(Q2))
    return g2, Q2
    


# I can't just use shooting method like this here; there isn't a roughly directly proportional relationship between r and Q
def calcWallThickness(targetTemp, rInner, Ts2, hCyl, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall):

    tol = 1e-4 # m
    e1 = 2 * tol
    Q2 = -1

    # iterate outer radius until the chamber temperature is close enough to the target
    r1 = rInner + 0.01
    r2 = rInner * 2
    
    while(abs(e1) > tol):

        print("r1 = " + str(r1) + ", r2 = " + str(r2))

        Tc1 = calcTchamber(rInner, r1, hCyl, Ts2, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall)[0]
        Tc2, Q2 = calcTchamber(rInner, r2, hCyl, Ts2, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall)

        e1 = targetTemp - Tc1
        e2 = targetTemp - Tc2

        print("e1 = " + str(e1) + ", e2 = " + str(e2))

        r3 = r1 + ((e1 / (e1 - e2)) * (r2 - r1))

        r1 = r2
        r2 = r3

    return r2, Q2



def calcOuterWallTemperature(Qtarget, Tambient, targetTemp, rInner, hCyl, pAmbient, pChamber, Cp, gasConstant, kWall):
    print("calculating outer wall temperature")

    tol = 1e-3
    e1 = 2 * tol
    rOuter2 = -1

    # calculate the heat loss from the wall for a given chamber temperature:
    T1 = Tambient + 1
    T2 = 317

    while(abs(e1) > tol):

        Q1 = calcWallThickness(targetTemp, rInner, T1, hCyl, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall)[1]
        rOuter2, Q2 = calcWallThickness(targetTemp, rInner, T2, hCyl, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall)

        e1 = Qtarget - Q1
        e2 = Qtarget - Q2

        T3 = T1 + ((e1 / (e1 - e2)) * (T2 - T1))
        T1 = T2
        T2 = T3

    return T2, rOuter2



"""Diagnostics Tools"""
def sweepTchamber(rInner, rOuter, hCyl, Ts2, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall):

    print("calculating chamber temperature")

    As1 = pi * (rInner**2) * hCyl
    As2 = pi * (rOuter**2) * hCyl

    # Calculate heat flow through the outer wall
    rConv2 = rConv(2 * rOuter, hCyl, Ts2, Tambient, Cp, As2, pAmbient, gasConstant)
    Qouter = (Ts2 - Tambient) / rConv2

    # calculate Ts1
    rCyl = rCond(rOuter, rInner, hCyl, kWall)
    Ts1 = calcTs1(rCyl, Ts2, Qouter)   

    Tchamber = np.linspace(Ts1 + 1, 1373, 50)
    Qchamber = np.zeros(Tchamber.size) # make sure this is the correct dimension (you'll find out soon enough)

    # create lists for Tchamber and Q, plot them
    for i in range(0, Tchamber.size):

        Qchamber[i] = (Tchamber[i] - Ts1) / rConv(2 * rInner, hCyl, Ts1, Tchamber[i], Cp, As1, pChamber, gasConstant)
        
    # plot results
    plt.plot(Tchamber, Qchamber, '-')
    plt.xlabel("Chamber temperature, K")
    plt.ylabel("Heat loss, W")
    plt.show()


def sweepOuterRadius(rInner, Ts2, hCyl, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall):

    # arrays for radius and furnace heat loss
    outerRadius = np.linspace(rInner + 0.001, rInner + 0.114, 100)
    heatLoss = np.zeros(outerRadius.size)
    chamberTemp = np.zeros(outerRadius.size)
    
    for i in range(0, outerRadius.size):

        chamberTemp[i], heatLoss[i] = calcTchamber(rInner, outerRadius[i], hCyl, Ts2, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall)

    plt.plot((outerRadius - rInner) * 1000, chamberTemp, '-')
    plt.xlabel("wall thickness (mm)")
    plt.ylabel("Tchamber (K)")
    plt.plot([0, (outerRadius[outerRadius.size -1] - rInner) * 1000], [1373, 1373], 'r--')
    plt.show()


    
# see how wall thickness varies with outer wall temperature, find the cut-off temperature for the thickness of a brick
def sweepTs2(Tchamber, rInner, hCyl, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall):

    # arrays for wall thickness and outer wall temperatures
    Ts2 = np.linspace(373, 573, 100)
    wallThickness = np.zeros(Ts2.size)

    for i in range(0, wallThickness.size):
        wallThickness[i] = calcWallThickness(Tchamber, rInner, Ts2[i], hCyl, Tambient, pAmbient, pChamber, Cp, gasConstant, kWall)[0] - rInner

    plt.plot(Ts2, wallThickness * 1000, '-')
    plt.xlabel("outer wall temperature, K")
    plt.ylabel("wall thickness, mm")
    plt.plot([0, Ts2[Ts2.size - 1]], [114, 114])
    plt.show()
        
        

main()