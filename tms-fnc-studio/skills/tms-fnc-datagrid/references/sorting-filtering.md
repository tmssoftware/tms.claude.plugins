# TMS FNC DataGrid – sorting and filtering

Verified against `*.TMSFNCDataGridData.pas`, `*.TMSFNCDataGridCore.pas`, `*.TMSFNCDataGridRenderer.pas`,
`*.TMSFNCDataGrid.pas` and the Basic `Sorting`/`Filtering` and Advanced `Filter Row` demos
(identical in VCL/FMX/WEB). Units: see core-api.md. Sort enums are in `*DataGridCore`; filter classes
and enums are in `*DataGridData`.

## Sorting

### Options (`Options.Sorting: TTMSFNCDataGridDataSortingOptions`)
```delphi
property Enabled: Boolean default False;          // True = clicking a header cell sorts
property Row: Integer default 0;                  // fixed row that reacts to clicks and shows the indicator
property Direction: TTMSFNCDataGridSortDirection default gsdAscending;  // default for calls without a direction
property Format: TTMSFNCDataGridSortFormat default gsfAutomatic;
property CaseSensitive: Boolean default True;     // case-SENSITIVE by default
```
```delphi
TTMSFNCDataGridSortDirection = (gsdNone, gsdAscending, gsdDescending);
TTMSFNCDataGridSortFormat = (gsfAutomatic, gsfAlphabetic, gsfNumeric, gsfDateTime, gsfBoolean, gsfCustom);
```
`gsfAutomatic` detects the type for each pair of values: Boolean, then numeric (also numeric strings),
then date/time (using the format settings, and ISO-8601 where supported), else alphabetic.

Header-click behaviour (from `DoCellClick`): clicking a fixed cell in `Options.Sorting.Row` toggles
ascending and descending. **Shift+click adds the column to a multi-column sort.** A plain click replaces
the sort. If the grid is grouped, the sort runs inside each group.
Indicator look: `SortIndicatorAppearance` (`IndexFont`, `IndexFill`, `IndexStroke`, `GlyphSize`);
icons are `Icons.SortAscendingIcon` and `Icons.SortDescendingIcon`.

### Programmatic sort
```delphi
procedure Sort(AColumn: Integer; ADirection: TTMSFNCDataGridSortDirection); overload;
procedure Sort(AColumn: Integer; ADirection: TTMSFNCDataGridSortDirection; AFromRow, AToRow: Integer); overload;
procedure Sort(AColumns: TArray<Integer>; ADirections: TArray<TTMSFNCDataGridSortDirection>;
  ACustomCompareCallback: TTMSFNCDataGridDataCustomCompareCallback = nil;
  ASortOptionsCallback: TTMSFNCDataGridDataGetSortOptionsCallback = nil); overload;
procedure Sort(AColumns: TArray<Integer>; ADirections: TArray<TTMSFNCDataGridSortDirection>;
  AFromRow, AToRow: Integer; ACustomCompareCallback: TTMSFNCDataGridDataCustomCompareCallback = nil;
  ASortOptionsCallback: TTMSFNCDataGridDataGetSortOptionsCallback = nil); overload;
procedure SortIndexed;                                     // re-run the sort stored in SortIndexList
property SortIndexList: TTMSFNCDataGridSortIndexList;      // read-only reference, TObjectList<TTMSFNCDataGridSortIndex>
  // function Add(AColumn: integer; ADirection: TTMSFNCDataGridSortDirection): TTMSFNCDataGridSortIndex;
  // function Find(AColumn: Integer; var ASortIndex: TTMSFNCDataGridSortIndex): Boolean;
  // procedure Toggle(AColumn: Integer);   TTMSFNCDataGridSortIndex has Column, Direction
procedure GroupSort(AColumn: Integer; ADirection: TTMSFNCDataGridSortDirection); overload;  // for grouped grids
```
`Sort(AColumn, ...)` replaces `SortIndexList` with that one column.

