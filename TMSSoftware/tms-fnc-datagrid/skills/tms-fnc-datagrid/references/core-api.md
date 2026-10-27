# TMS FNC DataGrid – core API reference

Verified against `tms.fnc.uipack\Source\*.TMSFNCDataGrid*.pas`. The published API of
`TTMSFNCDataGrid` is identical in VCL, FMX and WEB; only unit prefixes and a few type aliases differ.

## Uses clauses

```delphi
// VCL
uses
  System.Rtti, VCL.TMSFNCTypes, VCL.TMSFNCUtils, VCL.TMSFNCGraphics, VCL.TMSFNCGraphicsTypes,
  VCL.TMSFNCCustomControl, VCL.TMSFNCDataGridBase, VCL.TMSFNCDataGridCore,
  VCL.TMSFNCDataGridData, VCL.TMSFNCDataGridCell, VCL.TMSFNCDataGridRenderer,
  VCL.TMSFNCDataGrid;

// FMX
uses
  System.Rtti, FMX.TMSFNCTypes, FMX.TMSFNCUtils, FMX.TMSFNCGraphics, FMX.TMSFNCGraphicsTypes,
  FMX.TMSFNCCustomControl, FMX.TMSFNCDataGridBase, FMX.TMSFNCDataGridCore,
  FMX.TMSFNCDataGridData, FMX.TMSFNCDataGridCell, FMX.TMSFNCDataGridRenderer,
  FMX.TMSFNCDataGrid;

// TMS WEB Core
uses
  WEBLib.TMSFNCTypes, WEBLib.TMSFNCUtils, WEBLib.TMSFNCGraphics, WEBLib.TMSFNCGraphicsTypes,
  WEBLib.TMSFNCCustomControl, WEBLib.TMSFNCDataGridBase, WEBLib.TMSFNCDataGridCore,
  WEBLib.TMSFNCDataGridData, WEBLib.TMSFNCDataGridCell, WEBLib.TMSFNCDataGridRenderer,
  WEBLib.TMSFNCDataGrid;
```

Where things are declared:
- `TTMSFNCDataGridCellCoord`, `MakeCell`, `MakeCellRange`, sort directions: `*DataGridCore`
- Filter classes, `TTMSFNCDataGridDataFormattingType`, `TTMSFNCDataGridDataFilterType`: `*DataGridData`
- `TTMSFNCDataGridCell`, `TTMSFNCDataGridCellLayout`, `TTMSFNCDataGridCellValue`: `*DataGridCell`
- Options, columns, editor enums (`getComboBox`...), selection modes: `*DataGridRenderer`

WEB demos also list the `VCL.TMSFNC*` names next to the `WEBLib.` ones because the IDE adds them for
the form designer. Keep whatever the IDE generates; code uses the `WEBLib.` units.
`System.Rtti` is needed in VCL/FMX because cell values are `TValue`.

## Class hierarchy

```
TTMSFNCCustomControl
  TTMSFNCDataGridBase            (BeginUpdate/EndUpdate, Clear, ClearData, RefreshData, Root)
    TTMSFNCCustomDataGrid        (most properties, methods, events; forwards to Root)
      TTMSFNCDataGrid            (the component you drop on a form)

TTMSFNCDataGridCore -> TTMSFNCDataGridData -> TTMSFNCDataGridRenderer   (internal engine)
```

- `Grid.Root: TTMSFNCDataGridRenderer` is the internal renderer. The grid's events are stored on
  `Root`, so **`Sender` in grid events is the `TTMSFNCDataGridRenderer`, not the `TTMSFNCDataGrid`**.
  Use the form field (`TMSFNCDataGrid1`) and don't cast `Sender` to `TTMSFNCDataGrid`.
- `Columns`, `Options`, `CellAppearance` are properties of the grid. There is no `Appearance` property.

## Key types

