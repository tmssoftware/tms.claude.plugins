# Edit controls (TTMSFNCEdit, TTMSFNCEditButton, TTMSFNCSpinEdit, TTMSFNCComboBox, TTMSFNCSearchEdit, TTMSFNCIPEdit, TTMSFNCLabelEdit, TTMSFNCDirectoryEdit, TTMSFNCPassLock, TTMSFNCSignatureCapture, TTMSFNCTouchKeyboard)
> Sections (line ranges): 6-25 Units, palette, platforms · 26-94 TTMSFNCEdit · 95-127 TTMSFNCSpinEdit · 128-172 TTMSFNCComboBox · 173-185 TTMSFNCSearchEdit · 186-204 TTMSFNCIPEdit · 205-217 TTMSFNCLabelEdit · 218-227 TTMSFNCDirectoryEdit · 228-256 TTMSFNCPassLock · 257-268 TTMSFNCSignatureCapture · 269-288 TTMSFNCTouchKeyboard / TTMSFNCPopupTouchKeyboard · 289-296 Platform notes · 297-314 Does not exist / common mistakes

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCEdit`, `*.TMSFNCSpinEdit`, `*.TMSFNCTrackBar` (spin edit base), `*.TMSFNCComboBox`, `*.TMSFNCCustomPicker`, `*.TMSFNCSearchEdit`, `*.TMSFNCSearchList`, `*.TMSFNCIPEdit`, `*.TMSFNCLabelEdit`, `*.TMSFNCDirectoryEdit`, `*.TMSFNCPassLock`, `*.TMSFNCSignatureCapture`, `*.TMSFNCTouchKeyboard` (+ FNC Core 4.5.0.0 graphics types).

## Units, palette, platforms

All are registered on palette page **`TMS FNC UI`**. Unit = prefix + name: `VCL.` / `FMX.` / `WEBLib.`; Lazarus uses `LCLTMSFNC...` (no dot).

| Class | Unit | Native or FNC-drawn | Platforms |
|---|---|---|---|
| `TTMSFNCEdit` | `TMSFNCEdit` | **native wrapper**: descends from `TCustomEdit` (VCL `StdCtrls`, FMX `FMX.Edit`, WEB `WEBLib.StdCtrls`) | VCL, FMX, WEB, LCL |
| `TTMSFNCEditButton` | `TMSFNCEdit` | FNC control hosting a `TTMSFNCEdit` + a drop-down button | VCL, FMX, WEB, LCL |
| `TTMSFNCSpinEdit` | `TMSFNCSpinEdit` | FNC-drawn (a `TTMSFNCCustomTrackBar` descendant) with an embedded `TTMSFNCEdit` | VCL, FMX, WEB, LCL |
| `TTMSFNCComboBox` | `TMSFNCComboBox` | FNC picker; the box text is a native `TEdit`, the drop-down list is a `TTMSFNCTreeView` | VCL, FMX, WEB, LCL |
| `TTMSFNCSearchEdit` | `TMSFNCSearchEdit` (+ `TMSFNCSearchList` for item types) | FNC control with a `TTMSFNCEditButton`-based edit and a `TTMSFNCSearchList` drop-down | **VCL, FMX, LCL only (no WEB unit)** |
| `TTMSFNCIPEdit` | `TMSFNCIPEdit` | FNC-drawn frame with one `TTMSFNCEdit` per field | VCL, FMX, WEB, LCL |
| `TTMSFNCLabelEdit` | `TMSFNCLabelEdit` | FNC `TTMSFNCHTMLText` that swaps in a `TTMSFNCEdit` while editing | VCL, FMX, WEB, LCL |
| `TTMSFNCDirectoryEdit` | `TMSFNCDirectoryEdit` | FNC control hosting a `TTMSFNCEdit`, a `TTMSFNCToolBarButton` and a `TLabel` | **desktop only (VCL, FMX Win/macOS/Linux); no WEB, no LCL** |
| `TTMSFNCPassLock` | `TMSFNCPassLock` | fully FNC-drawn | VCL, FMX, WEB, LCL |
| `TTMSFNCSignatureCapture` | `TMSFNCSignatureCapture` | fully FNC-drawn | VCL, FMX, WEB, LCL |
| `TTMSFNCTouchKeyboard`, `TTMSFNCPopupTouchKeyboard` | `TMSFNCTouchKeyboard` | FNC-drawn keys | keyboard: desktop + WEB; popup: desktop only; no LCL |

Native wrappers inherit the framework edit's own members (VCL `Font`, `Color`, `MaxLength`, `TextHint`, `Alignment`; FMX `TextSettings`, `TextPrompt`, `KeyboardType`). FNC-drawn controls instead use FNC `Fill`/`Stroke`/`TTMSFNCGraphicsFont` and support `BeginUpdate`/`EndUpdate`.

## TTMSFNCEdit (input types, lookup / autocomplete)

```delphi
TTMSFNCEditType = (etString, etNumeric, etSignedNumeric, etFloat, etSignedFloat, etUpperCase,
  etMixedCase, etLowerCase, etMoney, etHex, etAlphaNumeric, etValidChars);
