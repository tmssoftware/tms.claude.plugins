# Filter row (TTMSFNCDataGrid)

The "filter row" is part of the core filtering (`Options.Filtering`, `*.TMSFNCDataGridData`), not a separate component. A **fixed** row (chosen by `Options.Filtering.Row`) shows per-column filter controls: a drop-down button (`gfcButton`, checklist popup) and/or an inline editor panel (`gfcEditor`: edit box + filter-type button + clear button). Filtering in code uses the same `Filter` collection.

## Options.Filtering (TTMSFNCDataGridDataFilteringOptions)

| Property | Default | Meaning |
|---|---|---|
| `Enabled: Boolean` | False | show filter controls in row `Row` (code filtering works regardless) |
| `Row: Integer` | 0 | fixed row hosting the controls; use FixedRowCount 2 + Row 1 to keep captions visible |
| `Controls: TTMSFNCDataGridDataFilterControls` | `[gfcButton]` | `gfcButton`, `gfcEditor` |
| `MultiColumn: Boolean` | False | drop-down pick keeps other columns' filters (otherwise clears all rules first) |
| `HideEmptyGroups: Boolean` | False | hide header/summary rows of groups with no matching rows |
| `Advanced: Boolean` | False | use filter-builder expression instead of `Filter`; filter row controls are then **not shown** |
| `Actions` | `[gdfaHideRow]` | `gdfaHideRow`, `gdfaExecuteActions`, `gdfaApplyAppearance` |
| `TrimValues: Boolean` | True | trim cell text before comparing |
| `DropDownWidth/DropDownHeight` | 200 / 280 | popup size |
| `Rows` | `gfrNormal` | (`gfrAll`) — not evaluated by the data grid drop-down currently |

A filter editor cell is created only when `Enabled`, not `Advanced`, the cell is in `Options.Filtering.Row`, and the column is between the fixed left/right columns.

## Setup (Advanced\Filter Row demo)

```delphi
procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCDataGrid1.BeginUpdate;
  TMSFNCDataGrid1.FixedColumnCount := 1;
  TMSFNCDataGrid1.Options.IO.StartRow := 1;
  TMSFNCDataGrid1.Options.IO.StartColumn := 1;
  TMSFNCDataGrid1.LoadFromCSVData('CARS.csv');
  TMSFNCDataGrid1.Cells[1, 0] := 'Brand';
  // ... captions for other columns ...

  TMSFNCDataGrid1.FixedRowCount := 2;      // row 0 = captions, row 1 = filter row
  TMSFNCDataGrid1.InsertRow(1);
  TMSFNCDataGrid1.Options.Column.Stretching.Enabled := True;
  TMSFNCDataGrid1.Options.Filtering.Enabled := True;
  TMSFNCDataGrid1.Options.Filtering.Row := 1;
  TMSFNCDataGrid1.Options.Filtering.Controls := [gfcButton, gfcEditor];
  TMSFNCDataGrid1.Options.Filtering.MultiColumn := True;

  TMSFNCDataGrid1.Group([8, 1]);           // filter row works on grouped data too (one level keyed on cols 8+1)
  TMSFNCDataGrid1.EndUpdate;
end;
```

## Per-column filter-row settings (TTMSFNCDataGridColumn)

```delphi
property FilterButton: Boolean default True;                                   // gcsFilterButton
property FilterEditor: Boolean default False;                                  // gcsFilterEditor
property FilterEditorType: TTMSFNCDataGridFilterEditorType default gfetAutomatic; // gcsFilterEditorType
property FilterDefaultType: TTMSFNCDataGridDataFilterType default gftEqual;    // gcsFilterDefaultType
```
These only take effect when the matching setting is in `Columns[i].Settings`; at **runtime call `AddSetting`** (auto-added only at design time). Without the setting, every column follows `Options.Filtering.Controls`.

