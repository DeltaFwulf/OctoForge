## Element Geometry
---
Given a maximum power requirement, heating element count, and selected material, the heating element geometry may be defined, and stock sourced.

The general design of a single heating element is that of a coiled wire, bent into a circular loop that sits within a channel on the chamber's inner wall. This element will provide power via radiation into the chamber.

![[steady power vs rockwool thickness, 1200C.png]] 
*Required thermal power required vs rockwool wall thickness.*

Following [[Thermal Modelling]] of furnace insulation, it was determined that the chamber should be able to achieve a temperature of 1200 C for a total power of 154 W. However, if the heating elements provide this steady power, the furnace will take an extremely long time to approach this temperature; more power is required to climb to target temperature than to maintain it.

OctoForge is designed to supply a maximum of 360 W. As such, this value will be used when selecting the elements. As the power board can supply this power evenly between 4 elements, each must supply one quarter of this value, 90 W.

Due to its availability, the first material choice is [Kanthal A1](https://www.kanthal.com/en/products/datasheets/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/kanthal-a-1/). Wire of various diameters may be sourced in coil form, saving production effort.

### Step 1: Calculate Element Resistance
As the power required and chamber temperature are known quantities, the radiative flux may be calculated. Two values are required: the emissivity of the heating element, and the maximum permitted element surface temperature.

Heat flux via radiation between two grey bodies at similar temperatures is given by:
$$q''_{rad} = \epsilon\sigma\left(T_{element}^4 - T_{wall}^4\right)  $$

From Kirchoff's rule, the absorptivity is equal to the emissivity. The heating element and walls are assumed perfect grey bodies. The maximum permitted flux is obtained from [this source](https://www.heating-element-alloy.com/article/heating-element-design-factors.html), set at 50,000 W/m^2. The radiative heating equation may be rearranged for the maximum element temperature, assuming a wall temperature of 1473K.

$$T_{element} =\sqrt[4]{\frac{q''_{max}}{\epsilon\sigma} + T_{wall}^4}$$

Assuming an emissivity of 0.7, the maximum element temperature is calculated to be 1563 K, lower than the maximum allowed temperature of 1673 K for Kanthal A1. To achieve the required 90 W at this temperature, the element would require 0.0018 m^3 of area. This is achieved by a combination of wire diameter and length, however a second constraint exists. The wire must have the correct resistance such that it will dissipate 90 W with a 12 V drop across it.

The resistance of the wire at temperature, $R_t$, may be calculated from the following:
$$ V = IR \xrightarrow{} I = \frac{V}{R}$$
$$Q = VI$$
$$ Q = \frac{V^2}{R} \xrightarrow{}R = \frac{V^2}{Q} $$
This gives a working resistance of 1.6 $\Omega$. 

### Step 2: Calculating Element Length

#### Solving length for total resistance:
The resistance of an element is a function of its resistivity, cross sectional area, and length:

$$ F\rho_0 = R \frac{A_c}{l} = R \frac{\pi D^2}{4l}$$
$$R = \frac{4F\rho_0 l}{\pi D^2}$$
where:
- $\rho$ is the material resistivity at 20 C
- D is the wire circular diameter
- F is the resistivity temperature factor (accounts for higher operating temperatures)

Rearranging for length:
$$ l = \frac{\pi R D^2}{4F\rho_0} $$
#### Solving length for correct flux:

The area of an element may be found, given total power and surface flux:
$$ Q = q''A_s = q''\pi Dl$$
From Ohm's law:
$$ V = IR $$
$$ Q = VI = \frac{V^2}{R} $$

substituting for Q:
$$ q'' \pi Dl = \frac{V^2}{R} $$
Rearranging for l:
$$ l = \frac{V^2}{q''\pi DR} $$
 $$R =FR_0 = \frac{F\rho_0 l}{A_c} = \frac{4F\rho_0l}{\pi D^2}$$
$$ l = \frac{V^2 \pi D^2}{4q'' \pi DF \rho_0 l} $$
Simplifying:
$$ l^2 = \frac{V^2 D}{4q'' F \rho_0} $$
$$ l = \frac{V}{2}\sqrt{\frac{D}{F\rho_0 q''}} $$
Does this also satisfy the relation for resistance?
Setting values for V, D, F, rho, and q, we obtain:
$$ l = \frac{12}{2}\sqrt{\frac{0.001}{1.04*1.45*10^{-6}*50000}} = 0.69098\ m$$
Solving for resistance at this length:
$$ R = \frac{4*1.04*1.45*10^{-6}*0.69098}{\pi 0.001^2} = 1.3267 \ \Omega $$
This doesn't solve the problem with the correct resistance; the solution is incomplete. The value of l is only solved when both relations are satisfied. This requires some extra degree of freedom, as in both equations, the diameter is fixed. This degree of freedom could be the surface flux, recalculating each time for F (this is very insensitive so will be quite well-behaved).

Equating the two lengths:
$$ \frac{\pi RD^2}{4F\rho_0} = \frac{V}{2}\sqrt{\frac{D}{F\rho_0q''}}$$
$$ \frac{\pi^2R^2D^4}{16F^2\rho_0^2} = \frac{V^2D}{4F\rho_0q''}$$
$$ q'' = \frac{V^2 D 16 F^2 \rho_0^2}{\pi^2R^2D^4 4F\rho_0} = 
         \frac{4V^2F\rho_0}{\pi^2 R^2 D^3}$$
Once q'' has been solved, the length can be calculated from either of the two original equations. Note that if the solved surface flux exceeds the maximum chosen value, the total power per element must be reduced (for a given total power, more elements must be used). 

For this element, the total power is given as 90 W. This requires 1.6 Ohms of resistance. The expected surface temperature, from the maximum flux estimate, is 1563K. This gives a resistivity factor of 1.04. Once the flux is calculated, the new element temperature must be solved and F updated.

For a 1mm diameter wire:

| Variable | Value       | Unit                 |
| -------- | ----------- | -------------------- |
| Q        | 90          | W                    |
| V        | 12          | V                    |
| R        | 1.6         | $\Omega$             |
| F        | 1.04        | ul                   |
| D        | 1.0         | mm                   |
| $\rho_0$ | 1.45        | $\mu \Omega$ m^2 / m |
| q''      | 34378.27761 | W/m^2                |
| T_new    | 1536.52514  | K                    |
| F_new    | 1.04        | ul                   |
| l        | 0.83331     | m                    |
The following Python function can be used to calculate Kanthal A1 wire length for a given power output and wire diameter:

```python

def wireLength(D:float, Q:float, voltage:float, qMax:float, Tchamber:float):
	"""Calculates the length of Kanthal A-1 wire that satisfies power requirements"""

    # Kanthal A-1 material properties:
    emissivity = 0.7
    resistivity = 1.45e-6
    
    T_el = (qMax / (emissivity*5.67 / 10**8) + Tchamber**4)**0.25
    T_arr = [373, 473, 573, 673, 773, 873, 973, 1073, 1173, 1273, 1373, 1473, 1573, 1673]
    F_arr = [1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.02, 1.03, 1.03, 1.04, 1.04, 1.04, 1.04, 1.05]

    F0 = np.interp(T_el, T_arr, F_arr)
    R = voltage**2 / Q
    q = (4*voltage**2*F0*resistivity) / (pi**2 *R**2 *D**3)
    T_el = (q / (emissivity*5.67 / 10**8) + Tchamber**4)**0.25
    F1 = np.interp(T_el, T_arr, F_arr)
    l = pi*R*D**2 / (4*F1*resistivity)

    print(f"Required wire length of Kanthal A-1: {'%.4f' % (l*1000)} mm, at a flux of {q} W/m^2, surface temperature: {T_el} K")
```

### Step 3: Calculate coil and loop geometry

The element is composed of a tight helix, looped into a major circular profile. To avoid excessive self heating of the element, several coil constraints are introduced:
- minimum coil diameter
- minimum pitch

The mean pitch is calculated at the loop mean diameter, referred to here as the pitch diameter, $D_p$.The minimum pitch is set at 3 wire diameters, to mitigate self heating. This is taken at the minor diameter, where the coils are bent closest together. The coil diameter itself should lie between 3 and 6 wire diameters, as per the [design guide](https://www.heating-element-alloy.com/article/heating-element-design-factors.html).

From this, a solution exists with some coil and loop diameter, and some pitch (driven by the loop diameter and wire diameter).

The minimum pitch is set as 3 wire diameters, $p_m = 3d_w$. The loop diameter, D, is chosen to just seat the wire within the chamber wall with no free hanging wire in the chamber, to prevent short circuits and stresses on brittle hot wires.

For a helical wire, the length of the wire along the path is related to the overall coil length by its coil diameter and pitch:

$$ l = \frac{L}{sin(\alpha)} $$
where L is the coil length, l is the wire length, and $\alpha$ is the ramp angle of the helix. This angle can be calculated as:
$$ \alpha = \arctan\left(\frac{p}{\pi d_c}\right) $$
Substituting and rearranging for L:
$$ L = l\sin\left(\arctan\left(\frac{p}{\pi d_c}\right)\right) $$
This helical wire will be bent into a circular arc about its centrum, such that the mean helical pitch is still p.
$$ L = \frac{D\theta}{2} $$
Where D is the loop diameter (through the centre of the coil), and $\theta$ is the angular sweep of the arc. Substituting for L in the previous equation:
$$ \frac{D\theta}{2} = l\sin\left(\arctan\left(\frac{p}{\pi d_c}\right)\right) $$
Rearranging to solve for p:
$$ p = \pi d_c \tan\left(\arcsin\left(\frac{D\theta}{2l}\right)\right)$$
The true constraint is the minimum pitch, $p_m$:
$$ p_m = \left(\frac{D - d_c}{D}\right)p \xrightarrow{} 
   p = \left(\frac{D}{D - d_c}\right)p_m$$
Substituting for p and rearranging for $d_c$:
$$ d_c^2 - Dd_c + \frac{Dp_m}{\pi}\cot\left(\arcsin\left(\frac{D\theta}{2l}\right)\right) = 0 $$
The solution of coil diameter is found by solving the quadratic:
$$ d_c = \frac{D \pm \sqrt{D^2 - \frac{4Dp_m}{\pi}\cot\left(\arcsin\left(\frac{D\theta}{2l}\right)\right)}}{2} $$
The solution chosen is up to the designer, though care must be taken to ensure the loop inner and outer diameters are as expected, or iterate until desired result is achieved.

The chosen wire is AWG 18, or 1.02 mm diameter, made from Kanthal A1. This gives a required length of 866.9796 mm.

Alternatively, since the planned coiling jig (link to this), will use some shaft with a given diameter, the coil diameter becomes a fixed quantity, or at least not the driven value. Instead, the coil diameter should be set based on available coil shaft diameters, and the pitch calculated. From before:

$$ L = l\sin\left(\arctan\left(\frac{p}{\pi d_c}\right)\right) $$
Rearranging for p and substituting for L:

$$ p = \pi d_c\tan\left(\arcsin\left(\frac{D\theta}{2l}\right)\right) $$
And for minimum pitch:
$$ p_m = \pi \frac{d_c(D - d_c)}{D} \tan\left(\arcsin\left(\frac{D\theta}{2l}\right)\right)$$

There exists a window of valid coil diameters, due to the parabolic nature of the minimum pitch equation. Any value of $d_c$within this window may be used to create heating elements. The bounds are given by the solution of the quadratic:

letting k = $\frac{\pi}{D}\tan\left(\arcsin\left(\frac{D\theta}{2l}\right)\right)$:
$$ d_c^2 - Dd_c + \frac{p_m}{k} = 0 $$
$$ d_c = \frac{D \pm \sqrt{D^2 - \frac{4p_m}{k}}}{2} $$

The proposed solution method is as follows:
1. Calculate, given the minimum pitch constraint, a valid coil diameter.
2. Adjust the coil diameter to some useable value and check the minimum pitch.
3. Repeat until a valid coil diameter is found, using the solved pitch.
4. Calculate the stretched loop length from the equation for L.

| Variable    | Value     | Unit                 |
| ----------- | --------- | -------------------- |
| Q           | 90        | W                    |
| V           | 12        | V                    |
| R           | 1.6       | $\Omega$             |
| F           | 1.04      | ul                   |
| D           | 1.02      | mm                   |
| $\rho_0$    | 1.45      | $\mu \Omega$ m^2 / m |
| q''         | 32395.419 | W/m^2                |
| T_new       | 1533.07   | K                    |
| F_new       | 1.04      | ul                   |
| l           | 866.9796  | mm                   |
| $p_m$       | 3.06      | mm                   |
| D           | 70        | mm                   |
| $\theta$    | 300       | deg                  |
| $d_c$       | 6.02      | mm                   |
| $d_{shaft}$ | 5         | mm                   |
| p           | 4.090     | mm                   |
| L           | 183.3     | mm                   |
| $D_i$       | 66.38     | mm                   |


![[heating element geometry.png]]
*Heating element geometry modelled in FreeCAD.*

The calculated coil diameter falls into the typical 3 to 6 diameter range for the wire and so was accepted. While thinner gauge wires do offer cheaper and shorter lengths, they are more sensitive to non-constant diameters caused by scratches or nicks, and so without careful handling these are more likely to suffer damage from hot spots.

To model the heating element in FreeCAD, the *PathHelix* macro was used, from the [GrabBag](https://github.com/pyro9/GrabBag) repository by pyro9. Click [here](https://www.youtube.com/watch?v=COVKF25ttLY) for an installation guide. To create the full path, multiple sketches were [joined](https://www.youtube.com/watch?v=jE-H_30MbcA) together in a single binder, then an additive pipe used to sweep the wire cross section - beware, this takes a VERY long time to render.


## Power Delivery
---
To supply power to the elements, terminals are required. These must withstand the extreme temperatures of the chamber and elements, provide reliable electrical connection, and allow for simple element replacement in the event of damage.

The proposed solution is to use stainless steel threaded bars and nuts to clamp the elements. Two nuts will clamp the elements in the chamber, and two others will clamp a copper wire on the supply side.  The inner nuts will be spaced such that they are located axially in the bricks, and the outer nuts used to clamp the terminals.

The terminals will be made from M4 threaded bar, with two full hexagonal nuts on each end. On the chamber side, the connection will be purely between the nuts, washers, and the wire; the outer connection will use a spade terminal between the nuts.

To minimise heat dissipation along the transmission lines, the resistance must be minimised. Copper wires will be used, with a total transmission resistance << 1$\Omega$.