# Popups, popup menus and hints (TTMSFNCPopup, TTMSFNCPopupMenu, TTMSFNCHint)
> Sections (line ranges): 6-16 Units and palette · 17-82 TTMSFNCPopup · 83-150 TTMSFNCPopupMenu · 151-186 TTMSFNCHint · 187-193 Platform notes · 194-206 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCPopup`, `*.TMSFNCPopupMenu`, `*.TMSFNCHint` and their `*Reg` units.

## Units and palette

| Class | Unit | Frameworks / platforms | Palette |
|---|---|---|---|
| `TTMSFNCPopup` | `*.TMSFNCPopup` | VCL, FMX, LCL, WEB | TMS FNC UI |
| `TTMSFNCNonFocusablePopup` | `*.TMSFNCPopup` | VCL, FMX, LCL (not registered) | - |
| `TTMSFNCPopupMenu`, `TTMSFNCMenuItem` | `*.TMSFNCPopupMenu` | VCL, FMX (`TMSPlatformsWinMac`), LCL; **no WEB unit** | TMS FNC UI |
| `TTMSFNCHint` | `*.TMSFNCHint` | VCL, FMX, LCL desktop (`TMSPlatformsDesktop`); **no WEB unit** | TMS FNC UI |

Prefix rule: `VCL.` / `FMX.` / `WEBLib.`, LCL is `LCLTMSFNC...`. `TTMSFNCPopupPlacement` is declared in `*.TMSFNCPopup` and is also used by the popup menu.

## TTMSFNCPopup

A non-visual component that shows an existing control (`ContentControl`) in a borderless popup form next to `PlacementControl`.

```delphi
TTMSFNCPopupPlacement = (ppBottom, ppTop, ppLeft, ppRight, ppCenter, ppBottomCenter, ppTopCenter, ppLeftCenter,
  ppRightCenter, ppAbsolute, ppMouse, ppMouseCenter, ppAboveMouse, ppAboveMouseCenter);

procedure Popup(const AShowModal: Boolean = False); virtual;
function PopupModal: TModalResult; virtual;   // shows modal (StaysOpen forced True), returns ModalResult
function HasPopupForm: Boolean;
function PointInPopup(APoint: TPointF): Boolean; virtual;
property IsOpen: Boolean;                      // public; IsOpen := False closes the popup
property ModalResult: TModalResult;            // public; setting it on the open popup closes a modal popup
property PopupForm: TTMSFNCCustomPopupForm;    // public, read-only
property PopupFormSize: TSizeF;                // public; overrides DropDownWidth/DropDownHeight when > 0
property DragWithParent: Boolean;              // public, default False
property FillColor, StrokeColor: TTMSFNCGraphicsColor;  property Transparent: Boolean;  // public
// published
property ContentControl: TControl;             // control shown inside the popup
property PlacementControl: TControl;
property Placement: TTMSFNCPopupPlacement;     // default ppBottom
property PlacementRectangle: TTMSFNCMargins;
property HorizontalOffset, VerticalOffset: Single;
property DropDownWidth, DropDownHeight: Single;
property StaysOpen: Boolean;                   // default False: closes when focus leaves
property FocusedControl: TControl;             // control focused when the popup opens
property OnPopup: TNotifyEvent;  property OnPopupShown: TNotifyEvent;  property OnClosePopup: TNotifyEvent;
property OnPopupPaint: TTMSFNCPopupPaint;      // procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF) of object
```

Behaviour from source:
- Assigning `ContentControl` sets that control's `Visible := False` and copies its `Width`/`Height` into `DropDownWidth`/`DropDownHeight`. When the popup is shown the control is placed on the popup form with `Align := alClient` (FMX `TAlignLayout.Client`). Size the content control first, then assign it.
- `Popup` does nothing if `IsOpen` is already True, and a click within 200 ms of the last close is ignored (so a toggle button does not reopen it immediately).
- On VCL the popup form gets `PopupParent` = the parent form of `PlacementControl`.

```delphi
uses VCL.TMSFNCPopup;

