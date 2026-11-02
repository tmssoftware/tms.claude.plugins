# Pickers and selectors (TTMSFNCCustomPicker / TTMSFNCCustomSelector, color / font / bitmap / fill kind / stroke kind, TTMSFNCColorWheel, TTMSFNCControlPicker, TTMSFNCCheckGroupPicker, TTMSFNCRadioGroupPicker)

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCCustomSelector`, `*.TMSFNCCustomPicker`, `*.TMSFNCColorSelector`, `*.TMSFNCColorPicker`, `*.TMSFNCFontNamePicker`, `*.TMSFNCFontSizePicker`, `*.TMSFNCBitmapSelector`, `*.TMSFNCBitmapPicker`, `*.TMSFNCFillKindSelector`, `*.TMSFNCFillKindPicker`, `*.TMSFNCStrokeKindSelector`, `*.TMSFNCStrokeKindPicker`, `*.TMSFNCColorWheel`, `*.TMSFNCControlPicker`, `*.TMSFNCCheckGroupPicker`, `*.TMSFNCRadioGroupPicker` (+ FNC Core 4.5.0.0 `TMSFNCGraphicsTypes`). Date/time pickers are documented separately.

## The pattern

- A **selector** (`TTMSFNCCustomSelector`, FNC-drawn) is an always-visible grid of `Rows` x `Columns` items (`Items` collection) with state appearance (normal/hover/down/selected/disabled). Selection: `SelectedItemIndex`, `OnItemSelected`.
- A **picker** (`TTMSFNCCustomPicker`) is a combo-like box that shows the current value and opens a `TTMSFNCPopup` containing a selector (or another control). Most pickers mirror the selector's typed properties (`SelectedColor`, `SelectedFillKind`, ...) and events.
- Pairs: `TTMSFNCColorSelector`/`TTMSFNCColorPicker`, `TTMSFNCBitmapSelector`/`TTMSFNCBitmapPicker`, `TTMSFNCFillKindSelector`/`TTMSFNCFillKindPicker`, `TTMSFNCStrokeKindSelector`/`TTMSFNCStrokeKindPicker`. Font name/size pickers have no selector counterpart (their popup is a native `TListBox`).

## Units, palette, platforms

All registered on **`TMS FNC UI`**; all are `TMSPlatformsWeb` (VCL, FMX, WEB) and exist for LCL. Prefix `VCL.` / `FMX.` / `WEBLib.` / `LCLTMSFNC`.

| Classes | Unit |
|---|---|
| base classes, `TTMSFNCCustomSelectorItem`, `TTMSFNCCustomSelectorAppearance` | `TMSFNCCustomSelector`, `TMSFNCCustomPicker` |
| `TTMSFNCColorSelector` / `TTMSFNCColorPicker` | `TMSFNCColorSelector` / `TMSFNCColorPicker` |
| `TTMSFNCFontNamePicker`, `TTMSFNCFontSizePicker` | `TMSFNCFontNamePicker`, `TMSFNCFontSizePicker` |
| `TTMSFNCBitmapSelector` / `TTMSFNCBitmapPicker` | `TMSFNCBitmapSelector` / `TMSFNCBitmapPicker` |
| `TTMSFNCFillKindSelector` / `TTMSFNCFillKindPicker` | `TMSFNCFillKindSelector` / `TMSFNCFillKindPicker` (reg unit `TMSFNCFillKindReg`) |
| `TTMSFNCStrokeKindSelector` / `TTMSFNCStrokeKindPicker` | `TMSFNCStrokeKindSelector` / `TMSFNCStrokeKindPicker` (reg unit `TMSFNCStrokeKindReg`) |
| `TTMSFNCColorWheel` | `TMSFNCColorWheel` |
| `TTMSFNCControlPicker` | `TMSFNCControlPicker` |
| `TTMSFNCCheckGroupPicker`, `TTMSFNCRadioGroupPicker` | `TMSFNCCheckGroupPicker`, `TMSFNCRadioGroupPicker` (+ `TMSFNCCheckGroup` / `TMSFNCRadioGroup` for title/event types) |

Fill/stroke kinds come from FNC Core `*.TMSFNCGraphicsTypes`: `TTMSFNCGraphicsFillKind = (gfkNone, gfkSolid, gfkGradient, gfkTexture)`, `TTMSFNCGraphicsStrokeKind = (gskNone, gskSolid, gskDash, gskDot, gskDashDot, gskDashDotDot)`. Color type `TTMSFNCGraphicsColor` (= `TColor` on VCL/WEB, `TAlphaColor` on FMX; constants `gcRed`, `gcNull`, ...).

## TTMSFNCCustomSelector (shared selector API)

```delphi
// protected in the base, published by the concrete selectors
property Items: TTMSFNCCustomSelectorItems;      // Add, Insert, Items[i] (typed per selector)
property Rows: Integer default 4;  property Columns: Integer default 4;
property SelectedItemIndex: Integer default -1;
property Appearance: TTMSFNCCustomSelectorAppearance; // Fill/Stroke + FillHover/StrokeHover, FillDown, FillSelected, FillDisabled, ..., HorizontalSpacing, VerticalSpacing, SeparatorStroke, Font
OnItemSelected / OnItemDeselected / OnItemClick: procedure(Sender: TObject; AItemIndex: Integer) of object;
OnItemBeforeDrawBackground: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; AItemIndex: Integer; var ADefaultDraw: Boolean) of object;
// also OnItemAfterDrawBackground, OnItemBefore/AfterDrawContent, OnItemBefore/AfterDrawText (var AText), OnBeforeDraw, OnAfterDraw
// public
procedure BeginUpdate; procedure EndUpdate;
procedure InitializeDefault; virtual;    // fills the default items (colors, fill kinds, ...)
function XYToItem(X, Y: Single): Integer;
```
`TTMSFNCCustomSelectorItem` (published): `Text`, `Hint`, `CanSelect`, `CanDeselect`, `Enabled`, `Visible`, `Separator`, `SeparatorHeight`, `ColumnSpan`, `RowSpan`, `Margins`, `HorizontalTextAlign`, `VerticalTextAlign`; public `DataInteger`, `DataString`, `DataObject`, `DataPointer`, `DataBoolean`, `function State: TTMSFNCCustomSelectorItemState` (`isNormal, isHover, isDown, isSelected, isDisabled`).

**Selectors fill their default items only at design time** (`if IsDesignTime then InitializeDefault`). A selector created in code is empty until you call `InitializeDefault` or add items. Pickers call the inner selector's `InitializeDefault` themselves.

## TTMSFNCCustomPicker (shared picker API)

```delphi
// public
procedure DropDown; virtual;              // toggles the popup open/closed
property Popup: TTMSFNCPopup;  property Selector: TTMSFNCCustomSelector;
property Edit: TEdit;                     // native edit used when the picker is editable
procedure BeginUpdate; procedure EndUpdate;
// published by TTMSFNCDefaultPicker
property Fill; property Stroke; property Font: TTMSFNCGraphicsFont; property DefaultStyle: Boolean default True;
property OnPopup, OnClosePopup: TNotifyEvent;
// published by most concrete pickers
property DropDownWidth, DropDownHeight: Single;
property CloseOnSelection: Boolean;       // default True, except BitmapPicker and CheckGroupPicker (False)
OnPickerBeforeDraw: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; var ADefaultDraw: Boolean) of object;
```

## Color: TTMSFNCColorSelector / TTMSFNCColorPicker (demo `Pickers`)

```delphi
TTMSFNCCustomColorSelectorMode = (csmSimple, csmExtended, csmExtendedMore);
// csmSimple 4x4, csmExtended 8x5, csmExtendedMore 8x7 incl. 'Automatic' and 'More Colors...' items (opens an embedded TTMSFNCColorWheel)
property SelectedColor: TTMSFNCGraphicsColor default gcNull;
property Mode: TTMSFNCCustomColorSelectorMode default csmSimple;
property Items: TTMSFNCColorSelectorItems;      // TTMSFNCColorSelectorItem.Color
OnColorSelected / OnColorDeselected: procedure(Sender: TObject; AColor: TTMSFNCGraphicsColor) of object;
// selector public
function FindItemByColor(AColor: TTMSFNCGraphicsColor): Integer;
function FindColorByItem(AItem: Integer): TTMSFNCGraphicsColor;
```
```delphi
uses VCL.TMSFNCColorPicker, VCL.TMSFNCColorSelector, VCL.TMSFNCGraphicsTypes;

