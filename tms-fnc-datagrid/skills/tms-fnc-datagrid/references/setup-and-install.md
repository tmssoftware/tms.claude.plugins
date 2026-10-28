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

## Building from the command line (new project)

When you create a project yourself and build it with `msbuild`, a hand-written `.dproj` often fails before any grid code compiles:
- `F2613 Unit 'Windows' not found` / `'System.SysUtils' not found`: the `.dproj` has no `DCC_Namespace`, so unit scope names aren't resolved.
- `File not found: 'FMX.TMSFNCDataGrid.dcu'` / `'FMX.TMSFNCDataGridExcelIO'`: the build doesn't see the IDE library path. This happens when msbuild runs as another user or in a sandbox, where the IDE's registry settings aren't available.

This minimal FMX `.dproj` builds with `msbuild` without relying on the IDE's library path. Replace `<UIPACK>` and `<CORE>` with the `Source` folders of the installed `tms.fnc.uipack` and `tms.fnc.core`, and `MainForm.pas` with your units. The IDE upgrades the file when you open it.

```xml
<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <ProjectGuid>{00000000-0000-0000-0000-000000000001}</ProjectGuid>
    <ProjectVersion>20.3</ProjectVersion>
    <FrameworkType>FMX</FrameworkType>
    <MainSource>MyApp.dpr</MainSource>
    <Base>True</Base>
    <Config Condition="'$(Config)'==''">Debug</Config>
    <Platform Condition="'$(Platform)'==''">Win32</Platform>
    <TargetedPlatforms>1</TargetedPlatforms>
    <AppType>Application</AppType>
    <DCC_Namespace>Winapi;System.Win;Data.Win;System;Xml;Data;Datasnap;Web;Soap;$(DCC_Namespace)</DCC_Namespace>
    <DCC_ExeOutput>.\$(Platform)\$(Config)</DCC_ExeOutput>
    <DCC_DcuOutput>.\$(Platform)\$(Config)</DCC_DcuOutput>
    <DCC_DcuSearchPath>$(BDS)\lib\$(Platform)\release;$(DCC_DcuSearchPath)</DCC_DcuSearchPath>
    <DCC_UnitSearchPath><UIPACK>;<UIPACK>\xlsAdapter;<CORE>;$(DCC_UnitSearchPath)</DCC_UnitSearchPath>
    <DCC_Define>DEBUG;$(DCC_Define)</DCC_Define>
    <DCC_Optimize>false</DCC_Optimize>
    <DCC_DebugInformation>2</DCC_DebugInformation>
  </PropertyGroup>
  <ItemGroup>
    <DelphiCompile Include="$(MainSource)"><MainSource>MainSource</MainSource></DelphiCompile>
    <DCCReference Include="MainForm.pas" />
  </ItemGroup>
  <Import Project="$(BDS)\Bin\CodeGear.Delphi.Targets" />
</Project>
```

Run the build through a small batch file. Nesting `cmd /c "... && call "...rsvars.bat" && msbuild ..."` inside PowerShell mangles the quotes, and you get errors like `F1026 File not found: 'true.dpr'`:

```bat
:: build.cmd, next to the .dproj
@echo off
cd /d "%~dp0"
call "C:\Program Files (x86)\Embarcadero\Studio\<version>\bin\rsvars.bat"
set EXTRA=
:: In a sandbox (e.g. a coding agent's) the IDE's environment.proj exists but can't be read, which fails
:: every build with MSB4024. Then point APPDATA at an empty local folder so msbuild skips it; the .dproj
:: above has explicit search paths, so nothing from that file is needed.
type "%APPDATA%\Embarcadero\BDS\<version>\environment.proj" >nul 2>&1 || set EXTRA="/p:APPDATA=%~dp0.bdsenv" /p:EnvOptionsWarn=false
msbuild MyApp.dproj /t:Build /p:Config=Debug /p:Platform=Win32 /v:minimal %EXTRA%
```

Then run `cmd /c build.cmd` from any shell. Look for `0 Error(s)` in the output. Other build stoppers:
- `MSB4024 ... environment.proj could not be loaded. Access to the path ... is denied`: the build runs in a sandbox that can't read `%APPDATA%\Embarcadero`. The `build.cmd` above handles it. For a one-off build, add `"/p:APPDATA=<project folder>\.bdsenv" /p:EnvOptionsWarn=false` to the msbuild line.
- `F2039 Could not create output file '...exe'`: the app is still running from an earlier test. Close it first (only the instance you started).
- Garbled `€`, `·`, `é` in the running app: the `.pas` is UTF-8 **without BOM**. Save it with a BOM or use `#$20AC`-style character codes.

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
