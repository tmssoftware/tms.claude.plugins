# Grouping (TTMSFNCDataGrid)

Grouping is done in code with `Group` / `Ungroup` on the grid (implemented in `TTMSFNCDataGridData`, unit `*.TMSFNCDataGridData`; the grid forwards to its root renderer). Group header rows are node rows (`grtNode`); summary rows are `grtSummary`. Visual drag-and-drop grouping is a zone inside `Header` (see below).

Units commonly needed: `VCL.TMSFNCDataGrid, VCL.TMSFNCDataGridData, VCL.TMSFNCDataGridCore, VCL.TMSFNCDataGridRenderer, VCL.TMSFNCDataGridCell` (prefix `FMX.` / `WEBLib.` on other platforms).

## Group / Ungroup

```delphi
procedure Group(AColumn: Integer); overload;
procedure Group(AColumns: TArray<Integer>; ASortColumns: TArray<Integer> = nil;
  ACustomGroupCallback: TTMSFNCDataGridDataGetCustomGroupCallback = nil;
  ACustomCompareCallback: TTMSFNCDataGridDataCustomCompareCallback = nil;
  AGroupOptionsCallback: TTMSFNCDataGridDataGetGroupOptionsCallback = nil;
  ASortOptionsCallback: TTMSFNCDataGridDataGetSortOptionsCallback = nil); overload;
procedure Group(AGroupInfo: TTMSFNCDataGridDataGroupInfo;
  ACustomGroupCallback: ... = nil; ACustomCompareCallback: ... = nil;
  AGroupOptionsCallback: ... = nil; ASortOptionsCallback: ... = nil); overload;
procedure Ungroup;
function IsGrouped: Boolean;
property GroupInfo: TTMSFNCDataGridDataGroupInfo read GetGroupInfo;  // read-only
```

Rules enforced by the source (`TTMSFNCDataGridData.Group`):
- If already grouped, nothing happens (log: "Grouping already applied, please ungroup first."). Call `Ungroup` before regrouping.
- If the data area has merged cells, nothing happens ("please split merged cells first"). Use `SplitCell` first.
- Rows are sorted by the grouped columns first (`Options.Grouping.AutoSort`, default True).

**Multi-level vs. multi-column — important:**
- `Group([8, 1])` = ONE level whose key combines columns 8 and 1 (values joined with `Options.Grouping.MergeDelimiter`, default `' ; '`).
- Nested levels need `TTMSFNCDataGridDataGroupInfo`, built with the global helpers:

```delphi
function CreateGroupInfo(AColumnsLevel0: TArray<Integer>): TTMSFNCDataGridDataGroupInfo; overload;
function CreateGroupInfo(AColumnsLevel0, AColumnsLevel1: TArray<Integer>): TTMSFNCDataGridDataGroupInfo; overload;
function CreateGroupInfo(AColumnsLevel0, AColumnsLevel1, AColumnsLevel2: TArray<Integer>): TTMSFNCDataGridDataGroupInfo; overload;
function CreateGroupAndSortInfo(AColumnsLevel0, ASortColumnsLevel0: TArray<Integer>; ...): TTMSFNCDataGridDataGroupInfo; overload; // up to 3 levels
```

`TTMSFNCDataGridDataGroupInfo` is a record: `Columns: TArray<Integer>; SubColumns: TArray<TTMSFNCDataGridDataGroupInfo>; SortColumns: TArray<Integer>; SortDirections: TArray<TTMSFNCDataGridSortDirection>`.

Demo (Multi-Column Grouping): level 0 = columns 4,5,7 combined, level 1 = column 11:

```delphi
TMSFNCDataGrid1.Options.Grouping.HideColumns := True;
TMSFNCDataGrid1.Group(CreateGroupInfo([4, 5, 7], [11]));
```

Basic demo (single column + summaries, toggle):

```delphi
if not FGrouped then
begin
  TMSFNCDataGrid1.Options.Grouping.MergeHeader := True;
  TMSFNCDataGrid1.Options.Grouping.Summary := True;
  TMSFNCDataGrid1.Group(1);
  TMSFNCDataGrid1.GroupSum(6);
  TMSFNCDataGrid1.GroupAverage(5);
end
else
  TMSFNCDataGrid1.Ungroup;
```