procedure TForm1.FormCreate(Sender: TObject);
begin
  FPicker := TTMSFNCColorPicker.Create(Self);
  FPicker.Parent := Self;
  FPicker.SetBounds(16, 16, 80, 26);       // FMX: Position.X/Y
  FPicker.Mode := csmExtended;
  FPicker.SelectedColor := gcRed;
  FPicker.OnColorSelected := ColorSelected;

  FSel := TTMSFNCColorSelector.Create(Self);
  FSel.Parent := Self;
  FSel.SetBounds(16, 60, 135, 135);
  FSel.InitializeDefault;                  // REQUIRED at runtime, otherwise no colors
  FSel.OnColorSelected := ColorSelected;
end;

procedure TForm1.ColorSelected(Sender: TObject; AColor: TTMSFNCGraphicsColor);
begin
  TMSFNCPanel1.Fill.Color := AColor;
end;
```
Custom palette: `FSel.BeginUpdate; FSel.Items.Clear; FSel.Columns := 3; FSel.Rows := 1; FSel.Items.Add.Color := gcRed; ... FSel.EndUpdate;`.

## Font name / font size pickers

```delphi
// TTMSFNCFontNamePicker
property SelectedFontName: String;
property Items: TStringList;            // public; filled with the system fonts (TTMSFNCUtils.GetFonts)
OnFontNameSelected: procedure(Sender: TObject; AFontName: string) of object;
// TTMSFNCFontSizePicker
property SelectedFontSize: Single;
property Items: TStringList;            // public; 8,9,10,11,12,14,...,72
OnFontSizeSelected: procedure(Sender: TObject; AFontSize: Single) of object;
// both: CloseOnSelection (True), DropDownWidth/Height, Font, OnCustomize: TNotifyEvent
```
They do **not** publish `Appearance`, `Rows`, `Columns` or the item draw events (the popup is a native list box).

## Bitmap: TTMSFNCBitmapSelector / TTMSFNCBitmapPicker

`TTMSFNCBitmapSelectorItem`: `Bitmap: TTMSFNCBitmap`, `BitmapName` (resolved through `BitmapContainer`), `BitmapAlign: TTMSFNCBitmapSelectorBitmapAlign = (baLeft, baCenter, baRight)`, `BitmapSize: Single`, plus base item members.
```delphi
property BitmapContainer: TTMSFNCBitmapContainer;
property SelectedBitmap: TTMSFNCBitmap;          // public, READ-ONLY: select via SelectedItemIndex
procedure LoadFromBitmapContainer; virtual;      // one item per container bitmap
function FindItemByBitmap(ABitmap: TTMSFNCBitmap): Integer;
function FindBitmapByItem(AItem: Integer): TTMSFNCBitmap;
OnBitmapSelected / OnBitmapDeselected: procedure(Sender: TObject; ABitmap: TTMSFNCBitmap) of object;
```
```delphi
TMSFNCBitmapPicker1.BitmapContainer := TMSFNCBitmapContainer1;
TMSFNCBitmapPicker1.LoadFromBitmapContainer;
TMSFNCBitmapPicker1.SelectedItemIndex := 0;
```

## Fill kind / stroke kind (demo `Pickers`)

```delphi
// TTMSFNCFillKindPicker (published) / TTMSFNCFillKindSelector (public only!)
property SelectedFillKind: TTMSFNCGraphicsFillKind default gfkNone;
OnFillKindSelected / OnFillKindDeselected: procedure(Sender: TObject; AFillKind: TTMSFNCGraphicsFillKind) of object;
// TTMSFNCStrokeKindPicker (default gskSolid, published) / TTMSFNCStrokeKindSelector (default gskNone, public only)
property SelectedStrokeKind: TTMSFNCGraphicsStrokeKind;
OnStrokeKindSelected / OnStrokeKindDeselected: procedure(Sender: TObject; AStrokeKind: TTMSFNCGraphicsStrokeKind) of object;
// selectors: FindItemByFillKind / FindFillKindByItem, FindItemByStrokeKind / FindStrokeKindByItem
```
Items: `TTMSFNCFillKindSelectorItem.Kind` + `Name`; `TTMSFNCStrokeKindSelectorItem.Kind`.
```delphi
procedure TForm130.TMSFNCFillKindPicker1FillKindSelected(Sender: TObject; AFillKind: TTMSFNCGraphicsFillKind);
begin
  TMSFNCFillKindSelector1.SelectedFillKind := AFillKind;
  TMSFNCPanel1.Fill.Kind := AFillKind;
