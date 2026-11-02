# Dialogs, filter view and misc (TTMSFNCTaskDialog, TTMSFNCFontDialog, TTMSFNCFindDialog, TTMSFNCReplaceDialog, TTMSFNCFilterView, TTMSFNCDataSetFilterDialog / TTMSFNCFilterDialog, TTMSFNCObjectInspector, TTMSFNCChat)

Verified against `tms.fnc.uipack` 7.3.1.2 source: `VCL.TMSFNCTaskDialog`, `VCL.TMSFNCFontDialog`, `VCL.TMSFNCCustomDialog`, `VCL.TMSFNCFindDialog`, `VCL.TMSFNCReplaceDialog`, `VCL.TMSFNCFilterView`, `VCL.TMSFNCFilterDialog`, `VCL.TMSFNCObjectInspector`, `VCL.TMSFNCChat`, their `*Reg.pas` units, the WEB package `Packages\web\TMSFNCUIPackWEB.dpk`, and FNC Core 4.5.0.0 `TMS.TMSFNCFilterBuilder`.

## Units, palette, platforms

All register on palette page **`TMS FNC UI`**. Use the `VCL.` / `FMX.` / `WEBLib.` prefix (LCL: no dot, e.g. `LCLTMSFNCTaskDialog`).

| Component | Unit | Registered on |
|---|---|---|
| `TTMSFNCTaskDialog` | `*.TMSFNCTaskDialog` | VCL, FMX, WEB, LCL |
| `TTMSFNCFontDialog` | `*.TMSFNCFontDialog` | VCL, FMX, WEB, LCL |
| `TTMSFNCFindDialog` | `*.TMSFNCFindDialog` (base `*.TMSFNCCustomDialog`) | VCL, FMX, WEB |
| `TTMSFNCReplaceDialog` | `*.TMSFNCReplaceDialog` | VCL, FMX, WEB |
| `TTMSFNCFilterView` (+ `TTMSFNCFilterView*` child controls) | `*.TMSFNCFilterView` + `TMS.TMSFNCFilterBuilder`, `TMS.TMSFNCFilterStructure`, `TMS.TMSFNCValue` | VCL, FMX, WEB |
| `TTMSFNCDataSetFilterDialog` | `*.TMSFNCFilterDialog` (+ `TMS.TMSFNCFilterBuilder`) | VCL, FMX only (`[ComponentPlatformsAttribute(TMSPlatformsDesktop)]`) |
| `TTMSFNCFilterDialog` (generic, no dataset) | `*.TMSFNCFilterDialog` | **not registered anywhere**; create in code. Attribute `TMSPlatformsWebDesktop`; the `WEBLib.TMSFNCFilterDialog` unit is in the WEB package, its Reg unit is not |
| `TTMSFNCObjectInspector` | `*.TMSFNCObjectInspector` (descends from `TTMSFNCTreeView`) | VCL, FMX, WEB, LCL |
| `TTMSFNCChat` | `*.TMSFNCChat` (descends from `TTMSFNCCustomTableView`) | VCL, FMX, WEB, LCL |

## How each dialog returns its result (read this first)

| Dialog | VCL / FMX desktop | FMX Android/iOS (`FMXMOBILE`) | WEB |
|---|---|---|---|
| TaskDialog | `function Execute: TModalResult;` (blocking) | `procedure Execute(const ResultProc: TProc<TModalResult> = nil);` | `function Execute(AProc: TDialogResultProc = nil): TModalResult;` - returns before the user clicks; use `AProc` |
| FontDialog | `procedure Execute;` (**no return value**) - read result in `OnDialogResult` | same, non-blocking | same, non-blocking |
| Find / Replace / FilterDialog (all `TTMSFNCCustomDialog`) | `function Execute(AModal: Boolean = True): TModalResult;` | same | `procedure Execute(AProc: TModalResultProc = nil; AModal: Boolean = True);` |

`OnDialogResult` (TaskDialog, FontDialog) fires on every platform, so it is the portable way. `TDialogResultProc` / `TModalResultProc` are TMS WEB Core types (`reference to procedure(AValue: TModalResult)`-style), not FNC ones.

## TTMSFNCTaskDialog