```delphi
// Sorting demo
TMSFNCDataGrid1.Options.Sorting.Enabled := True;
TMSFNCDataGrid1.Sort(1, gsdAscending);

// two-level sort: country ascending, then price descending
TMSFNCDataGrid1.Sort([8, 7], [gsdAscending, gsdDescending]);

// re-sort after changing data, keeping the current sort columns
TMSFNCDataGrid1.SortIndexed;
```

Sorting **physically reorders the rows**. Afterwards `Cells[c, r]` returns the value shown at
row r. `DisplayToRealRow` / `RealToDisplayRow` map to and from the original order (`RowOrders`).
There is no built-in "unsort"; to restore the original order, keep a key column (for example
`AutoNumberColumn(0, 1)`) and sort on it.

### Custom comparison

Three ways:

1. **Callback per call** (it runs first; set `AHandled := True` to use your result):
```delphi
TTMSFNCDataGridDataCustomCompareCallback = reference to function(AColumn, ARow1, ARow2: Integer;
  AData1, AData2: TTMSFNCDataGridCellValue; ALevel: Integer; var AHandled: Boolean): Integer;

TMSFNCDataGrid1.Sort([2], [gsdAscending],
  function(AColumn, ARow1, ARow2: Integer; AData1, AData2: TTMSFNCDataGridCellValue;
    ALevel: Integer; var AHandled: Boolean): Integer
  begin
    // sort column 2 by text length
    Result := Length(TMSFNCDataGrid1.ValueToString(AData1)) - Length(TMSFNCDataGrid1.ValueToString(AData2));
    AHandled := True;               // False = fall back to the built-in comparison
  end);
```

2. **`OnCustomCompare` event**. It is **called only when the effective sort format is `gsfCustom`**
(`Options.Sorting.Format := gsfCustom`, or set in `OnGetSortOptions`), or when automatic detection
finds non-string, non-numeric value types:
```delphi
OnCustomCompare: function(Sender: TObject; AColumn, ARow1, ARow2: Integer;
  AData1, AData2: TTMSFNCDataGridCellValue; ALevel: Integer): Integer of object;
```
Return <0, 0 or >0 for ascending order. The grid negates it for descending.

3. **Per-column options** with `OnGetSortOptions` (or the `ASortOptionsCallback` parameter):
```delphi
OnGetSortOptions: procedure(Sender: TObject; AColumn: Integer; ALevel: Integer;
  var AOptions: TTMSFNCDataGridDataSortOptions) of object;
TTMSFNCDataGridDataGetSortOptionsCallback = reference to procedure(AColumn: Integer; ALevel: Integer;
  var AOptions: TTMSFNCDataGridDataSortOptions);
TTMSFNCDataGridDataSortOptions = record
  CaseSensitive: Boolean; Direction: TTMSFNCDataGridSortDirection;
  Format: TTMSFNCDataGridSortFormat; FormatSettings: TFormatSettings;
end;
```
```delphi
procedure TForm1.TMSFNCDataGrid1GetSortOptions(Sender: TObject; AColumn, ALevel: Integer;
  var AOptions: TTMSFNCDataGridDataSortOptions);
begin
  case AColumn of
    1: AOptions.CaseSensitive := False;
    7: AOptions.Format := gsfNumeric;
    9: AOptions.Format := gsfCustom;     // routes column 9 to OnCustomCompare
  end;
end;
```

### Sort events
```delphi
OnBeforeSortColumn: procedure(Sender: TObject; AColumn: Integer; var ACanSort: Boolean) of object;
OnAfterSortColumn: procedure(Sender: TObject; AColumn: Integer) of object;
```
Both fire for header clicks. `Sender` is the internal renderer (`Root`), not the grid.

## Filtering

### Model

`property Filter: TTMSFNCDataGridDataFilter` (read-only reference) is a collection of
`TTMSFNCDataGridDataFilterData` rules. Build the rules, then call **`ApplyFilter`**. Rows that don't
match are hidden (default `Options.Filtering.Actions = [gdfaHideRow]`). They are not deleted, so their
row indexes stay the same.

