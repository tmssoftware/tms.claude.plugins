# Conditional formatting (TTMSFNCDataGrid)

Declarative, Excel-style rules evaluated while painting. Not a separate component: a rule collection on the grid / renderer.

- Unit: `VCL.TMSFNCDataGridConditionalFormatting` (`FMX.` / `WEBLib.` equivalents) — add it to `uses` for the enums.
- `property ConditionalFormatting: TTMSFNCDataGridConditionalFormatting` on `TTMSFNCDataGrid` (published), on `TTMSFNCDataGridRenderer`, and on `TTMSFNCDataGridRendererSource`. Assigning copies rules (`Assign`); owned by the root renderer.
- Applied to cells **before** `OnGetCellLayout`, so your event can still override.
- Design-time/runtime rule editor: `TTMSFNCDataGridConditionalFormattingEditor` (unit `*.TMSFNCDataGridConditionalFormattingEditor`, VCL/FMX only) with `Execute: Boolean`, `Execute(AGrid: TTMSFNCDataGridBase): Boolean`, `Execute(AFormatting; ARenderer: TTMSFNCDataGridRenderer = nil): Boolean`, properties `Grid`, `Renderer`. Shortcut on the grid: `function ShowConditionalFormattingEditor: Boolean` (`{$IFNDEF WEBLIB}` — not in TMS WEB Core).

## Collection: TTMSFNCDataGridConditionalFormatting

```delphi
function Add: TTMSFNCDataGridFormatRuleItem;   // blank grtCellValue rule on column 0, no visible effect until configured
function AddCellValueRule(AColumn: Integer; AComparison: TTMSFNCDataGridFormatComparison; const AValue: string): TTMSFNCDataGridFormatRuleItem; overload;
function AddCellValueRule(AColumn: Integer; AComparison: TTMSFNCDataGridFormatComparison; const AValue: TTMSFNCValue): TTMSFNCDataGridFormatRuleItem; overload;
function AddCellValueRule(AColumn: Integer; AComparison: TTMSFNCDataGridFormatComparison; const AFrom, ATo: TTMSFNCValue): TTMSFNCDataGridFormatRuleItem; overload;
function AddTextRule(AColumn: Integer; AComparison: TTMSFNCDataGridFormatComparison; const AText: string): TTMSFNCDataGridFormatRuleItem;
function AddColorScale(AColumn: Integer; AMin, AMid, AMax: TTMSFNCGraphicsColor): TTMSFNCDataGridFormatRuleItem;
function AddDataBar(AColumn: Integer; AColor: TTMSFNCGraphicsColor): TTMSFNCDataGridFormatRuleItem;
function AddIconSet(AColumn: Integer; AKind: TTMSFNCDataGridIconSetKind): TTMSFNCDataGridFormatRuleItem;
function AddTopBottomRule(AColumn: Integer; AKind: TTMSFNCDataGridRankKind; ACount: Integer): TTMSFNCDataGridFormatRuleItem;
function AddAverageRule(AColumn: Integer; AKind: TTMSFNCDataGridAverageKind): TTMSFNCDataGridFormatRuleItem;
function AddExpressionRule(const AExpression: string): TTMSFNCDataGridFormatRuleItem;   // scope grsGrid
// one-call "highlight" variants (rule + fill/font colour applied):
function AddValueHighlight(AColumn: Integer; AComparison: TTMSFNCDataGridFormatComparison; const AValue: string;
  AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull): TTMSFNCDataGridFormatRuleItem;
function AddValueRangeHighlight(AColumn: Integer; const AMinimum, AMaximum: string; AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull): TTMSFNCDataGridFormatRuleItem;
function AddTextHighlight(AColumn: Integer; AComparison: TTMSFNCDataGridFormatComparison; const AText: string; AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull): TTMSFNCDataGridFormatRuleItem;
function AddDateHighlight(AColumn: Integer; AInterval: TTMSFNCDataGridDateInterval; AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull): TTMSFNCDataGridFormatRuleItem;
function AddDateRangeHighlight(AColumn: Integer; AFrom, ATo: TDateTime; AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull): TTMSFNCDataGridFormatRuleItem;
function AddDuplicateHighlight(AColumn: Integer; AKind: TTMSFNCDataGridDuplicateKind; AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull): TTMSFNCDataGridFormatRuleItem;
function AddExpressionHighlight(const AExpression: string; AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull): TTMSFNCDataGridFormatRuleItem;
procedure ClearRules;        // frees all rules; held references become invalid
procedure InvalidateStats;   // only needed if data changes without going through the grid
property Items[Index: Integer]: TTMSFNCDataGridFormatRuleItem; default;
property Enabled: Boolean default True;   // master switch
property OnChange: TNotifyEvent;
```
Also usable: `BeginUpdate/EndUpdate`, `Count`, `Delete` (TCollection). `TTMSFNCValue` = `TValue` (VCL/FMX) / `JSValue` (WEB); for dates use the TValue overload, e.g. `TValue.From<TDateTime>(EncodeDate(2025,1,1))`.