TTMSFNCEditPrecisionDisplay = (pdNormal, pdShortest);

// published
property EditType: TTMSFNCEditType read FEditType write SetEditType default etString;
property ValidChars: string;                 // used with etValidChars
property Precision: smallint default 0;      // decimals for float/money types
property PrecisionDisplay: TTMSFNCEditPrecisionDisplay default pdNormal;
property AutoThousandSeparator: Boolean default True;
property AllowNumericNullValue: Boolean default False;
property LengthLimit: smallint default 0;
property AutoComplete: Boolean default False;   // inline completion from Lookup.DisplayList
property FullTextSearch: boolean default false; // lookup matches anywhere instead of prefix
property Lookup: TTMSFNCEditLookupSettings;
property Text: string;
property OnLookupSelect: TTMSFNCEditLookupSelectEvent;           // procedure(Sender: TObject; var Value: string) of object
property OnLookupIndexSelect: TTMSFNCEditLookupIndexSelectEvent; // procedure(Sender: TObject; Index: Integer; var Value: string) of object
property OnLookupNeedData: TTMSFNCEditLookupNeedDataEvent;       // procedure(Sender: TObject; Value: string; List: TStrings; var ItemIndex: integer) of object
property OnLookupOpen: TNotifyEvent;
property OnLookupClose: TNotifyEvent;
// public
property FloatValue: double;
property IntValue: Integer;
property Modified: Boolean;
procedure DisplayLookup;          // open the lookup list with all DisplayList values
function LookupListbox: TListBox; // native list box used by the popup
```

`TTMSFNCEditLookupSettings` (published): `Enabled` (False), `DisplayList: TStringList`, `ValueList: TStringList`, `UseValueList` (True: if a matching `ValueList` entry exists, `OnLookupSelect` gets it instead of the display text), `NumChars` (2: characters typed before the list opens), `DisplayCount` (4 visible rows), `CaseSensitive`, `History` (add entered text to the list), `Multi` + `Separator: char` (multiple values in one edit), `Width`, `Height`, `MinimumWidth`, `MinimumHeight`.

```delphi
uses VCL.TMSFNCEdit;

procedure TForm1.FormCreate(Sender: TObject);
var
  ed: TTMSFNCEdit;
begin
  ed := TTMSFNCEdit.Create(Self);
  ed.Parent := Self;
  ed.SetBounds(16, 16, 200, 24);          // FMX: ed.Position.X/Y, ed.Width
  ed.Lookup.Enabled := True;
  ed.Lookup.NumChars := 1;
  ed.Lookup.DisplayList.CommaText := 'Amsterdam,Antwerp,Berlin,Brussels,Paris';
  ed.Lookup.ValueList.CommaText := 'NL,BE,DE,BE,FR';     // optional
  ed.OnLookupSelect := EditLookupSelect;

  // numeric edit
  FPrice := TTMSFNCEdit.Create(Self);
  FPrice.Parent := Self;
  FPrice.SetBounds(16, 48, 120, 24);
  FPrice.EditType := etFloat;
  FPrice.Precision := 2;
  FPrice.FloatValue := 12.5;
end;

