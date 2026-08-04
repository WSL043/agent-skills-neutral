# Implementation variants

## Analysis and ordinary creation

Use dataframe and workbook libraries for efficient reading, formulas, tables, charts, and consistent formatting.

## Format-preserving edit

Unpack the workbook and edit only targeted XML parts when unsupported features such as macros, pivots, slicers, or complex drawings must survive. Compare package parts before and after, then repackage and recalculate.