```delphi
TTMSFNCDataGridCellValue = TValue;      // VCL/FMX (System.Rtti)
TTMSFNCDataGridCellValue = JSValue;     // WEB

TTMSFNCDataGridCellCoord = record
  function IsEqualTo(ACell: TTMSFNCDataGridCellCoord): Boolean;
  property Column: Integer; property Row: Integer;
  property ToString: string;
  class function FromString(AValue: string): TTMSFNCDataGridCellCoord; static;
end;
TTMSFNCDataGridCellCoordRange = record
  StartCell: TTMSFNCDataGridCellCoord;
  StopCell: TTMSFNCDataGridCellCoord;
end;
function MakeCell(AColumn, ARow: Integer): TTMSFNCDataGridCellCoord;
function MakeCellRange(AStartColumn, AStartRow, AStopColumn, AStopRow: Integer): TTMSFNCDataGridCellCoordRange;
```

All indexes are 0-based and include fixed rows and columns. Row 0 is the header row by default.

Value helpers on the grid (and as class functions on `TTMSFNCDataGridData`):
`ValueToString`, `ValueToInteger`, `ValueToInt64`, `ValueToFloat`, `ValueToBoolean`
(each `(AValue)` or `(AValue; AFormatSettings: TFormatSettings)`), plus `ValueIsEmpty`, `ValueIsFloat`,
`ValueIsInteger`, `ValueIsString` and `TypeOfValue(AValue): TTypeKind`.

## Dimensions

```delphi
property ColumnCount: Integer default 4;
property RowCount: Integer default 24;             // includes fixed rows
property FixedRowCount: Integer default 1;
property FixedColumnCount: Integer default 0;      // 0 by default, not 1
property FixedBottomRowCount: Integer default 0;
property FixedRightColumnCount: Integer default 0;
property FreezeColumnCount: Integer default 0;
property FreezeRowCount: Integer default 0;
property DefaultColumnWidth: Double;
property DefaultRowHeight: Double;
property ColumnWidths[AColumn: Integer]: Double;
property RowHeights[ARow: Integer]: Double;
```

`Columns` stays in sync with `ColumnCount`: setting `ColumnCount` adds or removes column items.

## Cell data access

```delphi
property Cells[AColumn, ARow: Integer]: TTMSFNCDataGridCellValue;  // read/write, typed value
property Strings[AColumn, ARow: Integer]: string;
property Ints[AColumn, ARow: Integer]: Int64;
property Floats[AColumn, ARow: Integer]: Double;
property Booleans[AColumn, ARow: Integer]: Boolean;      // checkbox state
property Objects[AColumn, ARow: Integer]: TObject;
property StrippedCells[AColumn, ARow: Integer]: string;   // read-only, HTML stripped
property StoredCells[AColumn, ARow: Integer]: TTMSFNCDataGridCellValue; // read-only
property CellData[AColumn, ARow: Integer]: TTMSFNCDataGridCellItem;     // read-only
property ReadOnlys[AColumn, ARow: Integer]: Boolean;
property Hints[AColumn, ARow: Integer]: string;
property Comments[AColumn, ARow: Integer]: string;
```

```delphi
Grid.Cells[1, 1] := 'Audi';          // string, Integer, Double, TDateTime all work (TValue/JSValue)
Grid.Cells[2, 1] := 42;
s := Grid.Strings[1, 1];             // use Strings/Floats/Ints to read typed values
```

There is no `Values[]`, `ColCount` or `Rows[]`/`Cols[]` TStrings property.

## Structure and update methods