## Options.Grouping (TTMSFNCDataGridDataGroupingOptions)

| Property | Type / default | Meaning |
|---|---|---|
| `AutoSort` | Boolean, True | sort by grouped columns before grouping |
| `CalculationFormat` | string, `'%g'` | format for calc results |
| `CalculationFormatType` | `gcfNumber` (Format) / `gcfFloat` (FormatFloat) | |
| `HeaderHeight` | Double, 30 | group header row height |
| `HideColumns` | Boolean, False | hide grouped columns (restored by Ungroup) |
| `MergeDelimiter` | string, `' ; '` | joins multi-column keys |
| `MergeHeader` | Boolean, True | merge header row across columns (not when Summary and SummaryInHeader both True) |
| `MergeSummary` | Boolean, False | merge calc result cell from first non-fixed column |
| `Summary` | Boolean, True | add summary row below each group |
| `SummaryHeight` | Double, 30 | |
| `SummaryInHeader` | Boolean, False | put results in the group header row instead |
| `UseFirstRowAsHeader` | Boolean, True | prefix header with row-0 caption, e.g. `Country: Belgium` |

Set options **before** calling `Group`. Per-level overrides: `OnGetGroupOptions` / `AGroupOptionsCallback` receive `var AOptions: TTMSFNCDataGridDataGroupOptions` (record with the same fields: AutoSort, HeaderHeight, HideColumns, MergeDelimiter, MergeHeader, ...).

## Custom group text

```delphi
TTMSFNCDataGridDataGetCustomGroupEvent = procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AData: TTMSFNCDataGridCellValue; ALevel: Integer; var AGroup: string) of object;
property OnGetCustomGroup: TTMSFNCDataGridDataGetCustomGroupEvent;
// callback form: TTMSFNCDataGridDataGetCustomGroupCallback = reference to procedure(ACell; AData; ALevel; var AGroup: string)
```

`AGroup` is both the grouping key and header text; returning the same string for different values buckets them (demo: age ranges). HTML is allowed:

```delphi
procedure TForm1.TMSFNCDataGrid1GetCustomGroup(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AData: TTMSFNCDataGridCellValue; ALevel: Integer; var AGroup: string);
var i: Integer;
begin
  if ACell.Column = 4 then
    AGroup := '<img src="graph.svg" height="95%"/> ' + AGroup   // image from BitmapContainer
  else if ACell.Column = 5 then
  begin
    i := TMSFNCDataGrid1.ValueToInteger(AData) div 10;
    AGroup := Format('Age Group: %d - %d', [i * 10, (i + 1) * 10]);
  end;
end;
```

## Group summaries / aggregates

Shortcut methods (call AFTER `Group`). Signatures **on `TTMSFNCDataGrid`** (`*.TMSFNCDataGrid.pas`), which differ from the ones on `TTMSFNCDataGridData`:

```delphi
// GroupAverage is the exception: its single-column overload takes NO callback on the grid
procedure GroupAverage(AColumn: Integer); overload;
procedure GroupAverage(AColumns: TArray<Integer>; ACalculationOptionsCallback: TTMSFNCDataGridDataGetColumnCalculationOptionsCallback = nil); overload;

// all the others accept an optional callback in both overloads
procedure GroupSum(AColumn: Integer; ACalculationOptionsCallback: TTMSFNCDataGridDataGetColumnCalculationOptionsCallback = nil); overload;
procedure GroupSum(AColumns: TArray<Integer>; ACalculationOptionsCallback: ... = nil); overload;
// same shape as GroupSum: GroupCount, GroupMin, GroupMax, GroupDistinct, GroupStandardDeviation
procedure GroupCustomCalculation(AColumn: Integer; ACalculationOptionsCallback: ... = nil;
  ACustomCalculationCallback: TTMSFNCDataGridDataCustomColumnCalculationCallback = nil); overload;
procedure GroupCalculation(AColumn: Integer; AMethod: TTMSFNCDataGridDataCalculationMethod;
  ACalculationOptionsCallback: ... = nil; ACustomCalculationCallback: ... = nil); overload;
```

