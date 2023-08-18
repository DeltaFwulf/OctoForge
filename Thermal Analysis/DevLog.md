## Modelling the chamber as a resistance network

A good method we can use to model the furnace is as a resistance network. Using this we can calculate the heat loss though multiple sides using simple analytical techniques.

as a first attempt, the cylinder may be modelled as a cylinder wall with a lid and a floor surrounded on all sides by ambient air subject to convective heat transfer. 

Total resistance for a single wall, $R_{wall}$, is equal to the sum of the inline resistances between the chamber air and the ambient air.

## Parameterising air properties

To save manually looking up values in dry air tables, I will create functions to predict air conductivity and viscosity:

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

How do we iterate to arrive at the correct answer for the cylinder surface temperatures? (calculating the film temperatures?)

Okay, about to go to sleep but I think that if I define the power loss, the temperatures may be definable