```delphi
procedure BeginUpdate; override;   procedure EndUpdate; override;
procedure Clear; virtual;          // blank state: data AND row/column metadata
procedure ClearData; virtual;      // data only, keeps structure
procedure ClearCells(ACellRange: TTMSFNCDataGridCellCoordRange);
procedure ClearColumns;
procedure AddRow;                  procedure AddColumn;      // append at end, no params
procedure InsertRow(ARow: Integer);  procedure InsertRows(ARow, ACount: Integer); virtual;
procedure DeleteRow(ARow: Integer);  procedure DeleteRows(ARow, ACount: Integer);
procedure InsertColumn(AColumn: Integer); procedure InsertColumns(AColumn, ACount: Integer);
procedure DeleteColumn(AColumn: Integer); procedure DeleteColumns(AColumn, ACount: Integer);
procedure MoveRow(AFromRow, AToRow: Integer); procedure SwapRows(AFromRow, AToRow: Integer);
procedure MoveColumn(AFromColumn, AToColumn: Integer); procedure SwapColumns(AFromColumn, AToColumn: Integer);
procedure HideRow(ARow: Integer); procedure UnhideRow(ARow: Integer); procedure UnhideAllRows;
procedure HideColumn(AColumn: Integer); procedure UnhideColumn(AColumn: Integer); procedure UnhideAllColumns;
procedure AutoNumberColumn(AColumn: Integer; AStartRow: Integer = 0; AStartValue: Integer = 0);
procedure LinearFill(ADoFixed: Boolean = False);   procedure RandomFill(ADoFixed: Boolean = False; ARandomNumber: Integer = 100);
procedure LoadSampleData;
procedure AutoSizeColumn(AColumn: Integer; const AMode: TTMSFNCDataGridAutoSizeMode = gamAllCells; const APadding: Integer = 5);
procedure AutoSizeColumns(const AMode: TTMSFNCDataGridAutoSizeMode = gamAllCells; const APadding: Integer = 5);
procedure AutoSizeRows(const AMode: TTMSFNCDataGridAutoSizeMode = gamAllCells; const APadding: Integer = 5);
procedure RefreshData(AUpdate: Boolean = True); overload; virtual;  // invalidate cached display values
function ColumnByName(AName: string): TTMSFNCDataGridColumn;
function ColumnByHeader(AHeader: string): TTMSFNCDataGridColumn;
function ColumnIndexByName(AName: string): Integer;
```
`TTMSFNCDataGridAutoSizeMode = (gamVisibleCells, gamAllCells)`.

```delphi
Grid.BeginUpdate;
try
  Grid.ClearData;
  Grid.ColumnCount := 3;
  Grid.RowCount := 11;               // 1 fixed + 10 data rows
  Grid.Cells[0, 0] := 'Name';
  Grid.Cells[1, 0] := 'Qty';
  for I := 1 to 10 do
  begin
    Grid.Cells[0, I] := 'Item ' + I.ToString;
    Grid.Cells[1, I] := I * 10;
  end;
finally
  Grid.EndUpdate;
end;
```

## Loading and saving

```delphi
procedure LoadFromCSVData(AFileName: string); overload; virtual;
procedure LoadFromCSVData(AFileName: string; AEncoding: TEncoding); overload; virtual;
procedure LoadFromCSVStreamData(AStream: TStream); overload; virtual;
procedure LoadFromJSONData(AFileName: string; ARowDataName: string = ''; AColumnDataName: string = '';
  AColumnNames: TTMSFNCDataGridDataJSONNamesArray = nil); overload; virtual;
procedure LoadFromJSONStreamData(AStream: TStream; ARowDataName: string = ''; AColumnDataName: string = '';
  AColumnNames: TTMSFNCDataGridDataJSONNamesArray = nil); overload; virtual;
procedure LoadFromJSONTextData(AText: string; ARowDataName: string = ''; AColumnDataName: string = '';
  AColumnNames: TTMSFNCDataGridDataJSONNamesArray = nil); virtual;
procedure LoadFromXMLData(AFileName: string); overload; virtual;
procedure LoadFromFileData(AFileName: string); overload; virtual;  // grid's own format
procedure SaveToCSVData(AFileName: string); overload;   // + (AFileName; AEncoding), stream variants
procedure SaveToHTMLData(AFileName: string); overload;
procedure SaveToFileData(AFileName: string); overload; virtual;
procedure SaveToImageData(AFileName: string); overload;
```
`TTMSFNCDataGridDataJSONNamesArray = array of string`. Every file and stream loader and saver
(CSV, JSON, XML, File, HTML) also has an `AEncoding: TEncoding` overload. There is no LoadFromStrings, LoadFromArray or
LoadFromDataSet. For datasets use the database adapter (separate reference).

