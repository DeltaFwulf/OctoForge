
# Creating Assemblies
There seem to be two main addons capable of handling assemblies: A2Plus and Assembly4. Each has their own advantages and trade-offs, which will be discussed here.

## 1. A2Plus

**Pros** 
- uses an intuitive constraint system, quick to whip up a small assembly

**Cons**
- document linking seems fairly primitive: only geometry is imported from parts
- no obvious way to integrate subassemblies into parent assemblies
- unclear how to recompute assembly if a component changes

## 2. Assembly 4

**Pros**
- can handle subassemblies
- robust constraints that rely on geometry
- components are automatically recomputed

**Cons**
- setting up geometry for EVERY link can be very clunky
- a strict hierarchy is enforced i.e. I can only attach a part to the highest level of subassembly within a parent assembly, not that subassembly's individual components. This leads to excess geometry needing to be defined, or potentially weird subassembly hierarchies.

-------------------------------------------------------------------------------
For now, I think I'll stick with Assembly 4 as it appears to scale better than A2Plus. With large assemblies coming down the line in future projects, it makes more sense to prepare by learning best practices now.