# Styles (TTMSFNCStylesManager, TTMSFNCStyles, AdaptToStyle)
> Sections (line ranges): 11-15 Units and palette · 16-57 TTMSFNCStylesManager · 58-88 Built-in styles · 89-124 Custom styles: create, load, combine · 125-162 AdaptToStyle · 163-167 Platform notes · 168-184 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0: `VCL/FMX/WEBLib.TMSFNCStyles`, `*.TMSFNCStylesEditor`, `*.TMSFNCStylesReg`, `*.TMSFNCCustomControl` (`AdaptToStyle`, `ApplyStyle`), `*.TMSFNCPersistence`, `VCL.TMSFNCGeneralDE` (design-time verbs), and the resource names inside `Source\TMSFNCStylesResources.res`. There is no styles demo in `tms.fnc.core.demos` or `tms.fnc.uipack.demos`.

FNC has **two independent mechanisms**:

1. **`TTMSFNCStylesManager`**: loads a JSON *style file* (FNC persistence format) and applies it to every FNC component on the form whose class name matches. This is how the built-in "FNC Dark / Light / Office 2019" looks are applied.
2. **`AdaptToStyle`** (per control, default `False`): the control derives its fill/stroke/font colors from the active **VCL style** (`TStyleManager`), the **FMX style** (StyleBook / platform style), or **CSS** on WEB.

## Units and palette

- `TTMSFNCStylesManager`, `TTMSFNCStyles`, `TTMSFNCStylesManagerOptions`, `ITMSFNCAdaptToStyle`: `VCL.TMSFNCStyles` / `FMX.TMSFNCStyles` / `WEBLib.TMSFNCStyles` / `LCLTMSFNCStyles`.
- Palette page **`TMS FNC UI`** (`*.TMSFNCStylesReg`: `RegisterComponents('TMS FNC UI', [TTMSFNCStylesManager])`). Available on VCL, FMX, WEB (`[ComponentPlatformsAttribute(TMSPlatformsWeb)]`) and LCL.

## TTMSFNCStylesManager (`class(TTMSFNCCustomComponent)`)

```delphi
procedure LoadStyleFromFile(AFile: string); overload; virtual;
procedure LoadStyleFromFile(AFile: string; AComponents: TTMSFNCStylesManagerComponentArray); overload; virtual;
procedure LoadStyleFromStream(AStream: TStream); overload; virtual;
procedure LoadStyleFromStream(AStream: TStream; AComponents: TTMSFNCStylesManagerComponentArray); overload; virtual;
procedure LoadStyleFromText(AText: string); overload; virtual;
procedure LoadStyleFromText(AText: string; AComponents: TTMSFNCStylesManagerComponentArray); overload; virtual;
// VCL / FMX / LCL only:
procedure LoadStyleFromResource(AResourceName: string); overload; virtual;
procedure LoadStyleFromResource(AResourceName: string; AComponents: TTMSFNCStylesManagerComponentArray); overload; virtual;
function GetStyleFromResource(AResourceName: string): string; virtual;
function GetStyleFromFile(AFile: string): string; virtual;
function CombineStyles(AFiles: TTMSFNCStylesManagerFileArray): string; virtual;   // file names or JSON texts -> {"Styles":[...]}
// WEB only:
procedure LoadStyleFromURL(AURL: string); overload; virtual;
procedure LoadStyleFromURL(AURL: string; AComponents: TTMSFNCStylesManagerComponentArray); overload; virtual;

property StyleForm: TCustomForm;                              // public: form to style (default: owner form / frame)
published
property Style: string;          // setting it calls LoadStyleFromFile(Style) (a FILE NAME, not a style name)
property StyleResource: string;  // setting it calls LoadStyleFromResource('TTMSFNCSTYLE_' + StyleResource); no-op on WEB
property Options: TTMSFNCStylesManagerOptions;                // AdaptFormColor: Boolean default True
property OnCanLoadStyle: TTMSFNCStylesManagerCanLoadStyleEvent;
// procedure(Sender: TObject; AStyle: string; AComponent: TComponent; var ACanLoadStyle: Boolean) of object
property OnStyleLoaded: TTMSFNCStylesManagerStyleLoadedEvent;
// procedure(Sender: TObject; AStyle: string; AComponent: TComponent) of object

type
  TTMSFNCStylesManagerComponentArray = array of TComponent;
  TTMSFNCStylesManagerFileArray = array of string;
```

