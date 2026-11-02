# Spreadsheet grid and legacy grid (TTMSFNCSpreadGrid, TTMSFNCGrid)

Verified against `tms.fnc.uipack\Source` v7.3.1.2: `*.TMSFNCSpreadGrid`, `*.TMSFNCSpreadGridTypes`, `*.TMSFNCSpreadGridLibs`, `*.TMSFNCFormulaParser`, `*.TMSFNCGrid`, `*.TMSFNCCustomGrid`, `*.TMSFNCGridData`, `*.TMSFNCGridOptions`, `*.TMSFNCGridCell`, `*.TMSFNCGridDatabaseAdapter`, `*.TMSFNCGridPDFIO`, `*.TMSFNCGridPrintIO`, `*.TMSFNCGridToolBarPopup`. The DataGrid side of the mapping table was checked in `*.TMSFNCDataGrid*.pas`.

**`TTMSFNCGrid` is the legacy grid.** Use it only to maintain existing code. **New code should use `TTMSFNCDataGrid`** (see the tms-fnc-datagrid references). `TTMSFNCSpreadGrid` derives from `TTMSFNCGrid`, so it uses the legacy API and has no DataGrid counterpart. DataGrid has no formula engine.

## Units and palette

All components are on palette page **'TMS FNC UI'**. Use the `VCL.`, `FMX.` or `WEBLib.` prefix (LCL: `LCLTMSFNC...`, no dot).

| Component | Unit | Registered in |
|---|---|---|
| `TTMSFNCSpreadGrid`, `TTMSFNCGridBinder` | `*.TMSFNCSpreadGrid` (`TTMSFNCGridBinder` is declared in `*.TMSFNCFormulaParser`) | `*.TMSFNCSpreadGridReg` |
| `TTMSFNCMiscMathLib`, `TTMSFNCStringMathLib`, `TTMSFNCConversionMathLib`, `TTMSFNCFinanceMathLib`, `TTMSFNCDBMathLib` | `*.TMSFNCSpreadGridLibs` | `*.TMSFNCSpreadGridReg` |
| `TTMSFNCGrid` | `*.TMSFNCGrid` (API in `*.TMSFNCCustomGrid`, `*.TMSFNCGridData`, `*.TMSFNCGridOptions`, `*.TMSFNCGridCell`) | `*.TMSFNCGridReg` |
| `TTMSFNCGridDatabaseAdapter` | `*.TMSFNCGridDatabaseAdapter` | `*.TMSFNCGridDatabaseAdapterReg` |
| `TTMSFNCGridPDFIO` | `*.TMSFNCGridPDFIO` | `*.TMSFNCGridIOReg` (not "GridPDFIOReg") |
| `TTMSFNCGridPrintIO` | `*.TMSFNCGridPrintIO` | `*.TMSFNCGridPrintIOReg` |
| `TTMSFNCGridToolBarPopup` | `*.TMSFNCGridToolBarPopup` | `*.TMSFNCGridToolBarPopupReg` |

Typical VCL uses for a spreadsheet form (from the demo):
```delphi
uses
  VCL.TMSFNCTypes, VCL.TMSFNCUtils, VCL.TMSFNCCustomControl, VCL.TMSFNCCustomScrollControl,
  VCL.TMSFNCGridData, VCL.TMSFNCCustomGrid, VCL.TMSFNCGrid, VCL.TMSFNCSpreadGrid,
  VCL.TMSFNCFormulaParser,   // TTMSFNCMathLib, TParamList, Error_* constants, TTMSFNCGridBinder
  VCL.TMSFNCSpreadGridTypes, // TGridCoord, TGridRect
  VCL.TMSFNCSpreadGridLibs;  // only if you use the *MathLib components
```

## TTMSFNCSpreadGrid

`TTMSFNCSpreadGrid = class(TTMSFNCGrid, IGridBinder)`. It inherits all of `TTMSFNCGrid` (Cells, Floats, LoadFromCSV, Options, ...) and adds:

```delphi
TCellNameMode = (nmA1, nmRC);
TFormulaErrorEvent = procedure(Sender: TObject; ACol, ARow: Integer; ErrType, ErrPos, ErrParam: Integer; ErrStr: string) of object;
TIsCustomFunction = procedure(sender: TObject; var func: string; var match: boolean) of object;
TCalcCustomFunction = procedure(sender: TObject; var func: string; var param: double) of object;

// public
function CellToName(Col, Row: Integer): string;
function NameToCell(s: string): TGridCoord;           // TGridCoord = record X, Y: Integer (X = column)
function RangeToName(gr: TGridRect): string;           // TGridRect = record Left, Top, Right, Bottom
function NameToRange(s: string): TGridRect;
function FindCellName(value: string): TGridCoord;      // X = Y = -1 when not found
procedure Recalc;
property CellName[Col, Row: Integer]: string;          // assign a named-cell alias, e.g. 'PRICE'
procedure DeleteRows(Row, Count: integer); override;  procedure InsertRows(Row, Count: integer); override;
procedure DeleteColumn(Col: integer); override;        procedure InsertColumn(Col: integer); override;

// published
property AutoHeaders: boolean default true;     // writes A,B,C... into row 0 and 1,2,3... into column 0
property AutoRecalc: boolean default true;
property CellNameMode: TCellNameMode default nmA1;
property FloatFormat: string;                   // Format() pattern for numeric results, default '%.2f'
property Libs: TLibBinderItems;                 // read-only collection of math libraries
property ShowFormula: boolean default false;    // True shows formula text instead of results
property OnFormulaError: TFormulaErrorEvent;
property OnAfterRecalc: TNotifyEvent;  property OnBeforeRecalc: TNotifyEvent;
property OnIsCustomFunction: TIsCustomFunction;
property OnCalcCustomFunction: TCalcCustomFunction;
```

Read results with the inherited `CalcStates[Col, Row]: TTMSFNCGridCellCalcState` (`csNoCalc, csCalcOk, csCalcErr`) and `CalcValues[Col, Row]: variant`.

### How formulas work (from source)

- A cell is a formula when its text starts with `=`. `Cells[c, r]` always holds the **formula text**. The result is computed in `DoGetCellData` when the cell is painted, cached in `CalcValues`, and formatted with `FloatFormat` (numbers) or `DateToStr` (date functions). A cell in error shows `Error`.
- Naming is relative to the fixed area. With the default `FixedColumns = 1` and `FixedRows = 1`, `A1` is `Cells[1, 1]`. Columns past Z use two letters (`AA`). In `nmRC` mode the same cell is `R1C1`. `$A$1` is accepted, and `$` keeps the reference fixed when formulas are pasted.
- Ranges use `:` (`SUM(A1:A10)`). Another grid uses `Name!A1`, where `Name` is a `TTMSFNCGridBinder` item name.
- **Parameter separator:** `;` always works. `,` works only when `FormatSettings.DecimalSeparator <> ','`. Both demos set `FormatSettings.DecimalSeparator := '.'` in `FormCreate`.
- Operators: `+ - * / ^` and `%` (integer modulo). There are **no comparison operators** (`<`, `>`, `=`) and no `&`. Use `LT(a;b)` (1 if a > b), `ST(a;b)` (1 if a < b), `EQ(a;b)` and `CHOOSE(cond;valueIfZero;valueIfNonZero)`.
- Function names are case-insensitive. `ReadWord` uppercases them, so `HandlesFunction` and `OnIsCustomFunction` receive uppercase names.

**Recalculation:** user edits (`DoCellEditDone`) recalculate the cell and its dependents automatically. **Assigning `Cells`/`Floats` in code does not.** Cached results of dependent cells stay stale until you call `Recalc`. `AutoRecalc` only controls the recalculation after `InsertRows`/`DeleteRows`/`InsertColumn`/`DeleteColumn`. `Recalc` returns early when no formula references any cell.

### Built-in functions (`TGridFormula.DoFunc`)

`ABS ACOS ACOTAN AND ASIN ATAN AVERAGE CEILING CHOOSE CHS COL COMPARE CONCATENATE COS COSH COTAN COTANH COUNT COUNTA COUNTBLANK COUNTIF CUBE DAY DEGREES DEVSQ E EQ EXP FACT FALSE FRAC HOUR INDEX INT LEFT LEN LN LOG10 LOG2 LOOKUP LOWER LT MATCH MAX MID MIN MINUTE MONTH NAND NOR NOT NOW OR PI POWER PRODUCT RADIANS RAND RIGHT ROUND ROW SEARCH SECOND SIN SINH SQR SQRT ST STDEV STDEVP SUBSTITUTE SUM TAN TANH TODAY TRIM TRUE TRUNC UPPER VAR WEEKDAY XOR YEAR`