```delphi
procedure ApplyFilter;
procedure RemoveFilter;   // shows all rows again but KEEPS the rules in Filter
procedure ClearFilter;    // clears the rules (and the advanced filter) and shows all rows
property HasFilter: Boolean;          // read-only
property FilteredRowCount: Integer;   // read-only
function IsRowFiltered(ARow: Integer): Boolean;
function MatchFilter(ARow: Integer): Boolean;
procedure ShowFilterDialog;
function GetFilterTypeName(AType: TTMSFNCDataGridDataFilterType): string;
```

`TTMSFNCDataGridDataFilter` (collection) public members:
```delphi
function Add: TTMSFNCDataGridDataFilterData; overload;
function Add(AColumn: Integer; ACondition: string; AOperation: TTMSFNCDataGridDataFilterOperation = gfoNone;
  ACaseSensitive: Boolean = False): TTMSFNCDataGridDataFilterData; overload;
function Add(AColumn: Integer; AType: TTMSFNCDataGridDataFilterType; AValue: TTMSFNCDataGridCellValue;
  AOperation: TTMSFNCDataGridDataFilterOperation = gfoNone; ACaseSensitive: Boolean = False): TTMSFNCDataGridDataFilterData; overload;
function Insert(AIndex: Integer): TTMSFNCDataGridDataFilterData;
function First: TTMSFNCDataGridDataFilterData;   function Last: TTMSFNCDataGridDataFilterData;
function HasFilter(AColumn: integer): Boolean;
procedure Clear; virtual;
procedure Parse(AColumn: Integer; AFilterText: string);
procedure RemoveColumnFilter(AColumn: Integer);
property ColumnFilter[AColumn: Integer]: TTMSFNCDataGridDataFilterData;  // finds the rule for AColumn, or CREATES one
```

`TTMSFNCDataGridDataFilterData` published members:
```delphi
property Column: Integer default 0;
property Condition: string;
property &Type: TTMSFNCDataGridDataFilterType default gftEqual;
property CaseSensitive: Boolean default False;
property Operation: TTMSFNCDataGridDataFilterOperation default gfoNONE;
property Method: TTMSFNCDataGridDataFilterMethod default gfmExpression;  // gfmExpression, gfmLiteral
property Data: TTMSFNCDataGridDataFilterCells default gfcNormal;         // gfcNormal, gfcStripHTML, gfcRow
property Enabled: Boolean default True;
property Prefix: string;  property Suffix: string;    // stripped from cell text before comparing
// public: property FilterCondition: string;
// public fluent chaining:
function &And(AColumn: Integer; ACondition: string; ACaseSensitive: Boolean = False): TTMSFNCDataGridDataFilterData; overload;
function &And(AColumn: Integer; AType: TTMSFNCDataGridDataFilterType; AValue: TTMSFNCDataGridCellValue; ACaseSensitive: Boolean = False): TTMSFNCDataGridDataFilterData; overload;
function &Or(...same overloads...): TTMSFNCDataGridDataFilterData; overload;
```

Enums:
```delphi
TTMSFNCDataGridDataFilterType = (gftStartsWith, gftEndsWith, gftContains, gftNotContains, gftEqual,
  gftNotEqual, gftEmpty, gftNotEmpty, gftLargerThan, gftSmallerThan, gftLargerOrEqualThan, gftSmallerOrEqualThan);
TTMSFNCDataGridDataFilterNumberType = gftEqual..gftSmallerOrEqualThan;   // subrange
TTMSFNCDataGridDataFilterOperation = (gfoSHORT, gfoNONE, gfoAND, gfoXOR, gfoOR);
```
- `gfoNONE` is for the first rule (its result replaces the running result). `gfoAND`, `gfoOR` and
  `gfoXOR` combine a rule with the result of the rules before it. `gfoSHORT` rejects the row at once if
  this rule fails.
- **Condition syntax.** The text types (StartsWith, EndsWith, Contains, NotContains) treat the condition
  as a substring. The other types, `gftEqual` included, treat it as an **expression**: wildcards `*` `?`,
  the prefixes `>` `<` `>=` `<=` `!`, and the operators `&` `|` `^` with parentheses. This is not a
  regex. `""` matches empty cells. Use `Method := gfmLiteral` to compare the text as-is.

