from math import pi, log
from pyfluids import Fluid, FluidsList, Input



def steadyPower(Tchamber:float, furnace:dict, **kwargs) -> float:
    """Accepts furnace geometry and chamber temperature, outputs net heat loss through sides into air at standard temperature."""

    qTol = 1e-4 if kwargs.get('qTol') is None else kwargs.get('qTol')
    Tambient = 288 if kwargs.get('Tambient') is None else kwargs.get('Tambient')
    rOuter = furnace['chamber']['r'] + sum(furnace['side']['thicknesses'])
    
    # Side Heat Loss ##############################################################################################################
    Ts_a = Tambient + 100
    Ts_b = Tchamber - 100

    A_side = 2*pi*rOuter*furnace['chamber']['h'] # FIXME: account for extra height, this may not be as good as conservative estimate

    ea = 2*qTol

    Rside = 0
    for i in range(len(furnace['side']['k'])):
        ri = furnace['chamber']['r'] + sum(furnace['side']['thicknesses'][:i])
        ro = ri + furnace['side']['thicknesses'][i]
        Rside += log(ro / ri) / (2*pi*furnace['chamber']['h']*furnace['side']['k'][i])
   
    while(abs(ea) > qTol):
        Qcond_a = (Tchamber - Ts_a) / Rside
        Qcond_b = (Tchamber - Ts_b) / Rside

        Qconv_a = (Ts_a - Tambient) / convectiveResistanceSide(diameter=2*rOuter, L=furnace['chamber']['h'], Tsurf=Ts_a, Tambient=Tambient, A=A_side)
        Qconv_b = (Ts_b - Tambient) / convectiveResistanceSide(diameter=2*rOuter, L=furnace['chamber']['h'], Tsurf=Ts_b, Tambient=Tambient, A=A_side)

        ea = Qcond_a - Qconv_a
        eb = Qcond_b - Qconv_b

        if(ea == eb and abs(eb) < qTol):
            break

        Ts_c = Ts_a + ((ea / (ea - eb)) * (Ts_b - Ts_a))
        Ts_a = Ts_b
        Ts_b = Ts_c
    
    Qside = Qconv_b
    Tside = Ts_b

    # Lid Heat Loss ###############################################################################################################
    L = rOuter / 2
    At = pi*rOuter**2

    Rtop = 0
    for i in range(len(furnace['top']['k'])):
        Rtop += furnace['top']['thicknesses'][i] / (furnace['top']['k'][i]*At)

    Tt_a = Tambient + 50
    Tt_b = 2*Tambient   

    et_a = 2*qTol
    kRelax = 0.1

    while(abs(et_a) > qTol):
        Qcond_a = (Tt_a - Tambient) / Rtop
        Qcond_b = (Tt_b - Tambient) / Rtop

        Qconv_a = (Tt_a - Tambient) / convectiveResistancePlane(hotTop=True, Tsurf=Tt_a, Tambient=Tambient, L=L, A=At)
        Qconv_b = (Tt_b - Tambient) / convectiveResistancePlane(hotTop=True, Tsurf=Tt_a, Tambient=Tambient, L=L, A=At)

        et_a = Qcond_a - Qconv_a
        et_b = Qcond_b - Qconv_b

        if(et_a == et_b and abs(et_b) < qTol):
            break

        Tt_c = Tt_a + ((et_a / (et_a - et_b))*(Tt_b - Tt_a))
        Tt_a = Tt_a + (kRelax*(Tt_b - Tt_a))
        Tt_b = Tt_b + (kRelax*(Tt_c - Tt_b))

    Qtop = Qconv_b
    Ttop = Tt_b

    # Base Heat Loss ##############################################################################################################
    Rbase = 0
    for i in range(len(furnace['base']['k'])):
        Rbase += furnace['base']['thicknesses'][i] / (furnace['base']['k'][i]*At)

    Tb_a = Tambient + 50
    Tb_b = 2*Tambient   

    eb_a = 2*qTol
    kRelax = 0.1

    while(abs(eb_a) > qTol):
        Qcond_a = (Tb_a - Tambient) / Rbase
        Qcond_b = (Tb_b - Tambient) / Rbase

        Qconv_a = (Tb_a - Tambient) / convectiveResistancePlane(hotTop=False, Tsurf=Tb_a, Tambient=Tambient, L=L, A=At)
        Qconv_b = (Tb_b - Tambient) / convectiveResistancePlane(hotTop=False, Tsurf=Tb_a, Tambient=Tambient, L=L, A=At)

        eb_a = Qcond_a - Qconv_a
        eb_b = Qcond_b - Qconv_b

        if(eb_a == eb_b and abs(eb_b) < qTol):
            break

        Tb_c = Tb_a + ((eb_a / (eb_a - eb_b))*(Tb_b - Tb_a))
        Tb_a = Tb_a + (kRelax*(Tb_b - Tb_a))
        Tb_b = Tb_b + (kRelax*(Tb_c - Tb_b))

    Qbase = Qconv_b
    Tbase = Tb_b

    print("Heat loss from wall = " + str(Qside) + " W for outer temp = " + str(Tside - 273.15) + " C")
    print("Heat loss from lid = " + str(Qtop) + " W for outer temp = " + str(Ttop - 273.15) + " C")
    print("Heat loss from base = " + str(Qbase) + " W for outer temp = " + str(Tbase - 273.15) + " C")

    return Qside + Qtop + Qbase