How applying works (from `InternalLoadStyle` / `InternalLoadStyleFromJSONValue`):

- The text is parsed as JSON. If it has `"FormColor"` and `Options.AdaptFormColor` is True, the form color is set (`Form.Color` on VCL, `Form.Fill` on FMX).
- A `"Styles"` array is processed entry by entry; otherwise the whole object is one entry.
- Each entry's `"$type"` (e.g. `"TTMSFNCDataGrid"`) is matched against `ClassName` of **every component in `StyleForm.Components`** (or the owner form / owning `TFrame`), plus sub-components exposed through `ITMSFNCStylesManager`. Matching components that implement `ITMSFNCPersistence` get `LoadSettingsFromStream`.
- An empty or nil `AComponents` array means "all matching components"; pass an array to restrict.
- Consequences: a component created with `Owner = nil`, or owned by another form/frame/panel-owner, is **not** styled. Descendant classes are matched by their own class name only (`TMyGrid` does not get the `TTMSFNCDataGrid` entry).

## Built-in styles

`Source\TMSFNCStylesResources.res` contains RCDATA resources `TTMSFNCSTYLE_FNC_DEFAULT`, `TTMSFNCSTYLE_FNC_LIGHT`, `TTMSFNCSTYLE_FNC_DARK`, `TTMSFNCSTYLE_FNC_OFFICE2019WHITE`, `TTMSFNCSTYLE_FNC_OFFICE2019GRAY`, `TTMSFNCSTYLE_FNC_OFFICE2019BLACK`. Each is a combined `{"FormColor": ..., "Styles": [...]}` file with entries for FNC Core and UI Pack classes (`TTMSFNCDataGrid`, `TTMSFNCTreeView`, `TTMSFNCPlanner`, `TTMSFNCToolBar`, `TTMSFNCPanel`, `TTMSFNCCalendar`, `TTMSFNCScrollBar`, ...).

The `.res` is linked by `*.TMSFNCStylesEditor` (`{$R 'TMSFNCStylesResources.res'}`), **not** by `*.TMSFNCStyles`. At run time either add that unit to `uses` or link the file yourself:

```delphi
{$R 'TMSFNCStylesResources.res'}        // file is in tms.fnc.core\Source (on the library path after install)

procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCStylesManager1.StyleResource := 'FNC_DARK';                     // -> TTMSFNCSTYLE_FNC_DARK
  // same as: TMSFNCStylesManager1.LoadStyleFromResource('TTMSFNCSTYLE_FNC_DARK');
end;
```

`StyleResource` only reloads when the value changes; to re-apply the same style call `LoadStyleFromResource` directly. Use the upper-case names shown above.

Order matters when you combine a built-in style with your own look (verified on VCL, UI Pack 7.3):

```delphi
Styles := TTMSFNCStylesManager.Create(Self);       // owner = the form
Styles.Options.AdaptFormColor := False;            // default True: every load also sets Form.Color (VCL) / Fill (FMX),
                                                   // even when AComponents restricts the load
Styles.LoadStyleFromResource('TTMSFNCSTYLE_FNC_DARK', [Board, Planner, StatusBar]);  // only these controls
Planner.ItemsAppearance.Fill.Color := ...;         // customise AFTER loading: the load overwrites fonts, fills,
                                                   // templates, row heights and item colours set earlier
```

Leave controls you style completely by hand (HTMLText, custom-drawn cards) out of the array, or the style resets them.