IO options (`Options.IO`): `StartRow`, `StartColumn` (Integer, default 0, where loaded data begins),
`Delimiter: Char` (default `#0` = auto-detect on import, comma on export), `AlwaysQuotes`,
`QuoteEmptyCells`, `TrimSpaces`, `MaxRows` (default -1), `HTML` (HTML export settings).

The demo pattern (load data below a header you write yourself):
```delphi
Grid.Options.IO.StartColumn := 1;
Grid.Options.IO.StartRow := 1;
Grid.LoadFromCSVData('CARS.csv');           // WEB demos: LoadFromCSVData('CARS.csv', TEncoding.UTF8)
Grid.Cells[1, 0] := 'Brand';
Grid.AutoNumberColumn(0, 1);
```

**WEB:** `LoadFromCSVData(AFileName)` (file-name variants) loads the file over HTTP **asynchronously**,
so the code after it runs before the data arrives, and the grid has no "load complete" event. If later
code depends on the data, fetch the text yourself and call `LoadFromJSONTextData` or a stream variant.

## Columns

`property Columns: TTMSFNCDataGridColumns;` with `Items[Index]` (default), `Add`, `Insert(Index)`,
`ColumnByName`, `ColumnByHeader`. Published members of `TTMSFNCDataGridColumn`:

```delphi
property Header: string;            // reads and writes Cells[Index, 0]
property Name: string;
property Width: Single;             // sets ColumnWidths[Index]
property Visible: Boolean default True;
property &ReadOnly: Boolean default False;
property &Type: TTMSFNCDataGridCellItemType default gcitNormal;
property TypeRange: TTMSFNCDataGridCellItemTypeRange default gcirAll;  // gcirNormal, gcirFixed, gcirAll
property Appearance: TTMSFNCDataGridCellAppearance;   // per-column layouts (alignment, font, fill)
property Formatting: TTMSFNCDataGridColumnFormatting; // &Type, Format, BooleanTrueText, BooleanFalseText
property Editor: TTMSFNCDataGridInplaceEditorType default getEdit;
property EditorItems: TStringList;
property EditorTarget: TTMSFNCDataGridInplaceEditorTarget default getCellValue;
property FilterButton: Boolean default True;
property FilterEditor: Boolean default False;
property FilterEditorType: TTMSFNCDataGridFilterEditorType default gfetAutomatic;
property FilterDefaultType: TTMSFNCDataGridDataFilterType default gftEqual;
property ControlAlign, ControlPosition, ControlWidth, ControlHeight, ControlMargins, ControlText;
property Settings: TTMSFNCDataGridColumnSettings default [];
property ValueType: TTypeKind;      // read-only
procedure AddSetting(ASetting: TTMSFNCDataGridColumnSetting);
procedure RemoveSetting(ASetting: TTMSFNCDataGridColumnSetting);
```

**Column `Settings` rule:** a column property only takes effect if its matching setting is in
`Settings`. The Object Inspector adds it for you at design time. **In code you must call `AddSetting`
yourself**, or the property is ignored:
`gcsAppearance, gcsType, gcsEditor, gcsEditorTarget, gcsEditorItems, gcsReadOnly, gcsFormatting,
gcsControlText, gcsControlWidth, gcsControlHeight, gcsControlAlign, gcsControlPosition,
gcsControlMargins, gcsFilterButton, gcsFilterEditor, gcsFilterEditorType, gcsFilterDefaultType`.
`Header`, `Width` and `Visible` don't need a setting.