```delphi
// no inline editor for column 0, numeric editor with ">=" default for column 7
TMSFNCDataGrid1.Columns[0].AddSetting(gcsFilterEditor);
TMSFNCDataGrid1.Columns[0].FilterEditor := False;
TMSFNCDataGrid1.Columns[7].AddSetting(gcsFilterEditorType);
TMSFNCDataGrid1.Columns[7].FilterEditorType := gfetFloat;
TMSFNCDataGrid1.Columns[7].AddSetting(gcsFilterDefaultType);
TMSFNCDataGrid1.Columns[7].FilterDefaultType := gftLargerOrEqualThan;
```

`TTMSFNCDataGridFilterEditorType = (gfetAutomatic, gfetString, gfetBoolean, gfetDateTime, gfetFloat, gfetNumber, gfetCustom)`. Default comparison of the inline editor when no `gcsFilterDefaultType`: `gftContains` for string/custom/automatic, `gftEqual` for boolean/datetime/float/number. (Drop-down popup default is `gftEqual`.)

Manual editor cells: `AddFilterEditor(AColumn, ARow)` / `RemoveFilterEditor(AColumn, ARow)` (+ `ACell` overloads), `FilterEditors[AColumn, ARow]: TTMSFNCDataGridCellControl` (read-only), `HasFilterEditor[AColumn, ARow]: Boolean`.

Filter-row events:
```delphi
OnBeforeCreateFilterEditor: procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; var ACanCreate: Boolean) of object;
OnAfterCreateFilterEditor:  procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; AEditor: TTMSFNCDataGridCellControl) of object;
OnCreateCustomFilterEditor: function(Sender: TObject; ACell: TTMSFNCDataGridCellCoord): TTMSFNCDataGridCellControl of object;   // for gfetCustom
OnCustomizeFilterPopupEditor: procedure(Sender: TObject; AColumn: Integer; var AEditor: TTMSFNCDataGridCellControl) of object;
OnBeforeApplyFilter: procedure(Sender: TObject; AColumn: Integer; var ACondition: string; var ACanApply: Boolean) of object;
OnAfterApplyFilter:  procedure(Sender: TObject; AColumn: Integer; ACondition: string) of object;
```
Also: `OnBeforeShowFilter`, `OnAfterShowFilter`, `OnNeedFilterDropDownData`, `OnRemoveFilter`.

## Filtering in code (same engine)

```delphi
property Filter: TTMSFNCDataGridDataFilter;      // collection of TTMSFNCDataGridDataFilterData
procedure ApplyFilter;      // re-evaluates Filter, hides non-matching rows
procedure RemoveFilter;     // shows all rows again; rules in Filter are KEPT (implementation only clears the filtered-row list)
procedure ClearFilter;      // empties Filter and FilterBuilder too, then shows all rows
function GetFilterTypeName(AType: TTMSFNCDataGridDataFilterType): string;
```
`Filter` members: `ColumnFilter[AColumn]: TTMSFNCDataGridDataFilterData` (**reading creates a rule** if none — use `HasFilter(AColumn)` to test), `Add(AColumn; ACondition: string; AOperation = gfoNone; ACaseSensitive = False)`, `Add(AColumn; AType: TTMSFNCDataGridDataFilterType; AValue: TTMSFNCDataGridCellValue; AOperation = gfoNone; ACaseSensitive = False)`, `RemoveColumnFilter(AColumn)`, `Clear`, `Parse(AColumn; AFilterText)`.
`TTMSFNCDataGridDataFilterData`: `Column`, `Condition: string`, `&Type: TTMSFNCDataGridDataFilterType`, `CaseSensitive`, `FilterCondition`.

```delphi
TTMSFNCDataGridDataFilterType = (gftStartsWith, gftEndsWith, gftContains, gftNotContains, gftEqual, gftNotEqual,
  gftEmpty, gftNotEmpty, gftLargerThan, gftSmallerThan, gftLargerOrEqualThan, gftSmallerOrEqualThan);
TTMSFNCDataGridDataFilterTextType   = gftStartsWith..gftNotEmpty;
TTMSFNCDataGridDataFilterNumberType = gftEqual..gftSmallerOrEqualThan;
```

