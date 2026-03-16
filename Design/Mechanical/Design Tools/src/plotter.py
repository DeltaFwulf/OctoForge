import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from steadyState import steadyPower

# def QvsWallThickness(innerWallTemp, chamberRadius, hCyl, casingThickness, conductivities, Tambient, pAmbient, Cp, gasConstant):

#     brickThickness = np.linspace(0.001, 1, 100)
#     rockWoolThickness = np.linspace(0.001, 1, 100)
#     heatLoss = np.zeros((brickThickness.size, rockWoolThickness.size))
#     TouterWall = np.zeros((brickThickness.size, rockWoolThickness.size))

#     for i in range(brickThickness.size):
#         for j in range(rockWoolThickness.size):

#             rCyl = getLayerResistances(chamberRadius, hCyl, conductivities, [brickThickness[i], rockWoolThickness[j], casingThickness])
#             heatLoss[i, j] = heatLossSide(innerWallTemp, chamberRadius + brickThickness[i] + rockWoolThickness[j] + casingThickness, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)[1]
        
#     fig = plt.figure(0)    
    
#     # surface plot against both wall thicknesses
#     brickThickness, rockWoolThickness = np.meshgrid(brickThickness, rockWoolThickness)

#     ax = fig.add_subplot(111, projection='3d')
#     ax.plot_surface(brickThickness * 1000, rockWoolThickness * 1000, heatLoss, cmap=cm.inferno)
#     ax.set_xlabel("brick thickness (mm)")
#     ax.set_ylabel("rockwool thickness (mm)")
#     ax.set_zlabel("heat loss (W)")



def plotPowerVsRockwoolThickness():
    """Plot the power required to maintain a chamber temperature vs the thickness of the wall layers."""

    Tchamber = 1473 # Kelvin

    # Furnace Definition ##########################################################################################################
    sideWall = {'thicknesses':[0.076, 0.1, 0.0015], 'k':[0.4, 0.2, 54.0]}
    topWall = {'thicknesses':[0.076, 0.0015], 'k':[0.4, 54.0]}
    baseWall = {'thicknesses':[0.076, 0.04], 'k':[0.4, 0.2]}
    chamber = {'r':0.035, 'h':0.145}

    furnace = {'chamber':chamber, 'side':sideWall, 'top':topWall, 'base':baseWall}

    rwThickness = np.linspace(0, 0.2, 40)
    Q = np.zeros_like(rwThickness)
    
    for i in range(rwThickness.size): # let's sweep the rockwool thickness (2nd term in the side wall calculation)
        furnace['side']['thicknesses'][1] = rwThickness[i]
        Q[i] = steadyPower(Tchamber=Tchamber, furnace=furnace)

    fig, ax = plt.subplots()
    ax.plot(1000*rwThickness, Q, '-')
    ax.set_xlabel("Rockwool thickness, mm")
    ax.set_ylabel("Minimum Power , W")
    ax.set_title(f"Q vs. Rockwool Thickness @ Chamber Temperature = {Tchamber - 273} C")
    ax.grid(True)

    plt.show()


# def plotPowerVsTemp(chamberRadius, thicknesses, hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant):
#     """Given a fixed furnace geometry, plot the minimum power required vs chamber temperature."""

#     Tchamber = np.linspace(500, 1373, 100)
#     heatLoss = np.zeros(Tchamber.size)
#     outerWallTemp = np.zeros(Tchamber.size)

#     for i in range(0, Tchamber.size):
#         outerWallTemp[i], heatLoss[i] = heatLossSide(Tchamber[i], chamberRadius + thicknesses[0] + thicknesses[1] + thicknesses[2], hCyl, rCyl, Tambient, pAmbient, Cp, gasConstant)
        
#     TchamberC = Tchamber - 273
#     outerWallTempC = outerWallTemp - 273

#     plt.figure(20)
#     plt.plot(TchamberC, outerWallTempC, '-')
#     #plt.plot([TchamberC[0], TchamberC[heatLoss.size - 1]], [outerWallTempC[0], outerWallTempC[heatLoss.size - 1]], '--r')
#     plt.xlabel("chamber temperature (C)")
#     plt.ylabel("outer wall temp (C)")
#     plt.title("Ts3 vs Tchamber")

#     plt.figure(21)
#     plt.plot(TchamberC, heatLoss, 'b-')
#     plt.xlabel("chamber temperature (C)")
#     plt.ylabel("heat loss (W)")
#     plt.title("Q vs Tchamber")
    


# def plotTempVsRadius(chamberTemp, chamberRadius, layerThicknesses, layerConductivities, chamberHeight, Q):
#     """Given a furnace definition and chamber temperature, plot the radial temperature distribution through the multilayer furnace  side wall."""

#     targetResolution = 1e-4

#     # for each layer, calculate the inner temperature distribution
#     tempDistribution = np.array([], dtype=float)
#     radii = np.array([], dtype=float)
    
#     for i in range(len(layerThicknesses)):

#         r0 = chamberRadius if i == 0 else chamberRadius + sum(layerThicknesses[:i])
#         T0 = chamberTemp if i == 0 else tempDistribution[tempDistribution.size - 1]

#         layerPoints = np.linspace(r0, r0 + layerThicknesses[i], num=ceil(layerThicknesses[i] / targetResolution))
#         radii = np.append(radii, layerPoints)
        
#         # solve for temperature at each layerPoint
#         layerTemps = np.empty((layerPoints.size), dtype=float)
#         for j in range(layerPoints.size):
#             layerTemps[j] = T0 - (Q * log(layerPoints[j] / layerPoints[0]) / (2 * pi * chamberHeight * layerConductivities[i]))

#         tempDistribution = np.append(tempDistribution, layerTemps)

#     # plot the temperature distribution, denoting layer boundaries
#     tempDistributionC = tempDistribution - 273

#     plt.figure(30)
#     plt.plot(radii, tempDistributionC, '-r')
    
#     for i in range(len(layerThicknesses)):
#         plt.plot([chamberRadius + sum(layerThicknesses[:i]), chamberRadius + sum(layerThicknesses[:i])], [tempDistributionC[0], tempDistributionC[tempDistributionC.size - 1]], '--k')

#     plt.title("Wall Temperature Distribution")  
#     plt.xlabel("radius, mm")
#     plt.ylabel("temperature, C")

plotPowerVsRockwoolThickness()