Examples:
```delphi
// Filtering demo: "Brand starts with A", using the default gftEqual expression with a wildcard
TMSFNCDataGrid1.ClearFilter;
fltr := TMSFNCDataGrid1.Filter.Add;
fltr.Column := 1;
fltr.CaseSensitive := False;
fltr.Condition := Edit1.Text + '*';
TMSFNCDataGrid1.ApplyFilter;

// Filter Row demo: typed rule through ColumnFilter (creates the rule if missing)
TMSFNCDataGrid1.RemoveFilter;
fltr := TMSFNCDataGrid1.Filter.ColumnFilter[7];
fltr.&Type := gftLargerThan;
fltr.Condition := '20000';
TMSFNCDataGrid1.ApplyFilter;

// two columns with AND
TMSFNCDataGrid1.Filter.Clear;
TMSFNCDataGrid1.Filter.Add(8, 'Germany');
TMSFNCDataGrid1.Filter.Add(7, '>30000', gfoAND);
TMSFNCDataGrid1.ApplyFilter;

// fluent form
TMSFNCDataGrid1.Filter.Add(1, gftStartsWith, 'A').&Or(1, gftStartsWith, 'B');
TMSFNCDataGrid1.ApplyFilter;
```
Use `ClearFilter` to start over and drop the rules. Use `RemoveFilter` to show all rows while keeping
the rules for a later `ApplyFilter`.

### Filter UI (drop-down buttons and filter row)

```delphi
// Options.Filtering: TTMSFNCDataGridDataFilteringOptions
property Enabled: Boolean default False;         // show filter controls in row `Row`
property Row: Integer default 0;                 // fixed row hosting the controls
property Controls: TTMSFNCDataGridDataFilterControls default [gfcButton];  // gfcButton, gfcEditor
property MultiColumn: Boolean default False;     // keep other columns' filters when picking a value
property Rows: TTMSFNCDataGridDataFilterRows default gfrNormal;  // gfrNormal (visible rows), gfrAll
property Actions: TTMSFNCDataGridDataFilteringActions default [gdfaHideRow];
  // gdfaHideRow, gdfaExecuteActions (run FilterActions), gdfaApplyAppearance (CellAppearance.FilterMatchLayout / FilterInverseMatchLayout)
property Advanced: Boolean default False;        // filter with FilterBuilder instead of Filter; enables the advanced dialog
property HideEmptyGroups: Boolean default False;
property TrimValues: Boolean default True;
property DropDownWidth: Integer default 200;  property DropDownHeight: Integer default 280;
```

Drop-down filter buttons in the header row (Filtering demo):
```delphi
TMSFNCDataGrid1.Options.Filtering.Enabled := True;

procedure TForm1.TMSFNCDataGrid1GetCellProperties(Sender: TObject; ACell: TTMSFNCDataGridCell);
begin
  if ACell.Column = 0 then
    ACell.FilterButton := False;        // hide the button for one column
end;
```
For each column you can also set `Columns[i].FilterButton := False` with `AddSetting(gcsFilterButton)`.

A **filter row** is not a separate built-in row. Add a second fixed row and point the filter controls
at it (Filter Row demo):
```delphi
TMSFNCDataGrid1.FixedRowCount := 2;
TMSFNCDataGrid1.InsertRow(1);                     // empty row 1 becomes the filter row
TMSFNCDataGrid1.Options.Filtering.Enabled := True;
TMSFNCDataGrid1.Options.Filtering.Row := 1;
TMSFNCDataGrid1.Options.Filtering.Controls := [gfcButton, gfcEditor];   // drop-down + inline editor
TMSFNCDataGrid1.Options.Filtering.MultiColumn := True;
```
Inline editor control: `Columns[i].FilterEditor`, `FilterEditorType` (`gfetAutomatic, gfetString,
gfetBoolean, gfetDateTime, gfetFloat, gfetNumber, gfetCustom`) and `FilterDefaultType`, each with its
`gcsFilter*` setting. You can also call `AddFilterEditor(AColumn, ARow)` and `RemoveFilterEditor(AColumn, ARow)`.
Look: `FilterAppearance` (`Fill`, `Font`, `Stroke`). UI texts are in `Options.Localization.Filter*Text`.