Demo: external edit boxes driving filters alongside the filter row:
```delphi
procedure TForm1.Edit1ChangeTracking(Sender: TObject);
var fltr: TTMSFNCDataGridDataFilterData;
begin
  TMSFNCDataGrid1.RemoveFilter;
  if Edit1.Text <> '' then
  begin
    fltr := TMSFNCDataGrid1.Filter.ColumnFilter[1];
    fltr.CaseSensitive := False;
    fltr.&Type := gftContains;
    fltr.Condition := Edit1.Text;
  end;
  TMSFNCDataGrid1.ApplyFilter;
end;

// populate a type combo with the number subrange
for I := Low(TTMSFNCDataGridDataFilterNumberType) to High(TTMSFNCDataGridDataFilterNumberType) do
  ComboBox1.Items.Add(TMSFNCDataGrid1.GetFilterTypeName(I));
// map ItemIndex back (subrange does not start at 0!):
fltr.&Type := TTMSFNCDataGridDataFilterNumberType(ComboBox1.ItemIndex + Ord(Low(TTMSFNCDataGridDataFilterNumberType)));
```
Note: the demo's `ComboBox1Change` casts `ItemIndex` directly (off by `Ord(gftEqual)` = 4); the `Edit2ChangeTracking` handler subtracts `Integer(Low(...))`, which is also off. Correct mapping is `ItemIndex + Ord(Low(TTMSFNCDataGridDataFilterNumberType))`.

Toggling HideEmptyGroups requires re-filtering:
```delphi
TMSFNCDataGrid1.Options.Filtering.HideEmptyGroups := CheckBox2.Checked;
TMSFNCDataGrid1.RemoveFilter;
TMSFNCDataGrid1.ApplyFilter;
```

With calculations/grouped summaries, call `UpdateCalculations` in `OnAfterApplyFilter` (and set `Options.Calculations.IncludeHiddenRows := False` to aggregate only visible rows).

Row type: `grtFilter` exists in `TTMSFNCDataGridRowType`, but setting `Options.Filtering.Row` does not assign it (the source only reads it in `IsRowFilter`). To detect the filter row in your own events compare `ARow = Grid.Options.Filtering.Row`.

## Platform notes

- FMX: `TCheckBox.IsChecked`, `Edit1.SetFocus` (demo); VCL `TCheckBox.Checked`, `ActiveControl := Edit1`.
- WEB: `LoadFromCSVData('CARS.csv', TEncoding.UTF8)`; otherwise identical.
- With a database adapter in `afmAdapter` filter mode the filter is passed to the dataset; `Options.Filtering.Actions` must include `gdfaHideRow` or `ApplyFilter` raises.

## Does not exist / common mistakes

- `FilterRow`, `ShowFilterRow`, `FilterRowVisible`, `Options.Filtering.FilterRow`, `FilterBar` — use `Options.Filtering.Enabled` + `Row` + `Controls := [..., gfcEditor]`.
- Pointing `Options.Filtering.Row` at a data (non-fixed) row, or leaving `Row := 0` and losing the column captions — add a fixed row (`FixedRowCount := 2; InsertRow(1); Row := 1`).
- Expecting `RemoveFilter` to delete rules (despite its summary text) — it only unhides rows; use `ClearFilter` or `Filter.RemoveColumnFilter(AColumn)` then `ApplyFilter`.
- Reading `Filter.ColumnFilter[c]` just to check for a filter — it creates an empty rule; use `Filter.HasFilter(c)`.
- Setting `Columns[i].FilterEditorType` / `FilterDefaultType` at runtime without `AddSetting(...)` — ignored.
- `Options.Filtering.Advanced := True` hides the filter row controls.
- `gftGreaterThan` / `gftLessThan` / `gftBeginsWith` — real names are `gftLargerThan`, `gftSmallerThan`, `gftStartsWith` (conditional formatting uses `gfcGreater`/`gfcBeginsWith` — different enum).
