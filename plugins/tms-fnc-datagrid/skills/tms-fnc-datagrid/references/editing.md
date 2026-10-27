# TMS FNC DataGrid – editing, AutoFill, clipboard

Verified against `*.TMSFNCDataGridRenderer.pas`, `*.TMSFNCDataGrid.pas`, `*.TMSFNCDataGridData.pas`
and the Basic `Editing` and `AutoFill` demos (VCL/FMX/WEB). Units: see core-api.md.
Editor enums and editor classes are in `*.TMSFNCDataGridRenderer`.

## Enabling editing

Editing is **on by default**: `Options.Editing.Enabled` defaults to `True`.

```delphi
// Options.Editing: TTMSFNCDataGridEditingOptions
property Enabled: Boolean default True;          // False = whole grid read-only
property AutoComplete: TTMSFNCDataGridAutoCompleteOptions;  // &Type, CaseSensitive, Items: TStringList
property DirectDropDown: Boolean default False;  // combo/date editors open their drop-down immediately
```
`TTMSFNCDataGridAutoCompleteType = (gactDisabled, gactNormal, gactLookupList)`.

How editing starts:
- F2, Enter, or typing a character on the focused cell.
- `Options.Mouse.DirectEdit := True` makes a single click enter edit mode (default False).
- Keyboard chaining (`Options.Keyboard`): `EnterKeyDirectEdit`, `TabKeyDirectEdit`, `ArrowKeyDirectEdit`
  (all default False) re-open the editor in the next cell. `EnterKeyHandling: TTMSFNCDataGridEnterKeyHandling`
  (default `gekhNone`) picks where focus goes after Enter: `gekhNextColumn, gekhNextRow, gekhNextColumnInRow,
  gekhNextRowInColumn, gekhNextColumnAndAppend, gekhNextRowAndAppend, gekhNextRowAndColumnAppend,
  gekhNextColumnAndRowAppend`.
- Other keyboard options: `TabKeyHandling` (`gtkhNextControl, gtkhNextCell, gtkhMixed`; default
  `gtkhMixed`), `TabKeyDirection` (`gtkdNextColumnCell, gtkdNextRowCell`), `InsertKeyHandling`
  (`gikhNone, gikhInsertRowBefore, gikhInsertRowAfter`), `DeleteKeyHandling` (`gdkhNone, gdkhDeleteRow,
  gdkhClearSelectedCells`), `AppendRowOnArrowKeyDown`, `AppendColumnOnArrowKeyRight`.

Demo setup:
```delphi
TMSFNCDataGrid1.Options.Keyboard.TabKeyDirectEdit := True;
TMSFNCDataGrid1.Options.Keyboard.ArrowKeyDirectEdit := True;
TMSFNCDataGrid1.Options.Keyboard.EnterKeyDirectEdit := True;
```

Read-only control:
```delphi
property ReadOnlys[AColumn, ARow: Integer]: Boolean;        // per cell
Grid.Columns[2].AddSetting(gcsReadOnly);                     // per column: setting is REQUIRED in code
Grid.Columns[2].&ReadOnly := True;
// or per cell with an event:
OnCanEditCell: procedure(Sender: TObject; AColumn, ARow: Integer; var ACanEdit: Boolean) of object;
```
`OnCanEditCell` runs before keyboard-started edits (F2, Enter, typing).

Programmatic control:
```delphi
procedure EditCell(ACell: TTMSFNCDataGridCellCoord; ACellStart: TTMSFNCDataGridEditCellStart = gcsNone;
  AInsertKey: Boolean = False; AValue: string = ''; AKey: Word = 0); virtual;
function StopEditing: Boolean;      // commit
function CancelEditing: Boolean;    // discard
function IsEditing: Boolean;
property EditingCell: TTMSFNCDataGridCellCoord;   // read-only
```
`TTMSFNCDataGridEditCellStart = (gcsNone, gcsStart, gcsEnd)` sets where the caret starts.
Its values clash by name with the column setting values (`gcsEditor`...), but they are different enums.

```delphi
TMSFNCDataGrid1.FocusedCell := MakeCell(2, 5);
TMSFNCDataGrid1.EditCell(MakeCell(2, 5), gcsEnd);
```

## Editor types

