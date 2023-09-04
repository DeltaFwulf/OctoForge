## 04/09/23

My initial thought for providing power to the heating element in a controllable measurable way is through the use of a MOSFET driven with a PWM signal. 
Next is to identify a suitable MOSFET with the following requirements.

- Low power losses and thus a temperate delta of at most +55°C. $I^2⋅R_{DS(on),max}⋅R_{thJA}<55$
- Can handle high enough power. $V_{DS}⋅I > K⋅P_{loss,max}$
- Low gate charge such that the operating frequency is above human hearing (20KHz) when driven by the low current output from a microcontroller.

where; $I$ is current flow through the MOSFET's drain, $R_{DS(on),max}$ is the maximum resistance of the MOSFET, $R_{thJA}$ is the increase in temperature of the MOSFET for a given power loss, $V_{DS}$ is the breakdown voltage between drain and source, K is some constant greater than 1, and $P_{loss,max}$ is the power maximum power loss through the walls of the furnace.

### IPP016N06NF2S
The [IPP016N06NF2S](https://www.mouser.co.uk/ProductDetail/Infineon-Technologies/IPP016N06NF2SAKMA1?qs=vvQtp7zwQdO2%252BKgNgsNqYA%3D%3D) power MOSFET drew my eye as being relatively cheap (at £2.00 for a single unit), high enough max voltage and current, and low enough resistance. Looking at the [datasheet](https://www.mouser.co.uk/datasheet/2/196/Infineon_IPP016N06NF2S_DataSheet_v02_01_EN-3164870.pdf) for the IPP016N06NF2S i can establish whether this component meets the requirements.

- $R_{DS(on),max} =$ 1.6mΩ
- $R_{thJA} =$ 40°C/W
	Device on 40 mm x 40 mm x 1.5 mm epoxy PCB FR4 with 6 cm2 (one layer, 70 μm thick) copper area for drain. 
	This is worst case, as we could just add a aluminium heatsink and a fan.
- $V_{DS} =$ 60v
- $I_D=$ 194A
- $Q_G=$ 155nC
Where $I_D$ is the max drain current, and $Q_G$ is the charge required to fill the gate.

#### Power Losses And Max Current
Let calculate the maximum current as limited by a maximum delta temperature of the MOSFET of +55°C.

${I}^2⋅R_{DS(on),max}⋅R_{thJA}<55$

Filling in the values for $R_{DS(on),max}$ and $R_{thJA}$, we can get a value for the current at which the MOSFET temperature will have a delta of +55°C.

$I = 29.3$

29.3A is below the rated max current of 194A which is also great. Current flowing through the MOSFET should not exceed this value. Assuming the worst happened (the fan died and the heatsink got gunked), the MOSFET should not overheat.

#### Max Power
Now lets plug some more values into the following equation.

$V_{DS}⋅I = P$

I'm gonna knock 10v off the max voltage.

$50⋅29.3=1465$

1465W seems a sufficient amount of power.

#### Max Frequency
This is mostly a nice to have as it would still function below 20KHz but it would be annoying. I'm assuming the microcontroller in question can supply 25mA at most. And i'm going to simplify the mathematics here to get a ball park.

I need to calculate how long it takes for a given current to charge up the gate. The datasheet provides the charge and i've just assumed a current so here goes.

$t=Q/I$

$t=6.2⋅10^{-6}$s

which means...

$f = 1.61⋅10^5$Hz

That's significantly greater than 20KHz so i'm happy.

#### Conclusion
A max current of 29.3A, a max power of 1465W given that max current, and a max frequency of 161KHZ makes this MOSFET suitable. All for the low low price of 2.