Plain `Add*Rule` builders set **no appearance** — configure `Appearance` or chain `.Highlight(...)`.

## Rule item: TTMSFNCDataGridFormatRuleItem (TCollectionItem)

Published: `Enabled` (True), `RuleType` (`grtCellValue`), `Scope` (`grsColumn`), `Column`, `ColumnTo`, `CellRangeStartColumn/StartRow/EndColumn/EndRow`, `Priority` (0), `StopIfTrue` (False), `Comparison` (`gfcEqual`), `Value1`, `Value2`: string, `CaseSensitive` (False), `DateInterval` (`diToday`), `DateFrom`, `DateTo`, `RankKind` (`rkTop`), `RankCount` (10), `RankIsPercent`, `AverageKind` (`akAbove`), `DuplicateKind` (`dkDuplicate`), `ApplyToEntireRow` (False), `Expression`, `Appearance: TTMSFNCDataGridCellLayout` (`Fill`, `Font`, `Stroke`, `TextAlign`, ...), `ColorScale`, `DataBar`, `IconSet`. Public: `CellRange: TTMSFNCDataGridCellCoordRange`.

Fluent helpers (return the rule):
```delphi
function ForColumn(AColumn: Integer): TTMSFNCDataGridFormatRuleItem;
function ForColumns(AFirstColumn, ALastColumn: Integer): TTMSFNCDataGridFormatRuleItem;   // stats over the whole range
function ForCellRange(AStartColumn, AStartRow, AEndColumn, AEndRow: Integer): TTMSFNCDataGridFormatRuleItem;
function ForEntireRow(AValueColumn: Integer): TTMSFNCDataGridFormatRuleItem;   // = ApplyToEntireRow on trigger column
function Highlight(AFillColor: TTMSFNCGraphicsColor; ATextColor: TTMSFNCGraphicsColor = gcNull; ABold: Boolean = False): TTMSFNCDataGridFormatRuleItem;
function WithBorder(AColor: TTMSFNCGraphicsColor): TTMSFNCDataGridFormatRuleItem;
function WithValue(const AValue: TTMSFNCValue): TTMSFNCDataGridFormatRuleItem;
function WithRange(const AFrom, ATo: TTMSFNCValue): TTMSFNCDataGridFormatRuleItem;   // does not set Comparison
function WithDateRange(AFrom, ATo: TDateTime): TTMSFNCDataGridFormatRuleItem;       // sets grtDate + diCustomRange
```

## Enums

