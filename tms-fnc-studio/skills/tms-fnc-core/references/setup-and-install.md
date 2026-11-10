# TMS FNC Core: setup, install, units and base classes (TTMSFNCCustomControl, TTMSFNCCustomComponent)
> Sections (line ranges): 6-23 Product and packages · 24-47 Install with TMS Smart Setup · 48-68 Components and palette pages · 69-87 Unit prefix rules · 88-100 Which unit declares what · 101-143 Base classes · 144-150 Common types · 151-166 Minimal runtime creation · 167-170 Building from the command line · 171-186 Does not exist / common mistakes

Verified against the source: `tms.fnc.core` 4.5.0.0 (`version.txt`), its `tmsbuild.yaml`, `Packages\d13\*.dpk`, `Packages\web\TMSFNCCoreWEB.dpk`, every `*Reg.pas` / `*RegDE.pas` unit, `VCL.TMSFNCCustomControl`, `VCL.TMSFNCCustomComponent`, `VCL.TMSFNCTypes`, `VCL.TMSFNCGraphicsTypes`. `tms` CLI commands as verified for the DataGrid setup file (Smart Setup `tms.exe` 3.5).

## Product and packages

- Smart Setup product id **`tms.fnc.core`** ("TMS FNC Core"). Every other FNC product (UI Pack, Maps, Cloud Pack, ...) depends on it. It has no dependencies itself.
- Frameworks in `tmsbuild.yaml`: VCL (Delphi Berlin and later; win32, win64, win64x, winarm64ec, C++Builder supported), FMX (Delphi Berlin and later, all platforms, C++Builder supported), LCL (Lazarus). TMS WEB Core uses the `.\source` folder (`web core paths`).
- `tmsbuild.yaml` also links `Edge Support\x86\WebView2Loader_x86.dll` / `x64\WebView2Loader_x64.dll` (needed by the browser components on Windows).
- Packages (`Packages\d13`, same layout under `d11`, `d12`, `drio`, `dsydney`, `dtokyo`, `dberlin`):

| Package | Framework | `requires` (verified) | Contains |
|---|---|---|---|
| `TMSFNCCorePkg` | framework-neutral runtime | rtl, dbrtl | the `TMS.*` data units: `TMS.TMSFNCDataSet`, `TMS.TMSFNCDataLinkCSV`, `TMS.TMSFNCDataLinkJSON`, `TMS.TMSFNCFilterBuilder`, `TMS.TMSFNCFilterRulesManager`, `TMS.TMSFNCValue`, `TMS.TMSFNCObjectResolver`, `Next.Core.*` |
| `VCLTMSFNCCorePkg` | VCL runtime | rtl, vcl, vclimg, VclSmp, vclie, xmlrtl, vclwinx, dbrtl, bindcomp, **TMSFNCCorePkg** | all `VCL.TMSFNC*` units |
| `FMXTMSFNCCorePkg` | FMX runtime | rtl, fmx, xmlrtl, dbrtl, bindengine, bindcomp, **TMSFNCCorePkg** | all `FMX.TMSFNC*` units, plus per-OS units (`.Android`, `.iOS`, `.Mac`, `.Unix`) |
| `TMSFNCCorePkgDE` | design-time (VCL + FMX) | rtl, designide, dcldb, FMXTMSFNCCorePkg, VCLTMSFNCCorePkg, TMSFNCCorePkg | property editors, `*GeneralRegDE` |
| `Packages\web\TMSFNCCoreWEB` | TMS WEB Core | webcore | `WEBLib.TMSFNC*` units |
| `Packages\lazarus\LCLTMSFNCCorePkg(.lpk)` / `LCLTMSFNCCorePkgDE` | Lazarus | | `LCLTMSFNC*` units |

UI Pack packages require `TMSFNCCorePkg` + `VCLTMSFNCCorePkg` (or `FMXTMSFNCCorePkg`); `TMSFNCUIPackWEB` requires `TMSFNCCoreWEB`.

## Install with TMS Smart Setup (`tms` CLI)