procedure TForm1.EditLookupSelect(Sender: TObject; var Value: string);
begin
  Caption := Value;   // 'BE' when 'Antwerp' was picked (UseValueList = True)
end;
```

### TTMSFNCEditButton

FNC control: `Edit: TTMSFNCEdit` (read-only, public), `Button: TTMSFNCToolBarDropDownButton`, `Popup: TTMSFNCPopup`, `ModalPopup: Boolean`, `procedure DropDown; virtual;`. Published: `Text`, `Bitmap`, `BitmapName`, `BitmapContainer`, `ButtonSize` (18), `PopupControl: TControl` (shown in the popup when the button is clicked), `OnButtonClick: TNotifyEvent`.

## TTMSFNCSpinEdit

Descends from `TTMSFNCCustomTrackBar`, so values are `Single` and the range is `Min`/`Max` (defaults 0/100).

```delphi
property Min: Single; property Max: Single; property Value: Single;
property EditFieldPrecision: SmallInt default 1;
property EditFieldPrecisionDisplay: TTMSFNCEditPrecisionDisplay default pdNormal;
property EditFieldKeyboardType: TVirtualKeyboardType;   // FMX only
property Appearance: TTMSFNCCustomSpinEditAppearance;   // ButtonSize, ButtonFill, ButtonStroke, ButtonShape, ButtonDownFill, ..., ValueFont, Orientation
property Interaction: TTMSFNCCustomSpinEditInteraction; // Frequency (step), Editable (True), RepeatClick (False), RepeatInterval (100)
property Edit: TTMSFNCEdit;                             // public, read-only
property OnValueChanged: TTMSFNCCustomTrackBarValueChangedEvent; // procedure(Sender: TObject; AValue: Single) of object
property OnChanged: TNotifyEvent;
property OnBeforeDrawValue / OnAfterDrawValue / OnBeforeDrawButton / OnAfterDrawButton;
```

```delphi
uses VCL.TMSFNCSpinEdit;

sp := TTMSFNCSpinEdit.Create(Self);
sp.Parent := Self;
sp.SetBounds(16, 80, 120, 28);
sp.BeginUpdate;
sp.Min := 0;
sp.Max := 10;
sp.Interaction.Frequency := 0.5;   // step per click
sp.EditFieldPrecision := 1;
sp.Value := 2.5;
sp.EndUpdate;
sp.OnValueChanged := SpinValueChanged;   // procedure(Sender: TObject; AValue: Single)
```

## TTMSFNCComboBox

A `TTMSFNCDefaultPicker` descendant (see pickers-and-selectors.md for the shared picker members: `DropDown`, `Popup`, `Edit`, `Fill`, `Stroke`, `DropDownHeight/Width`).

```delphi
TTMSFNCCustomComboBoxStyle = (csDropDown, csDropDownList);
TTMSFNCCustomComboBoxFilterMode = (fmStart, fmAny);

property Items: TStringList;
property ItemIndex: Integer default -1;   // setter selects the node and fires OnItemSelected + OnChange
property Text: string;
property Style: TTMSFNCCustomComboBoxStyle default csDropDown;  // csDropDownList = not editable
property AutoComplete: Boolean default True;  property AutoCompleteDelay: Integer default 500;
property AutoCompleteNumChar: Integer default 2;
property AutoFilter: Boolean default True;    property FilterMode: TTMSFNCCustomComboBoxFilterMode default fmStart;
property AutoDropDown, AutoCloseUp, CaseSensitive: Boolean;     // default False
property DropDownCount: Integer default 8;    property ItemHeight: Double;
property Font: TTMSFNCGraphicsFont;           property BitmapContainer: TTMSFNCBitmapContainer;
property ItemAppearance: TTMSFNCTreeViewNodesAppearance;   // drop-down list styling
property OnItemSelected: TTMSFNCCustomComboBoxItemSelectedEvent; // procedure(Sender: TObject; AText: string; AItemIndex: Integer) of object
property OnChange: TNotifyEvent;
property OnGetNumberOfItems: TTMSFNCComboBoxGetNumberOfItemsEvent; // virtual mode: procedure(Sender: TObject; var ANumberOfItems: Integer)
property OnGetItemText: TTMSFNCComboBoxGetItemTextEvent;           // procedure(Sender: TObject; AIndex: Integer; var AText: string)
// public
procedure AddItem(AItem: string);
property Count: Integer;
property ClearFilterOnSelection: Boolean;
```

```delphi
uses VCL.TMSFNCComboBox;

