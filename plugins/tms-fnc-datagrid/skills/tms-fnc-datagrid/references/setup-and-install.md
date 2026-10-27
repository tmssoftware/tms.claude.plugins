# TMS FNC DataGrid: setup and install

Verified against the source: `tms.fnc.uipack` 7.3.1.2 (`version.txt`), its `tmsbuild.yaml`, the `Packages\d13\*.dpk` files, the `*Reg.pas` units, and TMS Smart Setup `tms.exe` 3.5 (`tms help ...` output).

## Product and packages

- `TTMSFNCDataGrid` ships in **TMS FNC UI Pack**, Smart Setup product id **`tms.fnc.uipack`**. It is not a separate product.
- It depends on **TMS FNC Core**, product id **`tms.fnc.core`**. `tmsbuild.yaml` has `dependencies: - tms.fnc.core: TMS FNC Core`.
- Frameworks in `tmsbuild.yaml`: VCL (Delphi Berlin and later; win32, win64, win64x, winarm64ec), FMX (Delphi Berlin and later, all platforms), LCL (Lazarus). TMS WEB Core uses the `.\source` folder (`web core paths`).
- Packages (`Packages\d13`, with the same layout under `d11`, `d12`, `drio`, `dsydney`, `dtokyo`, `dberlin`):

| Package | Framework | `requires` (verified) |
|---|---|---|
| `VCLTMSFNCUIPackPkg` | VCL runtime + design | rtl, vcl, vclimg, VclSmp, dbrtl, bindengine, bindcomp, **TMSFNCCorePkg, VCLTMSFNCCorePkg**, dsnap, FireDAC, FireDACCommon |
| `FMXTMSFNCUIPackPkg` | FMX runtime + design | rtl, fmx, dbrtl, bindengine, bindcomp, **TMSFNCCorePkg, FMXTMSFNCCorePkg**, dsnap, FireDAC, FireDACCommon |
| `TMSFNCUIPackPkgDE` | design-time editors (VCL+FMX) | |
| `Packages\web\TMSFNCUIPackWEB` | TMS WEB Core | webcore, **TMSFNCCoreWEB** |

