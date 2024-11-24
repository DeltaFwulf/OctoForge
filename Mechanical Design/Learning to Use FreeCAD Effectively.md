
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

-------------------------------------------------------------------------------
## Creating part variants

To create multiple variants of a part (for example, side panels with different holes cut into them), it's useful to create a base part, then reference this geometry in different, dependent bodies. To do this, create the base body, create the dependent body, then in the properties tab of the dependent part, select the base body in the base feature row.

-------------------------------------------------------------------------------
## Using Links

These seem to be a less janky way to create part variants than using base geometry. (populate with notes once you figure out how to use them properly).

[wiki page](https://wiki.freecad.org/Std_LinkMake#Usage)

These are quite useful for instancing objects, however it doesn't replace base geometry (linked objects are the same, like a pointer rather than a copy and modifications apply to all copies regardless of the copy edited).

-------------------------------------------------------------------------------
## Spreadsheets & Master Documents

note to self: you can use a single spreadsheet in a single master document over multiple directories. I have been working with a single master in each directory, which works until a dimension is shared between subassemblies.

-------------------------------------------------------------------------------
### Creating a Shell

This is called Part Thickness and can be found in the *Part* workbench.
[guide](https://forum.freecad.org/viewtopic.php?f=3&t=3766&p=29741&hilit=enclosure#p29547)