procedure TForm1.FormCreate(Sender: TObject);
begin
  FPopup := TTMSFNCPopup.Create(Self);
  Panel1.Width := 250;            // size first: ContentControl copies Width/Height
  Panel1.Height := 180;
  FPopup.ContentControl := Panel1; // Panel1 is hidden until popped up
  FPopup.PlacementControl := Button1;
  FPopup.Placement := ppBottom;
  FPopup.FocusedControl := Edit1;
  FPopup.OnClosePopup := PopupClosed;
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
  FPopup.Popup;
end;

procedure TForm1.OKButtonClick(Sender: TObject);   // button inside Panel1
begin
  FPopup.IsOpen := False;
end;
```

Modal use: `if FPopup.PopupModal = mrOk then ...` and set `FPopup.ModalResult := mrOk` from a button in the content.

`TTMSFNCNonFocusablePopup` (VCL/FMX/LCL) has the same placement/content properties plus `Activate` / `Deactivate`, and does not steal focus from the active form (used for autocomplete-style lists).

## TTMSFNCPopupMenu

On VCL/LCL it descends from `TPopupMenu` (assign it to any control's `PopupMenu` property); on FMX from `TCustomPopupMenu`. Items are a `TTMSFNCMenuItems` collection of `TTMSFNCMenuItem`.

```delphi
TTMSFNCMenuItemType = (mitDefault, mitSeparator, mitDropDownButton, mitToolBar, mitCheck);

// TTMSFNCCustomPopupMenu, public
procedure Popup(X, Y: Integer); overload; override;      // VCL/LCL, screen coordinates
procedure Popup(X, Y: Single); overload; override;       // FMX only
procedure Popup(APopupControl: TControl; APopupMenuPlacement: TTMSFNCPopupPlacement); reintroduce; overload;
function AddMenuItem(AText: string; AType: TTMSFNCMenuItemType = mitDefault): TTMSFNCMenuItem; overload;
function AddMenuItem(AAction: TAction): TTMSFNCMenuItem; overload;
function AddMenuSeparatorItem: TTMSFNCMenuItem;
property IsOpen: Boolean;   // read-only
// published
property Items: TTMSFNCMenuItems;
property Appearance: TTMSFNCPopupMenuAppearance;   // Fill, Stroke, DefaultItemAppearance, CheckedIcon, SubMenuIcon,
                                                   // MenuMargins, MenuRounding (8), PopupMenuPlacement (ppAbsolute), MenuOffSetPoint
property BitmapContainer: TTMSFNCBitmapContainer;
property AdaptToStyle: Boolean;
property OnMenuItemClick: TTMSFNCPopupMenuItemControlEvent;  // procedure(Sender: TObject; AMenuItemControl: TTMSFNCMenuItemControl) of object
property OnItemCheck: TTMSFNCPopupMenuItemControlAllowEvent; // (Sender; AMenuItemControl; var AAllow: Boolean)
property OnMenuItemSelectable: TTMSFNCPopupMenuItemControlAllowEvent;
property OnMenuItemControlAdded: TTMSFNCPopupMenuItemControlEvent;   // customise each item control before showing
property OnGetNumberOfPopupMenuItems, OnGetNumberOfSubMenuItems;     // virtual mode (no Items needed)
property OnPopup, OnClose: TNotifyEvent;
// plus OnBefore/AfterDrawMenuItem(Text|Image|Note), OnItemMouseDown/Up, OnItemKeyDown, OnGetPopupControl ...
```

`TTMSFNCMenuItem` (collection item): `Text`, `Note`, `ItemType`, `Enabled`, `Checked`, `GroupName` (radio group of check items), `Selectable`, `Bitmap`, `BitmapName` (looked up in `BitmapContainer`), `ShortCut`, `Hint`, `ShowHint`, `Action`, `Control` + `ControlAlignment` + `ControlPosition` (embed a control), `Items` (sub menu), `Appearance`, `DataInteger`, `DataString`, `Tag`, `OnClick: TNotifyEvent`; methods `AddMenuItem`, `AddMenuSeparatorItem`, `AddBitmap`.

The click event receives the **item control** (`TTMSFNCMenuItemControl`), not the collection item: use `AMenuItemControl.Text`, `.Index`, `.Checked`, `.ParentMenuControl`, and `.MenuItem` (the `TTMSFNCMenuItem`, nil in virtual mode).

```delphi
uses VCL.TMSFNCPopupMenu, VCL.TMSFNCPopup;

