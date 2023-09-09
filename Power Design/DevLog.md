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

~~That's significantly greater than 20KHz so i'm happy.~~

##### EDIT
I'm not happy. I forget this time $t$ is just the time it takes to charge up the gate. The switching time is equal to the time it takes to charge up and charge down the gate. So the time is actually doubled, the frequency is actually halved and the simplification i made earlier means the frequency is even lower. This means even if a microcontroller could drive the MOSFET it would be spending most of its time in periods of switching (is this even the correct wording?) where the voltage on the gate is somewhere between 0v and 12v. The resistance at these voltages is greater than it is at 12v and so the power losses would be higher. So i'm gonna say my next step is to investigate MOSFET drivers.

#### Conclusion
A max current of 29.3A, a max power of 1465W given that max current, ~~and a max frequency of 161KHZ~~ makes this MOSFET suitable when paired with a MOSFET driver. All for the low low price of 2.

## 06/09/23

I've been toying around with [this paper](https://sci-hub.st/10.1080/00207217.2019.1625973) in [Falstad CircuitJS](http://falstad.com/circuit/circuitjs.html). You can find the file for the circuit i made [here](obsidian://open?vault=furnace-mk2&file=Power%20Design%2FResources%2FMOSFET_OCP). To open it just copy the text from within the file to the "import from text" option under File in CircuitJS. It works somewhat but trying to get it to shutoff at exactly 29.3A is difficult. I think experimentation should continue in a more robust simulation software - one that comes to mind is the real world.

## 09/09/23

I have devised a way for the shut off current to be much more precise. The circuit described in the paper relies on the voltage drop across the diode to be a specific value V<sub>D</sub>. This value is dependent on the current across said diode. A current which changes when adjustments are made to voltage divider and when the base of the transistor starts conducting. However by separating the diode and the transistors base with an opamp set up as a comparator there will be very minimal change in current across the diode. With the voltage V<sub>F</sub> being measured by the opamp's negative terminal and a reference voltage V<sub>ref</sub> being measured by the opamp's positive terminal, the exact moment the current i<sub>d</sub> is sufficiently high to cause V<sub>F</sub> to increase above V<sub>ref</sub> can be detected and capacitor C<sub>d</sub> will begin to be charged by the opamps 12v output. 

I have modified my CircuitJS circuit to demonstrate this [here](obsidian://open?vault=furnace-mk2&file=Power%20Design%2FResources%2FMOSFET_OCP_V2). The scopes along the bottom of the screen are used to track some specific values. Namely the voltages across C<sub>d</sub> (in red) and C<sub>t</sub> (in green), current across the current across the MOSFET and heating element (in yellow), and the voltages V<sub>F</sub> (in red) and V<sub>ref</sub>.

### Using the CircuitJS demonstration
It might not be so intuitive how exactly to use this circuit within CircuitJS so here's a quick guide. 
1. Wait for the voltage, V<sub>b</sub>, across C<sub>t</sub>, represented by the green line on scope 1, to increase to 2v. Current, i<sub>d</sub>, should begin to flow through the MOSFET, represented by the yellow line in scope 2.
2. You should notice that V<sub>F</sub> should have changed to a value closer to V<sub>ref</sub>, represented by the red and green lines in scope 3. By increasing the value of the slider labelled "Load" on the right side of the screen you will decrease i<sub>d</sub> and V<sub>F</sub>.
3. By decreasing the value of load slowly you will increase i<sub>d</sub> and V<sub>F</sub>. The moment V<sub>F</sub> is greater than V<sub>ref</sub>, V<sub>b</sub> should increase rapidly causing the transistor to dump the charge stored by C<sub>t</sub> and subsequently turn the MOSFET off.