```delphi
property Title: string;            property Instruction: string;      property Content: string;   // HTML-capable text
property Icon: TTMSFNCTaskDialogIcon default tdiBlank;   // tdiBlank, tdiWarning, tdiQuestion, tdiError, tdiInformation, tdiShield, tdiAbout
property FooterIcon: TTMSFNCTaskDialogIcon default tdiBlank;   // same enum (tdi*); TTMSFNCTaskDialogFooterIcon (tfi*) exists but is NOT the property type
property Footer: string;           property CustomIcon: TTMSFNCBitmap;
property CommonButtons: TTMSFNCTaskDialogCommonButtons default [];   // tcbOK, tcbYes, tcbNo, tcbCancel, tcbRetry, tcbClose
property CustomButtons: TStringList;   property RadioButtons: TStringList;
property DefaultButton: Integer default 0;   property DefaultRadioButton: Integer default 0;
property Options: TTMSFNCTaskDialogOptions default [];
  // tdoCommandLinks, tdoCommandLinksNoIcon, tdoExpandedDefault, tdoAllowMinimize*, tdoAllowDialogCancel*,
  // tdoVerifyChecked, tdoProgressBar, tdoTimer, tdoNoDefaultRadioButton   (* = not on WEB)
property DisplayedButtons: TTMSFNCTaskDialogDisplayedButtons default tdbDefault;  // tdbNone hides all buttons
property ExpandedText, ExpandControlText, CollapseControlText, VerifyText: string;
property InputType: TTMSFNCTaskDialogInputType default titNone;
  // titEdit, titMemo, titComboList, titDate, titCustom, titNone, titTime, titPassword
property InputItems: TStringList;  property InputText: string;  property InputControl: TControl;  // InputControl used with titCustom
property ProgressBarMin/ProgressBarMax: Integer;  property AutoClose: Boolean;  property AutoCloseTimeOut: Integer;
property DialogPosition: TTMSFNCTaskDialogPosition default tdpScreenCenter;   // tdpOwnerFormCenter
property MinDialogWidth: Integer default 350;  property MaxDialogWidth: Integer default 1000;
property Appearance: TTMSFNCTaskDialogAppearance;  // DialogColor, DialogPanelFill, DialogPanelStroke, InstructionColor, ContentColor, ExpandedTextColor, FooterColor
property ButtonFont, CommandLinkFont: TTMSFNCGraphicsFont;   property ApplicationIsParent: Boolean;
// public, read after closing:
property RadioButtonResult: Integer;   // 0-based index into RadioButtons
property VerifyResult: Boolean;
property DialogForm: TTMSFNCTaskDialogForm;
```

Events: `OnDialogResult: procedure(Sender: TObject; AModalResult: TModalResult)`, `OnBeforeCloseDialog: procedure(Sender: TObject; var AAllow: Boolean)`, `OnDialogButtonClick: procedure(Sender: TObject; ButtonID: Integer)`, `OnDialogRadioClick: procedure(Sender: TObject; RadioID: Integer)`, `OnDialogVerifyClick: procedure(Sender: TObject; Checked: Boolean)`, `OnDialogExpandButtonClick: procedure(Sender: TObject; Expanded: Boolean)`, `OnDialogProgress: procedure(Sender: TObject; var Pos: Integer)`, `OnDialogCreated`, `OnDialogClosed`, `OnDialogTimer`, `OnAutoClose` (TNotifyEvent).

Result values (from source): common buttons map tcbOK->`mrOk`, tcbYes->`mrYes`, tcbNo->`mrNo`, tcbCancel->`mrCancel`, tcbRetry->`mrRetry`, **tcbClose->`mrAbort`**. `CustomButtons[i]` returns **`100 + i`**, as command links (`tdoCommandLinks`) **`200 + i`** (i is 0-based). No buttons at all -> an OK button is shown.

```delphi
// VCL\TaskDialog demo (VCL / FMX desktop: blocking)
procedure TForm1.Button1Click(Sender: TObject);
var mr: TModalResult;
begin
  TMSFNCTaskDialog1.Title := 'Confirm';
  TMSFNCTaskDialog1.Instruction := 'Save changes?';
  TMSFNCTaskDialog1.Content := 'The document was modified.';
  TMSFNCTaskDialog1.Icon := tdiQuestion;
  TMSFNCTaskDialog1.CommonButtons := [tcbYes, tcbNo, tcbCancel];
  TMSFNCTaskDialog1.VerifyText := 'Do not ask again';
  TMSFNCTaskDialog1.InputType := titNone;
  mr := TMSFNCTaskDialog1.Execute;
  case mr of
    mrYes: SaveDoc;
    mrNo: ;
  end;
  if TMSFNCTaskDialog1.VerifyResult then FAskAgain := False;
end;

// custom command links
TMSFNCTaskDialog1.CustomButtons.Clear;
TMSFNCTaskDialog1.CustomButtons.Add('Install now');
TMSFNCTaskDialog1.CustomButtons.Add('Remind me later');
TMSFNCTaskDialog1.Options := TMSFNCTaskDialog1.Options + [tdoCommandLinks];
case TMSFNCTaskDialog1.Execute of
  200: Install;      // first link
  201: Postpone;
end;

// WEB (and portable): result arrives later
TMSFNCTaskDialog1.InputType := titEdit;
TMSFNCTaskDialog1.Execute(
  procedure(AValue: TModalResult)
  begin
    if AValue = mrOk then
      WebLabel1.Caption := TMSFNCTaskDialog1.InputText;
  end);
```
The FMX demo uses `OnDialogResult` instead of the return value; that handler works on all platforms (InputText/VerifyResult are already updated when it fires).