procedure TForm1.FormCreate(Sender: TObject);
var
  it, sub: TTMSFNCMenuItem;
begin
  pm := TTMSFNCPopupMenu.Create(Self);
  pm.BitmapContainer := TMSFNCBitmapContainer1;
  pm.Appearance.DefaultItemAppearance.ItemHeight := 30;
  pm.AddMenuItem('Cut').BitmapName := 'Cut';
  pm.AddMenuItem('Copy').BitmapName := 'Copy';
  pm.AddMenuSeparatorItem;
  it := pm.AddMenuItem('Word wrap', mitCheck);
  it.Checked := True;
  sub := pm.AddMenuItem('Sort');          // has sub items -> shows a sub menu
  sub.AddMenuItem('Ascending');
  sub.AddMenuItem('Descending');
  pm.OnMenuItemClick := DoMenuItemClick;
  Memo1.PopupMenu := pm;                 // VCL: works because it is a TPopupMenu
end;

procedure TForm1.DoMenuItemClick(Sender: TObject; AMenuItemControl: TTMSFNCMenuItemControl);
begin
  Caption := AMenuItemControl.Text + ' clicked';
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
  pm.Popup(Button1, ppBottom);
end;
```
Demos: `VCL\TMSFNCPopupMenu\Appearance` (design-time items, light/dark styling through `Appearance.DefaultItemAppearance`: `Font`, `SelectedFill`, `SelectedFontColor`, `DisabledFontColor`, `Separator`, `AccessoryWidth`), `VCL\TMSFNCPopupMenu\RuntimeBuildPopupMenu` (virtual mode: `OnGetNumberOfPopupMenuItems` + `OnMenuItemControlAdded` set `AMenuItemControl.Text/ItemType/BitmapName` per index). Existing items do not pick up a changed `DefaultItemAppearance` automatically; the demo re-assigns `AItems[I].Appearance.Assign(pm.Appearance.DefaultItemAppearance)` recursively.

## TTMSFNCHint

Drop one on the form: it replaces the application hint window, so every control with `ShowHint = True` shows its `Hint` drawn by FNC (HTML-formatted text supported, images by name from `BitmapContainer`). On VCL/LCL the constructor swaps the global `HintWindowClass` and the destructor restores it; on FMX it hooks form creation (Delphi 10 Seattle and later).

```delphi
property Fill: TTMSFNCGraphicsFill;   property Stroke: TTMSFNCGraphicsStroke;   property Font: TTMSFNCGraphicsFont;
property Shadow: Boolean;             // default True
property BitmapContainer: TTMSFNCBitmapContainer;
procedure ShowHintAt(AHint: string; X, Y: Integer);   // manual hint, screen coordinates; ignored while one is showing
procedure HideHint;
function IsShowing: Boolean;
function Calculate(AHint: string): TRect; virtual;
property OnBeforeDrawHint: TTMSFNCHintBeforeDrawHintEvent;   // (Sender; AGraphics: TTMSFNCGraphics; AHint: string; ARect: TRect; var ADefaultDraw: Boolean)
property OnAfterDrawHint: TTMSFNCHintAfterDrawHintEvent;
property OnCalculateHintRect: TTMSFNCHintCalculateHintRectEvent; // (Sender; AHint: String; var ARect: TRect)
```

```delphi
uses VCL.TMSFNCHint, VCL.TMSFNCGraphicsTypes;