```delphi
Grid.Columns[3].Header := 'Price';
Grid.Columns[3].Width := 90;
Grid.Columns[3].AddSetting(gcsFormatting);
Grid.Columns[3].Formatting.&Type := gdftFloat;
Grid.Columns[3].Formatting.Format := '#,##0.00';       // FormatFloat syntax
Grid.Columns[3].AddSetting(gcsAppearance);
Grid.Columns[3].Appearance.NormalLayout.TextAlign := gtaTrailing;   // right-align
```

`TTMSFNCDataGridDataFormattingType = (gdftDefault, gdftBoolean, gdftDateTime, gdftDate, gdftTime,
gdftFloat, gdftNumber)`. `gdftDefault` passes `Format` to `Format()` with the text (`'%s pcs'`).
`gdftFloat` uses `FormatFloat`. `gdftDateTime`/`gdftDate`/`gdftTime` use `FormatDateTime`.
`gdftNumber` uses `Format` if the string contains `%`, otherwise `FormatFloat`.

`TTMSFNCDataGridCellItemType = (gcitNormal, gcitCheckBox, gcitRadioButton, gcitDataCheckBox,
gcitDataRadioButton, gcitButton, gcitProgressBar, gcitDataProgressBar, gcitBitmap)`.
You can also add cell types with methods: `AddCheckBoxColumn(AColumn; AValue = False)`,
`AddCheckBox(AColumn, ARow; AValue = False)`, `AddButtonColumn(AColumn; AText = '')`,
`AddProgressBarColumn`, `AddDataCheckBoxColumn(AColumn)`, `AddRadioButtonColumn`, `AddBitmap(...)`,
and `Remove*` counterparts. Read checkbox state with `Booleans[c, r]`. You can also embed any control
with `Controls[c, r] := SomeControl` and `ControlAligns[c, r] := gcaClient`.

## Appearance and layout

```delphi
property CellAppearance: TTMSFNCDataGridCellAppearance;
  // NormalLayout, FixedLayout, SelectedLayout, FixedSelectedLayout, FocusedLayout, BandLayout,
  // GroupLayout, SummaryLayout, FilterMatchLayout, FilterInverseMatchLayout, ShowFocus: Boolean
property Layouts[AColumn, ARow: Integer]: TTMSFNCDataGridCellLayout;   // per-cell override (read-only ref)
property Colors[AColumn, ARow: Integer]: TTMSFNCGraphicsColor;
property FontColors / FontNames / FontSizes / FontStyles [AColumn, ARow];
property TextAligns[AColumn, ARow: Integer]: TTMSFNCGraphicsTextAlign;
property VerticalTextAligns / WordWrapping / TextAngles [AColumn, ARow];
property Fill: TTMSFNCGraphicsFill;  property Stroke: TTMSFNCGraphicsStroke;  // control background/border
property GlobalFont: TTMSFNCAppearanceGlobalFont;
property SortIndicatorAppearance, FilterAppearance, AutoFillAppearance, DragAppearance, Icons;
property Header: TTMSFNCDataGridHeader;  property Footer: TTMSFNCDataGridFooter;
```
`TTMSFNCDataGridCellLayout` published: `Fill`, `Font`, `Stroke`, `Sides`, `TextAlign`
(default `gtaLeading`), `VerticalTextAlign` (default `gtaCenter`), `TextMargins`, `Trimming`, `WordWrapping`.

`Header`/`Footer` are bars **above/below** the grid (button bar, visual grouping area, paging).
They are not the column header row. Column captions are row 0 (`Cells[c, 0]` / `Columns[c].Header`).

Banding: `Options.Banding.Enabled := True` (`BandRowCount`, `NormalRowCount`), styled by
`CellAppearance.BandLayout`. There is no hover-highlight layout. Column stretching:
`Options.Column.Stretching.Enabled := True` (`Mode: gstmIndex|gstmAll|gstmProportional`, `Index`).

