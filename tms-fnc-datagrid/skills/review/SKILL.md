---
name: review
description: >
  This skill should be used when the user asks to "review my TMS FNC DataGrid code", "check my TTMSFNCDataGrid usage",
  "why doesn't this grid code compile", "is this the right way to use the TMS data grid", or invokes /review in a
  Delphi project that uses TTMSFNCDataGrid. It checks grid code for members that don't exist, framework unit mismatches,
  missing update brackets and other common mistakes, and proposes fixes.
argument-hint: "[unit or folder]"
metadata:
  version: "0.1.2"
---

# Review TMS FNC DataGrid usage

Check the user's TTMSFNCDataGrid code against the real API and report problems with concrete fixes. Load the `tms-fnc-datagrid` skill first and keep its references open while reviewing. When a member isn't covered by the references, verify it in the user's installed source (`VCL.TMSFNCDataGrid*.pas` / `FMX.TMSFNCDataGrid*.pas`, usually under the TMS FNC UI Pack install folder) before calling it wrong or right.

## Scope

Review the unit or folder given as argument, otherwise every unit in the project that references `TMSFNCDataGrid`. Include `.dfm`/`.fmx` files for those forms: published properties set at design time count too.

## Checks

Go through each, in order of severity:

1. **Members that don't exist**: properties, methods, events or enum values that aren't in the API. These are often names carried over from TAdvStringGrid, TTMSFNCGrid or TStringGrid. Check against the "Does not exist / common mistakes" sections of every reference file.
2. **Wrong signatures**: event handlers whose parameters don't match the documented declarations, wrong argument order or types (e.g. column/row order in cell access), wrong value types. Known traps: `Grid.GroupAverage(ACol, ACallback)` (the grid only has `GroupAverage([ACol], ACallback)`), inline anonymous methods passed to overloaded `Group*` calls (use typed variables), and `TPath.Combine` in FMX units, where `TPath` is `FMX.Objects.TPath` (see `grouping.md`, `export.md`).
3. **Display and formatting order**: `OnGetCellFormatting` / `OnGetCellDisplayValue` assigned after the grid is filled, hard-coded number formats that depend on the Windows locale, or `True`/`False` text left visible behind data checkboxes (see `styling.md`).
4. **Framework mismatch**: mixing `VCL.`, `FMX.` and `WEBLib.` prefixed TMS units in one form, or the wrong prefix for the project's framework.
5. **Missing dependencies**: extra components (database adapter, PDF/Excel/print IO) used without their unit, or features that need a separate product per `export.md` / `setup-and-install.md`.
6. **Database binding mistakes**: filling cells by hand while a database adapter is connected, dataset not opened, adapter not linked to the grid or data source, per `database.md`.
7. **Performance**: bulk cell updates, row additions or column setup without `BeginUpdate`/`EndUpdate`; reloading all data where a targeted update exists.
8. **Lifetime & ownership**: grids or helper components created without an owner and never freed, event handlers on freed objects.
9. **Simpler built-in alternatives**: hand-written sorting, filtering, grouping, colouring or export code where the grid has a built-in feature. Point to `/unlock-feature`.

## Report

For each finding give: file and line, what's wrong in one sentence, and the corrected code. Order by severity: won't compile, wrong at runtime, then performance and style. Finish with a one-line overall verdict. If nothing is wrong, say so plainly.

Ask before applying fixes. When the user agrees, apply them, then offer to compile, or ask the user to compile.