## Custom styles: create, load, combine

```delphi
uses VCL.TMSFNCStyles;

// 1. Save the appearance of one configured control as a style file (AAppearanceOnly = True)
TMSFNCDataGrid1.SaveSettingsToFile('grid.style', True);

// 2. Apply it to all TTMSFNCDataGrid instances on this form
TMSFNCStylesManager1.LoadStyleFromFile('grid.style');

// 3. Apply only to selected components
TMSFNCStylesManager1.LoadStyleFromFile('grid.style', [TMSFNCDataGrid2]);

// 4. Several per-component files as one style
TMSFNCStylesManager1.LoadStyleFromText(
  TMSFNCStylesManager1.CombineStyles(['grid.style', 'treeview.style']));

// 5. Apply a style to one control directly, no manager needed
TMSFNCTreeView1.LoadSettingsFromFile('treeview.style');
```

Style JSON (FNC persistence, type key `$type` = `TTMSFNCPersistence.ClassTypeVariable`):

```json
{
  "$type": "TTMSFNCCalendar",
  "Color": "#484848",
  "DateAppearance": { "$type": "TTMSFNCCalendarDateAppearance", "Fill": { ... }, "Font": { ... } }
}
```

Which properties go into an "appearance only" file is decided per class by the protected `IsAppearanceProperty(AObject: TObject; APropertyName: string; APropertyType: TTypeKind): Boolean` (override in your own `TTMSFNCCustomControl` descendants). Filter at load time with `OnCanLoadStyle` (set `ACanLoadStyle := False`) or the control's `OnCanLoadProperty`.

Design time: right-click any FNC component, **Style** submenu: **Load Style**, **Save Style**, **Manager** (style picker dialog that applies to all FNC components on the form).

## AdaptToStyle

```delphi
property AdaptToStyle: Boolean default False;     // published on TTMSFNCCustomControl (protected on TTMSFNCCustomComponent)
procedure ApplyStyle; virtual;                     // protected: pull colors from TTMSFNCStyles
procedure ResetToDefaultStyle; virtual;            // protected: restore defaults when switched off
```

- Setting it calls `InitializeStyle` → `ApplyStyle` (or `ResetToDefaultStyle` when switched off) and `Invalidate`. The base `TTMSFNCCustomControl.ApplyStyle` sets `Fill.Color` from `TTMSFNCStyles.GetStyleBackgroundFillColor` and `Stroke.Color` from `GetStyleLineFillColor`; UI Pack controls override it for headers, selection, fonts, etc.
- VCL: active only when `StyleServices.Enabled` and the style name is not `Windows` / `Windows10`. Changing `TStyleManager.SetStyle(...)` at run time re-applies via `CM_STYLECHANGED`.
- FMX: reads the brushes of the current style scene (`TStyleChangedMessage` and `CM_STYLECHANGED` trigger re-apply). Works with a `TStyleBook` or the platform default.
- WEB: reads CSS rules (`.TMSFNCGridStyle`, `.TMSFNCButtonStyle`, `.TMSFNCEditStyle`, `.TMSFNCHeaderItemStyle`, `.TMSFNCMemoStyle`, `.TMSFNCStyle`) from the stylesheet whose file name is in the global `CSSStyleFileName` (unit `WEBLib.TMSFNCStyles`).
- LCL: `StyleServicesEnabled` returns False, so `AdaptToStyle` has no effect.

```delphi
// VCL: follow the application's VCL style
uses Vcl.Themes;
TStyleManager.TrySetStyle('Carbon');
TMSFNCDataGrid1.AdaptToStyle := True;

// FMX: StyleBook1 assigned to the form
TMSFNCTreeView1.AdaptToStyle := True;
```