```delphi
TTMSFNCDataGridInplaceEditorType = (getNone, getEdit, getNumericEdit, getSignedNumericEdit, getFloatEdit,
  getSignedFloatEdit, getUppercaseEdit, getMixedCaseEdit, getLowerCaseEdit, getMoneyEdit, getHexEdit,
  getAlphaNumericEdit, getValidCharsEdit, getComboBox, getComboEdit, getSpinBox, getDatePicker,
  getColorPicker, getTrackBar, getMemo, getHTMLEditor, getCustom, getTimePicker);
TTMSFNCDataGridInplaceEditorTarget = (getCellValue, getFillColor);   // getFillColor edits Layouts[c,r].Fill.Color
```

Editor control classes (cast `AInplaceEditor` to these):

| Editor type | Class | VCL / WEB base | FMX base |
|---|---|---|---|
| text/numeric edits | `TTMSFNCDataGridEdit` | `TTMSFNCEdit` | `TTMSFNCEdit` |
| `getComboBox` | `TTMSFNCDataGridComboBox` | `TComboBox` | `TComboBox` |
| `getComboEdit` | `TTMSFNCDataGridComboEdit` | `TComboBox` | `TComboEdit` |
| `getSpinBox` | `TTMSFNCDataGridSpinBox` | `TSpinEdit` | `TSpinBox` |
| `getDatePicker` | `TTMSFNCDataGridDatePicker` | `TDateTimePicker` | `TDateEdit` |
| `getTimePicker` | `TTMSFNCDataGridTimePicker` | `TDateTimePicker` | `TTimeEdit` |
| `getTrackBar` | `TTMSFNCDataGridTrackBar` | `TTrackBar` | `TTrackBar` |
| `getMemo` | `TTMSFNCDataGridMemo` | `TMemo` | `TMemo` |
| `getColorPicker` | `TTMSFNCDataGridColorPicker` | `TTMSFNCColorPicker` | same |
| `getHTMLEditor` | `TTMSFNCDataGridHTMLEditor` | `TTMSFNCHTMLEditor` | same |

`TTMSFNCDataGridInplaceEditor` is `TWinControl` in VCL/WEB and `TControl` in FMX.

### Per-column editors (Editing demo)

**At runtime you must `AddSetting` for each column property you set**, or the grid ignores it.

```delphi
TMSFNCDataGrid1.Columns[1].AddSetting(gcsEditor);
TMSFNCDataGrid1.Columns[1].AddSetting(gcsEditorItems);
TMSFNCDataGrid1.Columns[1].Editor := getComboBox;
TMSFNCDataGrid1.Columns[1].EditorItems.Add('Mercedes');
TMSFNCDataGrid1.Columns[1].EditorItems.Add('Audi');

TMSFNCDataGrid1.Columns[3].AddSetting(gcsEditor);
TMSFNCDataGrid1.Columns[3].Editor := getTrackBar;

TMSFNCDataGrid1.Columns[4].AddSetting(gcsEditor);
TMSFNCDataGrid1.Columns[4].Editor := getDatePicker;
TMSFNCDataGrid1.Columns[4].AddSetting(gcsFormatting);
TMSFNCDataGrid1.Columns[4].Formatting.&Type := gdftDateTime;

TMSFNCDataGrid1.Columns[5].AddSetting(gcsEditor);
TMSFNCDataGrid1.Columns[5].Editor := getColorPicker;
TMSFNCDataGrid1.Columns[5].AddSetting(gcsEditorTarget);
TMSFNCDataGrid1.Columns[5].EditorTarget := getFillColor;   // edits the cell background colour

TMSFNCDataGrid1.Columns[6].AddSetting(gcsEditor);
TMSFNCDataGrid1.Columns[6].Editor := getSpinBox;
```

### Per-cell editors and editor tweaks via events

```delphi
OnGetInplaceEditorType: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  var AInplaceEditorType: TTMSFNCDataGridInplaceEditorType) of object;
OnGetInplaceEditorTarget: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  var AInplaceEditorTarget: TTMSFNCDataGridInplaceEditorTarget) of object;
OnGetInplaceEditorClass: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  var AInplaceEditorClass: TTMSFNCDataGridInplaceEditorClass) of object;   // used with getCustom
OnGetInplaceEditorProperties: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AInplaceEditor: TTMSFNCDataGridInplaceEditor; AInplaceEditorType: TTMSFNCDataGridInplaceEditorType) of object;
```

