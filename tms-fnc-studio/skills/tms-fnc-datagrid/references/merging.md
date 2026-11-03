# Cell merging / splitting (TTMSFNCDataGrid)

Merging is per-cell merge info stored in the data layer (`TTMSFNCDataGridData`); the grid methods forward to `Root`. The top-left cell of a merged block is the **base cell**: value, layout, editing and controls live there.

Coordinate helpers (unit `*.TMSFNCDataGridCore`):
```delphi
function MakeCell(AColumn, ARow: Integer): TTMSFNCDataGridCellCoord;
function MakeCellRange(AStartColumn, AStartRow, AStopColumn, AStopRow: Integer): TTMSFNCDataGridCellCoordRange;
// TTMSFNCDataGridCellCoordRange = record StartCell, StopCell: TTMSFNCDataGridCellCoord; end;
// TTMSFNCDataGridCellCoord has Column, Row properties
```

## Merge API (grid)

```delphi
procedure MergeCells(AColumn, ARow, AColumnCount, ARowCount: Integer);   // count-based, NOT end coordinates
procedure MergeRange(ARange: TTMSFNCDataGridCellCoordRange);              // inclusive Start..Stop
procedure MergeColumn(AColumn: Integer);            // = MergeColumns(AColumn, 1)
procedure MergeColumns(AColumn, ACount: Integer);
procedure MergeRow(ARow: Integer);                  // = MergeRows(ARow, 1)
procedure MergeRows(ARow, ACount: Integer);
procedure SplitCell(ACell: TTMSFNCDataGridCellCoord);
function CanMergeCells(AColumn, ARow, AColumnCount, ARowCount: Integer): Boolean;
function BaseCell(ACell: TTMSFNCDataGridCellCoord): TTMSFNCDataGridCellCoord;
function IsCellMerged(ACell: TTMSFNCDataGridCellCoord): Boolean;
function IsColumnMerged(AColumn: Integer): Boolean;
function IsRowMerged(ARow: Integer): Boolean;
property MergedColumns[AColumn: Integer]: Boolean;  // flags maintained by MergeCells/SplitCell
property MergedRows[ARow: Integer]: Boolean;
```

Behaviour (from `TTMSFNCDataGridData.MergeCells` / `SplitCell` source):
- `MergeCells` overlapping an existing merge **extends** it: the result is the bounding box of the new range and every merge it touches.
- Otherwise `CanMergeCells` must pass: every cell in range valid (inside `ColumnCount`/`RowCount`) and all cells of the **same area type** (normal, fixed, fixed root, freeze root). You cannot merge a header (fixed) cell with a data cell. On failure nothing happens and a warning is logged (no exception).
- `SplitCell` accepts **any** cell of the merged block (it uses the stored offsets), not only the base cell. Calling it on a non-merged cell logs a warning.
- There is no "split all" method; loop over cells and call `SplitCell` where `IsCellMerged`.

## Demo (Basic\Merging)

```delphi
procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCDataGrid1.FixedColumnCount := 1;
  TMSFNCDataGrid1.Options.IO.StartRow := 1;
  TMSFNCDataGrid1.Options.IO.StartColumn := 1;
  TMSFNCDataGrid1.LoadFromCSVData('CARS.csv');
  TMSFNCDataGrid1.Options.Selection.Mode := gsmCellRange;   // lets the user select a block
  TMSFNCDataGrid1.MergeCells(3, 3, 3, 3);    // col 3,row 3, 3 cols x 3 rows
  TMSFNCDataGrid1.MergeCells(7, 10, 2, 4);
end;

procedure TForm1.MergeButtonClick(Sender: TObject);
begin
  TMSFNCDataGrid1.MergeRange(TMSFNCDataGrid1.Selection);    // Selection: TTMSFNCDataGridCellCoordRange
end;

procedure TForm1.SplitButtonClick(Sender: TObject);
begin
  TMSFNCDataGrid1.SplitCell(TMSFNCDataGrid1.Selection.StartCell);
end;
```