`ROUND` takes one argument and rounds to an integer. For decimals use `ROUNDUP(x;digits)` from `TTMSFNCMiscMathLib`. `PI`, `E`, `NOW`, `TODAY`, `TRUE` and `FALSE` take no parentheses (`=PI*B12*B12`, `=TODAY+5`).

### Library components (`*.TMSFNCSpreadGridLibs`)

Drop the component and add it to the grid's `Libs`. Libraries are consulted **before** the built-ins, so a library can override a built-in name.

| Component | Functions (exact names from `HandlesFunction`/`HandlesStrFunction`) |
|---|---|
| `TTMSFNCMiscMathLib` | `HARMEAN`, `GEOMEAN`, `ROUNDUP(value;digits)` |
| `TTMSFNCFinanceMathLib` | `CUMINT`, `CTERM`, `TERM`, `RATE`, `PV`, `PMT` (3 params each, e.g. `PMT(principal;rate;term)`) |
| `TTMSFNCConversionMathLib` | `CELSTOFAHR`, `FAHRTOCELS`, `GALTOL`, `LTOGAL`, `INCHTOCM`, `CMTOINCH`, `LBTOKG`, `KGTOLB` |
| `TTMSFNCStringMathLib` | `REVERSE`, `CAPITALIZE`, `IF(cond;then;else)` (true only when the first param's text is `'1'`), `GETVAR` (sample) |
| `TTMSFNCDBMathLib` | `DBV(fieldname;recordoffset)`. Needs `property DataSource: TDataSource` with an active dataset. It moves the dataset (`First` + `MoveBy`). |

```delphi
TMSFNCSpreadGrid1.Libs.Add.MathLib := TMSFNCMiscMathLib1;   // TLibBinderItem.MathLib: TTMSFNCMathLib
TMSFNCSpreadGrid1.Libs.Add.MathLib := TMSFNCFinanceMathLib1;
TMSFNCSpreadGrid1.Cells[2, 1] := '=ROUNDUP(B1;2)';
TMSFNCSpreadGrid1.Recalc;
```

### Custom functions

There are two ways to add a function.

1. **Events** (demo): a single numeric argument only (`MatchFunc` parses one expression).
```delphi
procedure TForm1.TMSFNCSpreadGrid1IsCustomFunction(sender: TObject; var func: string; var match: Boolean);
begin
  match := func = 'BFS';
end;

procedure TForm1.TMSFNCSpreadGrid1CalcCustomFunction(sender: TObject; var func: string; var param: Double);
begin
  if func = 'BFS' then
    param := param * 2;     // param is in/out: the argument comes in, the result goes out
end;
// cell: =BFS(B12)
```
Both events must be assigned, or the function is never matched.

2. **Your own library** (any number of numeric args, ranges expanded into `Params`):
```delphi
type
  TMyMathLib = class(TTMSFNCMathLib)   // VCL.TMSFNCFormulaParser
  public
    function HandlesFunction(FuncName: string): Boolean; override;
    function CalcFunction(FuncName: string; Params: TParamList; var ErrType, ErrParam: Integer): Double; override;
  end;

function TMyMathLib.HandlesFunction(FuncName: string): Boolean;
begin
  Result := FuncName = 'SUMSQ';        // arrives uppercase
end;

function TMyMathLib.CalcFunction(FuncName: string; Params: TParamList; var ErrType, ErrParam: Integer): Double;
var
  i: Integer;
begin
  Result := 0;
  if Params.Count = 0 then
  begin
    ErrType := Error_InvalidNrOfParams;
    Exit;
  end;
  for i := 0 to Params.Count - 1 do    // TParamList = TList<Double>
    Result := Result + Sqr(Params[i]);
end;

// FormCreate
FLib := TMyMathLib.Create(Self);
TMSFNCSpreadGrid1.Libs.Add.MathLib := FLib;
```
For string functions, override `HandlesStrFunction` and `CalcStrFunction(FuncName: string; Params: TStringList; var ErrType, ErrParam: Integer): string`. Constants use `HandlesConstant` and `GetConstant`.

### Demo (`{VCL,FMX}\SpreadGrid`)

```delphi
procedure TForm1.FormCreate(Sender: TObject);
begin
  FormatSettings.DecimalSeparator := '.';
  FormatSettings.ThousandSeparator := ',';
  TMSFNCSpreadGrid1.DefaultColumnWidth := 96;
end;

procedure TForm1.Button3Click(Sender: TObject);   // named cells
begin
  with TMSFNCSpreadGrid1 do
  begin
    ClearNormalCells;
    CellNameMode := nmRC;
    Cells[1,1] := 'Price';  Floats[2,1] := 100;  CellName[2,1] := 'PRICE';
    Cells[1,2] := 'Tax';    Floats[2,2] := 15;   CellName[2,2] := 'TAX';
    Cells[2,3] := '=PRICE+(PRICE*TAX/100)';
    Floats[3,1] := 100; Floats[3,2] := 15;
    Cells[3,3] := '=R1C3+(R1C3*R2C3/100)';
    Recalc;
  end;
end;

procedure TForm1.Button4Click(Sender: TObject);   // bulk fill: switch AutoRecalc off, Recalc once
var i: Integer;
begin
  with TMSFNCSpreadGrid1 do
  begin
    BeginUpdate;
    RowCount := 101;
    ClearNormalCells;
    AutoRecalc := False;
    CellNameMode := nmRC;
    for i := 1 to 100 do
    begin
      Floats[1,i] := i;
      Cells[2,i] := '=SUM(R' + IntToStr(i) + 'C1:R100C1)';
    end;
    Recalc;
    AutoRecalc := True;
    EndUpdate;
  end;
end;

procedure TForm1.TMSFNCSpreadGrid1FormulaError(Sender: TObject; ACol, ARow,
  ErrType, ErrPos, ErrParam: Integer; ErrStr: string);
begin
  StatusBar1.SimpleText := 'Error at: ' + IntToStr(ACol) + ':' + IntToStr(ARow) +
    ' position ' + IntToStr(ErrPos) + ' ' + ErrStr;
end;
```
The demo also loads formulas from CSV (`LoadFromCSV('.\spread.csv')`, with cells like `=SUM(A1:A10)` and `=CHOOSE(D17;B17;B18)`). After loading, call `Recalc`.

`TTMSFNCGridBinder` (published `Grids: TTMSFNCGridBinderItems`, items have `Grid: TTMSFNCGrid` and `Name: string`) links several spread grids. Assigning `Item.Grid` registers the binder with that grid. Then a formula can use `=Sheet2!A1` or `=SUM(Sheet2!A1:A5)`.

## TTMSFNCGrid (legacy): core API for maintenance

Hierarchy: `TTMSFNCCustomScrollControl` → `TTMSFNCGridData` (data, IO, sort, filter, merge, cell types) → `TTMSFNCCustomGrid` (drawing, editing, events, `Appearance`, `Adapter`) → `TTMSFNCGrid`.

```delphi
// TTMSFNCGridData
property ColumnCount: Integer default 5;     property RowCount: Integer default 10;
property FixedColumns: Integer default 1;     property FixedRows: Integer default 1;
property FixedRightColumns: Integer default 0; property FixedFooterRows: Integer default 0;
property DefaultColumnWidth: Single;          property DefaultRowHeight: Single;
property ColumnWidths[Col: Integer]: Single;  property RowHeights[Row: Integer]: Single;
property Cells[Col,Row: Integer]: TTMSFNCGridCellData;   // = string
property Floats[Col,Row: Integer]: double;  property Ints[Col,Row: Integer]: Integer;
property Booleans[Col,Row: Integer]: Boolean;  property Objects[Col,Row: Integer]: TObject;
property Colors[Col,Row: Integer]: TTMSFNCGraphicsColor;  property FontColors[Col,Row: Integer]: TTMSFNCGraphicsColor;
property FontNames / FontSizes / FontStyles / HorzAlignments / VertAlignments / ReadOnlys / Comments [Col,Row];
property Columns: TTMSFNCGridColumns;   // public; items: Width, Color, Font, FixedFont, HorzAlignment,
                                        // VertAlignment, ReadOnly, Editor: TTMSFNCGridEditorType, ComboItems,
                                        // ColumnType, SortFormat, WordWrap, Name, ID, Tag
property FocusedCell: TTMSFNCGridCellRec;          // record Col, Row
property Selection: TTMSFNCGridCellRecRange;       // record StartCol, StartRow, EndCol, EndRow
property ColumnCalculation[Col: Integer]: TTMSFNCGridColumnCalculation;  // ccNone, ccSum, ccAvg, ...
property Filter: TTMSFNCGridFilter;   // Add: TTMSFNCGridFilterData (Column, Condition, CaseSensitive, Operation)
procedure ApplyFilter;  procedure RemoveFilter;  procedure RemoveFilters;
procedure SortData(Column: integer; Direction: TTMSFNCGridSortDirection);   // sdAscending, sdDescending
procedure MergeCells(Col,Row,ColCount,RowCount: integer);  procedure SplitCell(Col,Row: integer);
function IsMerged(Col,Row: integer): boolean;  function BaseCell(Col,Row: integer): TTMSFNCGridCellRec;
procedure Group(Column: integer);  procedure UnGroup;  procedure GroupSum(Col: Integer);
procedure InsertRows(Row,Count: integer); virtual;  procedure DeleteRows(Row,Count: integer); virtual;
procedure HideRow(Row: integer);  procedure UnHideRowsAll;  procedure HideColumn(Col: integer);
procedure AddCheckBox(Col,Row: integer; State: boolean = false);
procedure AddButton(Col,Row: integer; AText: string; AWidth: integer = 20; AHeight: Integer = 20);
procedure AddProgressBar(Col,Row: Integer; Value: Single);
procedure AddComboBox(Col,Row: Integer; Items: TStrings);
procedure ClearNormalCells;  procedure Clear;
procedure LoadFromCSV(FileName: string; MaxRows: Integer = -1); overload;
procedure LoadFromCSV(FileName: string; Encoding: TEncoding; MaxRows: Integer = -1); overload;
procedure SaveToCSV(FileName: string; Unicode: boolean = true);      // not on WEB
procedure SaveToHTML(FileName: string; ShowHTML: boolean = false; Unicode: boolean = true);  // not on WEB
procedure LoadFromFile(FileName: string);  procedure SaveToFile(FileName: string; Unicode: boolean = true);
property Options: TTMSFNCGridOptions;
// TTMSFNCCustomGrid
property Appearance: TTMSFNCGridAppearance;  // FixedLayout, NormalLayout, SelectedLayout, FocusedLayout,
                                             // FixedSelectedLayout, BandLayout, GroupLayout, SummaryLayout
property Adapter: TTMSFNCGridAdapter;  property FreezeColumns, FreezeRows: Integer;
property ToolBarPopup: TTMSFNCGridCustomToolBarPopup;  property ToolBarPopupMode default tpmActiveCell;
procedure AutoSizeColumns(Accurate: Boolean = True; const Padding: Integer = 5);
procedure EditCell(ACell: TTMSFNCGridCellRec; ...);  procedure StopEdit; virtual;  procedure CancelEdit;
```
`Options`: `Editing` (`Enabled` default True, `CalcFormat`), `Mouse` (`DirectEdit`, `ColumnSizing`/`RowSizing`/`ColumnDragging` default False), `Selection.Mode` (`smNone, smSingleCell, smSingleRow, smSingleColumn, smCellRange, smRowRange, smColumnRange, smDisjunctRow, smDisjunctColumn, smDisjunctCell`), `Sorting` (`Mode: gsmNone|gsmNormal|gsmIndexed`, default `gsmNone`, so header-click sort is off), `Filtering` (`DropDown`, `MultiColumn`), `Bands.Enabled`, `ColumnSize.Stretch`, `IO.Delimiter`, `Keyboard`, `Clipboard`, `Grouping`, `URL`, `Lookup`.

Events (exact types from `*.TMSFNCCustomGrid`):
```delphi
OnGetCellLayout: procedure(Sender: TObject; ACol, ARow: Integer; ALayout: TTMSFNCGridCellLayout; ACellState: TTMSFNCGridCellState) of object;
OnGetCellData: procedure(Sender: TObject; ACol, ARow: Integer; var CellString: String) of object;
OnGetCellReadOnly: procedure(Sender: TObject; ACol, ARow: Integer; var AReadOnly: Boolean) of object;
OnGetCellEditorType: procedure(Sender: TObject; ACol, ARow: Integer; var CellEditorType: TTMSFNCGridEditorType) of object;
OnCellEditValidateData: procedure(Sender: TObject; ACol, ARow: Integer; CellEditor: TTMSFNCGridEditor; var CellString: String; var Allow: Boolean) of object;
OnCellEditDone: procedure(Sender: TObject; ACol, ARow: Integer; CellEditor: TTMSFNCGridEditor) of object;
OnCellClick: procedure(Sender: TObject; ACol, ARow: Integer) of object;
OnCellCheckBoxClick, OnCellButtonClick: procedure(Sender: TObject; ACol, ARow: Integer; ACell: TTMSFNCGridCell) of object;
OnColumnSorted: procedure(Sender: TObject; ACol: Integer; Direction: TTMSFNCGridSortDirection) of object;
```
`TTMSFNCGridEditor` is `TWinControl` on VCL/WEB and `TControl` on FMX. `TTMSFNCGridCellLayout` has `Fill`, `Stroke`, `Font`, `Sides`, `TextAlign`, `VerticalTextAlign` and `WordWrapping`.

```delphi
procedure TForm1.TMSFNCGrid1GetCellLayout(Sender: TObject; ACol, ARow: Integer;
  ALayout: TTMSFNCGridCellLayout; ACellState: TTMSFNCGridCellState);
begin
  if (ARow >= TMSFNCGrid1.FixedRows) and (TMSFNCGrid1.Floats[3, ARow] < 0) then
    ALayout.Font.Color := gcRed;
end;
```

### Companion components (legacy)

```delphi
// Database: Active defaults to False (DataGrid's adapter defaults to True)
TMSFNCGridDatabaseAdapter1.Grid := TMSFNCGrid1;          // or TMSFNCGrid1.Adapter := ...; both link both ways
TMSFNCGridDatabaseAdapter1.DataSource := DataSource1;     // AutoCreateColumns default True
TMSFNCGridDatabaseAdapter1.Active := True;                // PostMode: apmNone | apmCell | apmRow (default)

// PDF (base TTMSFNCCustomPDFIO is in FNC Core *.TMSFNCPDFIO)
TMSFNCGridPDFIO1.Grid := TMSFNCGrid1;
TMSFNCGridPDFIO1.Options.FitToPage := True;               // also RepeatFixedRows, CellLayout (gclFull|gclColor|gclNone)
TMSFNCGridPDFIO1.Options.Header := 'Report';
TMSFNCGridPDFIO1.Save('grid.pdf');

// Print (base TTMSFNCCustomPrintIO in FNC Core *.TMSFNCPrintIO)
TMSFNCGridPrintIO1.Grid := TMSFNCGrid1;
TMSFNCGridPrintIO1.Print;

// Formatting toolbar that pops up above the cell (bold/italic/font/colors/alignment)
TMSFNCGrid1.ToolBarPopup := TMSFNCGridToolBarPopup1;
TMSFNCGrid1.ToolBarPopupMode := tpmActiveCell;            // tpmHoverCell, tpmHoverNormalCell, tpmNone
```

## TTMSFNCGrid → TTMSFNCDataGrid mapping

| TTMSFNCGrid | TTMSFNCDataGrid |
|---|---|
| `ColumnCount` / `RowCount` (defaults 5 / 10) | same names (defaults 4 / 24) |
| `FixedColumns` / `FixedRows` (default 1 / 1) | `FixedColumnCount` (default **0**) / `FixedRowCount` (1) |
| `FixedRightColumns` / `FixedFooterRows` | `FixedRightColumnCount` / `FixedBottomRowCount` |
| `FreezeColumns` / `FreezeRows` | `FreezeColumnCount` / `FreezeRowCount` |
| `Cells[c,r]: string` | `Cells[c,r]: TTMSFNCDataGridCellValue` (TValue/JSValue); text via `Strings[c,r]` |
| `Floats`, `Ints` (Integer), `Booleans` | `Floats`, `Ints` (Int64), `Booleans` |
| `Colors`, `FontColors`, `FontNames`, `FontSizes`, `FontStyles` | same names |
| `HorzAlignments` / `VertAlignments` | `TextAligns` / `VerticalTextAligns` |
| `Appearance.NormalLayout` etc. | `CellAppearance.NormalLayout` etc. |
| `OnGetCellLayout(Sender; ACol, ARow; ALayout; ACellState)` | `OnGetCellLayout(Sender; ACell: TTMSFNCDataGridCell)`: use `ACell.Column`, `ACell.Row`, `ACell.Layout` |
| `Options.Editing.Enabled` | `Options.Editing.Enabled` (both default True) |
| `OnGetCellEditorType` (`etComboBox`...) | `OnGetInplaceEditorType(Sender; ACell; var AInplaceEditorType)` (`getComboBox`...) |
| `OnGetCellReadOnly(var AReadOnly)` | `OnCanEditCell(Sender; AColumn, ARow; var ACanEdit)` (inverted meaning) |
| `OnCellEditValidateData(...; var CellString; var Allow)` | `OnCellEditValidateData(Sender; ACell; AInplaceEditor; var AValue; var AValid)` |
| `Options.Sorting.Mode := gsmNormal`; `SortData(c, sdAscending)` | `Options.Sorting.Enabled := True`; `Sort(c, gsdAscending)` |
| `OnColumnSorted` / `OnCanSortColumn` | `OnAfterSortColumn` / `OnBeforeSortColumn(var ACanSort)` |
| `Filter.Add` + `.Column`/`.Condition`, `ApplyFilter`, `RemoveFilters` | `Filter.Add(...)`, `ApplyFilter`, `ClearFilter` |
| `Options.Filtering.DropDown := True` | `Options.Filtering.Enabled := True` |
| `MergeCells(c, r, colCount, rowCount)` | `MergeCells(c, r, colCount, rowCount)` (also counts) |
| `SplitCell(c, r)`, `IsMerged(c, r)` | `SplitCell(MakeCell(c, r))`, `IsCellMerged(MakeCell(c, r))` |
| `LoadFromCSV`, `SaveToCSV`, `SaveToHTML`, `LoadFromFile`/`SaveToFile` | `LoadFromCSVData`, `SaveToCSVData`, `SaveToHTMLData`, `LoadFromFileData`/`SaveToFileData` |
| `Columns[i].Width` | `Columns[i].Width` |
| `Columns[i].Color` / `.Font` / `.HorzAlignment` | `Columns[i].AddSetting(gcsAppearance)` + `Columns[i].Appearance.NormalLayout.Fill/Font/TextAlign` |
| `Columns[i].ReadOnly`, `.Editor`, `.ComboItems` | `.ReadOnly` + `gcsReadOnly`, `.Editor` + `gcsEditor`, `.EditorItems` + `gcsEditorItems` |
| header text in `Cells[c, 0]` | `Cells[c, 0]` or `Columns[c].Header` |
| `FocusedCell.Col` / `Selection.StartCol` | `FocusedCell.Column` / `Selection.StartCell.Column` |
| `Options.Selection.Mode := smCellRange` | `Options.Selection.Mode := gsmCellRange` |
| `AutoNumberCol`, `UnHideRowsAll`, `ClearNormalCells` | `AutoNumberColumn`, `UnhideAllRows`, `ClearCells(range)` / `ClearData` (also clears headers) |
| `AddCheckBox(c, r, State)`, `AddButton(c, r, Text, W, H)` | `AddCheckBox(c, r, AValue)`, `AddButton(c, r, AText)` |
| `AddComboBox(c, r, Items)` | none: use a combo inplace editor (`Columns[c].Editor := getComboBox`) |
| `ColumnCalculation[c] := ccSum` | `ColumnCalculation(c, gcmSum)` / `ColumnCalculations[c, name]` |
| `TTMSFNCGridDatabaseAdapter`, `TTMSFNCGridPDFIO.Grid`, `TTMSFNCGridPrintIO.Grid` | `TTMSFNCDataGridDatabaseAdapter`, `TTMSFNCDataGridPDFIO.DataGrid`, `TTMSFNCDataGridPrintIO.DataGrid` |
| `TTMSFNCGridToolBarPopup` | no DataGrid equivalent |

## Platform notes

- `TTMSFNCGrid`, `TTMSFNCGridDatabaseAdapter`, `TTMSFNCGridPDFIO` and `TTMSFNCGridPrintIO` are in the WEB package (`TMSFNCUIPackWEB.dpk`). On WEB the old grid has `LoadFromCSV`/`LoadFromFile`/streams, but `SaveToCSV`, `SaveToFile`, `SaveToHTML`, `SaveToXML` and `LoadXMLFromFile` are compiled out (`{$IFNDEF WEBLIB}`).
- **SpreadGrid is not available in TMS WEB Core.** `WEBLib.TMSFNCSpreadGrid*.pas` files exist and the class carries `[ComponentPlatformsAttribute(TMSPlatformsWeb)]`, but no SpreadGrid unit (nor `WEBLib.TMSFNCFormulaParser`) is in the WEB package. Treat it as VCL/FMX/LCL only.
- **`TTMSFNCGridToolBarPopup` is VCL/FMX/LCL only.** There is no `WEBLib.TMSFNCGridToolBarPopup.pas` (only an orphan Reg unit, not in the dpk), and its attribute is `TMSPlatforms`, not `TMSPlatformsWeb`.
- The formula parser takes its decimal and parameter separators from `FormatSettings`. Results are formatted with `Format(FloatFormat, ...)`, so locale matters on every platform.

## Does not exist / common mistakes

- Choosing `TTMSFNCGrid` for new work: use `TTMSFNCDataGrid`. Only `TTMSFNCSpreadGrid` (formulas) still needs the legacy base.
- `IF(A1>5, ...)`: there is no built-in `IF` and no `>`/`<`/`=` operators. Use `CHOOSE(LT(A1;5);elseValue;thenValue)`, or `IF` from `TTMSFNCStringMathLib`, which tests for the text `'1'`.
- `=SUM(A1,A2)` on a comma-decimal locale fails. `;` is the separator that always works.
- `ROUND(x;2)`: `ROUND` has one argument (integer rounding). Use `ROUNDUP(x;digits)` (MiscMathLib) or `FloatFormat`.
- `Calculate`, `RecalcAll`, `Recalculate`, `CalcAll`, `Grid.Formulas[c,r]`, `CellFormula[]`, `Values[]`: none exist. Use `Recalc`. The formula is in `Cells`, the result in `CalcValues`.
- Expecting `Cells[c,r]` to return the computed value: it returns the formula text. Read `CalcValues[c,r]` (variant, valid when `CalcStates[c,r] = csCalcOk`).
- Changing input cells in code and expecting dependents to refresh: call `Recalc`. `AutoRecalc` does not cover `Cells` assignments.
- `AddFunction`, `RegisterFunction`, `OnCustomFunction`, `OnGetFunctionValue`: use `OnIsCustomFunction` + `OnCalcCustomFunction` (one numeric argument) or a `TTMSFNCMathLib` descendant added via `Libs.Add.MathLib`.
- `Libs.Add(MyLib)`: `TLibBinderItems.Add` takes no parameter. Write `Libs.Add.MathLib := MyLib`.
- `TTMSFNCSpreadGrid.Sheets`, `ActiveSheet`, `Workbook`: there are no sheets. Use several grids plus `TTMSFNCGridBinder` and `Name!A1` references.
- Typing captions into row 0/column 0 with `AutoHeaders = True`: they are overwritten on row/column count changes. Set `AutoHeaders := False` or put captions in data cells (the demo does this).
- Old grid: `FixedColumnCount`/`FixedRowCount` don't exist (`FixedColumns`/`FixedRows`). DataGrid is the reverse. `ColCount`/`ColWidths` exist in neither.
- Old grid: `Sort(...)`, `SortSettings` don't exist. Use `SortData(Col, sdAscending)`. Click-sorting needs `Options.Sorting.Mode := gsmNormal`.
- Old grid: `Options.Filtering.Enabled` doesn't exist. Use `Options.Filtering.DropDown`.
- Old grid: `CellAppearance` doesn't exist (`Appearance`). DataGrid has no `Appearance`.
- `TTMSFNCGridDatabaseAdapter` showing nothing: set `Active := True` (default False).
- `TTMSFNCGridPDFIO.DataGrid` / `TTMSFNCDataGridPDFIO.Grid`: the old IO components use `Grid`, the DataGrid IO components use `DataGrid`. `TTMSFNCGridPDFIOReg` doesn't exist; it registers from `*.TMSFNCGridIOReg`.