`TTMSFNCStyles` class functions you can call in your own `ApplyStyle` (all `class function X(var AColor: TTMSFNCGraphicsColor): Boolean`, True when the style provides a value): `GetStyleBackgroundFillColor`, `GetStyleBackgroundFillColorTo`, `GetStyleAlternativeBackgroundFillColor(To)`, `GetStyleBackgroundStrokeColor`, `GetStyleLineFillColor`, `GetStyleHeaderFillColor(To)`, `GetStyleHeaderStrokeColor`, `GetStyleSelectionFillColor(To)`, `GetStyleTextFontColor`, `GetStyleAlternativeTextFontColor`, `GetStyleDefaultButtonFillColor`, `GetStyleDefaultButtonStrokeColor`; plus `StyleServicesEnabled: Boolean`.

```delphi
procedure TMyControl.ApplyStyle;
var
  c: TTMSFNCGraphicsColor;
begin
  inherited;
  c := gcNull;
  if TTMSFNCStyles.GetStyleTextFontColor(c) then
    FValueFont.Color := c;      // FValueFont: a TTMSFNCGraphicsFont field of your control
end;
```

## Platform notes

- WEB: no resources, so `StyleResource` and `LoadStyleFromResource` are unavailable; copy the `.style` files to the web server and call `LoadStyleFromURL('TTMSFNCStyle_FNC_Dark.style')` (asynchronous; it calls `LoadStyleFromFile` internally). For a user-picked file: `TWebFilePicker` → `OnGetFileAsText` → `TMSFNCStylesManager1.LoadStyleFromText(AText)`.
- FMX/VCL/LCL: `Style := 'C:\styles\dark.style'` loads immediately when set (`FileExists` check; a relative path resolves against the working directory). When `Style`/`StyleResource` is set in the Object Inspector it is applied while the form is being streamed, so components streamed after the manager may not exist yet; loading in `FormCreate` (or later) is the reliable choice.

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `StylesManager.Style := 'Dark'` (expecting a built-in name) | `Style` is a file name. Built-ins: `StyleResource := 'FNC_DARK'` (+ linked `TMSFNCStylesResources.res`) |
| `StylesManager.Apply` / `ApplyStyle` / `Refresh` | loading applies immediately; there is no Apply method |
| `StylesManager.LoadFromFile` / `LoadFromResource` | `LoadStyleFromFile`, `LoadStyleFromResource`, `LoadStyleFromStream`, `LoadStyleFromText` |
| `.tss` / `.vsf` / `.fsf` style files for the manager | FNC JSON style files (`.style` by convention); VCL `.vsf` / FMX `.fsf` styles are used only through `AdaptToStyle` |
| Built-in names "Ocean", "Metro", "Office2016" | only FNC_DEFAULT, FNC_LIGHT, FNC_DARK, FNC_OFFICE2019WHITE, FNC_OFFICE2019GRAY, FNC_OFFICE2019BLACK |
| `TTMSFNCStyleManager` / `TTMSFNCStyleBook` / `TTMSFNCAppearanceManager` | `TTMSFNCStylesManager` (plural "Styles") |
| `StylesManager.SaveStyleToFile` | `Control.SaveSettingsToFile(AFileName, True)` per control, then `CombineStyles` |
| `StylesManager.RegisterControl(...)` / `Components.Add` | it styles components owned by the form (`StyleForm`); create runtime controls with `Create(Self)` or pass them in `AComponents` |
| Expecting `AdaptToStyle` to apply the manager's FNC style | separate mechanisms; `AdaptToStyle` follows VCL/FMX/CSS styles |
| `AdaptToStyle` with the VCL "Windows" style | ignored by design (`StyleServicesEnabled` returns False) |
| Expecting `LoadStyleFromResource(..., [SomeControl])` to leave the form colour alone | it still applies `FormColor`; set `Options.AdaptFormColor := False` first |
| `TTMSFNCGraphicsAppearance` class | does not exist; appearance lives in each control's `Fill`/`Stroke`/`Font`/`*Appearance` properties (`TTMSFNCGraphicsFillEditor`/`TTMSFNCGraphicsStrokeEditor` are design-time editors) |