```delphi
TTMSFNCDataGridFormatRuleType = (grtCellValue, grtText, grtDate, grtTopBottom, grtAverage,
  grtUniqueDuplicate, grtColorScale, grtDataBar, grtIconSet, grtExpression);
TTMSFNCDataGridFormatRuleScope = (grsColumn, grsColumnRange, grsCellRange, grsGrid);
TTMSFNCDataGridFormatComparison = (gfcEqual, gfcNotEqual, gfcGreater, gfcGreaterEqual, gfcLess, gfcLessEqual,
  gfcBetween, gfcNotBetween, gfcContains, gfcNotContains, gfcBeginsWith, gfcEndsWith);
TTMSFNCDataGridRankKind = (rkTop, rkBottom);
TTMSFNCDataGridAverageKind = (akAbove, akBelow, akAboveOrEqual, akBelowOrEqual, akAbovePlusStdDev, akBelowMinusStdDev);
TTMSFNCDataGridDuplicateKind = (dkDuplicate, dkUnique);
TTMSFNCDataGridDateInterval = (diToday, diYesterday, diTomorrow, diThisWeek, diLastWeek, diNextWeek,
  diThisMonth, diLastMonth, diNextMonth, diThisYear, diCustomRange);
TTMSFNCDataGridIconSetKind = (gisArrows3, gisArrows4, gisArrows5, gisTrafficLights3, gisTrafficLights4,
  gisFlags3, gisSymbols3, gisStars3, gisStars5, gisRating4, gisRating5, gisCustom);
TTMSFNCDataGridScaleBoundKind = (sbkLowestHighest, sbkNumber, sbkPercent, sbkPercentile);
TTMSFNCDataGridBarBoundKind = (bbkAuto, bbkNumber, bbkPercent, bbkPercentile);
TTMSFNCDataGridBarDirection = (bdLeftToRight, bdRightToLeft);
```
Note: the rule-type prefix `grt` overlaps visually with row types (`grtDefault, grtSummary, grtNode, grtFilter` in `TTMSFNCDataGridRowType`) — different enums, do not mix.

Settings objects:
- `ColorScale: TTMSFNCDataGridColorScaleSettings` — `ThreeColor` (True), `MinColor/MidColor/MaxColor`, `MinKind/MaxKind` (`sbkLowestHighest`), `MidKind` (`sbkPercent`), `MinValue/MidValue/MaxValue`.
- `DataBar: TTMSFNCDataGridDataBarSettings` — `Fill`, `NegativeFill` (red), `Border`, `ShowValue` (True), `ShowBarOnly` (False), `Direction`, `MinKind/MaxKind` (`bbkAuto`), `MinValue/MaxValue`.
- `IconSet: TTMSFNCDataGridIconSetSettings` — `Kind` (`gisArrows3`), `Reverse` (False; set when low is good), `ShowValue` (True). Range is split into equal-width bands.

## Priority and conflict resolution

- **Lower `Priority` value wins** (default 0, negatives allowed; ties keep declaration order).
- Evaluated from lowest Priority upward; the first matching rule that sets an aspect (fill, font colour, font style, border, alignment, ...) owns that aspect for the cell. Other matching rules still add aspects nobody set — a red-fill rule and a bold-font rule combine.
- Only aspects that differ from a fresh rule's appearance count as "set" — a rule cannot force an aspect back to its default.
- `StopIfTrue` stops evaluating lower-priority rules (including data bar / icon set overlays) once the rule matches.
- Only one overlay (data bar or icon set) is painted per cell: the first matching one in priority order.
- Aggregate rules (top/bottom, average, duplicates, colour scale, bars, icon sets) use statistics over the **visible rows** of the scope; recomputed automatically on cell writes, sort, filter, paste and rule changes.

## Expression rules

`Expression` uses the grid's filter expression syntax (`FilterFormatType`, default `fftUniversalFilterExpressions`): columns in `[ ]`, `&` = and, `|` = or, `!=` not equal, `NOT`, strings in double quotes, `*` / `?` wildcards. Column names are the **data names**: with a database adapter the field name; without an adapter the column **index as text** (`[3]`). A bare condition without `[ ]` (e.g. `>1000`, `M*`) binds to the rule's `Column` (default 0 — set it).

```delphi
// highlight whole row where column 3 > 2000 and column 10 = "Active"
FGrid.ConditionalFormatting.AddExpressionHighlight('[3] > 2000 & [10] = "Active"', gcHoneydew);
// format only one column with a bare condition
with FGrid.ConditionalFormatting.AddExpressionRule('>1000').ForColumn(3) do
  Appearance.Font.Color := gcRed;
```