**The user runs these commands themselves.** `tms credentials` stores their TMS account details and the install commands download from TMS. Never run them for the user, never ask for, read or type their e-mail or registration code, and never pass them on the command line. Show the commands and let the user run them in their own terminal.

```bat
:: 1. one-time: the user enters their TMS account details when prompted
tms credentials

:: 2. see what your license can install
tms list-remote

:: 3. install FNC Core (downloads, builds the packages, registers them in the IDEs)
tms install tms.fnc.core

:: later
tms update tms.fnc.core        :: same as "tms fetch" followed by "tms build"
tms list                       :: list installed products
tms doctor                     :: check and optionally fix common Delphi installation problems
```

- Installing any FNC product (`tms install tms.fnc.uipack`) installs `tms.fnc.core` automatically (dependency in that product's `tmsbuild.yaml`). FNC Core on its own only gives the non-visual helpers and the components below.
- `tms install` accepts several ids and wildcards (`tms install tms.fnc.*`); `-nobuild` downloads without building; limit IDEs/platforms with `"-p:configuration-for-all-products:platforms=[win32intel,win64intel]"`.
- `tmsgui.exe` is the GUI front end. Docs: https://doc.tmssoftware.com/smartsetup and https://doc.tmssoftware.com/fnc/core/

## Components and palette pages (from every `RegisterComponents` call)

| Component | Palette page | Reg unit | Frameworks |
|---|---|---|---|
| `TTMSFNCBitmapContainer`, `TTMSFNCURLBitmapContainer` | `TMS FNC UI` | `*.TMSFNCBitmapContainerReg` | VCL, FMX, WEB, LCL |
| `TTMSFNCStylesManager` | `TMS FNC UI` | `*.TMSFNCStylesReg` | VCL, FMX, WEB, LCL |
| `TTMSFNCScrollBar` | `TMS FNC UI` | `*.TMSFNCScrollBarReg` | VCL, FMX, WEB, LCL |
| `TTMSFNCPopup` | `TMS FNC UI` | `*.TMSFNCPopupReg` | VCL, FMX, WEB, LCL |
| `TTMSFNCPopupMenu` | `TMS FNC UI` | `*.TMSFNCPopupMenuReg` | VCL, FMX only |
| `TTMSFNCHint` | `TMS FNC UI` | `*.TMSFNCHintReg` | VCL, FMX, LCL (no WEB unit) |
| `TTMSFNCPDFLib` | `TMS FNC UI` | `*.TMSFNCPDFLibReg` | all |
| `TTMSFNCGraphicsPDFIO` | `TMS FNC UI` | `*.TMSFNCGraphicsPDFIOReg` | all |
| `TTMSFNCGraphicsPrintIO` | `TMS FNC UI` | `*.TMSFNCPrintIOReg` | all |
| `TTMSFNCResponsiveManager` | `TMS FNC UI` | `*.TMSFNCResponsiveManagerReg` | all |
| `TTMSFNCWebBrowser`, `TTMSFNCWebCoreClientBrowser` | `TMS FNC UI` | `*.TMSFNCWebBrowserReg` | VCL, FMX (LCL: WebBrowser only) |
| `TTMSFNCEdgeWebBrowser` | `TMS FNC UI` | `*.TMSFNCEdgeWebBrowserReg` | VCL, FMX, Windows only |
| `TTMSFNCSVGImageCollection` | `TMS FNC UI` | `VCL.TMSFNCGeneralRegDE` | **VCL only**, Delphi 10.3+ (`COMPILERVERSION >= 33`) |
| `TTMSFNCFilterRulesManager` | `TMS FNC UI` | `TMS.TMSFNCFilterRulesManagerReg` | all |
| `TTMSFNCDataBinder` | **`TMS FNC DB`** | `*.TMSFNCDataBindingReg` | all |
| `TTMSFNCDataSet`, `TTMSFNCDataLinkCSV`, `TTMSFNCDataLinkJSON` | **`TMS FNC DB`** | `TMS.TMSFNCDataSetReg`, `TMS.TMSFNCDataLinkCSVReg`, `TMS.TMSFNCDataLinkJSONReg` | VCL, FMX |

## Unit prefix rules

- VCL: `VCL.TMSFNCxxx`, FMX: `FMX.TMSFNCxxx`, WEB: `WEBLib.TMSFNCxxx`, Lazarus: `LCLTMSFNCxxx` (**no dot**). The prefixed copies are generated from one source, so class and member names are identical; only `{$IFDEF FMXLIB/VCLLIB/WEBLIB/LCLLIB}` sections differ.
- Framework-neutral `TMS.TMSFNCxxx` units: `TMS.TMSFNCDataSet`, `TMS.TMSFNCCustomDataLink`, `TMS.TMSFNCDataLinkCSV/JSON`, `TMS.TMSFNCFilterBuilder`, `TMS.TMSFNCFilterRulesManager`, `TMS.TMSFNCFilterStructure`, `TMS.TMSFNCValue`, `TMS.TMSFNCObjectResolver` (all in `TMSFNCCorePkg`; the WEB package contains only `TMS.TMSFNCValue`, `TMS.TMSFNCFilterBuilder`, `TMS.TMSFNCFilterRulesManager`). The other `TMS.*` files in `Source` (`TMS.TMSFNCTypes`, `TMS.TMSFNCUtils`, `TMS.TMSFNCPersistence`, `TMS.TMSFNCCloudBase*`, `TMS.TMSFNCJSONReader/Writer`, `TMS.TMSFNCHTTPServer*`) are `RTLONLY` copies used by console/server code and are **not** in the d13 IDE packages. In a VCL/FMX/WEB app use the prefixed `VCL.`/`FMX.`/`WEBLib.` units, never `TMS.TMSFNCTypes`.
- Never mix `VCL.` and `FMX.` FNC units in one project.

Units that exist only for some frameworks (verified by file listing):

| Unit | VCL | FMX | WEB | LCL |
|---|---|---|---|---|
| `*.TMSFNCGraphicsSVGEngine` (SVG rendering) | yes | yes | **no** (browser renders SVG) | yes |
| `*.TMSFNCHint` | yes | yes | no | yes |
| `*.TMSFNCPopupMenu` | yes | yes | no | no |
| `*.TMSFNCEdgeWebBrowser` | yes | yes | no | no |
| `*.TMSFNCGDIPlusApi`, `*.TMSFNCGraphics.Win` | yes | yes (Windows) | no | (`LCLTMSFNCGraphicsWin`) |
| `*.TMSFNCGraphics.WEB`, `*.TMSFNCCloudBase.WEB` | no | yes (unused at run time on FMX) | yes | no |
| `VCL.TMSFNCXPVS` | yes | no | no | yes |
| `VCL.TMSFNCFilterRulesManager` (editor host) | yes | no | yes | yes |

## Which unit declares what

| Purpose | Unit (VCL shown) |
|---|---|
| `TTMSFNCBitmap`, `TTMSFNCBitmapHelperClass`, `TTMSFNCMargins`, `TTMSFNCScaledBitmaps`, `TTMSFNCSVGImageCollection`, `InflateRectEx`, `ConvertToRectF`, `RectF`/`PointF` (only where `TRectF` is missing), `TMSPlatforms*` constants | `VCL.TMSFNCTypes` |
| `TTMSFNCGraphicsColor`, all `gcXXX` colors, `TTMSFNCGraphicsFill`, `TTMSFNCGraphicsStroke`, `TTMSFNCGraphicsFont`, `TTMSFNCGraphicsPath`, `TTMSFNCAppearanceGlobalFont`, enums (`gfk*`, `gsk*`, `gta*`, `gtt*`), `Lighter`/`Darker`/`Blend`/`MakeGraphicsColor` | `VCL.TMSFNCGraphicsTypes` |
| `TTMSFNCGraphics` (drawing) | `VCL.TMSFNCGraphics` |
| `TTMSFNCCustomControl`, `TTMSFNCControl` | `VCL.TMSFNCCustomControl` |
| `TTMSFNCCustomComponent` | `VCL.TMSFNCCustomComponent` |
| `TTMSFNCUtils` (class helpers: `GetDPIScale`, `SetFontSize`, `HTMLStrip`, JSON, Base64) | `VCL.TMSFNCUtils` |
| `TTMSFNCBitmapContainer` / `TTMSFNCURLBitmapContainer` | `VCL.TMSFNCBitmapContainer` / `VCL.TMSFNCURLBitmapContainer` |
| `TTMSFNCStylesManager`, `TTMSFNCStyles` | `VCL.TMSFNCStyles` |

## Base classes

### TTMSFNCCustomControl (`*.TMSFNCCustomControl`)

Chain: `TTMSFNCCustomControlBaseCommon` (VCL/LCL: `TCustomControl`; WEB: `TWebCustomControl`; FMX: `TControl`) → `TTMSFNCCustomControlBase` → `TTMSFNCCustomControl` → `TTMSFNCControl`. Every visual FNC control (UI Pack grid, tree view, planner, ...) descends from it. It gives:

```delphi
// protected (descendants decide whether to publish them; most UI Pack controls do)
property Fill: TTMSFNCGraphicsFill read FFill write SetFill;
property Stroke: TTMSFNCGraphicsStroke read FStroke write SetStroke;
procedure Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF); virtual;           // your painting
procedure DrawBackground(AGraphics: TTMSFNCGraphics; ARect: TRectF); virtual; // Fill + Stroke rectangle
procedure ApplyStyle; override;            // called when AdaptToStyle = True
procedure ResetToDefaultStyle; override;   // called when AdaptToStyle is switched off
// published
property AdaptToStyle: Boolean default False;   // follow VCL style / FMX style / WEB CSS
property OnBeforeDraw: TTMSFNCCustomControlBeforeDrawEvent;  // (Sender; AGraphics; ARect: TRectF; var ADefaultDraw: Boolean)
property OnAfterDraw: TTMSFNCCustomControlAfterDrawEvent;    // (Sender; AGraphics; ARect: TRectF)
property Color default gcWhite;   // kept in sync with Fill.Color
// public
procedure BeginUpdate; virtual;  procedure EndUpdate; virtual;
procedure SaveSettingsToFile(AFileName: string; AAppearanceOnly: Boolean = False); virtual;
procedure LoadSettingsFromFile(AFileName: string); virtual;
procedure SaveSettingsToStream(AStream: TStream; AAppearanceOnly: Boolean = False); virtual;
procedure LoadSettingsFromStream(AStream: TStream); virtual;
procedure DisableFill; procedure EnableFill; procedure DisableStroke; procedure EnableStroke;
procedure DisableBackground; procedure EnableBackground;
function IsDesignTime: Boolean; function IsLoading: Boolean; function IsDestroying: Boolean;
procedure SetControlMargins(ALeft, ATop, ARight, ABottom: Single);
property ControlAlignment: TTMSFNCControlAlignment default caNone; // caTop, caClient, ... cross-framework Align
property AllowFocus: Boolean default True;
property UndoManager: TTMSFNCUndoManager;
property DataPointer / DataBoolean / DataObject / DataString / DataInteger;   // free tag storage
// protected rendering switches: Transparent, BufferedPainting, NativeCanvas, AntiAliasing (True),
// OptimizedHTMLDrawing (True), ShowAcceleratorChar (True), TextQuality (gtqAntiAliasing)
```

There is **no** `GlobalFont` on the base class. `GlobalFont: TTMSFNCAppearanceGlobalFont` (in `*.TMSFNCGraphicsTypes`, properties `Color`, `Size`, `Name`, `Scale`, `Style`) is declared per control in the UI Pack (DataGrid, TreeView, Calendar, ...).

### TTMSFNCCustomComponent (`*.TMSFNCCustomComponent`)

Base of the non-visual FNC components (BitmapContainer, StylesManager, PDFLib, DataBinder...). On VCL/WEB it is a `TCustomControl` (FMX: `TControl`) that is only shown as an icon at design time (`Visible` default False on VCL). It implements `ITMSFNCPersistence` (`SaveSettingsToFile/Stream`, `LoadSettingsFromFile/Stream`), `BeginUpdate/EndUpdate`, `IsDesignTime/IsLoading/IsDestroying`, `OnCanSaveProperty/OnCanLoadProperty`, and a protected `AdaptToStyle`.

## Common types

- `TTMSFNCGraphicsColor` = `TAlphaColor` on FMX, `TColor` on VCL/WEB/LCL. The `gcXXX` constants (154 CSS colors: `gcRed`, `gcSteelblue`, `gcWhitesmoke`, `gcDarkgray`, `gcYellowgreen`, ...) adapt per framework. `gcNull` = `$00000000` on FMX and `-1` on VCL/WEB (means "no color", not `clNone`).
- `TTMSFNCBitmap`: FMX `class(TBitmap)`; **VCL/LCL `class(TPicture)`**; WEB `class(TBitmap)` of WEB Core. See bitmaps-and-svg.md.
- `TTMSFNCMargins` (`Left`, `Top`, `Right`, `Bottom: Single`, `Rect`, `PaddingRect(R)`, `Empty`, `OnChange`).
- `TTMSFNCMouseButton` = `TMouseButton`. Rect helpers: `InflateRectEx(var R: TRectF; DX, DY: Single)`, `OffsetRectEx`, `PtInRectEx`, `ConvertToRectF(TRect)`, `ConvertToRect(TRectF)`.

## Minimal runtime creation

```delphi
uses VCL.TMSFNCTypes, VCL.TMSFNCGraphicsTypes, VCL.TMSFNCBitmapContainer, VCL.TMSFNCStyles;

procedure TForm1.FormCreate(Sender: TObject);
var
  bc: TTMSFNCBitmapContainer;
  sm: TTMSFNCStylesManager;
begin
  bc := TTMSFNCBitmapContainer.Create(Self);           // owner = form
  bc.AddFromFile('logo.svg', 'logo');
  sm := TTMSFNCStylesManager.Create(Self);             // must be owned by the form (see styles.md)
end;
```

## Building from the command line

Use the minimal `.dproj` + `build.cmd` approach from the DataGrid `setup-and-install.md` (`skills\tms-fnc-datagrid\references\setup-and-install.md`). For an FNC Core only project put just the TMS FNC Core entries of the IDE library path in `<FNCPATHS>`; with the UI Pack add its entries too. These point to the compiled `.dcu` files, so no component source code is needed. Same build stoppers: missing `DCC_Namespace`, unreadable `environment.proj` (MSB4024), app still running (F2039).

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `tms install tms.fnc.coreui` / `tms.fnc.graphics` | `tms install tms.fnc.core` |
| `uses TMSFNCTypes;` / `uses TMS.TMSFNCTypes;` in a VCL app | `VCL.TMSFNCTypes` (`FMX.` / `WEBLib.` / `LCLTMSFNCTypes`) |
| `LCL.TMSFNCTypes` | `LCLTMSFNCTypes` (no dot on Lazarus) |
| Palette page "TMS FNC Core" | `TMS FNC UI` (and `TMS FNC DB` for DataBinder / DataSet / DataLinks) |
| `TTMSFNCGraphicsColor` is always `TAlphaColor` | only on FMX; `clRed` works on VCL, use `gcRed` for cross-framework code |
| `if c = clNone` to test "no color" | compare with `gcNull` |
| `MyControl.Fill.Color := ...` on a custom `TTMSFNCCustomControl` descendant from outside | `Fill`/`Stroke` are protected in the base; publish them in your class, or set `Color` |
| `MyControl.GlobalFont` on any FNC control | only controls that declare it (UI Pack); not on `TTMSFNCCustomControl` |
| `TTMSFNCCustomControl.Paint` override for drawing | override `Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF)` |
| `TTMSFNCSVGImageCollection` on FMX/WEB | VCL only (Delphi 10.3+); on FMX/WEB put SVGs in a `TTMSFNCBitmapContainer` |
| `TTMSFNCPopupMenu` / `TTMSFNCHint` in a WEB Core app | not available on WEB |