Merging fixed header cells (Grid in Grid demo) — a two-column header caption:
```delphi
TMSFNCDataGrid1.Columns[4].Header := 'More <b>HTML</b>';
TMSFNCDataGrid1.MergeCells(4, 0, 2, 1);   // row 0 is fixed; both cells fixed -> allowed
```

Reading/writing a merged block — always go through the base cell:
```delphi
var c: TTMSFNCDataGridCellCoord;
c := TMSFNCDataGrid1.BaseCell(MakeCell(ACol, ARow));
TMSFNCDataGrid1.Cells[c.Column, c.Row] := 'Merged text';
```

## Interaction with other features

- **Grouping refuses to run** when the data area contains merged cells (log: "please split merged cells first"). Split before `Group`. Grouping itself creates merged node rows (`Options.Grouping.MergeHeader`, `AddNodeRow(..., AMerge = True)`); `Ungroup` / `ClearNodeRow` split them.
- **Moving/inserting/deleting**: `CanMoveColumn`/`CanMoveRow` return False for merged columns/rows; `CanInsertColumn/Row`, `CanDeleteColumn/Row` return False when a merge spans that index.
- **Calculations** only count the base cell of a merged range.
- **Controls / sub-grids** in a merged area: place them on the base cell; the control or nested grid gets the whole merged rect. Grid in Grid demo: `g := AddGrid(1, idx); ... MergeCells(1, m, 1, 5);` and Cell Controls demo: `MergeCells(2, 9, 4, 5); g := AddGrid(2, 9);` — either order works.

## Caveat: MergeColumn(s) / MergeRow(s) ranges

From source:
```delphi
procedure TTMSFNCDataGridData.MergeColumns(AColumn, ACount: Integer);
begin
  MergeCells(AColumn, FixedRowCount, ACount, RowCount - FixedBottomRowCount);
end;
procedure TTMSFNCDataGridData.MergeRows(ARow, ACount: Integer);
begin
  MergeCells(FixedColumnCount, ARow, ColumnCount - FixedRightColumnCount, ACount);
end;
```
The row (column) **count** passed is `RowCount - FixedBottomRowCount` starting at `FixedRowCount`, so with `FixedRowCount > 0` (or `FixedColumnCount > 0` for MergeRows) the range runs past the last row/column, `CanMergeCells` fails, and nothing is merged (warning only). With a fixed header row, prefer the explicit form:

```delphi
// merge all data rows of column C
Grid.MergeCells(C, Grid.FixedRowCount, 1, Grid.RowCount - Grid.FixedRowCount - Grid.FixedBottomRowCount);
// merge all data columns of row R
Grid.MergeCells(Grid.FixedColumnCount, R, Grid.ColumnCount - Grid.FixedColumnCount - Grid.FixedRightColumnCount, 1);
```

## Platform notes

Same API on VCL, FMX and WEB (WEB demo only differs in `LoadFromCSVData('CARS.csv', TEncoding.UTF8)`).

## Does not exist / common mistakes

- `MergeCells(ACol1, ARow1, ACol2, ARow2)` with end coordinates — the 3rd/4th params are **counts**. Use `MergeRange(MakeCellRange(c1, r1, c2, r2))` for corner coordinates.
- `SplitCells(c, r)` (TAdvStringGrid), `UnMergeCells`, `SplitAllCells`, `UnmergeAll` — only `SplitCell(ACell: TTMSFNCDataGridCellCoord)` exists; pass `MakeCell(c, r)`.
- `IsMergedCell(c, r)` / `IsBaseCell` / `CellSpan` — use `IsCellMerged(MakeCell(c, r))` and `BaseCell(...)`.
- Writing `MergedColumns[]`/`MergedRows[]` to create a merge — they are bookkeeping flags; use `MergeCells`.
- Auto-merging equal values (`MergeSameValues`, `AutoMerge`) — not a feature; compute runs yourself and call `MergeCells`.
- Merging a fixed header cell together with data cells — rejected by `CanMergeCells`.
