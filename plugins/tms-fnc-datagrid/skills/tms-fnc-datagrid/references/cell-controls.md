# Cell controls and Grid in Grid (TTMSFNCDataGrid)

Three mechanisms, all per cell (or per column):
1. **Built-in cell types** — checkbox, radio button, button, progress bar, bitmap, created with `Add*` methods (or `Columns[i].Type`). The grid draws them itself; each has its own cell class.
2. **Any framework control** — assign it to `Controls[Col, Row]`.
3. **Nested grid** — `AddGrid` puts a full `TTMSFNCDataGridRenderer` inside a cell.

## 1. Built-in cell types

```delphi
procedure AddCheckBox(AColumn, ARow: Integer; AValue: Boolean = False); overload;        // + (ACell: TTMSFNCDataGridCellCoord; ...)
procedure AddCheckBoxColumn(AColumn: Integer; AValue: Boolean = False);
procedure AddDataCheckBox(AColumn, ARow: Integer); overload;
procedure AddDataCheckBoxColumn(AColumn: Integer);
procedure AddRadioButton(AColumn, ARow: Integer; AValue: Boolean = False; AGroupIndex: Integer = 0); overload;
procedure AddRadioButtonColumn(AColumn: Integer; AValue: Boolean = False; AGroupIndex: Integer = 0);
procedure AddDataRadioButton(AColumn, ARow: Integer; AValue: Boolean = False; AGroupIndex: Integer = 0); overload; // AValue unused
procedure AddDataRadioButtonColumn(AColumn: Integer; AValue: Boolean = False; AGroupIndex: Integer = 0);
procedure AddButton(AColumn, ARow: Integer; AText: string = ''); overload;
procedure AddButtonColumn(AColumn: Integer; AText: string = '');
procedure AddProgressBar(AColumn, ARow: Integer; AValue: Integer = 0); overload;
procedure AddProgressBarColumn(AColumn: Integer; AValue: Integer = 0);
procedure AddDataProgressBar(AColumn, ARow: Integer); overload;
procedure AddDataProgressBarColumn(AColumn: Integer);
procedure AddBitmap(AColumn, ARow: Integer; ABitmap: TTMSFNCBitmap); overload;
procedure AddBitmap(AColumn, ARow: Integer; AName: string); overload;     // name in BitmapContainer
procedure AddBitmapColumn(AColumn: Integer; ABitmap: TTMSFNCBitmap); overload;
procedure AddBitmapColumn(AColumn: Integer; AName: string); overload;
// Remove: RemoveCheckBox, RemoveDataCheckBox, RemoveRadioButton, RemoveDataRadioButton,
//         RemoveButton, RemoveProgressBar, RemoveBitmap  (AColumn, ARow) / (ACell)
```
Every `Add*(AColumn, ARow ...)` also has an `(ACell: TTMSFNCDataGridCellCoord ...)` overload. `*Column` variants cover the rows between the fixed top and fixed bottom rows.

**"Data" vs plain variants** (key distinction):
- `AddCheckBox` / `AddRadioButton`: checked state stored **separately** from the cell value; read/write via `Booleans[C, R]`.
- `AddDataCheckBox` / `AddDataRadioButton`: state **follows the cell value** (use for Boolean data / dataset fields).
- `AddProgressBar`: position stored separately in `ProgressValue[C, R]: Integer`.
- `AddDataProgressBar`: position is the numeric cell value (`Ints[C, R]`).

Events (`TTMSFNCDataGridCellClickEvent = procedure(Sender: TObject; AColumn, ARow: Integer) of object`):
`OnCellCheckBoxChange`, `OnCellRadioButtonChange`, `OnCellButtonClick` (also `OnCellClick`, `OnCellDblClick`, `OnCellRightClick`).

Demo (Basic\Cell Controls):
```delphi
TMSFNCDataGrid1.AddDataProgressBar(0, 5);
TMSFNCDataGrid1.Ints[0, 5] := 25;              // data progress bar reads the cell value
TMSFNCDataGrid1.AddDataCheckBoxColumn(5);
TMSFNCDataGrid1.AddRadioButtonColumn(6);
for I := 0 to TMSFNCDataGrid1.RowCount - 1 do
  TMSFNCDataGrid1.Booleans[5, I] := Boolean(RandomRange(-1, 1));
```