Dynamic per-cell styling (demo pattern):
```delphi
procedure TForm1.TMSFNCDataGrid1GetCellLayout(Sender: TObject; ACell: TTMSFNCDataGridCell);
begin
  if (ACell.Column = 5) and (ACell.Row >= TMSFNCDataGrid1.FixedRowCount) then
  begin
    ACell.Layout.Font.Color := gcRed;
    ACell.Layout.TextAlign := gtaTrailing;
  end;
end;
```
`TTMSFNCDataGridCell` exposes `Column`, `Row`, `Coordinate`, `Text`, `Layout`, `Kind`, `Rect`,
`FilterButton`, `Control`, `Data` and other members.

Mouse sizing and dragging are **off by default**: `Options.Mouse.ColumnSizing`, `RowSizing`,
`ColumnDragging`, `RowDragging` are all `False`. `ColumnAutoSizeOnDblClick` defaults to `True`.

## Selection

`Options.Selection.Mode: TTMSFNCDataGridSelectionMode` (default `gsmSingleCell`):
`gsmNone, gsmSingleCell, gsmSingleRow, gsmSingleColumn, gsmCellRange, gsmRowRange, gsmColumnRange,
gsmDisjunctRow, gsmDisjunctColumn, gsmDisjunctCell, gsmDisjunctCellRange`.
Other selection options: `RangeType` (`gsrtMoveFocusedCell`/`gsrtKeepFocusedCell`), `AutoFill`,
`ShowSelectionInFixedCells`. `Options.Mouse.FixedCellSelection: set of (gfcsAll, gfcsRow, gfcsColumn, ...)`.

```delphi
property FocusedCell: TTMSFNCDataGridCellCoord;          // read/write
property Selection: TTMSFNCDataGridCellCoordRange;       // read/write
property SelectedRows[ARow: Integer]: Boolean;  property SelectedRowCount: Integer;
property SelectedColumns[AColumn: Integer]: Boolean; property SelectedColumnCount: Integer;
property SelectedCells[AColumn, ARow: Integer]: Boolean; property SelectedCellCount: Integer;
procedure SelectCell(ACell: TTMSFNCDataGridCellCoord; AShift: TShiftState = []);
procedure SelectCellRange(AFromCol, AFromRow, AToCol, AToRow: Integer);
procedure SelectRows(AFromRow, AToRow: Integer);  procedure SelectColumns(AFromColumn, AToColumn: Integer);
procedure SelectAllCells(AIncludeHidden: Boolean = True);
procedure ClearSelection;
procedure GoToCell(ACell: TTMSFNCDataGridCellCoord; ASelect: Boolean = True);
function IsCellSelected(ACell: TTMSFNCDataGridCellCoord): Boolean;
```
In disjunct modes `SelectedRows`/`SelectedRowCount` read a dictionary. In the other modes they are
computed from `Selection.StartCell.Row..StopCell.Row`. There is no list-returning `GetSelectedRows`.

```delphi
for R := TMSFNCDataGrid1.FixedRowCount to TMSFNCDataGrid1.RowCount - 1 do
  if TMSFNCDataGrid1.SelectedRows[R] then
    Memo1.Lines.Add(TMSFNCDataGrid1.Strings[1, R]);
```

## Row index mapping (sort / filter)

Sorting physically moves row data, so `Cells[c, r]` always means "the row shown at sorted position r".
Filtering hides rows but keeps their indexes. Mappings: `DisplayToRealRow(ARow)` / `RealToDisplayRow`
(original-order index), `RealToVisualRow` / `VisualToRealRow` (0-based on-screen position with sort,
filter and hidden rows applied). The column versions are `RealToVisualColumn` and `VisualToRealColumn`. Helpers: `IsRowFiltered(ARow)`, `IsRowHidden(ARow)`,
`FilteredRowCount`.

## Most-used events (exact types)