## TTMSFNCFontDialog

No `Font` property: the selection is exposed as separate values.
```delphi
property FontName: string;   property FontSize: Integer default -1;   property FontColor: TTMSFNCGraphicsColor default gcNull;
property BoldSelected, ItalicSelected, UnderlineSelected, StrikethroughSelected: Boolean;
property ApplicationIsParent: Boolean;
procedure Execute;   // no result
OnDialogResult: procedure(Sender: TObject; AModalResult: TModalResult) of object;
OnFontNameChanged(Sender; FontName: string); OnFontSizeChanged(Sender; FontSize: Integer);
OnFontColorChanged(Sender; FontColor: TTMSFNCGraphicsColor); OnFontStyleChanged(Sender; ABold, AItalic, AUnderline, AStrikethrough: Boolean);
OnDialogCreated, OnDialogClosed: TNotifyEvent;
```
`FontName/FontSize/FontColor` are written back when the form closes **even on Cancel**, so always check `AModalResult` (VCL\Pickers demo):
```delphi
procedure TForm1.Button1Click(Sender: TObject);
begin
  TMSFNCFontDialog1.Execute;
end;

procedure TForm1.TMSFNCFontDialog1DialogResult(Sender: TObject; AModalResult: TModalResult);
begin
  if AModalResult = mrOK then
  begin
    TMSFNCHTMLText1.Font.Name := TMSFNCFontDialog1.FontName;
    TMSFNCHTMLText1.Font.Size := TMSFNCFontDialog1.FontSize;
    TMSFNCHTMLText1.Font.Color := TMSFNCFontDialog1.FontColor;
    if TMSFNCFontDialog1.BoldSelected then
      TMSFNCHTMLText1.Font.Style := TMSFNCHTMLText1.Font.Style + [TFontStyle.fsBold]
    else
      TMSFNCHTMLText1.Font.Style := TMSFNCHTMLText1.Font.Style - [TFontStyle.fsBold];
  end;
end;
```

## TTMSFNCFindDialog / TTMSFNCReplaceDialog

Both descend from `TTMSFNCCustomDialog` (`Execute(AModal)`, `Close`, `OnClose`, `OnBeforeShowForm: procedure(ASender: TObject; AForm: TCustomForm)`). The dialog does not search anything itself: you do the search in the events (or the control implements `ITMSFNCFind`/`ITMSFNCReplace`, which only built-in controls such as the DataGrid renderer and `TTMSFNCMemo` wire up; the `Control` property is protected). Usually shown modeless: `Execute(False)`.

```delphi
// Find
property FindText: string;  property FindList: TStringList;  property AutoHistory: Boolean default True;
property Options: TTMSFNCFindDialogOptions;   // fdoCaseSensitive, fdoExpression, fdoCloseIfFound, fdoWholeWordOnly, fdoWrapAtEndOfFile,
  // fdoContinueToNextFile, fdoMoreEnabled, fdoSetMarkerEnabled, fdoNextEnabled, fdoFindEnabled, fdoCloseEnabled, fdoMoreExpanded, fdoDown, fdoSelection
  // default [fdoMoreEnabled, fdoNextEnabled, fdoSetMarkerEnabled, fdoFindEnabled, fdoCloseEnabled, fdoDown]
property VisibleOptions: TTMSFNCFindDialogVisibleOptions;  // fdovCaseSensitive ... fdovFindCombo, fdovFindMemo, fdovDirection, fdovSelection
property UILanguage: TTMSFNCFindDialogUILanguage;          // Caption, FindWhat, Find, Next, Close, CaseSensitive, ...
OnFind, OnFindNext: procedure(Sender: TObject; AFindText: string; var AFound: Boolean) of object;
OnFindEditChange: procedure(Sender: TObject; APrevText, ANewText: string) of object;
OnSetMarker: TNotifyEvent;

// Replace (no AFound parameter here!)
property ReplaceText: string;  property ReplaceList: TStringList;  property Options: TTMSFNCReplaceDialogOptions;  // rdo*
property VisibleOptions: TTMSFNCReplaceDialogVisibleOptions;   // rdov*
OnFind, OnFindNext: procedure(Sender: TObject; AFindText: string) of object;
OnReplace, OnReplaceAll: procedure(Sender: TObject; AFindText, AReplaceText: string) of object;
OnFindEditChange, OnReplaceEditChange: procedure(Sender: TObject; APrevText, ANewText: string) of object;
```
The check boxes update `Options` live (e.g. `fdoCaseSensitive`, `fdoDown`; `rdoCaseSensitive`, `rdoDown`), so read `Options` inside the handler.