end;
```

## TTMSFNCColorWheel

FNC control combining a hue/saturation wheel image with native track bars (`TTrackBar`, `TWebTrackBar` on WEB) and `TTMSFNCEdit` fields for R, G, B and HEX.
```delphi
property SelectedColor: TTMSFNCGraphicsColor default gcWhite;
property RValue, GValue, BValue: Integer default 255;
property HEXValue: string;
property Font: TTMSFNCGraphicsFont;
OnSelectedColorChanged: procedure(Sender: TObject; ASelectedColor: TTMSFNCGraphicsColor) of object;
OnRValueChanged: procedure(Sender: TObject; AR: Integer; ASelectedColor: TTMSFNCGraphicsColor) of object; // also OnGValueChanged (AG), OnBValueChanged (AB)
OnBeforeDrawSelectedColorPanel / OnAfterDrawSelectedColorPanel
// public
function ColorToRValue(AColor: TTMSFNCGraphicsColor): Integer; // + ColorToGValue, ColorToBValue
function RGBToGraphicsColor(R, G, B: Integer): TTMSFNCGraphicsColor;
```
```delphi
wh := TTMSFNCColorWheel.Create(Self);
wh.Parent := Self;
wh.SetBounds(200, 16, 300, 220);
wh.SelectedColor := gcTeal;
wh.OnSelectedColorChanged := WheelChanged;
```

## TTMSFNCControlPicker (demo `ControlPicker`)

Drops down **any** control you assign to `Control`. Best with controls implementing the picker interfaces (in UI Pack: `TTMSFNCListBox`, `TTMSFNCTreeView`, `TTMSFNCTableView` implement `ITMSFNCControlPickerFull`; `TTMSFNCListEditor` implements `ITMSFNCControlPickerItems`). Other controls work via `OnSetContent` / `CallItemClicked`, or by implementing `ITMSFNCControlPickerBase` (`function PickerGetContent: String;`).
```delphi
TTMSFNCControlPickerStyle = (csDropDown, csDropDownList);
TTMSFNCControlPickerDropDownHeightMode = (chmDropDownHeight, chmControl, chmItems, chmPickerHeight);
TTMSFNCControlPickerDropDownWidthMode = (cwmDropDownWidth, cwmControl, cwmItems, cwmPickerWidth);
property Control: TControl;   property Style: TTMSFNCControlPickerStyle default csDropDown;
property ItemIndex: Integer default -1;  property Text: string;  property ItemHeight, ItemWidth: Single;
property DropDownControlHeight, DropDownControlWidth: Single;
property DropDownHeightMode / DropDownWidthMode;
property AutoComplete (True), AutoCompleteDelay (500), AutoCompleteNumChar (2), AutoDropDown, AutoCloseUp, CaseSensitive;
OnItemSelected: procedure(Sender: TObject; AText: string; AItemIndex: Integer) of object;
OnSetContent: procedure(Sender: TObject; var AText: string; var AAllow: Boolean) of object;
OnAdjustDropDownHeight / OnAdjustDropDownWidth: procedure(Sender: TObject; var ASize: Single; var AAllow: Boolean) of object;
// public
procedure CallItemClicked(AItemIndex: Integer);  procedure UpdatePickerContent; procedure UpdateDropDown;
property Count: Integer;
```
```delphi
// native TListBox in the drop-down (demo)
TMSFNCControlPicker3.Control := ListBox1;
procedure TForm130.ListBox1Click(Sender: TObject);
begin
  TMSFNCControlPicker3.CallItemClicked(ListBox1.ItemIndex);