## Demo (Advanced\Conditional Formatting, condensed)

Grid built in code; columns: 3 Sales, 4 Quota %, 5 Pipeline, 6 Deals, 7 Win %, 8 Growth %, 9 CSAT, 10 Status.

```delphi
uses ..., VCL.TMSFNCDataGrid, VCL.TMSFNCDataGridConditionalFormatting;

procedure TfrmConditionalFormatting.AddRules;
begin
  // 3-colour scale, low priority (high number) so highlights override its fill
  FGrid.ConditionalFormatting.AddColorScale(COL_SALES, gcRed, gcYellow, gcLimegreen).Priority := 100;

  // top 5 performers -> whole row tinted + bold
  with FGrid.ConditionalFormatting.AddTopBottomRule(COL_SALES, rkTop, 5) do
  begin
    Priority := 10;
    ApplyToEntireRow := True;
    Appearance.Fill.Color := gcLightgoldenrodyellow;
    Appearance.Font.Style := [TFontStyle.fsBold];
  end;

  FGrid.ConditionalFormatting.AddDataBar(COL_QUOTA, gcDodgerblue);
  with FGrid.ConditionalFormatting.AddCellValueRule(COL_QUOTA, gfcLess, '100') do
    Appearance.Font.Color := gcRed;

  FGrid.ConditionalFormatting.AddIconSet(COL_DEALS, gisArrows4);

  with FGrid.ConditionalFormatting.AddCellValueRule(COL_GROWTH, gfcLess, '0') do
    Appearance.Font.Color := gcRed;
  with FGrid.ConditionalFormatting.AddCellValueRule(COL_GROWTH, gfcGreater, '0') do
    Appearance.Font.Color := gcGreen;
  FGrid.ConditionalFormatting.AddIconSet(COL_GROWTH, gisTrafficLights3);

  FGrid.ConditionalFormatting.AddIconSet(COL_CSAT, gisStars5);

  with FGrid.ConditionalFormatting.AddTextRule(COL_STATUS, gfcEqual, 'Active') do
    Appearance.Font.Color := gcGreen;
  with FGrid.ConditionalFormatting.AddTextRule(COL_STATUS, gfcEqual, 'Churned') do
  begin
    Appearance.Fill.Color := gcMistyrose;
    Appearance.Font.Color := gcRed;
  end;
end;
```
Cells were filled with numbers (`FGrid.Cells[COL_SALES, i + 1] := SAMPLE[i].Sales;` — `Cells` accepts TValue), so numeric comparisons work. Fluent equivalent from the source docs: `Grid.ConditionalFormatting.AddTopBottomRule(3, rkTop, 5).ForEntireRow(3).Highlight(gcHoneydew);`

Toggle all formatting: `FGrid.ConditionalFormatting.Enabled := False;`. Wrap bulk rule creation in `ConditionalFormatting.BeginUpdate/EndUpdate`.

## Platform notes

Same API on VCL/FMX/WEB (WEB demo identical except `WebFormCreate`). `TFontStyle.fsBold` is used on all platforms. The rule editor dialog and `ShowConditionalFormattingEditor` are not available in WEB.

## Does not exist / common mistakes

- `AddRule`, `AddFormatRule`, `Rules`, `TTMSFNCDataGridConditionalFormat` component — use `ConditionalFormatting.Add*` on the grid.
- Assuming a higher `Priority` number wins — **lower** wins.
- `AddCellValueRule(...)` alone and expecting a visual change — add `Appearance.*` or `.Highlight(...)`, or use `AddValueHighlight`.
- `rtCellValue`, `cfGreater`, `gfcGreaterThan`, `gfcLessThan`, `gfcStartsWith`, `isArrows` — real names: `grtCellValue`, `gfcGreater`, `gfcLess`, `gfcBeginsWith`, `gisArrows3`.
- Expression rule using header captions like `[Sales]` in a non-database grid — names are column indexes (`[3]`) unless a database adapter supplies field names.
- Using `OnGetCellLayout` to do per-value colouring is still valid, but it runs **after** conditional formatting and overrides it.