```delphi
procedure TForm1.TMSFNCDataGrid1GetInplaceEditorType(Sender: TObject;
  ACell: TTMSFNCDataGridCellCoord; var AInplaceEditorType: TTMSFNCDataGridInplaceEditorType);
begin
  if ACell.Column = 3 then
    AInplaceEditorType := getFloatEdit;
end;

procedure TForm1.TMSFNCDataGrid1GetInplaceEditorProperties(Sender: TObject;
  ACell: TTMSFNCDataGridCellCoord; AInplaceEditor: TTMSFNCDataGridInplaceEditor;
  AInplaceEditorType: TTMSFNCDataGridInplaceEditorType);
begin
  if AInplaceEditorType = getTrackBar then
    (AInplaceEditor as TTMSFNCDataGridTrackBar).Max := 3000;   // from the Editing demo
end;
```

Custom editor control: return `getCustom` from `OnGetInplaceEditorType` and the class from
`OnGetInplaceEditorClass`. The grid moves values in and out of an editor through RTTI (for example
the `Text`, `Value` or `Time` property). For a control it can't handle, move the value yourself with:
```delphi
OnBeforeInplaceEditorSetValue: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AInplaceEditor: TTMSFNCDataGridInplaceEditor; var AValue: TTMSFNCDataGridCellValue;
  var AHandled: Boolean) of object;   // cell -> editor; set AHandled := True after writing it
OnBeforeInplaceEditorGetValue: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AInplaceEditor: TTMSFNCDataGridInplaceEditor; var AValue: TTMSFNCDataGridCellValue;
  var AHandled: Boolean) of object;   // editor -> cell; fill AValue, AHandled := True
```
`OnAfterInplaceEditorSetValue` and `OnAfterInplaceEditorGetValue` take
`(Sender; ACell; AInplaceEditor; AValue: TTMSFNCDataGridCellValue)`.

## Edit lifecycle and validation (verified call order)

Opening:
1. `OnGetInplaceEditorTarget`, `OnGetInplaceEditorType`
2. `OnBeforeOpenInplaceEditor(Sender; ACell; var AValue; var ACanOpen: Boolean)`
3. `OnGetInplaceEditorClass` (only for `getCustom`)
4. `OnGetInplaceEditorProperties`
5. `OnCellEditGetData(Sender; ACell; AInplaceEditor; var AValue)`: change the value shown in the editor
6. `OnBeforeInplaceEditorSetValue`, then `OnAfterInplaceEditorSetValue`
7. `OnAfterOpenInplaceEditor(Sender; ACell; AInplaceEditor; AValue)`

Closing:
1. `OnBeforeInplaceEditorGetValue`, then `OnAfterInplaceEditorGetValue`
2. `OnBeforeCloseInplaceEditor(Sender; ACell; AInplaceEditor; ACancelled: Boolean; var AValue; var ACanClose: Boolean)`
3. If not cancelled: `OnCellEditValidateData(Sender; ACell; AInplaceEditor; var AValue; var AValid: Boolean)`.
   **`AValid := False` keeps the editor open with focus**, and nothing is committed.
4. `OnCellEditSetData(Sender; ACell; AInplaceEditor; var AValue)`: last chance to change the value
   before it's written to `Cells[]` (or to `Layouts[].Fill.Color` for `getFillColor`)
5. `OnAfterCloseInplaceEditor(Sender; ACell; ACancel: Boolean; AValue)`: use this as the
   "cell edited" notification

`OnBeforeExitInplaceEditor(...; var AExitMode: TTMSFNCDataGridInplaceEditorExitMode)` and
`OnAfterExitInplaceEditor(...; AExitMode)` use `(gieeIgnoreEditing, gieeStopEditing, gieeCancelEditing)`.