Column-level cell type: `Columns[i].Type: TTMSFNCDataGridCellItemType` = `gcitNormal, gcitCheckBox, gcitRadioButton, gcitDataCheckBox, gcitDataRadioButton, gcitButton, gcitProgressBar, gcitDataProgressBar, gcitBitmap`, with `Columns[i].TypeRange` = `gcirNormal` (default, between fixed rows), `gcirFixed`, `gcirAll`. Column properties only override cells when the matching setting is in `Columns[i].Settings` — at **runtime** add it yourself (it is only auto-added at design time):

```delphi
TMSFNCDataGrid1.Columns[3].AddSetting(gcsType);
TMSFNCDataGrid1.Columns[3].&Type := gcitDataCheckBox;
// same pattern for the editor (Grid in Grid demo):
TMSFNCDataGrid1.Columns[2].AddSetting(gcsEditor);
TMSFNCDataGrid1.Columns[2].Editor := getHTMLEditor;
```
`TTMSFNCDataGridColumnSetting = (gcsAppearance, gcsType, gcsEditor, gcsEditorTarget, gcsEditorItems, gcsReadOnly, gcsFormatting, gcsControlText, gcsControlWidth, gcsControlHeight, gcsControlAlign, gcsControlPosition, gcsControlMargins, gcsFilterButton, gcsFilterEditor, gcsFilterEditorType, gcsFilterDefaultType)`. Column control props: `ControlAlign, ControlPosition, ControlWidth, ControlHeight, ControlMargins, ControlText`.

Inplace editors (combo, date picker, spin, memo, HTML...) are **editors**, not cell controls: `TTMSFNCDataGridInplaceEditorType` = `getNone, getEdit, getNumericEdit, ..., getComboBox, getComboEdit, getSpinBox, getDatePicker, getColorPicker, getTrackBar, getMemo, getHTMLEditor, getCustom, getTimePicker` (see editing docs; `Columns[i].Editor`, `EditorItems`, `OnGetInplaceEditorType`).

## 2. Arbitrary controls: Controls[Col, Row]

```delphi
property Controls[AColumn, ARow: Integer]: TTMSFNCDataGridCellControl;
property ControlAligns[AColumn, ARow: Integer]: TTMSFNCDataGridCellControlAlign;      // gcaNone, gcaLeft, gcaTop, gcaRight, gcaBottom, gcaClient
property ControlPositions[AColumn, ARow: Integer]: TTMSFNCDataGridCellControlPosition; // gcpTopLeft, gcpTopCenter, gcpTopRight, gcpCenterLeft, gcpCenterCenter, gcpCenterRight, gcpBottomLeft, gcpBottomCenter, gcpBottomRight
property ControlWidths[AColumn, ARow: Integer]: Integer;   property ControlHeights[AColumn, ARow: Integer]: Integer;
property ControlWidthsDIP / ControlHeightsDIP [AColumn, ARow: Integer]: Integer;
property ControlMargins[AColumn, ARow: Integer]: TTMSFNCMargins;   // read-only object
property ControlTexts[AColumn, ARow: Integer]: string;
```
`ControlPositions` applies when `ControlAligns` is `gcaNone`.

**Type per platform** (`*.TMSFNCDataGridCell`):
- FMX: `TTMSFNCDataGridCellControl = TControl` (any FMX control, e.g. `TButton` with `.Text`).
- VCL and WEB: `TTMSFNCDataGridCellControl = TWinControl` — `TLabel`, `TImage`, `TShape` (TGraphicControl) cannot be assigned. WEB demos use `TWebButton`.

Ownership: the grid does **not** own or free the control (setter sets `Parent := nil` and stores the reference; the grid parents it into an internal wrapper while shown). Create it with an owner (`TButton.Create(Self)`) or free it yourself. Assigning another control/nil un-parents the old one.