```delphi
OnCellClick, OnCellDblClick, OnCellRightClick, OnCellCheckBoxChange, OnCellButtonClick:
  procedure(Sender: TObject; AColumn, ARow: Integer) of object;
OnCellAnchorClick: procedure(Sender: TObject; AColumn, ARow: Integer; AAnchor: string) of object;
OnSelectCell: procedure(Sender: TObject; AStartCell, AEndCell, AFocusedCell: TTMSFNCDataGridCellCoord) of object;
OnSelectingCell: procedure(Sender: TObject; AStartCell, AEndCell, AFocusedCell: TTMSFNCDataGridCellCoord;
  var ACanSelect: Boolean) of object;
OnGetCellLayout, OnGetCellProperties: procedure(Sender: TObject; ACell: TTMSFNCDataGridCell) of object;
OnGetCellData: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; var AData: TTMSFNCDataGridCellValue) of object;
OnGetCellDisplayValue: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AData: TTMSFNCDataGridCellValue; var AValue: string) of object;
OnGetCellFormatting: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; AData: TTMSFNCDataGridCellValue;
  var AFormatting: TTMSFNCDataGridDataFormatting; var AConvertSettings: TFormatSettings;
  var ACanFormat: Boolean) of object;
OnGetCellHint: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; var AHint: string) of object;
OnBeforeDrawCell: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ACell: TTMSFNCDataGridCell;
  var ACanDraw: Boolean) of object;
OnAfterDrawCell: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ACell: TTMSFNCDataGridCell) of object;
OnColumnSized: procedure(Sender: TObject; AColumn: Integer; ASize: Double) of object;
```
For editing events see editing.md. For sort and filter events see sorting-filtering.md.
`TTMSFNCDataGridDataFormatting` is a record with fields `Format: string`,
`&Type: TTMSFNCDataGridDataFormattingType`, `BooleanTrueText` and `BooleanFalseText`.

## Does not exist / common mistakes

| Wrong (TStringGrid / TAdvStringGrid / TTMSFNCGrid habit) | Use instead |
|---|---|
| `ColCount`, `FixedRows`, `FixedCols`, `ColWidths` | `ColumnCount`, `FixedRowCount`, `FixedColumnCount`, `ColumnWidths` |
| `Values[c,r]`, `Cells[c,r]` as string | `Cells` is `TValue`/`JSValue`; read text with `Strings[c,r]` |
| `Grid.Options := [goEditing, ...]` | `Options` is an object: `Options.Editing.Enabled`, `Options.Selection.Mode`, ... |
| `Grid.Appearance.*` | `CellAppearance.*Layout`, `Fill`, `Stroke`, `GlobalFont` |
| `Columns[i].Alignment`, `Columns[i].Color`, `Columns[i].Font` | `AddSetting(gcsAppearance)` + `Columns[i].Appearance.NormalLayout.TextAlign/Fill/Font` |
| Setting `Columns[i].Editor` in code and nothing happens | You forgot `Columns[i].AddSetting(gcsEditor)` (same for Formatting, ReadOnly, Type, ...) |
| `RemoveRows`, `ClearRows`, `AddRow(n)` | `DeleteRows(ARow, ACount)`, `ClearData`, `AddRow` (no params) / `RowCount := n` |
| `LoadFromStrings`, `LoadFromArray`, `LoadFromCSV` | `LoadFromCSVData`, `LoadFromJSONTextData`, `LoadFromCSVStreamData` |
| `OnSelectionChanged`, `OnCellChanged`, `OnGetCellColor`, `OnGetAlignment` | `OnSelectCell`, `OnCellEditSetData`, `OnGetCellLayout` |
| `GetSelectedRows` list, `SelectedRow[i]` index list | loop rows and test `SelectedRows[R]`, or read `Selection` |
| `(Sender as TTMSFNCDataGrid)` in events | `Sender` is `Root` (`TTMSFNCDataGridRenderer`); use the form field |
| `Grid.Header` = column headers | `Header` is the top bar; column captions are row 0 |
| Expecting resizable columns by default | set `Options.Mouse.ColumnSizing := True` |
| `HoverLayout` / hover row color | does not exist |
