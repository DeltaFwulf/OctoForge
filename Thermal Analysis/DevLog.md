## Modelling the chamber as a resistance network

A good method we can use to model the furnace is as a resistance network. Using this we can calculate the heat loss though multiple sides using simple analytical techniques.

as a first attempt, the cylinder may be modelled as a cylinder wall with a lid and a floor surrounded on all sides by ambient air subject to convective heat transfer. 

Total resistance for a single wall, $R_{wall}$, is equal to the sum of the inline resistances between the chamber air and the ambient air.

## Parameterising air properties

To save manually looking up values in dry air tables, I will create functions to predict air conductivity and viscosity:

[here](https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)is a good source for maths formatting using MathJax

### Assumptions
- air is at 101325 Pa
- mean mass of an "air" molecule to be $0.02896 \div 6.022\ast 10^{23} = 4.809 \ast 10^{-26}$ kg
- air is dry

### Viscosity 
[Source](https://en.wikipedia.org/wiki/Temperature_dependence_of_viscosity#:~:text=Since%20the%20momentum%20transfer%20is,gaseous%20viscosity%20increases%20with%20temperature) 

$$\mu = \frac{5}{16\sqrt{\pi}} \times \frac{(mk_bT)^\frac{1}{2}}{\sigma\Omega(T)}$$

$$\Omega(T)  = 1.16145T^{\ast-0.14874} + 0.52487e^{-0.77320T^\ast} + 2.16178e^{-2.43787T^\ast}$$

where:

$T^\ast=\frac{k_bT}{\epsilon}$,  
($k_b/\epsilon = \frac{1}{97}$) K$^{-1}$,
$\sigma = 3.617 \ast 10^{-10}$ m

### Thermal conductivity, $\lambda$
[Source](https://srd.nist.gov/jpcrdreprint/1.555749.pdf)

$\lambda(\rho,T) = \lambda_0(T) + \lambda_R(\rho)$ W/m$\ast$K

$\lambda_{0R} = \frac{\lambda_0}{\Lambda}$,

$\Lambda = \frac{R^\frac{5}{6}p_c^\frac{2}{3}}{(TMN_A^2)^\frac{1}{6}} = 4.358\ast10^{-3}$ W/m$\ast$K,

$$\lambda_{0R} = C_1T_R^{-1} + C_2T_R^{\frac{-2}{3}} + C_3T_R^{\frac{-1}{3}} + C_4 + C_5T_R^{\frac{1}{3}} + C_6T_R^{\frac{2}{3}} + C_7T_R + C_8T_R^{\frac{4}{3}} + C_9T_R^{\frac{5}{3}}$$

where:
$C_1 = 33.9729025$,
$C_2 = -164.702679$,
$C_3 = 262.108546$,
$C_4 = -21.5346955$,
$C_5 = -443.455815$,
$C_6 = 607.339582$,
$C_7 = -368.790121$,
$C_8 = 111.296674$,
$C_9 = -13.4122465$

Critical values:
$T_c = 132.52$ K
$\rho_c = 313$ kg$\ast$m$^{-3}$

$\Delta\lambda_R = D_1\rho_R + D_2\rho_R^2 + D_3\rho_R^3 + D_4\rho_R^4$

where:
$D_1 = 3.12013125$
$D_2 = -23.0762400$
$D_3 = 1.65049430$
$D_4 = -0.191148175$

How do we iterate to arrive at the correct answer for the cylinder surface temperatures? (calculating the film temperatures?) There seem to be two unknowns (Ts1, Ts2) and one equation

**19/08/2023**
Okay, so the initial question was incomplete. I need to set more design constraints to be able to solve for the wall thickness. I'll set the outside wall temperature to a temperature that's either:

1. safe to touch comfortably - I need to find a temperature chart for this
2. low enough to hold the handles (modelling conduction)
3. some other arbitrary value if we use a shroud like [Here](https://www.hswalsh.com/product/melting-crucible-furnace-3kg-italian-manufactured-tf58b)

I'll also be aiming to minimise the heat loss for a given chamber-ambient temperature difference within some design constraint (I can't just make the walls 10km thick due to cost and maintenance restrictions, never mind portability lol)

I'll define the thermal efficiency of the furnace at temperature T as $1-(\frac{Q_{loss}} {Q_{max}})$ for the time being, and aim for an efficiency greater than 80% at 1000$^{\circ}$C

So, we can solve for wall thickness given a certain heat loss, chamber temperature and wall outer temperature. Therefore we can solve for furnace performance over a range of temperatures (if not efficiently): 
1. solve the specified case to get target wall thickness
2. for each temperature we want to investigate, alter the heat flux and solve for wall thickness as in the specified case; when the wall thickness equals the target wall thickness this is the performance of the furnace at this temperature. We can use a shooting method to obtain results relatively efficiently.

We can predict floor and lid performances similarly, assuming the furnace is airtight

To get better results, we will need to run a thermal simulation of the frame after initial models have been produced in software such as openFoam.

The results produced here can also be used to inform the convection-radiation analysis of the heating elements

### Setting boundary conditions 

How hot can the outer wall get if not shrouded? [Possible Source](https://ntrs.nasa.gov/api/citations/20100020960/downloads/20100020960.pdf)

For testing, I'll use 44$^{\circ}$C, but I'll figure out the $k{\rho}c$ of fire bricks later on

**20/08/2023**

Okay, so the method for getting the design point performance is actually very convoluted:
1. Set outer wall radius and outer wall temperature
2. Calculate heat flow from outer wall condition
3. Use shooting method to find inner wall temperature
4. using a shooting method, iterate for chamber temperature to satisfy conservation of energy
5. repeat steps 2-4, varying outer radius until the chamber temperature converges to target
6. vary outer wall temperature  and solve for chamber temperature again until heat flow matches target

I'm almost definitely sure that by setting $T_{s,2}$ to enforce target heat flow in step 1 is possible, however the stability of this algorithm would probably go WAY down, so for now I'm going to do it this way as it seems to be able to converge most of the time.

To calculate the performance of this furnace over different chamber temperatures, we can now fix the wall thickness and not enforce a heat flow target, simply converge to the desired chamber temperature and treat heat flow as a target

I found something saying that $k_{wall}$ will be about 0.2-0.4 [Source](http://www.ccewool.com/News/main-difference-between-insulating-fire-brick-and-refractory-brick/#:~:text=Heat%20conductivity%20of%20insulating%20fire,better%20than%20refractory%20fire%20brick.)
We'll likely use more VITCAS bricks [Source](https://shop.vitcas.com/insulating-fire-bricks-vitcas-grade-30.html)

$R_{conv,2}$ is returning a complex value, one sec
now Ts1 is coming back complex, might be to do with Q? I'll check in the morning, time to snooze

**21/08/2023**
The problem seems to be the conductivity calculation returning negative, everything else seems to be returning normal results (the viscosity equation is p cool)

**21/08/2023**
I was using $T_{crit}$ not $T_R$ in the conductivity calculation. For some reason, the chamber temperature solver goes unstable after a few iterations, I'll see tomorrow if there's an issue in the chamber temp solver and might have to switch to an inherently stable solver (bisection, etc). I'll also sweep through a range of chamber temperatures and see if the line is super shaky

**26/08/2023**
fuck me, there was a g1 where there should have been a g2, so errors weren't being calculated properly, leading to a runaway chamber temperature

Another seemingly big issue is that if Ts2 is assumed constant when varying $r_{outer}$, power constantly increases at the same time as thermal resistance in the wall, leading to runaway chamber temperatures. I will find, for each value of $T_{s,2}$, the outer radius that gives the target chamber temperature using the shooting method:

**Definition of Shooting Method** (I can't remember its real name so I just rederive it every time I need it)

**Assumption:** there is a positive correlation between guesses and cost function output. 

1. make two initial guesses, $g_1$, and $g_2$.
2. calculate the cost function output for these errors i.e. the difference in heat output to target (make sure it is positively correlated with guess magnitude or you may have a problem)
3. calculate the new guess by: $g_3 = g_1 + (\frac{e_1}{e_1-e_2}) \ast (g_2 - g_1)$
4. let $g_1 = g_2$ then let $g_2 = g_3$
5. repeat until $e_2 < e_{max}$
6. return $g_2$ and whatever else useful you may have calculated

this works, the last layer is to solve for $T_{s,2}$ that requires a specific wall thickness (brick thickness in this case)

The next steps will be to create a planar wall version to calculate conductive losses and inner wall temps, but they will be called as variant functions (as arguments into the higher function or smth)

I'll solve for the lowest outer wall temps that I can get away with for the time being, which can give answers for all dimensions, then begin modelling the heating element in a similar (but hopefully slightly simpler) way.

As a sanity check, I'll attempt to perform a simulation on the furnace once the chamber has an initial model (this will take ages but should provide a clearer answer)

**Sanity Check**
The heat loss from the wall seems very low. To check if we're WAY off, I'm going to model the furnace as a planar wall and measure the conductive heat loss through it given assumed inner surface temperature and wall thickness.

Cylinder prediction: ($T_{s1} = 1373 K$, $T_{s2} = 373K$) = 200 W
Cylinder prediction: ($T_{s1} = 416 K$, $T_{s2} = 373K$)  = 17 W

Planar wall prediction: ($T_{s1} = 1373 K$, $T_{s2} = 373K$) = 700 W
Planar wall prediction: ($T_{s1} = 416 K$, $T_{s2} = 373K$)  = 30.4 W

It seems that the prediction for inner wall temperature may be too low? Why is the solved value of $T_{s1} << T_{chamber}$?

I'll set $T_{s1}$ to be equal to the chamber temperature of 1100$^{\circ}$C. I believe this is a better (and conservative) approximation as the inside of the furnace will not form a well developed boundary layer as there is no net flow upwards along the chamber wall. This gives an estimated heat loss of 400W through the walls (this makes more sense intuitively).

## Results

some table of results here


# Heating Element Analysis

## You guessed it, it's a resistance network (literally)

we will model the wire as one long coil subject to blackbody / grey-body radiation and convection in a large black/grey body chamber (partially accurate assumptions).