- The grid, the database adapter, PDF IO, Print IO **and Excel IO** (`Source\xlsAdapter\`) are all compiled into the same VCL/FMX package. Excel IO needs no other product, but it is **not** in the WEB package (see export.md).
- The packages require FireDAC and dsnap, so the Delphi edition must include them.

## Install with TMS Smart Setup (`tms` CLI)

Commands verified from `tms.exe` 3.5 help output:

```bat
:: 1. one-time: store your TMS account credentials (prompts for email + registration code)
tms credentials
::   non-interactive form (options verified in "tms help credentials"):
tms credentials -email:you@example.com -code:YOUR-CODE -check

:: 2. see what your license can install
tms list-remote

:: 3. install the UI Pack (downloads, builds the packages, registers them in the IDEs)
tms install tms.fnc.uipack

:: later
tms update tms.fnc.uipack      :: same as "tms fetch" followed by "tms build"
tms list                       :: list installed products
tms doctor                     :: check and optionally fix common Delphi installation problems
```

- `tms install` takes several ids (`tms install tms.fnc.core tms.fnc.uipack`) and wildcards (examples in help: `tms install tms.biz.*`). Option `-nobuild` downloads without building.
- Smart Setup resolves dependencies from `tmsbuild.yaml`, so installing `tms.fnc.uipack` also installs `tms.fnc.core`. Naming both ids is also fine.
- Limit Delphi versions or platforms with `-p:`, for example (syntax from the help text):
  `tms install tms.fnc.uipack "-p:configuration-for-all-products:platforms=[win32intel,win64intel]"`
- `tmsgui.exe` is the GUI front end that ships next to `tms.exe`.
- Docs: https://doc.tmssoftware.com/smartsetup and https://doc.tmssoftware.com/fnc/uipack/

## Checking that it is installed

- `tms list` shows `tms.fnc.uipack` and `tms.fnc.core`.
- IDE Tool Palette page **`TMS FNC UI`**. All Reg units call `RegisterComponents('TMS FNC UI', [...])` with:
  - `TTMSFNCDataGrid`, `TTMSFNCDataGridRendererSource` (`*.TMSFNCDataGridReg`)
  - `TTMSFNCDataGridDatabaseAdapter` (`*.TMSFNCDataGridDatabaseAdapterReg`)
  - `TTMSFNCDataGridPDFIO` (`*.TMSFNCDataGridPDFIOReg`)
  - `TTMSFNCDataGridPrintIO` (`*.TMSFNCDataGridPrintIOReg`)
  - `TTMSFNCDataGridExcelIO` (`VCL.`/`FMX.TMSFNCDataGridExcelIOReg`, VCL and FMX only)
- Compile check: a unit containing `uses VCL.TMSFNCDataGrid;` (or `FMX.` / `WEBLib.`) compiles. "File not found: VCL.TMSFNCDataGrid.dcu" means the library path is missing the UI Pack output, so run `tms build` or `tms doctor`. A missing `VCL.TMSFNCTypes` / `VCL.TMSFNCCustomControl` means FNC Core is missing.

## Unit prefixes per framework

The same unit names exist with three prefixes: `VCL.`, `FMX.`, `WEBLib.`. Never mix VCL and FMX units in one unit.

| Purpose | Unit (VCL shown; use `FMX.` / `WEBLib.` for the others) |
|---|---|
| Grid component `TTMSFNCDataGrid`, `TTMSFNCCustomDataGrid` | `VCL.TMSFNCDataGrid` |
| `TTMSFNCDataGridCellCoord`, `TTMSFNCDataGridSortDirection` (`gsdAscending`...) | `VCL.TMSFNCDataGridCore` |
| `TTMSFNCDataGridCell`, `TTMSFNCDataGridCellValue` (= `TValue`; `JSValue` on WEB) | `VCL.TMSFNCDataGridCell` |
| Filter/sort data classes (`TTMSFNCDataGridDataFilterData`), options | `VCL.TMSFNCDataGridData` |
| `TTMSFNCDataGridRenderer`, `TTMSFNCDataGridScrollMode`, `TTMSFNCDataGridInplaceEditor` | `VCL.TMSFNCDataGridRenderer` |
| Base | `VCL.TMSFNCDataGridBase` |
| Dataset binding | `VCL.TMSFNCDataGridDatabaseAdapter` |
| PDF / Print / Excel | `VCL.TMSFNCDataGridPDFIO`, `VCL.TMSFNCDataGridPrintIO`, `VCL.TMSFNCDataGridExcelIO` |
| FNC Core helpers | `VCL.TMSFNCTypes`, `VCL.TMSFNCUtils`, `VCL.TMSFNCGraphics`, `VCL.TMSFNCGraphicsTypes`, `VCL.TMSFNCCustomControl`, `VCL.TMSFNCCustomComponent` |

`TTMSFNCDataGridCellValue` is `TValue`, so add `System.Rtti` when event handlers use it. The demos always include it.

Typical VCL uses clause (taken from the demo `VCL\DataGrid\Database\Biolife_ClientDataSet`):

```delphi
uses
  System.SysUtils, System.Classes, System.Rtti, Vcl.Controls, Vcl.Forms,
  VCL.TMSFNCTypes, VCL.TMSFNCUtils, VCL.TMSFNCGraphics, VCL.TMSFNCGraphicsTypes,
  VCL.TMSFNCCustomControl, VCL.TMSFNCCustomComponent,
  VCL.TMSFNCDataGridCell, VCL.TMSFNCDataGridData, VCL.TMSFNCDataGridBase,
  VCL.TMSFNCDataGridCore, VCL.TMSFNCDataGridRenderer, VCL.TMSFNCDataGrid,
  Data.DB, VCL.TMSFNCDataGridDatabaseAdapter;
```

FMX is the same with `FMX.` prefixes plus `FMX.Types, FMX.Controls, FMX.Forms`. On FMX, `TTMSFNCDataGridCellControl` / `TTMSFNCDataGridInplaceEditor` are `TControl`; on VCL and WEB they are `TWinControl`.

## Creating the grid in code

```delphi
// VCL
uses VCL.TMSFNCDataGrid;
var Grid: TTMSFNCDataGrid;
...
Grid := TTMSFNCDataGrid.Create(Self);
Grid.Parent := Self;          // required, or nothing is shown
Grid.Align := alClient;       // FMX: Grid.Align := TAlignLayout.Client;
Grid.BeginUpdate;
try
  Grid.ColumnCount := 5;      // default 4
  Grid.RowCount := 20;        // default 24, includes FixedRowCount (default 1)
  Grid.Cells[1, 1] := 'Hello';          // Cells[AColumn, ARow]: TTMSFNCDataGridCellValue
  Grid.Strings[2, 1] := 'text';         // Strings[AColumn, ARow]: string
  Grid.AutoNumberColumn(0);             // AutoNumberColumn(AColumn; AStartRow = 0; AStartValue = 0)
finally
  Grid.EndUpdate;
end;
```

Index order is always **column first, then row**: `Cells[ACol, ARow]`, `Layouts[ACol, ARow]`, `MergeCells(ACol, ARow, AColCount, ARowCount)`.

Verified helpers used in the demos: `LoadSampleData`, `RandomFill(ADoFixed: Boolean = False; ARandomNumber: Integer = 100)`, `AutoSizeColumns(const AMode: TTMSFNCDataGridAutoSizeMode = gamAllCells; const APadding: Integer = 5)`, `AutoSizeGrid(...)`, `ColumnWidths[AColumn]: Double`, `LoadFromCSVData(AFileName: string)`, `SaveToCSVData(AFileName: string)`, `ScrollMode := gsmCellScrolling` (default `gsmPixelScrolling`).

## TMS WEB Core specifics

- Units use the `WEBLib.` prefix (`WEBLib.TMSFNCDataGrid`, `WEBLib.TMSFNCDataGridDatabaseAdapter`, `WEBLib.TMSFNCDataGridPDFIO`, ...). They are prefix-renamed copies of the VCL sources, so class and member names are identical.
- Package `TMSFNCUIPackWEB` requires `TMSFNCCoreWEB`. Smart Setup adds `.\source` to the TMS WEB Core library path (`web core paths` in `tmsbuild.yaml`).
- The UI Pack WEB demos (`WEB\DataGrid\...`) list **both** `WEBLib.TMSFNC*` and `VCL.TMSFNC*` units in the interface uses clause (the IDE adds the VCL ones for the form designer). Keep what the IDE generates and do not delete either set by hand. Forms are `TWebForm`, with `WEBLib.Forms`, `WEBLib.StdCtrls`, `WEBLib.ExtCtrls`, `JS`, `Web`.
- Not available on WEB: `TTMSFNCDataGridExcelIO` (attribute `TMSPlatformsDesktop`, not in the WEB package). Available on WEB: the grid, `TTMSFNCDataGridDatabaseAdapter`, `TTMSFNCDataGridPDFIO`, `TTMSFNCDataGridPrintIO` (`[ComponentPlatformsAttribute(TMSPlatformsWEB)]`).
- Datasets on WEB: the adapter uses unit `DB` (instead of `Data.DB`) and recognises `TCustomClientDataSet` from `WEBLib.CDS` for built-in sorting. The FireDAC and `TTMSFNCCustomDataSet` sort paths are VCL/FMX only. There is no WEB database demo in the demos tree.
- PDF export on WEB needs fonts loaded into the font cache first (see export.md, `AddFontToCache` / `Application.OnFontCacheReady`).

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `tms install tms.fnc.datagrid` / `tms.fnc.grid` | `tms install tms.fnc.uipack` (the grid is part of the UI Pack) |
| `tms login` / `tms register` | `tms credentials` |
| `tms --help` (gives "Unknown command line option") | `tms help <command>`, or plain `tms` |
| Palette page "TMS FNC DataGrid" / "TMS FNC Grid" | `TMS FNC UI` |
| `uses TMSFNCDataGrid;` (no prefix) | `VCL.TMSFNCDataGrid` / `FMX.TMSFNCDataGrid` / `WEBLib.TMSFNCDataGrid` |
| `TTMSFNCGrid` (older FNC grid, `*.TMSFNCGrid`) | `TTMSFNCDataGrid`. They are different components, and the old grid has its own `TTMSFNCGridExcelIO` etc. Do not mix their units or events |
| `Grid.Cells[ARow, ACol]` | `Grid.Cells[AColumn, ARow]` |
| `Grid.ColCount` | `Grid.ColumnCount` |
| Forgetting `Parent` when creating at run time | `Grid.Parent := Self` |
| Excel export in a WEB Core app | Not available. Use PDF, `SaveToCSVData`, or the renderer's `SaveToHTMLData` |