Filter events:
```delphi
OnBeforeApplyFilter: procedure(Sender: TObject; AColumn: Integer; var ACondition: string; var ACanApply: Boolean) of object;
OnAfterApplyFilter: procedure(Sender: TObject; AColumn: Integer; ACondition: string) of object;
OnRemoveFilter: procedure(Sender: TObject; AColumn: Integer) of object;
OnBeforeShowFilter: procedure(Sender: TObject; AColumn: Integer; var ACanShow: Boolean) of object;
OnAfterShowFilter: procedure(Sender: TObject; AColumn: Integer) of object;
OnNeedFilterDropDownData: procedure(Sender: TObject; AColumn: Integer; AValues: TStrings) of object;  // fill AValues yourself
OnCustomizeFilterPopupEditor: procedure(Sender: TObject; AColumn: Integer; var AEditor: TTMSFNCDataGridCellControl) of object;
OnCreateCustomFilterEditor: function(Sender: TObject; ACell: TTMSFNCDataGridCellCoord): TTMSFNCDataGridCellControl of object;  // with gfetCustom
```
```delphi
procedure TForm1.TMSFNCDataGrid1NeedFilterDropDownData(Sender: TObject; AColumn: Integer; AValues: TStrings);
begin
  if AColumn = 8 then
  begin
    AValues.Clear;
    AValues.Add('Germany');
    AValues.Add('Italy');
  end;
end;
```

Filter actions (`gdfaExecuteActions`): `FilterActions: TTMSFNCDataGridDataFilterActions`. Each item has
`Name`, `Enabled`, `OnApply(Sender; ARow: Integer; AMatches: Boolean)`, `OnRemove(Sender; ARow: Integer)`
and `OnClear: TNotifyEvent`. Use them to run your own code per row instead of hiding rows.

## Does not exist / common mistakes

| Wrong | Use instead |
|---|---|
| `SortSettings.Show/Column/Direction`, `SortByColumn`, `QSort` (TAdvStringGrid) | `Options.Sorting.Enabled`, `Sort(AColumn, gsdAscending)` |
| `sdAscending`, `soAscending`, `TSortDirection` | `gsdAscending`, `gsdDescending`, `gsdNone` (`TTMSFNCDataGridSortDirection`) |
| `OnCompareCells`, `OnCustomCompare` firing for normal text columns | `OnCustomCompare` fires only for `gsfCustom` format; or pass a compare callback to `Sort` |
| `OnCanSort`, `OnBeforeSort`, `OnAfterSort` | `OnBeforeSortColumn(var ACanSort)`, `OnAfterSortColumn` |
| Expecting case-insensitive sort by default | `Options.Sorting.CaseSensitive` defaults to `True` |
| `Filter.Add(...)` and expecting rows to hide | call `ApplyFilter` afterwards |
| `FilterActive := True`, `Filter.Active` | `ApplyFilter`; check with `HasFilter` |
| `RemoveFilter` to drop rules | `RemoveFilter` keeps the rules; `ClearFilter` (or `Filter.Clear`) drops them |
| `FilterDropDown`, `OnFilterSelect`, `OnGetColumnFilter` (TAdvStringGrid) | `Options.Filtering.Enabled`, `OnAfterApplyFilter`, `OnNeedFilterDropDownData` |
| `Options.Filtering.FilterRow := True`, `ShowFilterRow` | `FixedRowCount := 2` + `InsertRow(1)` + `Options.Filtering.Row := 1` + `Controls := [gfcEditor]` |
| Regex in `Condition` | wildcard/expression syntax (`*`, `?`, `>`, `!`, `&`, `|`); not a regex |
| `fltr.FilterType`, `fltr.Value`, `fltr.Col` | `fltr.&Type`, `fltr.Condition`, `fltr.Column` |
| Using a row index from before sort/filter as the screen position | sort moves rows; filter hides them. Use `RealToVisualRow` / `IsRowFiltered` |
