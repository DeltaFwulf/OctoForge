from math import pi, sqrt, tan, asin
import numpy as np


def wireLength(D:float, Q:float, voltage:float, qMax:float, Tchamber:float) -> None:
    """Calculates the length of Kanthal A-1 wire that satisfies power requirements"""

    # Kanthal A-1 material properties:
    emissivity = 0.7
    resistivity = 1.45e-6

    # estimate F from max surface loading:
    T_el = (qMax / (emissivity*5.67 / 10**8) + Tchamber**4)**0.25
    T_arr = [373, 473, 573, 673, 773, 873, 973, 1073, 1173, 1273, 1373, 1473, 1573, 1673]
    F_arr = [1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.02, 1.03, 1.03, 1.04, 1.04, 1.04, 1.04, 1.05]
    F0 = np.interp(T_el, T_arr, F_arr)

    # Solve for length
    R = voltage**2 / Q
    q = (4*voltage**2*F0*resistivity) / (pi**2 *R**2 *D**3)
    T_el = (q / (emissivity*5.67 / 10**8) + Tchamber**4)**0.25
    F1 = np.interp(T_el, T_arr, F_arr)
    l = pi*R*D**2 / (4*F1*resistivity)

    print(f"Required wire length of Kanthal A-1: {'%.4f' % (l*1000)} mm, at a flux of {q} W/m^2, surface temperature: {T_el} K")


def coilDiameter(dLoop:float, dWire:float, minPitch:float, lWire:float, sweepAng:float) -> None:

    c = dLoop*minPitch / (pi*tan(asin(0.5*dLoop*sweepAng / lWire)))

    dCoilLow = (dLoop - sqrt(dLoop**2 - 4*c)) / 2
    dCoilHigh = (dLoop + sqrt(dLoop**2 + 4*c)) / 2

    pitchLow = minPitch*dLoop / (dLoop - dCoilLow)
    pitchHigh = minPitch*dLoop / (dLoop - dCoilHigh)

    print(f"Low coil diameter: {'%.3f' % (1000*dCoilLow)} mm, wire diameters: {'%.1f' % (dCoilLow / dWire)}, mean pitch = {'%.3f' % (1000*pitchLow)} mm")
    print(f"High coil diameter: {'%.3f' % (1000*dCoilHigh)} mm, wire diameters: {'%.1f' % (dCoilHigh / dWire)}, mean pitch = {'%.3f' % (1000*pitchHigh)} mm")



wireLength(D=0.00102, Q=90.0, voltage=12.0, qMax=50e3, Tchamber=1473)
coilDiameter(dLoop=0.08, dWire=0.00102, minPitch=0.00306, lWire=0.8669796, sweepAng=7*pi / 4)