Validation example (cross-platform, because `AValue` is `TValue` in VCL/FMX and `JSValue` in WEB):
```delphi
procedure TForm1.TMSFNCDataGrid1CellEditValidateData(Sender: TObject;
  ACell: TTMSFNCDataGridCellCoord; AInplaceEditor: TTMSFNCDataGridInplaceEditor;
  var AValue: TTMSFNCDataGridCellValue; var AValid: Boolean);
var
  d: Double;
begin
  if ACell.Column = 3 then
    AValid := TryStrToFloat(TMSFNCDataGrid1.ValueToString(AValue), d) and (d >= 0);
end;

procedure TForm1.TMSFNCDataGrid1AfterCloseInplaceEditor(Sender: TObject;
  ACell: TTMSFNCDataGridCellCoord; ACancel: Boolean; AValue: TTMSFNCDataGridCellValue);
begin
  if not ACancel then
    StatusBar1.SimpleText := 'Edited ' + ACell.ToString;
end;
```

## AutoFill (Excel-style fill handle)

AutoFill is a selection feature. Turn it on with a range selection mode, then drag the small handle at the
selection corner:
```delphi
TMSFNCDataGrid1.Options.Selection.Mode := gsmCellRange;
TMSFNCDataGrid1.Options.Selection.AutoFill := True;     // default False
```
It continues number, float, date, time and weekday sequences, `ITEM-001`-style codes, and registered
custom lists. Handle and preview look: `AutoFillAppearance` (`HandleFill`, `HandleStroke`,
`HandleSize`, `PreviewFill`, `PreviewStroke`).

API:
```delphi
procedure AutoFill(const ASourceStart: TTMSFNCDataGridCellCoord; const ASourceEnd: TTMSFNCDataGridCellCoord;
  const ATargetStart: TTMSFNCDataGridCellCoord; const ATargetEnd: TTMSFNCDataGridCellCoord;
  const ADirection: TTMSFNCDataGridDataAutoFillDirection = gafdAuto);
// TTMSFNCDataGridDataAutoFillDirection = (gafdAuto, gafdDown, gafdUp, gafdRight, gafdLeft)
procedure AutoFillCustomListSet(const AKey: string; const AValues: array of string);
procedure AutoFillCustomListRemove(const AKey: string);
procedure AutoFillCustomListsClear;
function AutoFillCustomListTryGet(const AKey: string; out AValues: TTMSFNCDataGridDataCustomList): Boolean;
function AutoFillCustomListsCount: Integer;
```

Events (`TTMSFNCDataGridDataValues = TArray<TTMSFNCDataGridCellValue>`):
```delphi
OnAutoFillGetCustomList: procedure(Sender: TObject; BaseValue: string; var Values: TArray<string>;
  var Handled: Boolean) of object;
OnAutoFillCalculateValue: procedure(Sender: TObject; SourceCells: TTMSFNCDataGridCellCoordRange;
  SourceValues: TTMSFNCDataGridDataValues; TargetCells: TTMSFNCDataGridCellCoordRange; FillIndex: Integer;
  Direction: TTMSFNCDataGridDataAutoFillDirection; var NewValue: TTMSFNCDataGridCellValue;
  var Handled: Boolean) of object;
OnBeforeApplyAutoFill: procedure(Sender: TObject; SourceCells: TTMSFNCDataGridCellCoordRange;
  SourceValues: TTMSFNCDataGridDataValues; TargetCells: TTMSFNCDataGridCellCoordRange;
  TargetCell: TTMSFNCDataGridCellCoord; Direction: TTMSFNCDataGridDataAutoFillDirection;
  var NewValue: TTMSFNCDataGridCellValue; var Accept: Boolean) of object;
OnAfterApplyAutoFill: procedure(Sender: TObject; SourceCells: TTMSFNCDataGridCellCoordRange;
  SourceValues: TTMSFNCDataGridDataValues; TargetCells: TTMSFNCDataGridCellCoordRange;
  TargetCell: TTMSFNCDataGridCellCoord; Direction: TTMSFNCDataGridDataAutoFillDirection;
  OldValue, NewValue: TTMSFNCDataGridCellValue) of object;
```
These event parameters have **no `A` prefix** (`BaseValue`, `NewValue`, `Handled`), unlike most
other grid events.