**Callbacks: assign them to typed variables first.** An anonymous method written inline in a call to an overloaded method (`Group`, `GroupAverage`, `GroupSum`, ...) often fails with "There is no overloaded version of ... that can be called with these arguments", because the compiler can't pick the overload from an untyped anonymous method. Declare a variable of the callback type, assign the anonymous method to it, and pass the variable. For an average with formatting, use the array overload:

```delphi
var
  avgFmt: TTMSFNCDataGridDataGetColumnCalculationOptionsCallback;
  groupText: TTMSFNCDataGridDataGetCustomGroupCallback;
begin
  groupText :=
    procedure(ACell: TTMSFNCDataGridCellCoord; AData: TTMSFNCDataGridCellValue; ALevel: Integer; var AGroup: string)
    begin
      AGroup := 'Region: ' + AGroup;
    end;
  Grid.Group([COL_REGION], nil, groupText);       // array overload; nil = default sort columns

  avgFmt :=
    procedure(AColumn: Integer; ALevel: Integer; var AOptions: TTMSFNCDataGridDataColumnCalculationOptions)
    begin
      AOptions.CalculationFormatType := gcfNumber;
      AOptions.CalculationFormat := 'avg %.1f %%';
    end;
  Grid.GroupAverage([COL_MARGIN], avgFmt);         // NOT GroupAverage(COL_MARGIN, avgFmt)
end;
```

`GroupSort(AColumn, gsdDescending)` sorts rows inside each group after grouping (e.g. "Revenue descending within each region").

`TTMSFNCDataGridDataCalculationMethod = (gcmSum, gcmAverage, gcmMin, gcmMax, gcmCount, gcmCustom, gcmDistinct, gcmStandardDeviation)`.

Callback types:
```delphi
TTMSFNCDataGridDataGetColumnCalculationOptionsCallback = reference to procedure(AColumn: Integer; ALevel: Integer;
  var AOptions: TTMSFNCDataGridDataColumnCalculationOptions);
// AOptions fields: CalculationFormatType, CalculationFormat: string, MergeSummary, SummaryInHeader
TTMSFNCDataGridDataCustomColumnCalculationCallback = reference to function(AColumn, ALevel, AFromRow, AToRow: Integer): Double;
```

### Persistent, named calculations: ColumnCalculations

```delphi
property ColumnCalculations[AColumn: Integer; AName: string]: TTMSFNCDataGridDataColumnCalculationArray;
function CreateGroupColumnCalculation(AMethod; ACalculationOptionsCallback = nil; ACustomCalculationCallback = nil;
  AFromRow = -1; AToRow = -1; AOutputRow = -1): TTMSFNCDataGridDataColumnCalculation;  // per group
function CreateNormalColumnCalculation(AMethod; ...same...): TTMSFNCDataGridDataColumnCalculation;  // whole column
function CreateColumnCalculation(AMethod; AType: TTMSFNCDataGridDataColumnCalculationType = gctNormal; ...);  // gctNormal / gctGroup
procedure UpdateCalculations;   // re-run all column/row calculations
```

`AOutputRow = -1`: normal calc writes to the **first fixed bottom row** (nothing if `FixedBottomRowCount = 0`); group calc writes to the group's summary (or header) row. `AName` is a key; several calculations can coexist per column. Demo (level-dependent format):

