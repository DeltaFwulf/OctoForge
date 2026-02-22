
# Creating Assemblies
There seem to be two main addons capable of handling assemblies: A2Plus and Assembly4. Each has their own advantages and trade-offs, which will be discussed here.

## 1. A2Plus

**Pros** 
- uses an intuitive constraint system, quick to whip up a small assembly

**Cons**
- document linking seems fairly primitive: only geometry is imported from parts
- no obvious way to integrate subassemblies into parent assemblies
- unclear how to recompute assembly if a component changes

## 2. Assembly 4 (preferred)

**Pros**
- can handle subassemblies
- robust constraints that rely on geometry
- components are automatically recomputed
- actively being maintained, compatible with v0.21

**Cons**
- setting up geometry for EVERY link can be very clunky
- a strict hierarchy is enforced i.e. I can only attach a part to the highest level of subassembly within a parent assembly, not that subassembly's individual components. This leads to excess geometry needing to be defined, or potentially weird subassembly hierarchies. **EDIT** - you can use "import datum object" to pull lower level geometry up to the required level, solving this issue.

For now, I think I'll stick with Assembly 4 as it appears to scale better than A2Plus. With large assemblies coming down the line in future projects, it makes more sense to prepare by learning best practices now.

N.B. it is quite convenient to create simpler assemblies (2 or 3 minor components) just using the Part object with several bodies contained within.

**22/02/2026**
Until further notice, all assemblies must use the integrated assembly workbench for compatibility with existing models.

-------------------------------------------------------------------------------
## Creating part variants

To create multiple variants of a part (for example, side panels with different holes cut into them), it's useful to create a base part, then reference this geometry in different, dependent bodies. To do this, create the base body, create the dependent body, then in the properties tab of the dependent part, select the base body in the base feature row.

**22/02/2026**
A better method for this is to use [clones](https://wiki.freecad.org/PartDesign_Clone). For example, when panels with the same overall footprint but different hole patterns are required, the base panel with only share features should be made in one body, then cloned to create other bodies. These then reference the original geometry directly, and can have their own downstream geometries. [Here](https://www.youtube.com/watch?v=6_FBijwp-l0) is a good video explaining this feature.

-------------------------------------------------------------------------------
## Spreadsheets & Master Documents

note to self: you can use a single spreadsheet in a single master document over multiple directories. I have been working with a single master in each directory, which works until a dimension is shared between subassemblies.

-------------------------------------------------------------------------------
### Creating a Shell

This is called Part Thickness and can be found in the *Part* workbench.
[guide](https://forum.freecad.org/viewtopic.php?f=3&t=3766&p=29741&hilit=enclosure#p29547)

## Generating a Bill of Materials (BOM)
---
**21/02/2026**
Get ready for some bullshit. This is the current best way I've found to add many components to an assembly and also get some sort of information about quantities inside of a BOM. 

- Do not use Draft WB arrays - they will not appear in the assembly BOM [see here](https://github.com/FreeCAD/FreeCAD/issues/26221), and the fastener BOM lists them but gives quantity 0.
- If link arrays are used, they do not appear at all in the BOM, however they do appear in the fastener WB BOM.

To get the fastener BOM to show all fasteners, fasteners can be created, placed using the assembly, but placing the fasteners into their own part containers. To include the fasteners in the assembly, they can later be added by dragging into the assembly and dragging back out (this is the only way the insert component will recognise it as able to be added).

Hot tip: if fasteners are not visible, they are not added to the fastener BOM - use this to hide any duplicates, either those in the assembly or those in the part containers.

Each type of fastener has been added to a part. For example, the lower panel bracket fasteners have all been added to the *Lower panel bracket fasteners* part. In this method, if link arrays are convenient, they have been used; otherwise, placement was manual for each occurrence of each fastener.

The fastener BOM should now show all occurrences of all fasteners this way.