procedure TForm1.FormCreate(Sender: TObject);
var
  p: TPoint;
begin
  FHint := TTMSFNCHint.Create(Self);
  FHint.Fill.Color := gcLightyellow;
  FHint.Font.Size := 10;
  Button1.ShowHint := True;
  Button1.Hint := 'Saves the <b>current</b> file<br><font color="gcRed">Ctrl+S</font>';
  // manual:
  // p := Button1.ClientToScreen(Point(0, Button1.Height));
  // FHint.ShowHintAt('Done', p.X, p.Y);
end;
```
Use only one `TTMSFNCHint` per application; it is global by nature.

## Platform notes

- WEB: only `TTMSFNCPopup` exists (`WEBLib.TMSFNCPopup`). There is no `WEBLib.TMSFNCPopupMenu` and no `WEBLib.TMSFNCHint`.
- `TTMSFNCPopupMenu` platforms: Windows and macOS (FMX). `TTMSFNCHint`: desktop only (`TMSPlatformsDesktop`; native hint hooks exist for Windows and macOS); FMX needs Delphi 10 Seattle+ (`COMPILERVERSION > 29`), otherwise the component compiles but does nothing.
- FMX `Popup(X, Y: Single)` vs VCL `Popup(X, Y: Integer)`: only the framework's own overload is declared.
- FMX mobile: a modal popup uses a normal form style.

## Does not exist / common mistakes

- `TTMSFNCPopup.Show`, `.Close`, `.Hide`, `.ShowAt(X, Y)`, `.Execute`: use `Popup` / `PopupModal`, close with `IsOpen := False` (or `ModalResult := ...` for modal). For absolute positions use `Placement := ppAbsolute` with `PlacementRectangle`, or `ppMouse`.
- `TTMSFNCPopup.Control`, `.Content`, `.Child`, `Width`/`Height`: the properties are `ContentControl`, `DropDownWidth`, `DropDownHeight` (or `PopupFormSize`).
- `TTMSFNCPopup.OnClose` / `OnShow`: the events are `OnClosePopup`, `OnPopup`, `OnPopupShown`.
- `TTMSFNCMenuItem.Caption`, `.ImageIndex`, `.Images`, `.RadioItem`, `.Default`: use `Text`, `BitmapName`/`Bitmap` with `BitmapContainer`, `ItemType := mitCheck` + `GroupName`.
- `pm.Items.Add.Caption := ...` / `NewItem(...)` / `TMenuItem` children: use `pm.AddMenuItem(Text, Type)` or `Items.Add` then set `Text`; sub items via `Item.AddMenuItem` / `Item.Items`. `TTMSFNCMenuItem` is a collection item, not a `TMenuItem`.
- `OnItemClick(Sender; AItem: TTMSFNCMenuItem)`: the event is `OnMenuItemClick(Sender; AMenuItemControl: TTMSFNCMenuItemControl)`; per-item `TTMSFNCMenuItem.OnClick: TNotifyEvent` also exists.
- `TAdvPopupMenu` / `TAdvMenuStyler` style properties (`MenuStyler`, `Style := ...`): style through `Appearance` / `Appearance.DefaultItemAppearance`, or `AdaptToStyle`.
- `TTMSFNCHint.ShowHint(...)`, `.HintText`, `.Hint`, `TTMSFNCHint.Active`: the API is `ShowHintAt(AHint, X, Y)` / `HideHint`; normal hints come from each control's `Hint` + `ShowHint`.
- `TTMSFNCBalloonHint` / `TTMSFNCToolTip`: not in FNC Core.
- Using `TTMSFNCPopupMenu` or `TTMSFNCHint` in a TMS WEB Core project: no WEB units exist.