```delphi
TMSFNCDataGrid1.RowCount := TMSFNCDataGrid1.RowCount + 2;
TMSFNCDataGrid1.FixedBottomRowCount := 2;
TMSFNCDataGrid1.Group(CreateGroupInfo([4, 5, 7], [11]));

TMSFNCDataGrid1.ColumnCalculations[3, 'Total Count'] := [CreateGroupColumnCalculation(gcmCount,
  procedure(AColumn: Integer; ALevel: Integer; var AOptions: TTMSFNCDataGridDataColumnCalculationOptions)
  begin
    case ALevel of
      0: AOptions.CalculationFormat := 'Count: %g';
      1: AOptions.CalculationFormat := 'Sub-Count: %g';
    end;
  end)];

TMSFNCDataGrid1.ColumnCalculations[9, 'Sum'] := [
  CreateNormalColumnCalculation(gcmSum,
    procedure(AColumn: Integer; ALevel: Integer; var AOptions: TTMSFNCDataGridDataColumnCalculationOptions)
    begin AOptions.CalculationFormat := 'Total Sum: $%.2f'; end),
  CreateNormalColumnCalculation(gcmMax,
    procedure(AColumn: Integer; ALevel: Integer; var AOptions: TTMSFNCDataGridDataColumnCalculationOptions)
    begin AOptions.CalculationFormat := '<br>The Maximum: $%.2f'; end)];

TMSFNCDataGrid1.Options.Calculations.IncludeHiddenRows := False;  // default True
```

`Options.Calculations` also has `AutoUpdate` (default **False**) and `IncludeHiddenColumns`. With AutoUpdate False, call `UpdateCalculations` yourself after edits/filters — demo does it in `OnAfterApplyFilter`, `OnAfterCloseInplaceEditor`, `OnCellCheckBoxChange`.

Typical guard so users cannot edit node/summary rows:
```delphi
procedure TForm1.TMSFNCDataGrid1CanEditCell(Sender: TObject; AColumn, ARow: Integer; var ACanEdit: Boolean);
begin
  ACanEdit := TMSFNCDataGrid1.RowTypes[ARow] = grtDefault;
end;
```

## Expand / collapse (node rows)

```delphi
procedure ExpandAllNodes;    procedure CollapseAllNodes;
procedure ExpandNode(ARow: Integer);   procedure CollapseNode(ARow: Integer);
procedure ToggleNode(ARow: Integer);
function IsRowNode(ARow: Integer): Boolean;   function IsRowSummary(ARow: Integer): Boolean;
property RowNodeState[ARow: Integer]: TTMSFNCDataGridRowNodeState;   // grnsCollapsed, grnsExpanded
property RowNodeLevel[ARow: Integer]: Integer;
property RowNodeChildCount[ARow: Integer]: Integer;
property RowTypes[ARow: Integer]: TTMSFNCDataGridRowType;   // grtDefault, grtSummary, grtNode, grtFilter
```

Events: `OnRowExpand`, `OnRowCollapse` (`procedure(Sender: TObject; ARow: Integer)`); cell-level `OnCellBeforeNodeExpand/Collapse` (`ACell: TTMSFNCDataGridCellCoord; var ACanExpand/ACanCollapse: Boolean`) and `OnCellAfterNodeExpand/Collapse` (`ACell`).

Manual (non-grouping) tree rows — see cell-controls.md (Grid in Grid):
```delphi
procedure AddNodeRow(ARow: Integer; AChildCount: Integer; ALevel: Integer = 0; AMerge: Boolean = True);
procedure SetNodeRow(ARow: Integer; AChildCount: Integer; ALevel: Integer = 0; AMerge: Boolean = True);
procedure ClearNodeRow(ARow: Integer);   procedure RemoveNodeRow(ARow: Integer);
```

Styling node/summary rows: `CellAppearance.GroupLayout`, `CellAppearance.SummaryLayout` (`TTMSFNCDataGridCellLayout`).

Sorting inside groups without reordering groups: `GroupSort(AColumn; ADirection: TTMSFNCDataGridSortDirection)` / `GroupSort(AColumns; ADirections; ...)`.

## Visual grouping (drag columns to a group zone)

It is part of `Header` (not a separate panel component):

```delphi
property Header: TTMSFNCDataGridHeader;             // Header.Visible default False
Header.VisualGrouping: TTMSFNCDataGridHeaderVisualGrouping
  // Visible (True), Dragging (True), SortOnClick (True), CloseIndicator (True),
  // ConnectionLines (True), ConnectionStroke, Layout, AutoSize, Size (30),
  // LevelIndicationFill/Stroke, LevelActiveIndicationFill/Stroke
Header.Bar: TTMSFNCDataGridHeaderFooterBar           // Visible (False), Size, Fill, Stroke, Buttons
```