cb := TTMSFNCComboBox.Create(Self);
cb.Parent := Self;
cb.SetBounds(16, 120, 180, 26);
cb.BeginUpdate;
cb.Items.Add('Red');
cb.Items.Add('Green');
cb.Items.Add('Blue');
cb.Style := TTMSFNCCustomComboBoxStyle.csDropDownList;   // qualify: VCL StdCtrls also has csDropDownList
cb.EndUpdate;
cb.ItemIndex := 0;           // after Items are filled
cb.OnItemSelected := ComboItemSelected;
```

## TTMSFNCSearchEdit (VCL/FMX/LCL)

Published: `Items: TSearchList`, `Columns: TColumnItems`, `Categories: TCategoryList`, `FilterCondition: TFilterCondition`, `Appearance: TTMSFNCSearchListAppearance`, `Text`, `EmptyText`, `ItemHeight`, `DropDownHeight`, `DropDownWidth`, `AutoDropDown` (True), `AutoSelect`, `SearchButton: TTMSFNCSearchEditButton`, `CategoryButton: TTMSFNCSearchEditPopupButton`, events `OnSelect`, `OnChange`, `OnBeforeDropDown`, `OnDropDown`, `OnDropUp`, `OnSearchButtonClick`, `OnCategoryItemClick` (`procedure(Sender: TObject; CategoryIndex: integer; isChecked: boolean)`). Public: `ItemIndex`, `SearchList`, `Edit`, `UpdateFilter`, `LoadStrings(Value: TStrings)`.

Item types (unit `*.TMSFNCSearchList`, no `TTMSFNC` prefix): `TSearchList.Add(ACaption: string; ADescription: string = '')`, `TSearchListItem.Captions[i]`, `Descriptions[i]`, `CategoryID`, `ItemType: TSearchItemType = (itItem, itCategory)`; `TCategoryList.Add(Caption: string; ID: integer)`; `TFilterCondition`: `FilterType: TFilterType = (mText, mEntireWord, mStartWord, mEndWord)`, `Column`, `AllColumns`, `CaseSensitive`, `Categories`, `CategoryItems`, `AutoSelect`.

Demo `VCL\SearchList` fills a `TTMSFNCSearchList` and copies it:
```delphi
TMSFNCSearchEdit1.FilterCondition.Assign(TMSFNCSearchList1.FilterCondition);
TMSFNCSearchEdit1.Appearance.Assign(TMSFNCSearchList1.Appearance);
TMSFNCSearchEdit1.Items.Assign(TMSFNCSearchList1.Items);
```

## TTMSFNCIPEdit

```delphi
TTMSFNCIPEditType = (IPv4, IPv6, MAC);            // NOTE: no prefix
property IPAddress: string;                       // '192.168.0.1', 'xxxx:...' (8 hex groups), 'AA-BB-...' (6)
property IPAddressType: TTMSFNCIPEditType default IPv4;
property IPAddressFont: TTMSFNCGraphicsFont;
property OnChange: TNotifyEvent;
// public
property IPv4Address: DWORD;                      // raises if IPAddressType <> IPv4
property IPv6Address: TTMSFNCIPv6Address;         // record IPv6HiHi, IPv6HiLo, IPv6LoHi, IPv6LoLo: DWORD
```
```delphi
ip := TTMSFNCIPEdit.Create(Self);
ip.Parent := Self;
ip.IPAddressType := IPv4;
ip.IPAddress := '192.168.1.10';
```

## TTMSFNCLabelEdit

Shows HTML text; click (or Enter when focused) switches to an inline edit with accept/cancel buttons. Enter accepts, Escape cancels, focus loss accepts.

Published: `Text` (inherited from `TTMSFNCHTMLText`), `Editable: Boolean` (True), `AcceptButtonStroke`, `CancelButtonStroke`, events `OnAccept`, `OnCancel`, `OnEditStart`, `OnEditEnd`, `OnEditExit` (all `TNotifyEvent`), `OnEditKeyDown`. Public: `EditMode: Boolean` (set True to start editing in code), `Edit: TTMSFNCEdit`, `AcceptButton`, `CancelButton: TTMSFNCImage`.

```delphi
le := TTMSFNCLabelEdit.Create(Self);
le.Parent := Self;
le.Text := 'Click to rename';
le.OnAccept := LabelAccepted;    // read le.Text there
```

## TTMSFNCDirectoryEdit (desktop only)

Published: `Text` (the path), `EmptyText`, `DialogCaption`, `EditorEnabled` (True), `AutoDirectoryLookup` (False: lookup list of sub-folders while typing), `ButtonSettings` (`Text`, `Width`, `Align: TTMSFNCDirectoryEditButtonAlign = (debaLeft, debaRight)`, `Appearance`, `Bitmap`, `BitmapName`), `LabelSettings` (`Text`, `Position: TTMSFNCDirectoryEditLabelPosition` (`delpLeftCenter` default, `delpTopLeft`, ...), `Font`, `Spacing`), `BitmapContainer`. Events:
```delphi
OnDialogShow: procedure(Sender: TObject; var AInitialPath: string) of object;
OnDialogClose: procedure(Sender: TObject; var AResultPath: string; ASuccess: Boolean) of object;
OnChange: TNotifyEvent;   // + OnLookupSelect/OnLookupIndexSelect/OnLookupNeedData/OnLookupOpen/OnLookupClose (TTMSFNCEdit types)
```
Public: `function IsValidDirectory: Boolean;`, `procedure ClickButton;` (opens the dialog), `Edit: TTMSFNCEdit`, `Button: TTMSFNCToolBarButton`.

## TTMSFNCPassLock (demo `PassLock`)

```delphi
TTMSFNCPassLockType = (pltNumber, pltPattern);
TTMSFNCPassLockButtonShape = (plbsCircle, plbsRectangle, plbsRoundedRectangle);
property PasswordValue: string;       // the expected password; also sets PasswordLength
property PasswordLength: integer;     // READ-ONLY (= Length(PasswordValue))
property PasswordEntry: string;       // what the user typed so far
property Options: TTMSFNCPassLockOptions;  // LockType, LearnMode, ShowEntry, ShowPasswordLength, ShowOKButton, ShowClearEntryButton, EnableKeyboardInput
property ButtonAppearance: TTMSFNCPassLockButtonAppearance;  // Fill/Stroke/Font + Hover*/Down*, Shape, Spacing, MaxSize, PatternLine, CaptionOK, CaptionClearEntry
property EntryAppearance: TTMSFNCPassLockEntryAppearance;
OnPasswordCheck: TTMSFNCPassLockPasswordCheckEvent;   // procedure(Sender: TObject; AEntry: string; var AMatch: Boolean) of object
OnLearnPassword, OnNewPassword, OnPatternEntryEnd: TTMSFNCPassLockPasswordEvent; // procedure(Sender: TObject; APassword: string)
OnConfirmPassword: TTMSFNCPassLockPasswordCheckEvent;
OnPasswordEntryChanged: TTMSFNCPassLockPasswordEntryChangedEvent; // procedure(Sender: TObject; APasswordEntry: string; AValue: string)
// public
procedure AddPasswordEntry(AEntry: string); procedure ClearLastPasswordEntry;
procedure ClearPasswordEntry; function PasswordCheck: Boolean;
```
With `pltNumber` + `ShowPasswordLength` the check runs automatically once the entry reaches the password length; otherwise via the OK button / Enter (`ShowOKButton`) or by calling `PasswordCheck`. A failed check clears the entry. `LearnMode`: first entry fires `OnLearnPassword`, the repeat fires `OnConfirmPassword`; on match `PasswordValue` is set and `LearnMode` turns off.
```delphi
TMSFNCPassLock1.PasswordValue := '1234';
procedure TForm1.TMSFNCPassLock1PasswordCheck(Sender: TObject; AEntry: string; var AMatch: Boolean);
begin
  if AMatch then
    TMSFNCPassLock1.Visible := False;
