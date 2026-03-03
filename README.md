# OctoForge: 
A work in progress electric furnace capable of reaching chamber temperatures of 1200 C.

This project is simply a display of technical knowledge and something through which we have learned further technologies. The hope is that any projects tackled in the future will be easier due to the experience and skills learned here.

There are three main areas of which the furnace is comprised:
- Mechanical - Frame design complete and in production, insulation under final design iteration, heating element under final design iteration.
- Power electronics - Still iterating over design and testing.
- Control electronics - Yet to be started.

Progress is being tracked [here](https://github.com/users/DeltaFwulf/projects/2).

![Screenshot of OctoForge](/resources/furnace-screenshot-03-03-2026.png)

## How to use this project?
The following software is required to view the various CAD files:
- FreeCAD-1.0.2
- KiCAD-9.0

## How to reproduce OctoForge?
- Sheet metal components were ordered from [Fractory](https://fractory.com/) with the following parameters:
  - Thicknesses:
    - Plates: 3mm
    - Lower panels: 2mm
    - Upper panels: 1.5mm
    - Lid: 2mm
  - High temperature components will be black oxide treated, and exterior components will be painted with high temperature paint and clear coat.
- The other mechanical components were machined from stock using the drawings provided within the CAD directory.
- Fittings were ordered using the provided [BOM](Documentation/Mechanical/BOM.ods) from [Accu](https://www.accu.co.uk/) and [Vital Parts](https://www.vital-parts.co.uk/).
- Feet and handles are standard components, but were sourced from WDS components as listed in the BOM.
- PCBs were ordered from [JLCPCB](jlcpcb.com) with the following parameters:
  - 2 layers
  - PCB thickness - 1.6mm
  - Material type - TG135
  - Outer copper weight - 1oz