```delphi
procedure TForm1.FindBtnClick(Sender: TObject);
begin
  TMSFNCFindDialog1.FindText := 'hello';
  TMSFNCFindDialog1.Execute(False);   // modeless
end;

procedure TForm1.TMSFNCFindDialog1Find(Sender: TObject; AFindText: string; var AFound: Boolean);
var p: Integer;
begin
  if fdoCaseSensitive in TMSFNCFindDialog1.Options then
    p := Pos(AFindText, Memo1.Text)
  else
    p := Pos(LowerCase(AFindText), LowerCase(Memo1.Text));
  AFound := p > 0;     // with "close if found" checked the dialog closes when True
  if AFound then begin Memo1.SelStart := p - 1; Memo1.SelLength := Length(AFindText); end;
end;

procedure TForm1.TMSFNCReplaceDialog1ReplaceAll(Sender: TObject; AFindText, AReplaceText: string);
var f: TReplaceFlags;
begin
  f := [rfReplaceAll];
  if not (rdoCaseSensitive in TMSFNCReplaceDialog1.Options) then Include(f, rfIgnoreCase);
  Memo1.Text := StringReplace(Memo1.Text, AFindText, AReplaceText, f);
end;
```
The DataGrid has its own instances: `Grid.ShowFindDialog`, `Grid.ShowReplaceDialog`, `OnBeforeShowFindDialog(Sender; AFindDialog: TTMSFNCFindDialog; var ACanShow)`.

## TTMSFNCFilterView

A scroll box (VCL/WEB `TScrollBox`, FMX `TVertScrollBox`) holding filter controls. Each control contributes expressions to a filter structure; the view produces `FilterText` and fires `OnFilterTextChanged`. It does **not** filter a dataset itself (no `DataSet` property).

```delphi
property FilterText: string;   // public, read-only
property FilterFormatType: TTMSFNCFilterBuilderFormatType default fftDelphiDataSet;  // fftUniversalFilterExpressions, fftOData, fftCustom
property GroupOperator: TTMSFNCFilterBuilderGroupOperator default fgoAnd;   // fgoAND, fgoOR
property UILanguage: TTMSFNCFilterViewUILanguage;   property FilterParseFormat; property AdaptToStyle;
OnFilterTextChanged: procedure(Sender: TObject; AFilterText: string) of object;
OnFilterTextParse / OnFilterTextParsed / OnFilterViewItemParse / OnFilterViewGroupParse / OnFilterViewGroupParsed
procedure BeginUpdate; procedure EndUpdate;
// factory methods (same on TTMSFNCFilterViewPanel, which uses AddLabel instead of AddText):
function AddFilterPanel(AGroupOperator: TTMSFNCFilterBuilderGroupOperator = fgoAND; AOwner: TComponent = nil): TTMSFNCFilterViewPanel;
function AddFilterCheckBox(AValue: TTMSFNCValue; AFilterFieldName: string = ''; AFilterFieldType: TTMSFNCFilterBuilderDataType = fdtAutomatic; AExpressionOperator: TTMSFNCFilterBuilderExpressionOperator = feoEqual; AChecked: Boolean = False): TTMSFNCFilterViewCheckBox;
function AddFilterCheckGroup(AItems: array of string; ASelectedItemIndexes: array of Integer; AFilterFieldName: string = ''; AFilterFieldType = fdtText; AExpressionOperator = feoEqual): TTMSFNCFilterViewCheckGroup;   // also TStrings overload
function AddFilterRadioGroup(AItems: array of string; ASelectedItemIndex: Integer = -1; AFilterFieldName: string = ''; ...): TTMSFNCFilterViewRadioGroup;
function AddFilterComboBox(AItems: array of string; ASelectedItemIndex: Integer = -1; AFilterFieldName: string = ''; ...): TTMSFNCFilterViewComboBox;
function AddFilterTrackBar(AValue: Single = 0; AMinimum: Single = 0; AMaximum: Single = 100; AFilterFieldName: string = ''; AFilterFieldType = fdtAutomatic; AExpressionOperator = feoEqual): TTMSFNCFilterViewTrackBar;
function AddFilterRangeSlider(AValueLeft: Single = 0; AValueRight: Single = 100; AMinimum: Single = 0; AMaximum: Single = 100; AFilterFieldName: string = ''; AFilterFieldType = fdtAutomatic; ALeftExpressionOperator = feoLargerThanOrEqual; ARightExpressionOperator = feoSmallerThanOrEqual): TTMSFNCFilterViewRangeSlider;
function AddFilterExpressionValueEdit(AFilterValueText: string = ''; AFilterFieldName: string = ''; AFilterFieldType = fdtAutomatic; AExpressionOperator = feoNotEmpty): TTMSFNCFilterViewExpressionValueEdit;
function AddFilterDatePicker(ADate: TDate; AFilterFieldName: string = ''; AFilterFieldType = fdtDate; AExpressionOperator = feoEqual): TTMSFNCFilterViewDatePicker;
function AddFilterRadioButton(AValue: TTMSFNCValue; AGroupName: string = ''; AFilterFieldName: string = ''; ...): TTMSFNCFilterViewRadioButton;
function AddFilterControlContainer(AFilterValueText: string; AFilterFieldName: string = ''; ...): TTMSFNCFilterViewControlContainer;
function AddText(AText: string): TTMSFNCFilterViewLabel;
function AddCustomItemControl(AControl: TControl; AValue: TTMSFNCValue; AFilterFieldName: string; AFilterFieldType = fdtAutomatic; AExpressionOperator = feoEqual; AAddToFilter: Boolean = True; AGroupControl: TControl = nil): TTMSFNCFilterStructureItem;
function UpdateCustomItemControlValue(AControl: TControl; AValue: TTMSFNCValue): Boolean;
function RemoveCustomItemControl(AControl: TControl): Boolean;
```
Enums (FNC Core `TMS.TMSFNCFilterBuilder`): `TTMSFNCFilterBuilderExpressionOperator = (feoStartsWith, feoEndsWith, feoContains, feoEqual, feoNotEqual, feoEmpty, feoNotEmpty, feoLargerThan, feoSmallerThan, feoLargerThanOrEqual, feoSmallerThanOrEqual)`; `TTMSFNCFilterBuilderDataType = (fdtAutomatic, fdtText, fdtBoolean, fdtDateTime, fdtDate, fdtTime, fdtFloat, fdtNumber, fdtOther)`.