end;
procedure TForm130.TMSFNCControlPicker3SetContent(Sender: TObject; var AText: string; var AAllow: Boolean);
begin
  if ListBox1.ItemIndex >= 0 then
    AText := ListBox1.Items[ListBox1.ItemIndex];
end;
```

## TTMSFNCCheckGroupPicker / TTMSFNCRadioGroupPicker

Popup hosts a `TTMSFNCCheckGroup` / `TTMSFNCRadioGroup` (see buttons-and-toggles.md).
```delphi
// TTMSFNCCheckGroupPicker
property Items: TStringList;
property Value: Int64 default 0;            // bitmask: bit i = Items[i] checked (max 64 items)
property SelectedItems: String;             // Separator-delimited checked item texts (read/write)
property Separator: Char;                   // ',' by default
property Checked[AIndex: Integer]: Boolean; // public; reads/writes the popup group only
property Columns: Integer default 1;  property CloseOnSelection default False;  property BitmapContainer;
OnCheckBoxClick: TTMSFNCCheckGroupClickEvent; // procedure(Sender: TObject; AItemIndex: Integer; AValue: Int64) of object
OnTitleCheckBoxClick, OnCustomize: TNotifyEvent;
// TTMSFNCRadioGroupPicker
property Items: TStringList;  property ItemIndex: Integer default -1;  property SelectedItem: String;
property Columns: Integer default 1;  property CloseOnSelection default True;
OnRadioButtonClick: TTMSFNCRadioGroupClickEvent; // procedure(Sender: TObject; AItemIndex: Integer) of object
```
```delphi
cgp := TTMSFNCCheckGroupPicker.Create(Self);
cgp.Parent := Self;
cgp.Items.CommaText := 'Mon,Tue,Wed,Thu,Fri';
cgp.Value := 1 or 4;                  // Mon + Wed
// or: cgp.SelectedItems := 'Mon,Wed';
cgp.OnCheckBoxClick := DaysClicked;
```

## Platform notes

- VCL/WEB: `TTMSFNCGraphicsColor` is `TColor`, so demo handlers are written `(Sender: TObject; AColor: TColor)`; FMX handlers get `TAlphaColor`. Use `TTMSFNCGraphicsColor` in shared code.
- The picker text box is a native `TEdit` of the framework (`Edit` property) and the font pickers use a native `TListBox`; the color wheel uses native track bars (`TWebTrackBar` on WEB).
- Positioning: VCL/WEB `SetBounds`, FMX `Position.X/Y` + `Width/Height`.

## Does not exist / common mistakes

- `TTMSFNCColorPicker.Color`, `.Value`, `OnChange`, `OnSelect` — use `SelectedColor` and `OnColorSelected`. Same pattern for `SelectedFillKind`/`OnFillKindSelected`, `SelectedStrokeKind`/`OnStrokeKindSelected`, `SelectedFontName`/`OnFontNameSelected`, `SelectedFontSize`/`OnFontSizeSelected`.
- `TTMSFNCColorPicker.Editable`, `.Text`, `.ShowColorName` — not published; the box only draws the color.
- An empty `TTMSFNCColorSelector` / `TTMSFNCFillKindSelector` / `TTMSFNCStrokeKindSelector` created in code — call `InitializeDefault` (design-time drops get it automatically).
- `TTMSFNCFontNamePicker.Appearance` / `.Rows` / `OnItemSelected` — not published for the font pickers.
- `TTMSFNCBitmapPicker.SelectedBitmap := ...` — read-only; set `SelectedItemIndex` (or use `FindItemByBitmap`).
- Setting `TTMSFNCFillKindSelector.SelectedFillKind` in the Object Inspector — it is public only on the selectors (published on the pickers).
- `TTMSFNCColorWheel.Color`, `OnColorChanged`, `.Hue`/`.Saturation` properties — use `SelectedColor`, `OnSelectedColorChanged`, `RValue/GValue/BValue/HEXValue`.
- `TTMSFNCControlPicker.DropDownControl`, `.PopupControl`, `.Items` — the property is `Control`; items live in the assigned control.
- `TTMSFNCCheckGroupPicker.Checked[i] := True` to preselect — it writes only the popup's group, `Value` is not updated and is re-applied when the popup opens; set `Value` or `SelectedItems` instead. `Title` is not published on the group pickers.
- `TTMSFNCRadioGroupPicker.Value` / `.Selected` — use `ItemIndex` / `SelectedItem`.
- `TAdvColorPickerDropDown`, `TAdvOfficeColorSelector`, `TAdvFontSelector`, `TColorBox`, `TTMSFNCFontPicker`, `TTMSFNCColorComboBox` — FNC names are `TTMSFNCColorPicker`, `TTMSFNCColorSelector`, `TTMSFNCFontNamePicker`, `TTMSFNCFontSizePicker`.
- Unqualified `csDropDown`/`csDropDownList` with both `*.TMSFNCControlPicker` and `*.TMSFNCComboBox` (or `Vcl.StdCtrls`) in uses — qualify as `TTMSFNCControlPickerStyle.csDropDownList`.
