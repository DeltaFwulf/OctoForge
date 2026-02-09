The furnace is composed of two main mechanical subassemblies, the chamber and the frame. The frame forms the furnaces structure, housing the chamber as well as the electronics.


[ IMAGE OF FRAME ]


To simplify manufacture and make the frame as cheap as possible, parts are to be made largely from sheet metal, allowing for quick and low-cost laser cut / bend services to be used. Where this is not possible, simple machining operations that can be performed on a mill / lathe must be chosen, such that these parts can be produced by hand.


## General Concept

- panels and bulkheads hold together, allowing ease of modification
- eight panels to approximate cylindrical shape while still using easy to cut angles

**General Requirements**
- The furnace must be able to be carried by two people via handles
- The furnace must be able to be moved while in operation (cool touchpoints)
- The furnace must survive a car journey when not in operation
- The furnace should survive tipping over unless containing molten metal
- The frame must not slip easily, and be able to prevent rocking by adjustable feet
- The frame must be easy to disassemble into individual components via fastener joints, for maintenance or upgrade purposes


## Bill of Materials
Parts have sorted into three categories: machined components, that must be produced from some stock, fasteners (such as bolts, nuts, washers), and off-the shelf components, such as handles, feet, etc.
### Machined Components

| NAME | QTY | MATERIAL | BUY / MAKE | SUPPLIER | COST | STATUS |
| ---- | --- | -------- | ---------- | -------- | ---- | ------ |
|      |     |          |            |          |      |        |
|      |     |          |            |          |      |        |
|      |     |          |            |          |      |        |
|      |     |          |            |          |      |        |
|      |     |          |            |          |      |        |
|      |     |          |            |          |      |        |

### Fasteners

| NAME                  | STD      | QTY | MATERIAL    | SUPPLIER | COST | ORDER     | STATUS  |
| --------------------- | -------- | --- | ----------- | -------- | ---- | --------- | ------- |
| *M4 flat washer*      | DIN 125  | 192 | A2 SS       | Accu     | 9.60 | QYMLGSMJN | ORDERED |
| *M4x12 Caphead screw* | ISO 4762 | 50  | A2 SS       | Accu     | 4.50 | QYMLGSMJN | ORDERED |
| *M4x10 Caphead screw* | ISO 4762 | 50  | A2 SS       | Accu     | 4.50 | QYMLGSMJN | ORDERED |
| *M4 hex nut*          | DIN 934  | 96  | A2 SS       | Accu     | 5.60 | QYMLGSMJN | ORDERED |
| *M6x16 Caphead screw* | ISO 4762 | 6   | A2 SS       | Accu     | 1.44 | QYMLGSMJN | ORDERED |
| *M6 flat washer*      | DIN 1440 | 12  | A2 SS       | Accu     | 1.44 | QYMLGSMJN | ORDERED |
| *M6 hex nut*          | ISO 4032 | 6   | A2 SS       | Accu     | 1.68 | QYMLGSMJN | ORDERED |
| M3 x 10 M/F standoff  | N/A      | 4   | POM / Brass | Accu     | 2.84 | QYMLGSMJN | ORDERED |
| M3 x 6 caphead screw  | N/A      | 4   | PC          | Accu     | 1.64 | QYMLGSMJN | ORDERED |

# Objective
create a strong and portable frame that houses all furnace components and provides suitable environmental conditions for all subsystems

## Key Features
- Portability: the furnace should be carriable by a single person up to chest height.
- Durability: the furnace should have no exposed insulation on the outer surfaces - should be able to take a light kick or bump against a rough, hard surface.
- Ease of maintenance / assembly: the furnace should be made of modules that can be disassembled and maintained easily and cheaply. Unique fastener types should be minimised. 


The furnace structure consists of two main sections: the chamber and the lower frame.

The chamber houses the heating elements, sensors and insulation, while the lower frame houses the control electronics, power supply, and tool storage.


## Manufacturing Options
Fabrication: https://fractory.com/
## Coating options
Powder coating: https://www.cheshirepowdercoating.com/gallery/

## Adjustable Feet
https://www.vital-parts.co.uk/weight-rated-tilting-adjustable-feet---wamf040-2523-p.asp

[No Mesothelioma hopefully](https://shop.vitcas.com/bio-soluble-fibre-blanket-1200-c-25mm.html)


# Lower Panel Blocks
---
When the frame structure was changed from using extruded aluminium sections to using angle bar brackets, an oversight was missed; the lower frame panels cannot all be attached as the brackets do not retain the nuts like the extruded sections do. Therefore, the final panels to be mounted cannot use this nut and bolt connection. Instead, they must use a connection that only requires exterior access, such as a tapped hole and bolt.

**Design Requirements**
- Brackets must adhere to existing component interfaces, avoiding reworking any other components (including bolts).
- The brackets should be made from aluminium to make machining quicker and easier.
- All components must be made from the same piece of stock.
- The brackets must only require external access to mount the final two panels.
- The brackets cannot impede internal access when mounting the other panels to the frame.
- The brackets must be able to be attached after other panels are installed.

To solve this problem, several block brackets have been designed, and will be machined from either aluminium offcuts or square bar stock. 

The final panels to be installed are the front panel, which holds the controller and power delivery boards, and the rear panel, which holds the ATX power supply. These panels are mounted as shown below:

![[lower panel blocks.png]]

# Upper Panel Redesign
---
The original design of the upper panels has made drilling the upper holes accurately very difficult with available equipment. To address this, the upper section is to be redesigned. The panel design does not need to be adhered to, however all component interfaces must remain the same, and access cannot be lost to internal components, such as the terminal wiring.

Two concepts have been imagined; a split panel design which resembles the current design but with flat panels and brackets as seen in the lower frame section, and a wraparound design, with one thin sheet of metal formed into an octagonal shape, with brackets as before and an access hatch for the terminal wiring. These concepts will be investigated for cost and viability, then one selected and pursued.

**Individual Panels Advantages**
- Repair and replacement will be cheaper for individual panels.
- Upgrading panels is simpler as they are flat and fit into a mill.
- Looser tolerances can be accepted as errors will not stack over the whole perimeter.

**Wraparound Design Advantages**
- The number of parts to produce is almost halved over the panel design.
- Yes, access panels can be added, allowing tool-less opening of the upper frame.
- The upper frame will be stronger, as corners are connected. This permits a lighter subassembly, reducing risks of injury when handling the furnace, and improving stability.


Given the high cost of the wraparound design, as well as concerns regarding accuracy over 7 successive bends, the individual panels design has been selected. Three variants of panel are required: 

- Base panel
- Hinge panel
- Handle panel

The handles must be spring loaded to prevent accidentally catching on casting equipment on non-level ground, and should be corrosion-resistant to prevent weakening if stored in humid conditions for extended periods of time. Finally, the hole pattern must be available, so that panels may be ordered before receiving handles. One candidate is [this](https://protex.com/95-637SS-spring-loaded-handle-stainless-steel-natural) handle from Protex, made from stainless steel.