Each filter child control publishes `DefaultFilterProperties` (`FilterFieldName`, `FilterFieldType`, `ExpressionOperator`, ...) and `FilterExpressions: TTMSFNCFilterViewExpressions` (map a control value to an expression; `AddOrUpdateExpression(...)`, `AddFilterItem`, `UpdateFilterItem(APropertyValue)`, event `OnExpressionNotFound`). `TTMSFNCFilterViewExpressionValueEdit`: `FilterExpression.FilterValue / .ExpressionOperator`, `ShowNameLabel`. `TTMSFNCFilterViewPanel.UpdateHeight` after adding/removing children.

```delphi
// based on VCL\Filter View demo (TMSFNCFilterView_DataSetDemo)
procedure TForm1.FormCreate(Sender: TObject);
var p: TTMSFNCFilterViewPanel;
begin
  TMSFNCFilterView1.BeginUpdate;
  try
    TMSFNCFilterView1.AddText('Size');
    TMSFNCFilterView1.AddFilterRangeSlider(0, 100, 0, 100, 'SIZE', fdtNumber);
    p := TMSFNCFilterView1.AddFilterPanel(fgoOR);
    p.AddFilterCheckGroup(['Ocean', 'Lake'], [0], 'AREA', fdtText, feoEqual);
    p.UpdateHeight;
  finally
    TMSFNCFilterView1.EndUpdate;
  end;
end;

procedure TForm1.TMSFNCFilterView1FilterTextChanged(Sender: TObject; AFilterText: string);
begin
  AnimalDataSet.Filter := AFilterText;
  AnimalDataSet.Filtered := AFilterText <> '';
end;
```
Use `FilterFormatType := fftDelphiDataSet` (default) for `TDataSet.Filter`; the other formats are for OData / universal expressions.

## TTMSFNCDataSetFilterDialog and TTMSFNCFilterDialog

Both live in `*.TMSFNCFilterDialog` and show a visual filter-builder (groups, AND/OR, expressions). `TTMSFNCDataSetFilterDialog` (the palette component, VCL/FMX) builds its columns from `DataSet` fields and applies the result to the dataset itself. `TTMSFNCFilterDialog` (create in code, also WEB) has a public `FilterBuilder: TTMSFNCFilterBuilder` whose `DataColumns` you fill yourself; its `FormatType` is set to `fftUniversalFilterExpressions` in its constructor.