Requirements for drag-to-group: `Header.Visible := True`, `Header.VisualGrouping.Visible` and `.Dragging` True, `Options.Mouse.ColumnDragging := True` (default False), and `gcdmVisualGrouping in Options.Mouse.ColumnDragModes` (default `[gcdmReorder, gcdmVisualGrouping]`). Up to three nested levels. Grouping done in code (`Group(...)`) is reflected as chips.

Demo (Visual Grouping), including toolbar buttons in the header bar:

```delphi
TMSFNCDataGrid1.Group(CreateGroupInfo([4, 5, 7], [11]));
TMSFNCDataGrid1.Header.Visible := True;
TMSFNCDataGrid1.Options.Mouse.ColumnDragging := True;
TMSFNCDataGrid1.Header.Bar.Visible := True;
TMSFNCDataGrid1.Header.Bar.Size := 35;

btn := TMSFNCDataGrid1.Header.Bar.Buttons.Add;   // TTMSFNCDataGridButton
btn.OnClick := DoCollapseClick;   // calls CollapseAllNodes
btn.Width := 100;
btn.Text := 'Collapse';
// ...same for Expand (ExpandAllNodes) and Ungroup (Ungroup)
```

`TTMSFNCDataGridButton` published: `Name, Hint, Text, Bitmap, Width, Enabled, Visible, OnClick, Control`; public: `Callback: TProc`, `Data*` tags.

Visual grouping events (all `AColumn: Integer`): `OnCanDragHeaderGroup(var ACanDrag)`, `OnBeforeDropHeaderGroup(var ACanDrop)`, `OnAfterDropHeaderGroup`, `OnBeforeSortHeaderGroup(var ACanSort)`, `OnAfterSortHeaderGroup`, `OnBeforeCloseHeaderGroup(var ACanClose)`, `OnAfterCloseHeaderGroup`, `OnHeaderGroupClick`; `OnCustomizeHeaderGroup(AHeaderGroup: TTMSFNCDataGridHeaderGroup)`; drawing: `OnBefore/AfterDrawHeaderGroup`, `OnBefore/AfterDrawHeaderGroupLevel`. `OnGroup` / `OnUngroup` (TNotifyEvent) fire **only for grouping through the visual zone**, not for `Group()` in code. Read-only: `HeaderGroups`, `XYToHeaderGroup(X, Y)`.

## Platform notes

Identical API on VCL/FMX/WEB. WEB demos load CSV with `LoadFromCSVData('train.csv', TEncoding.UTF8)`. Anonymous-method callbacks are used identically in the WEB demos.

## Does not exist / common mistakes

- `GroupColumn` property (TAdvStringGrid) — use `Group(AColumn)`; read state with `IsGrouped` / `GroupInfo`.
- `ExpandAll` / `ContractAll` / `ContractNode` / `ExpandRow` — use `ExpandAllNodes`, `CollapseAllNodes`, `CollapseNode`, `ExpandNode`, `ToggleNode`.
- `GroupPanel`, `GroupingPanel`, `OnGroupDrop` — use `Header.VisualGrouping` + `OnAfterDropHeaderGroup`.
- `Group([a, b])` is not two levels — use `CreateGroupInfo([a], [b])`.
- Calling `Group` twice to change grouping silently does nothing — `Ungroup` first.
- `GroupSum` etc. before `Group` — must be after.
- `Grid.GroupAverage(ACol, ACallback)` — the grid has no such overload; use `Grid.GroupAverage([ACol], ACallback)`.
- Inline anonymous methods passed straight into `Group` / `Group*` calls — assign them to a typed callback variable first (see above).
- Expecting `OnGroup` after `Group()` in code — it only fires for visual grouping.
- `Options.Grouping.Summary` already defaults to True; `MergeHeader` defaults to True.