Controls not shown live are painted from a **cached bitmap**. Cache key = class, size, Text/Caption, focus, `Tag`, plus names you list in `OnGetCellControlExtraProperties(Sender; AColumn, ARow: Integer; AControl: TControl; var AExtraProperties: TArray<string>)`. If a custom control's look changes through another property and the cell does not repaint correctly, add that property name there. `OnGetCellSupportsRealControl(Sender; AColumn, ARow: Integer; AControl: TControl; var ASupportsRealControl: Boolean)` forces live vs bitmap for application controls. Export (PDF/print) always uses bitmaps.

Demo:
```delphi
TMSFNCDataGrid1.RowHeights[1] := 100;
b := TButton.Create(Self);
b.Caption := 'Left';
TMSFNCDataGrid1.Controls[0, 1] := b;
TMSFNCDataGrid1.ControlAligns[0, 1] := gcaLeft;

b := TButton.Create(Self);
b.Caption := 'Center Center';
TMSFNCDataGrid1.Controls[1, 3] := b;
TMSFNCDataGrid1.ControlPositions[1, 3] := gcpCenterCenter;
```

Updating a control per repaint — `OnGetCellProperties(Sender: TObject; ACell: TTMSFNCDataGridCell)`; `ACell.Control` is the assigned control (Grid in Grid demo flips button captions by node state):
```delphi
procedure TForm1.TMSFNCDataGrid1GetCellProperties(Sender: TObject; ACell: TTMSFNCDataGridCell);
var c: TControl;
begin
  c := ACell.Control;
  if Assigned(c) and (c is TButton) then
    case TMSFNCDataGrid1.RowNodeState[c.Tag] of
      grnsCollapsed: TButton(c).Caption := 'Expand';     // FMX: .Text
      grnsExpanded:  TButton(c).Caption := 'Collapse';
    end;
end;
```

Cell class helpers on `TTMSFNCDataGridCell` (class helper): `IsCheckBoxCell / AsCheckBoxCell`, `IsRadioButtonCell`, `IsButtonCell / AsButtonCell` (`.Button: TButton`, `.OnClick`), `IsProgressBarCell`, `IsBitmapCell`, `IsNodeCell`, `IsCheckedCell`, `IsFNCButtonCell / AsFNCButtonCell` (`.Button: TTMSFNCButton`). `TTMSFNCDataGridFNCButtonCell` (styleable TMS button) is never chosen automatically: return it from `OnGetCellClass(Sender; AColumn, ARow: Integer; var ACellClass: TTMSFNCDataGridCellClass)` and assign `AsFNCButtonCell.OnClick` in `OnGetCellProperties`.

## 3. Grid in Grid (nested / detail grids)

```delphi
function AddGrid(AColumn, ARow: Integer): TTMSFNCDataGridRenderer; overload;
function AddGrid(ACell: TTMSFNCDataGridCellCoord): TTMSFNCDataGridRenderer; overload;
property Grids[AColumn, ARow: Integer]: TTMSFNCDataGridRenderer;   // read-only
procedure RemoveGrid(AColumn, ARow: Integer); overload;   // + (ACell)
```
- Returns the existing renderer if the cell already hosts one; `nil` for an invalid cell.
- The nested renderer is **owned by the cell — never free it**; use `RemoveGrid`.
- It is a full renderer (same data/appearance API as the grid: `ColumnCount`, `Cells`, `LoadSampleData`, `LoadFromCSVData`, `Options`, `CellAppearance`, `ConditionalFormatting`...). It is not a separate `TTMSFNCDataGrid` control and has no own scrollbars component.
- Give it room: set `RowHeights` and/or merge the host cell (`MergeCells`).

Simple (Cell Controls demo):
```delphi
TMSFNCDataGrid1.MergeCells(2, 9, 4, 5);
g := TMSFNCDataGrid1.AddGrid(2, 9);
g.ColumnCount := 10;
g.LoadSampleData;
```

Master/detail with expandable rows (Advanced\Grid in Grid demo, condensed): a manual node row whose children contain the nested grid.