def calcGrashof(Tsurf, Tfluid, length, density, viscosity):
    return density**2 *9.81*(2 / (Tsurf + Tfluid))*abs(Tsurf - Tfluid)*length**3 / viscosity**2



def convectiveResistanceSide(diameter:float, L:float, Tsurf:float, Tambient:float, A:float) -> float:
    """Calculates the mean convective resistance of the outer side wall of a right, vertical cylinder under natural convection."""
    film = Fluid(FluidsList.Air).with_state(
        Input.pressure(100e3),
        Input.temperature((Tsurf + Tambient) / 2)
    )

    grashof = calcGrashof(Tsurf, Tambient, L, film.density, film.dynamic_viscosity)
    raleigh = grashof*film.prandtl

    if(diameter < 35*L / (grashof**0.25)): # can we treat the cylinder as a vertical flat plate?
        print("Nusselt calculation may be less accurate")

    Nusselt = 0.825 + ((0.387*raleigh**(1/6)) / ((1 + (0.492 / film.prandtl)**(9/16))**(8/27)))**2
    hMean = Nusselt*film.conductivity / L
    return 1 / (hMean*A)



def convectiveResistancePlane(hotTop:bool, Tsurf:float, Tambient:float, L:float, A:float) -> float:
    """Calculates the mean convective thermal resistance of a horizontal planar wall under natural convection."""

    film = Fluid(FluidsList.Air).with_state(
        Input.pressure(100e3),
        Input.temperature((Tsurf + Tambient) / 2)
    )

    grashof = calcGrashof(Tsurf, Tambient, L, film.density, film.dynamic_viscosity)
    raleigh = grashof*film.prandtl
    nusselt = 1

    if hotTop == (Tsurf != Tambient and Tsurf > Tambient): # XXX: we could linearly blend between different Nusselt correlations to remove discontinuities
    
        if(raleigh >= 1e4 and raleigh <= 1e7):
            nusselt = 0.54 * (raleigh**0.25)

        elif(raleigh > 1e7 and raleigh <= 1e11):
            nusselt = 0.15 * (raleigh**(1/3))
        
    elif(raleigh >= 1e5 and raleigh <= 1e11):
        nusselt = 0.27 * (raleigh**0.25)

    elif(raleigh > 5e3 and raleigh < 1e5):
        nusselt = 1.611 * (raleigh**0.145)

    hMean = nusselt*film.conductivity / L
    return 1 / (hMean*A)