```delphi
property DataSet: TDataSet;                       // TTMSFNCDataSetFilterDialog only
property FilterText: string;                      // get/set the filter
property DisplayFilterText: string;               // TTMSFNCFilterDialog only (uses display names)
property DisplayNames: TTMSFNCFilterDialogDisplayNames;   // FieldName -> DisplayName (filled from TField.DisplayLabel)
property Options: TTMSFNCFilterDialogOptions;     // .Buttons: TTMSFNCFilterDialogButtons = set of (fdbApply, fdbCancel, fdbClear, fdbOk)
                                                  //  default [fdbApply, fdbClear, fdbCancel]; .UILanguage
property Appearance: TTMSFNCFilterDialogAppearance;
OnApplyButtonClicked, OnOKButtonClicked, OnCancelButtonClicked: procedure(Sender: TObject; AFilterBuilder: TTMSFNCFilterBuilder; var AClose: Boolean) of object;
OnClearButtonClicked: procedure(Sender: TObject; AFilterBuilder: TTMSFNCFilterBuilder; var AClear: Boolean) of object;
OnBeforeAddColumn: procedure(Sender: TObject; AField: TField; var AColumnProperties: TTMSFNCFilterBuilderColumnProperties; var AAdd: Boolean) of object;  // DataSet version
OnAfterAddColumn: procedure(Sender: TObject; AColumn: TTMSFNCFilterBuilderColumn) of object;
OnGetExpressionValues: procedure(Sender: TObject; AColumn: TTMSFNCFilterBuilderColumn; AValues: TStringList) of object;
OnGetFormatSettings, OnShowGroupEditor, OnShowExpressionEditor, OnShowCustomEditor, OnClose, OnBeforeShowForm
function Execute(AModal: Boolean = True): TModalResult;   // WEB: procedure Execute(AProc: TModalResultProc = nil; AModal: Boolean = True)
function ValidateFilterRow(AInputRow: TTMSFNCFilterValidateInputRow): Boolean;      // TArray<TTMSFNCValue>
function ValidateFilterArray(AInputArray: TTMSFNCFilterValidateInputArray): TTMSFNCFilterValidateOutputArray;
```
Behaviour from source: with `fdbOk` **not** in `Buttons`, Apply sets `mrOk` and closes; with `fdbOk` present, Apply keeps the dialog open. The DataSet version sets `DataSet.Filter`/`Filtered` on Apply/OK and restores the previous filter on Cancel **only if you do not assign** `OnApplyButtonClicked` / `OnOKButtonClicked` / `OnCancelButtonClicked` (assigning a handler replaces that default). `Execute` returns `mrAbort` without showing when there is no filter builder.

```delphi
// VCL\FilterDialog\DataSet\Biolife_ClientDataSet demo (DataSet set at design time)
procedure TForm1.FilterBtnClick(Sender: TObject);
begin
  TMSFNCDataSetFilterDialog1.FilterText := FilterTextEdit.Text;
  TMSFNCDataSetFilterDialog1.Execute;          // OK/Apply already filtered ClientDataSet1
  FilterTextEdit.Text := TMSFNCDataSetFilterDialog1.FilterText;
end;

// generic dialog in code (no dataset)
var dlg: TTMSFNCFilterDialog;
begin
  dlg := TTMSFNCFilterDialog.Create(Self);
  dlg.FilterBuilder.DataColumns.AddColumn('Name', fdtText);
  dlg.FilterBuilder.DataColumns.AddColumn('Price', fdtFloat, 'Unit price');
  if dlg.Execute = mrOk then
    Memo1.Text := dlg.FilterText;
end;
```

## TTMSFNCObjectInspector

A tree-view-based property grid for any object, or for the current record of a dataset.
```delphi
property &Object: TObject;          // public (not published) - the inspected instance; nil clears
property Mode: TTMSFNCObjectInspectorMode default oimProperties;   // public; oimAll, oimProperties, oimEvents
property DataSource: TDataSource;   // published: inspect/edit fields of the current record instead
property Designer: TComponent;      // root used to list components for component-typed properties
procedure RebuildList;
OnReadProperty: procedure(Sender: TObject; AObject: TObject; APropertyInfo: TTMSFNCPropertyInfo; APropertyName: string; APropertyType: TTypeKind; var ACanRead: Boolean) of object;
OnReadPropertyValue / OnWritePropertyValue: (... ; var APropertyValue: string; var ACanRead/ACanWrite: Boolean)
OnPropertyValueChanged: procedure(Sender: TObject; AObject: TObject; APropertyInfo: TTMSFNCPropertyInfo; APropertyName: string; APropertyType: TTypeKind; APropertyValue: string) of object;
OnReadDBField(Sender; AField: TField; var ACanRead), OnReadDBFieldValue, OnWriteDBFieldValue, OnFieldValueChanged(Sender; AField: TField; APropertyValue: string)
OnBeforeOpenObjectEditor, OnCustomizeObjectEditor
```
`TTMSFNCPropertyInfo` is declared in FNC Core `*.TMSFNCPersistence` (`PPropInfo`, on WEB `TTypeMemberProperty`); add that unit and `TypInfo` when writing these handlers.

```delphi
// VCL\Object Inspector demo
procedure TForm1.FormCreate(Sender: TObject);
begin
  FActiveControl := TTMSFNCTreeView.Create(Self);
  TTMSFNCTreeView(FActiveControl).InitSample;
  FActiveControl.Parent := Panel1;
  TMSFNCObjectInspector1.&Object := FActiveControl;
end;

// hide a property
procedure TForm1.TMSFNCObjectInspector1ReadProperty(Sender: TObject; AObject: TObject;
  APropertyInfo: TTMSFNCPropertyInfo; APropertyName: string; APropertyType: TTypeKind; var ACanRead: Boolean);
begin
  ACanRead := APropertyName <> 'Tag';
end;
```