```delphi
for I := 0 to 9 do
begin
  TMSFNCDataGrid1.AddRow;
  nr := TMSFNCDataGrid1.RowCount - 1;                   // node (master) row
  TMSFNCDataGrid1.Cells[0, nr] := (I + 1).ToString;
  b := TButton.Create(Self);
  b.OnClick := DoCollapse;                              // DoCollapse: ToggleNode((Sender as TButton).Tag)
  b.Tag := nr;
  TMSFNCDataGrid1.Controls[1, nr] := b;

  TMSFNCDataGrid1.AddRow;
  idx := TMSFNCDataGrid1.RowCount - 1;                  // first detail row
  g := TMSFNCDataGrid1.AddGrid(1, idx);
  g.LoadSampleData;
  g.Options.Column.Stretching.Enabled := True;
  TMSFNCDataGrid1.RowHeights[idx] := 150;
  m := idx;
  TMSFNCDataGrid1.RowCount := TMSFNCDataGrid1.RowCount + 4;
  for K := m to m + 4 do
  begin
    TMSFNCDataGrid1.AddCheckBox(3, K);
    TMSFNCDataGrid1.ControlPositions[3, K] := gcpCenterCenter;
  end;
  TMSFNCDataGrid1.MergeCells(1, m, 1, 5);               // nested grid spans 5 detail rows
  TMSFNCDataGrid1.SetNodeRow(nr, 5, 0, True);           // node row owns the 5 rows below (summary row added separately in demo)
end;
```
Node API: `AddNodeRow` / `SetNodeRow(ARow, AChildCount: Integer; ALevel: Integer = 0; AMerge: Boolean = True)` (fails with a log message if the row is already a node or a child is not a `grtDefault` row), `ClearNodeRow`, `ToggleNode`, `ExpandNode`, `CollapseNode`, `ExpandAllNodes`, `CollapseAllNodes`, `RowNodeState[]`. A summary row can be marked with `RowTypes[idx] := grtSummary` and filled with `ColumnCalculations` (see grouping.md). Styling node/summary cells in `OnGetCellLayout`:
```delphi
if TMSFNCDataGrid1.IsRowNode(ACell.Row) then
  ACell.Layout.Assign(TMSFNCDataGrid1.CellAppearance.GroupLayout)
else if TMSFNCDataGrid1.IsRowSummary(ACell.Row) then
  ACell.Layout.Assign(TMSFNCDataGrid1.CellAppearance.SummaryLayout);
```

For database master/detail, use the database adapter (see database.md), not AddGrid.

## Platform notes

- VCL: `TButton.Caption`; FMX: `TButton.Text`, `TCheckBox.IsChecked`; WEB: `TWebButton`.
- Cell control type differs (TWinControl on VCL/WEB, TControl on FMX).

## Does not exist / common mistakes

- `AddCheckBox(c, r, State, Data)` / `AddButton(c, r, W, H, Caption, HAlign, VAlign)` (TAdvStringGrid signatures) — use the signatures above.
- `AddComboBox`, `AddImage`, `AddImageIdx`, `AddProgress`, `AddRating`, `AddDetailGrid`, `SubGrid`, `DetailGrid` — do not exist. Images: `AddBitmap` (+ `BitmapContainer`); combos: inplace editor `getComboBox`; detail grid: `AddGrid`.
- `OnCheckBoxClick`, `OnButtonClick`, `OnCheckBoxChange` — use `OnCellCheckBoxChange`, `OnCellButtonClick`.
- `ColumnType` / `CellType` properties — use `Columns[i].&Type` (+ `AddSetting(gcsType)` at runtime) or `OnGetCellClass`.
- Setting `Columns[i].Type`/`Editor` at runtime without `AddSetting` — has no effect on cells.
- Reading `Booleans[]` for an `AddDataCheckBox` and expecting it independent of the cell value — data variants follow the value.
- Freeing the renderer returned by `AddGrid` — owned by the cell.
- Assigning a `TLabel`/`TImage` to `Controls[]` in VCL — needs a `TWinControl`.