end;
```

## TTMSFNCSignatureCapture (demo `SignatureCapture`)

Published: `Pen: TTMSFNCGraphicsStroke` (color/width of the ink), `Text` (hint text), `TextPosition` (`Position: TTMSFNCSignatureCaptureTextHintPosition` = `tpBottomCenter`, ..., `tpXY`, `tpNone`; `X`, `Y`, `Line`), `ClearSig` (clear icon: `Position` = `cpBottomLeft`, ..., `cpNone`; `Image`), `Font`, `Fill`, `Stroke`. **No events.** Public: `Empty: Boolean` (read = no points; **assign True to clear**), `SignaturePoints`.
VCL/FMX/LCL only: `SaveToFile`, `LoadFromFile`, `SaveToStream`, `LoadFromStream` (vector points), `SaveToImageFile(FileName)`, `SaveToImageStream(AStream)`, `GetImageFromStream(AStream): TBitmap`. WEB only: `function GetBase64Img: string;`.
```delphi
TMSFNCSignatureCapture1.Pen.Color := gcNavy;
TMSFNCSignatureCapture1.Pen.Width := 3;
if not TMSFNCSignatureCapture1.Empty then
  TMSFNCSignatureCapture1.SaveToImageFile('signature.png');
TMSFNCSignatureCapture1.Empty := True;   // clear
```

## TTMSFNCTouchKeyboard / TTMSFNCPopupTouchKeyboard

```delphi
TTMSFNCKeyboardType = (ktQWERTY, ktAZERTY, ktDVORAK, ktNUMERIC, ktCELLPHONE, ktQWERTZ {$IFDEF MSWINDOWS}, ktCustom{$ENDIF});
// TTMSFNCTouchKeyboard published
property KeyboardType: TTMSFNCKeyboardType;  property Keys: TTMSFNCTouchKeyCollection;
property AutoPostKey: Boolean default True;  // send key presses to the focused control
property AutoCapsDisplay, AllowAutoZoom: Boolean; property KeySpacing, BorderRounding: Integer;
property Font, SmallFont: TTMSFNCGraphicsFont; property HighlightCaps, HighlightAltGr: TTMSFNCGraphicsColor;
OnKeyClick: TTMSFNCTouchKeyEvent;   // procedure(Sender: TObject; AIndex: Integer) of object
OnDrawKey: TTMSFNCDrawKeyEvent;     // procedure(Sender: TObject; AKey: TTMSFNCTouchKeyItem; AGraphics: TTMSFNCGraphics; ADown: Boolean; ARect: TRectF; var ADefaultDraw: Boolean)
// public
procedure Zoom(AHorz, AVert: Double; AKeysOnly: Boolean = False; AAbsoluteZoom: Boolean = False);
procedure AutoZoom; procedure SaveKeybdLayout(AFileName: string);
procedure LoadKeybdLayout(AFileName: string; AAutoSize: TTMSFNCAutoSizeLayout = aslKeyboard);
// TTMSFNCPopupTouchKeyboard (non-visual): KeyboardType, AutoPostKey (default False!), OnShow, OnClose,
procedure ShowKeyboard; procedure HideKeyboard; property Keyboard: TTMSFNCTouchKeyBoard;
```
`TTMSFNCTouchKeyItem`: `Caption`, `ShiftCaption`, `AltGrCaption`, `KeyValue`, `SpecialKey: TTMSFNCSpecialKey` (`skNone`, `skShift`, `skReturn`, `skBackSpace`, `skSpaceBar`, ...), `X`, `Y`, `Width`, `Height`, `Color`, `ColorDown`, `TextColor`, `ImageName`.

## Platform notes

- Positioning in code: VCL/WEB `SetBounds`/`Left`/`Top`/`Align := alTop`; FMX `Position.X/Y`, `Align := TAlignLayout.Top`.
- `TTMSFNCEdit` members differ per framework because they come from the native base: VCL `Font`/`Color`/`TextHint`; FMX `TextSettings`/`TextPrompt`/`KeyboardType`/`OnChangeTracking`; `FloatValue`/`IntValue`/`Lookup`/`EditType` are the same everywhere.
- `TTMSFNCSpinEdit.EditFieldKeyboardType` exists only on FMX.
- No WEB: `TTMSFNCSearchEdit`, `TTMSFNCDirectoryEdit`, `TTMSFNCPopupTouchKeyboard` (desktop attribute). No LCL: `TTMSFNCDirectoryEdit`, `TTMSFNCTouchKeyboard`.
- `TTMSFNCSignatureCapture` file/stream/image methods are compiled out on WEB (`{$IFNDEF WEBLIB}`); use `GetBase64Img`.

## Does not exist / common mistakes

- `TTMSFNCEdit.Value`, `.AsFloat`, `.AsInteger`, `.NumbersOnly`, `etDate`, `etTime`, `etInteger`, `etNumber` — use `EditType := etNumeric/etSignedNumeric/etFloat/etMoney` and `IntValue`/`FloatValue` (public, not published).
- `TTMSFNCEdit.Fill` / `.Stroke` / `.Appearance` / `.Buttons` / `.EditButton` — it is a native edit; for a button use `TTMSFNCEditButton` (`OnButtonClick`, `PopupControl`).
- `TTMSFNCEdit.AutoCompleteList`, `.Items`, `.LookupList` (as a property) — fill `Lookup.DisplayList` and set `Lookup.Enabled := True`; `LookupList`/`LookupListbox` are functions returning the popup objects.
- Expecting the lookup to open after 1 character — `Lookup.NumChars` defaults to 2.
- `TTMSFNCSpinEdit.Increment`, `.MinValue`, `.MaxValue`, `.Position`, `.Text`, `OnChange` — use `Interaction.Frequency`, `Min`, `Max`, `Value` (Single), `Edit.Text`, `OnValueChanged`/`OnChanged`.
- `TTMSFNCComboBox.OnSelect`, `.Sorted`, `.DroppedDown`, `.Items.Objects` for display — use `OnItemSelected(Sender; AText; AItemIndex)`, sort `Items` yourself, `DropDown` (toggles the popup).
- Unqualified `csDropDownList` / `csDropDown` in a unit that also uses `Vcl.StdCtrls` (or `*.TMSFNCControlPicker`, which declares the same names) resolves to the wrong enum — write `TTMSFNCCustomComboBoxStyle.csDropDownList`.
- Setting `TTMSFNCComboBox.ItemIndex` in `FormCreate` and being surprised by `OnItemSelected`/`OnChange` firing — the setter fires both; assign the handlers afterwards or guard them.
- `TTMSFNCSearchEdit` on TMS WEB Core — no WEB unit; use `TTMSFNCEdit` with `Lookup` or `TTMSFNCComboBox` (`AutoFilter`, `FilterMode := fmAny`).
- `TTMSFNCIPEdit.Text` / `itIPv4` / `ipv4Type` — the property is `IPAddress` and the enum values are bare `IPv4`, `IPv6`, `MAC`. `IPv4Address`/`IPv6Address` raise unless `IPAddressType` matches.
- `TTMSFNCLabelEdit.Caption`, `.OnChange`, `.StartEdit` — use `Text`, `OnAccept`/`OnEditEnd`, `EditMode := True`.
- `TTMSFNCDirectoryEdit.Directory`, `.Path`, `.Execute`, `TTMSFNCFileEdit` — use `Text`, `ClickButton`; there is no FNC file-edit counterpart in UI Pack.
- `TTMSFNCPassLock.Password`, `.PasswordLength := 6`, `OnPasswordOK` — use `PasswordValue` (sets the length), `OnPasswordCheck` with `AMatch`.
- `TTMSFNCSignatureCapture.Clear`, `.IsEmpty`, `.OnChange`, `.SaveToPNG`, `.PenColor` — use `Empty := True`, `Empty`, `SaveToImageFile`, `Pen.Color` / `Pen.Width`; there are no published events.
- `TTMSFNCTouchKeyboard.Show` / `TTMSFNCPopupTouchKeyboard.Execute` / `.Popup` — the popup uses `ShowKeyboard` / `HideKeyboard`; and its `AutoPostKey` defaults to **False** (the docked keyboard's to True).