## TTMSFNCChat

A chat-bubble list (table view) with a built-in message memo and send/attachment buttons.
```delphi
property ChatMessages: TTMSFNCChatItems;          // Add, Insert, Clear, Items[Index] (default)
property DefaultLeftItem, DefaultRightItem: TTMSFNCChatItem;   // template; AddMessage assigns DefaultRightItem only for cmlRight
property Appearance: TTMSFNCChatAppearance;       // TitleFont, StatusFont, Spacing, SideMargin, MessageStyle (cmsAll/cmsTextOnly),
                                                  // MinEntryBoxHeight, MaxEntryBoxHeight, ShowAttachmentButton
property ChatInteraction: TTMSFNCChatInteraction; // AutoScrollToBottom, AutoOpenURL, AutoReplaceLinks, MultiSelect, SendButtonTrigger (sbtClick/sbtMouseDown), LongPressInterval
property MessageTimestamp: TTMSFNCChatMessageTimestamp;  // Show (default False), Position (mtpTopLeft..mtpBottomRight), Format, Font
property ShowMessageField: Boolean default True;  property AddImagesToBitmapContainer: Boolean default True;
function AddMessage(AText: string; ALocation: TTMSFNCChatMessageLocation = cmlRight; ATriggerSendEvent: Boolean = True): TTMSFNCChatItem; overload;
function AddMessage(AText: string; ATitle: string; ALocation: TTMSFNCChatMessageLocation = cmlRight; ATriggerSendEvent: Boolean = True): TTMSFNCChatItem; overload;
function AddImage(AImagePath: string; AText: string = ''; ALocation: TTMSFNCChatMessageLocation = cmlRight; AImageWidth: Integer = 150): TTMSFNCChatItem; overload;
function AddImageWithName(AImagePath: string; AImageName: string; AText: string = ''; ...): TTMSFNCChatItem; overload;
function AddFile(AFilePath: string; AFileName: string; ATitle: string = ''; ALocation: TTMSFNCChatMessageLocation = cmlRight): TTMSFNCChatItem;
procedure Clear; procedure DisableInputControls; procedure EnableInputControls; procedure ScrollToBottom; procedure ScrollToTop;
function XYToChatItem(X, Y: Single): TTMSFNCChatItem;
property Memo: TTMSFNCChatMemo; property SendButton, AttachmentButton: TTMSFNCToolBarButton;   // public, read-only
```
`TTMSFNCChatItem` (published): `Text`, `Title`, `Status`, `StatusPosition` (cisBottomLeft/cisBottomRight), `MessageLocation` (`cmlLeft`, `cmlRight`), `MessageType` (`cmtText`, `cmtImage`, `cmtFile`), `Fill`, `Stroke`, `TextColor`, `TitleColor`, `URLColor`, `Bitmap`, `BitmapName`, `BitmapWidth/Height`, `BitmapPosition`, `Rounding`, `Corners`, `MessageIndent`; public `Timestamp: TDateTime`, `DataString/DataInteger/DataObject/DataPointer`.

Send events:
- `OnBeforeSendMessage: procedure(Sender: TObject; var AText: string; var AAllow: Boolean)` and `OnAfterSendMessage: procedure(Sender: TObject; var AItem: TTMSFNCChatItem)` fire from **every `AddMessage` with `ATriggerSendEvent = True`** (the default), including the send button.
- `OnBeforeSendButtonMessage` / `OnAfterSendButtonMessage` (same signatures) and `OnSendButtonClick: TNotifyEvent` fire only for the send button.
- Others: `OnMessageClick`, `OnMessageDblClick`, `OnMessageAnchorClick(Sender; AItem; AAnchor: String)`, `OnAttachmentButtonClick`, `OnFileDrop(Sender; AFileList: TTMSFNCChatDropFileList)` (`array of string`), `OnFileDragOver`, `OnLongPressItem`, `OnBefore/AfterDrawMessage*`.

```delphi
// VCL\Chat\Client demo (WEB\Chat\Client is the same with a TWebSocketClient)
procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCChat1.Clear;                   // remove the sample messages
  TMSFNCChat1.DisableInputControls;    // until connected
end;

procedure TForm1.TMSFNCChat1SendMessage(Sender: TObject; var AItem: TTMSFNCChatItem);  // OnAfterSendMessage
begin
  AItem.Fill.Color := gcDodgerblue;
  AItem.TextColor := gcWhite;
  AItem.TitleColor := gcWhite;
  AItem.Title := 'Me';
  SendToServer(AItem.Text);
end;

procedure TForm1.MessageReceived(const AUser, AText: string);
begin
  TMSFNCChat1.AddMessage(AText, AUser, cmlLeft, False);   // False: do NOT fire the send events again
end;
```

