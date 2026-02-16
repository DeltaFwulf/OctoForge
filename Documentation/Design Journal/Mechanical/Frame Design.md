The furnace frame represents the mechanical structure that houses the chamber and electronics.

**General Requirements**
- The furnace must be able to be carried by two people via handles
- The furnace must be able to be moved while in operation by provision of touch points < 44°C with a chamber temperature of 1200°C
- The furnace must survive a car journey when not in operation
- The furnace should survive tipping over unless containing molten metal
- The frame must not easily slip along the ground
- On a normal surface, the furnace should be adjustable such that it does not rock
- The furnace should not scratch or damage wooden floors
- The frame must be easy to disassemble into individual components via fastener joints, for maintenance or upgrade purposes
- Electronics must be able to run for over 8 hours continuously within the frame without overheating
- The chamber must be accessible without needing any tools, and quickly re-covered to prevent excessive heat loss when removing i.e. crucibles.

The furnace will take on an octagonal prism shape, as with 8 sides a cylinder is approximated (the most thermally efficient profile for wall thickness) within 8.2%, but angles are cut at 45°, keeping machining operations simple. The frame will be held together by bolted connections to allow any part to be interchangeable, in case it is damaged or needs upgrading.

To simplify manufacture and make the frame as cheap as possible, parts are to be made largely from sheet metal, allowing for quick and low-cost laser cut / bend services to be used. Where this is not possible, simple machining operations that can be performed on a mill / lathe must be chosen, such that these parts can be produced by hand.

## Bill of Materials
Parts have sorted into three categories: machined components, that must be produced from some stock, fasteners (such as bolts, nuts, washers), and off-the shelf components, such as handles, feet, etc.
### Fasteners
---

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

## Production Information
---
[Fractory](https://fractory.com/) offers relatively affordable laser cut / bending options for mild steel or galvanised steel parts.

## Adjustable Feet
https://www.vital-parts.co.uk/weight-rated-tilting-adjustable-feet---wamf040-2523-p.asp

[No Mesothelioma hopefully](https://shop.vitcas.com/bio-soluble-fibre-blanket-1200-c-25mm.html)

# February 2026 - Frame Redesign
---
During manufacture of the frame, several issues were highlighted with the lower panel mounting solution and the upper panels. These, as well as final design iterations for other components, are discussed below.

## Lower panel mounting solution
---
When the frame structure was changed from using extruded aluminium sections to using angle bar brackets, a design flaw was missed; the lower frame panels cannot all be attached as the brackets do not retain the nuts like the extruded sections do. Therefore, the final panels to be mounted cannot use this nut and bolt connection. Instead, they must use a connection that only requires exterior access, such as a tapped hole and bolt.

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

The blocks can all be produced from a single length of 20 mm aluminium 6082T6 square bar using a chop saw and mill for hole drilling.

## Upper Panel Redesign
---
The original design of the upper panels has made drilling the upper holes accurately very difficult with available equipment. To address this, the upper section is to be redesigned. The panel design does not need to be adhered to, however all component interfaces must remain the same, and access cannot be lost to internal components, such as the terminal wiring.

### Single Wraparound Panel vs 8 Individual Panels
Two concepts have been imagined; a split panel design which resembles the current design but with flat panels and brackets as seen in the lower frame section, and a wraparound design, with one thin sheet of metal formed into an octagonal shape, with brackets as before and an access hatch for the terminal wiring. These concepts will be investigated for cost and viability, then one selected and pursued.

**Individual Panels Advantages**
- Repair and replacement will be cheaper for individual panels.
- Upgrading panels is simpler as they are flat and fit into a mill.
- Looser tolerances can be accepted as errors will not stack over the whole perimeter.

**Wraparound Design Advantages**
- The number of parts to produce is almost halved over the panel design.
- Access panels can be added, allowing tool-less opening of the upper frame.
- The upper frame will be stronger, as corners are connected. This permits a lighter sub-assembly, reducing risks of injury when handling the furnace, and improving stability.

Given the high cost of the wraparound design, as well as concerns regarding accuracy over 7 successive bends,  I have decided to go with the individual panel concept. Three panel variants must be designed:

- base panel
- lid hinge panel
- lifting handle panel

The panels have been made thinner, at 1.5 mm thick, to save weight, since the 2 mm lower panels are more than rigid enough.

## Lifting Handles
---
During transportation, the furnace will be lifted and carried by a set of handles on the side of the furnace. These handles must support the full weight of the furnace and be cool enough to touch during operation.

A spring loaded, stainless steel [handle](https://protex.com/95-637SS-spring-loaded-handle-stainless-steel-natural) has been selected, made by Protex. This has available CAD and meets all design requirements, while being made from a highly corrosion resistant material (this lets me trust that it will retain its strength after several years in a garage... in Leeds).

## Selecting the Lid Handle
---
Stupidly, I've lost the original lid handle, but have also produced a lid with drilled holes spaced at 100 mm apart. This means that unless I want to drill a really weirdly shaped object, I have to find a handle that's also 100 mm wide (they're not that common). [this](https://uk.rs-online.com/web/p/drawer-handles-cabinet-handles/9174321) handle would do the trick, but it's not stainless like I want, or the colour I'd like.

### Other Changes

> - chamber braces have been redesigned for manufacture
> - fasteners have been selected and added to the GA
> - the bill of materials has been updated to track all frame components
> - the furnace colour has been chosen: an off-white as a reference to [Cooker](https://wallaceandgromit.fandom.com/wiki/Cooker) from *A Grand Day Out*
> - Lid handle has been selected and added to the GA


