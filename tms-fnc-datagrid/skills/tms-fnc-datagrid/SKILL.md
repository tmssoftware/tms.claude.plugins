---
name: tms-fnc-datagrid
description: >
  Accurate API knowledge for TMS FNC DataGrid (TTMSFNCDataGrid) in Delphi for VCL, FMX and TMS WEB Core, part of
  the TMS FNC UI Pack. This skill should be used whenever code references TTMSFNCDataGrid, TMSFNCDataGrid units
  (VCL.TMSFNCDataGrid, FMX.TMSFNCDataGrid, WEBLib.TMSFNCDataGrid), TTMSFNCDataGridDatabaseAdapter,
  TTMSFNCDataGridPDFIO, TTMSFNCDataGridExcelIO, TTMSFNCDataGridPrintIO, TTMSFNCDataGridRenderer or
  TTMSFNCDataGridConditionalFormatting, or when the user asks how to fill, sort, filter, group, merge, edit, format,
  bind to a database, or export a TMS FNC data grid. Read it before writing or reviewing any TMS FNC DataGrid code,
  because the real API differs from TStringGrid, TAdvStringGrid and the older TTMSFNCGrid.
metadata:
  version: "0.1.3"
---

# TMS FNC DataGrid API knowledge

TTMSFNCDataGrid is the data grid in the TMS FNC UI Pack (product id `tms.fnc.uipack`, depends on TMS FNC Core). The same API works in VCL, FMX and TMS WEB Core. Only the unit prefix (`VCL.`, `FMX.`, `WEBLib.`) and a few types differ.

## Ground rules

- **Never guess member names.** Use only members in the reference files below. If something isn't covered, verify it in the installed source (`*.TMSFNCDataGrid*.pas` in the UI Pack's `Source` folder) before using it. If it can't be verified, say so instead of inventing it.
- **Don't carry over names from other grids.** TStringGrid, TAdvStringGrid and the older TTMSFNCGrid have similar-looking but different APIs. Each reference file ends with a "Does not exist / common mistakes" list; check it.
- **Match the framework.** All TMS units in a form use the same prefix as the project's framework.
- **Bracket bulk changes** with `BeginUpdate` / `EndUpdate`.
- Prefer patterns from the reference files (derived from the official demos) over invented approaches.

## The pitfalls that matter most