```delphi
TMSFNCDataGrid1.AutoFillCustomListSet('StatusList', ['TODO', 'In Progress', 'Review', 'Done']);
// fill rows 3..19 of column 0 from the pattern in rows 1..2
TMSFNCDataGrid1.AutoFill(MakeCell(0, 1), MakeCell(0, 2), MakeCell(0, 1), MakeCell(0, 19));

procedure TForm1.TMSFNCDataGrid1AutoFillGetCustomList(Sender: TObject; BaseValue: string;
  var Values: TArray<string>; var Handled: Boolean);
begin
  if SameText(BaseValue, 'Sales') then
  begin
    Values := TArray<string>.Create('Sales', 'Marketing', 'Engineering', 'Support', 'HR');
    Handled := True;
  end;
end;
```

## Clipboard

```delphi
// Options.Clipboard: TTMSFNCDataGridClipboardOptions
property Enabled: Boolean default True;            // enables the keyboard shortcuts
property AllowRowGrow: Boolean default False;       // paste adds rows if needed
property AllowColumnGrow: Boolean default False;    // paste adds columns if needed
property IgnoreReadOnly: Boolean default False;
property PasteAction: TTMSFNCDataGridClipboardPasteAction default gpaReplace;  // gpaReplace, gpaInsert

procedure CopyToClipboard(ASelectedCells: Boolean = True);  // False = whole grid incl. fixed cells
procedure CutToClipboard(ASelectedCells: Boolean = True);   // copy, then clear
procedure PasteFromClipboard;                               // tab-delimited text at FocusedCell
```
Shortcuts when `Options.Clipboard.Enabled` is True and no cell is being edited: Ctrl+C / Ctrl+Insert
copy, Ctrl+X / Ctrl+Delete cut, Ctrl+V / Shift+Insert paste. On FMX, Cmd works in place of Ctrl.
Ctrl+A selects all cells. Ctrl+F and Ctrl+H open the find and replace dialogs (controlled by
`Options.Keyboard.FindShortcut` and `ReplaceShortcut`).

Events: `OnBeforeCopyToClipboard`, `OnBeforeCutToClipboard`, `OnBeforePasteFromClipboard`:
`procedure(Sender: TObject; var ACanExecute: Boolean) of object`.
`OnAfterCopyToClipboard`, `OnAfterCutToClipboard`, `OnAfterPasteFromClipboard`:
`procedure(Sender: TObject) of object`.
Delete-key clearing (`Options.Keyboard.DeleteKeyHandling := gdkhClearSelectedCells`) fires
`OnBeforeClearSelectedCells(Sender; ASelection: TTMSFNCDataGridCellCoordRange; var ACanClear: Boolean)`
and `OnAfterClearSelectedCells(Sender; ASelection)`.

There is no undo/redo in the grid.

## Does not exist / common mistakes

| Wrong | Use instead |
|---|---|
| `Options := [goEditing]`, `Options.Editing := True`, `ReadOnly := False` on grid | editing is on by default; `Options.Editing.Enabled` |
| `Columns[i].Editor := getComboBox` alone (runtime) | also `Columns[i].AddSetting(gcsEditor)` (+ `gcsEditorItems` for `EditorItems`) |
| `Columns[i].ReadOnly := True` alone (runtime) | `AddSetting(gcsReadOnly)` first |
| `OnGetEditorType`, `OnGetEditorProp`, `edComboList`, `edSpinEdit` (TAdvStringGrid) | `OnGetInplaceEditorType`, `OnGetInplaceEditorProperties`, `getComboBox`, `getSpinBox` |
| `OnCellValidate`, `OnEditCellDone`, `OnCellChanged`, `OnCellValueChanged` | `OnCellEditValidateData` (`AValid`), `OnAfterCloseInplaceEditor`, `OnCellEditSetData` |
| `ShowInplaceEdit`, `EditMode := True`, `StartEdit` | `EditCell(MakeCell(c, r))` |
| `HideInplaceEdit`, `EndEdit` | `StopEditing` / `CancelEditing` (functions returning Boolean) |
| `AValue.AsString` in WEB | `AValue` is `JSValue` there; use `Grid.ValueToString(AValue)` |
| `Options.AutoFill` / `Options.Editing.AutoFill` | `Options.Selection.AutoFill` with a range `Options.Selection.Mode` |
| `Undo` / `Redo` | not available |
| `AEditor as TEdit` / `TDateTimePicker` in FMX | FMX editors are `TTMSFNCDataGridEdit` (TTMSFNCEdit), `TDateEdit`, `TSpinBox`, ... (table above) |
