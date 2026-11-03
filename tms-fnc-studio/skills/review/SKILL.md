---
name: review
description: >
  This skill should be used when the user asks to "review my TMS FNC code", "check my TTMSFNCDataGrid / TTMSFNCTreeView /
  TTMSFNCPlanner / TTMSFNCRichEditor usage", "why doesn't this FNC code compile", "is this the right way to use the TMS
  FNC grid / tree view / planner / PDF lib", or invokes /review in a Delphi project that uses TMS FNC UI Pack or TMS FNC
  Core. It checks FNC code for members that don't exist, framework unit mismatches, missing update brackets and other
  common mistakes, and proposes fixes.
argument-hint: "[unit or folder]"
metadata:
  version: "0.2.0"
---

# Review TMS FNC UI Pack and TMS FNC Core usage

Check the user's TMS FNC code against the real API and report problems with concrete fixes. First see which FNC classes the code uses, then load the matching skills and keep their references open while reviewing:
- `TTMSFNCDataGrid*` → `tms-fnc-datagrid`
- Other `TTMSFNC*` UI Pack controls → `tms-fnc-uipack` (find the class in `setup-and-components.md`, then read its file)
- Core classes (`TTMSFNCGraphics`, `TTMSFNCBitmapContainer`, `TTMSFNCPDFLib`, `TTMSFNCWebBrowser`, `TTMSFNCPersistence`, `TTMSFNCUtils`, `TTMSFNCCloudBase`, ...) → `tms-fnc-core`

Review from the references, not from component source code (many users have trial or DCU-only installs). When a member isn't covered by the references, check the official API reference at doc.tmssoftware.com if web access is available, or confirm it by compiling. If it still can't be confirmed, report it as "unverified" rather than calling it wrong or right.

## Scope

Review the unit or folder given as argument, otherwise every unit in the project that references a `TMSFNC` unit. Include `.dfm`/`.fmx` files for those forms: published properties set at design time count too.

## Checks

Go through each, in order of severity:

1. **Members that don't exist**: properties, methods, events or enum values that aren't in the API. These are often names carried over from VCL/FMX standard controls, TMS VCL UI Pack (`TAdv*`), the older TTMSFNCGrid, or another FNC control. Check against the "Does not exist / common mistakes" sections of the relevant reference files.
2. **Wrong signatures**: event handlers whose parameters don't match the documented declarations, wrong argument order or types, wrong value types, wrong enum prefixes. For the DataGrid, the known traps are in its skill (`GroupAverage`, inline anonymous methods on overloaded `Group*` calls, `TPath` in FMX units).
3. **Display and formatting order**: formatting events or formats assigned after data is loaded, hard-coded number formats that depend on the Windows locale (see the datagrid `styling.md`).
4. **Framework mismatch**: mixing `VCL.`, `FMX.` and `WEBLib.` prefixed TMS units in one form, the wrong prefix for the project's framework, or a unit or class that doesn't exist for that framework (the references list framework-only classes).
5. **Missing dependencies**: extra components (database adapters, PDF/Excel/print IO, toolbars, bitmap containers) used without their unit, or features that need another product or runtime (for example the WebView2 runtime for the web browser and Memo on Windows).
6. **Database binding mistakes**: filling a control by hand while a database adapter is connected, dataset not opened, adapter not linked to the control or data source, field mappings missing, per the control's reference.
7. **Performance**: bulk updates without `BeginUpdate`/`EndUpdate`; reloading all data where a targeted update exists; collection mode where virtual mode fits large data (TreeView).
8. **Lifetime & ownership**: components created without an owner and never freed, objects returned by FNC methods freed when the control owns them (or leaked when the caller owns them), event handlers on freed objects.
9. **Simpler built-in alternatives**: hand-written sorting, filtering, grouping, drawing, persistence or export code where the FNC control or Core already has the feature. Point to `/unlock-feature`.

## Report

For each finding give: file and line, what's wrong in one sentence, and the corrected code. Order by severity: won't compile, wrong at runtime, then performance and style. Finish with a one-line overall verdict. If nothing is wrong, say so plainly.

Ask before applying fixes. When the user agrees, apply them, then offer to compile, or ask the user to compile.