## Platform notes

- WEB: modal dialogs cannot block. TaskDialog `Execute(AProc)`, Find/Replace/FilterDialog `Execute(AProc, AModal)`; FontDialog only via `OnDialogResult`. The TaskDialog options `tdoAllowMinimize`/`tdoAllowDialogCancel` do not exist on WEB (compile error if used).
- FMX Android/iOS: TaskDialog `Execute` is a procedure with `ResultProc: TProc<TModalResult>`; FontDialog is shown as a popup (iOS) / async (Android).
- FilterView: FMX publishes `Fill`/`Stroke`; VCL publishes `Ctl3D`. Ancestor is `TScrollBox` (VCL/WEB) or `TVertScrollBox` (FMX).
- FilterDialog: the dataset version is desktop-only; on WEB create `TTMSFNCFilterDialog` in code and apply `FilterText` yourself.
- Chat (VCL): implements `IDropTarget` for Windows file drop (`OnFileDrop`).

## Does not exist / common mistakes

- `TaskDialog.Text` / `MainInstruction` / `ExpandedInformation` / `VerificationText` / `FooterText` / `Buttons` / `Flags` (VCL `TTaskDialog` names) -> `Content`, `Instruction`, `ExpandedText`, `VerifyText`, `Footer`, `CommonButtons` + `CustomButtons`, `Options`.
- `TaskDialog.RadioButton` / `.Verified` / `.InputValue` -> `RadioButtonResult`, `VerifyResult`, `InputText`.
- `tcbClose` returning `mrClose` - it returns **`mrAbort`** (the demo's `mrClose` case never matches). Custom buttons are `100 + i`, command links `200 + i`, not `mrYes`/`100`-based-1.
- `FooterIcon := tfiInformation` - property type is `TTMSFNCTaskDialogIcon`; use `tdiInformation`.
- `if TMSFNCFontDialog1.Execute then` / `FontDialog.Font` / `FontDialog.Options` - `Execute` is a procedure; use `OnDialogResult` + `FontName/FontSize/FontColor/BoldSelected...`. Check `AModalResult = mrOk`; values change even on Cancel.
- `FindDialog.Execute` returning `Boolean`, `FindDialog.FindNext`, `FindDialog.OnReplace`, `FindDialog.Control := Memo1` -> `Execute(AModal): TModalResult`, events `OnFind`/`OnFindNext`, replace is a separate `TTMSFNCReplaceDialog`; `Control` is protected.
- ReplaceDialog `OnFind` has **no** `var AFound` parameter (FindDialog's does).
- `TTMSFNCFilterDialog` on the palette - only `TTMSFNCDataSetFilterDialog` is registered (VCL/FMX). `TTMSFNCFilterDialog` exists but must be created in code.
- `FilterDialog.ApplyFilter` / `.Columns` / `.Grid` -> set `DataSet` (dataset version) or `FilterBuilder.DataColumns.AddColumn(...)` (generic), read `FilterText`.
- Assigning `OnOKButtonClicked`/`OnApplyButtonClicked` on `TTMSFNCDataSetFilterDialog` and expecting the dataset to still be filtered - your handler replaces the default; set `DataSet.Filter`/`Filtered` yourself.
- `FilterView.DataSet` / `ApplyFilter` / `OnFilterChanged` / `Filter` -> handle `OnFilterTextChanged` and assign `AFilterText` to your dataset. `feoNotContains`, `feoGreaterThan`, `feoLessThan` do not exist (`feoLargerThan`, `feoSmallerThan`, `...OrEqual`). `TTMSFNCFilterViewPanel.AddText` -> `AddLabel` (the view itself has `AddText`).
- `ObjectInspector.SelectedObject` / `.Inspect(obj)` / `.InspectedObject` / `.Instance` / `.TIObject` / `.ShowEvents` -> `&Object := obj` and `Mode := oimEvents` / `oimAll` (both public, not settable in the Object Inspector at design time).
- `Chat.Messages` / `Chat.Items` / `AddItem` / `SendMessage` / `OnSend` / `OnMessageSent` / `OnMessageReceived` -> `ChatMessages`, `AddMessage`, `OnAfterSendMessage` / `OnAfterSendButtonMessage`; incoming messages: `AddMessage(Text, Title, cmlLeft, False)`.
- Calling `AddMessage(s)` for an incoming message with the default `ATriggerSendEvent = True` -> your `OnAfterSendMessage` re-sends it (echo loop).
- `cmlLeft` items do not get `DefaultLeftItem` styling from `AddMessage` (source only assigns `DefaultRightItem` for `cmlRight`); style the returned item yourself.