1. Cell indexing is `Cells[AColumn, ARow]`, and the counts are `ColumnCount` / `RowCount`. There is no `ColCount`, `FixedCols` or `ColWidths`.
2. `Cells[c, r]` is a `TValue` (VCL/FMX) or `JSValue` (WEB), not a string. Read text with `Strings[c, r]`.
3. Column properties set **in code** (type, editor, formatting, read-only, appearance, filter) are ignored unless the matching `Columns[i].AddSetting(gcs...)` is called. The designer adds these settings automatically; code doesn't.
4. `Sender` in grid events is the internal renderer, not the grid. Don't cast it to `TTMSFNCDataGrid`. Use the form's grid field.
5. Column captions are row 0 (`Columns[i].Header` maps to `Cells[i, 0]`). `Grid.Header` / `Grid.Footer` are separate bars above and below the grid.
6. Sorting and filtering UI is off until `Options.Sorting.Enabled` / `Options.Filtering.Enabled` is set. Editing is on by default. `Options.Sorting.CaseSensitive` defaults to True.
7. Filtering in code: build rules with `Filter.Add` / `Filter.ColumnFilter[c]`, then call `ApplyFilter`. `RemoveFilter` only unhides rows and keeps the rules; `ClearFilter` drops them. Reading `Filter.ColumnFilter[c]` creates a rule, so test with `HasFilter(c)`.
8. A filter row is not a separate component: add a fixed row and set `Options.Filtering.Row` (see `filter-row.md`).
9. `Group([a, b])` is **one** level keyed on both columns. Nested levels need `Group(CreateGroupInfo([a], [b]))`. `Group` does nothing if the grid is already grouped (call `Ungroup` first) or has merged data cells.
10. `MergeCells(AColumn, ARow, AColumnCount, ARowCount)` takes **counts**, not end coordinates. Avoid `MergeColumn(s)` / `MergeRow(s)` when the grid has fixed rows or columns (the range overruns and nothing merges); use explicit `MergeCells`.
11. Database binding direction: `Grid.Adapter := Adapter; Adapter.DataSource := DataSource;`. There is no `Grid.DataSource` and no `Adapter.Grid`. Edits aren't posted until the record changes or `Adapter.DataSetPost` is called. The default `LoadMode` (`almBuffered`) disables in-grid grouping and multi-column sorting; use `almAllRecords` for those.
12. Export uses separate components linked through their `DataGrid` property: `TTMSFNCDataGridPDFIO.Save`, `TTMSFNCDataGridExcelIO.XLSExport` (VCL/FMX only, `.xls`), `TTMSFNCDataGridPrintIO.Print`. There is no `Grid.ExportToPDF` / `SaveToXLS`. The `TTMSFNCGrid...IO` classes are for the older grid. Excel export skips grid row 0 (the column captions) and column 0 by default (`DataGridStartRow` / `DataGridStartCol` = 1). Set both to `0` to export the whole grid.
13. In WEB, `LoadFromCSVData` loads asynchronously, so code that runs straight after it may see no data.
14. On the grid, `GroupAverage(AColumn)` has **no** callback parameter. For a formatted average use `GroupAverage([AColumn], ACallback)`. Assign every anonymous callback (group text, calculation options) to a **typed variable** before passing it to an overloaded `Group*` method; inline anonymous methods trigger "no overloaded version" errors.
15. Display text is computed when a value is written. Assign `OnGetCellFormatting` / `OnGetCellDisplayValue` and column formats **before** filling the grid, and set `FormatSettings` separators at startup when a fixed number format (e.g. `€ 12,345.00`) is required. Otherwise the Windows locale decides.
16. A data checkbox column still draws `True`/`False` behind the checkbox. Hide the text (`ACell.Layout.Font.Color := TAlphaColors.Null` in `OnGetCellLayout`), never the value.
17. For a styled or "dashboard" grid, start from the recipe in `references/styling.md` instead of discovering layout properties one build at a time. To check the look, have the app save an image of itself. Never capture the user's whole desktop.

## Reference files

Read the file(s) for the task at hand. Don't load all of them.

| File | Covers |
|---|---|
| `references/setup-and-install.md` | Product/package, TMS Smart Setup install commands, palette page, uses clauses per framework, creating the grid in code, a minimal `.dproj` + `build.cmd` for command-line builds, WEB Core specifics |
| `references/core-api.md` | Class structure, data access, rows/columns, column settings, appearance, selection, key events |
| `references/styling.md` | Dashboard look in one pass: state layouts, per-cell layout, locale-proof number/date formats, checkbox and data-bar columns, checking the look safely |
| `references/editing.md` | Editing options, editors per column, validation, AutoFill, clipboard |
| `references/sorting-filtering.md` | Sorting (multi-column, custom compare), filtering API and UI |
| `references/filter-row.md` | Filter row setup and filter editor controls |
| `references/grouping.md` | Single/multi-level grouping, drag-to-group, summaries, expand/collapse |
| `references/merging.md` | Merging and splitting cells |
| `references/cell-controls.md` | Checkboxes, buttons, progress bars, embedded controls, grid in grid |
| `references/conditional-formatting.md` | Conditional formatting component, rules, priorities, expressions |
| `references/renderer.md` | Renderer vs data, renderer source, non-visual data processing/export |
| `references/database.md` | Database adapter, load modes, editing write-back, master-detail, FireDAC/ClientDataSet |
| `references/export.md` | PDF, Excel and print components |

## Related skills

- `/get-started`: add a working grid to a project.
- `/unlock-feature`: add an advanced feature to an existing grid.
- `/review`: check existing grid code against this API.
