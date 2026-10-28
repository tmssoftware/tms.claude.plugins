# Styling and number formatting (TTMSFNCDataGrid)

How to make the grid look like a polished business dashboard in one pass: state layouts, per-cell layout, number/date formats that don't depend on the Windows locale, checkbox and bar columns, and how to check the look. Code below is FMX and compiled against `tms.fnc.uipack` 7.3.1.2. For VCL use `TColor` / `gcXxx` colours and `[fsBold]` instead of `TAlphaColor` and `[TFontStyle.fsBold]`.

Units: `FMX.TMSFNCDataGrid, FMX.TMSFNCDataGridCell, FMX.TMSFNCDataGridData, FMX.TMSFNCDataGridCore, FMX.TMSFNCDataGridRenderer, FMX.TMSFNCGraphicsTypes, FMX.TMSFNCTypes` (+ `System.UITypes` for `TAlphaColor` / `TFontStyle`).

## Order of setup

1. Set `FormatSettings` (see "Locale-proof formats") before any value is written.
2. Create the grid, set `ColumnCount`, `RowCount`, `FixedRowCount`, `FixedBottomRowCount`.
3. Assign `OnGetCellFormatting` / `OnGetCellDisplayValue` **before filling data**. The grid computes and stores each cell's display text when the value is written (`TTMSFNCDataGridData.CreateDisplayValue`), and only recomputes it when rows are rebuilt (grouping, sorting). A handler assigned after filling seems to "do nothing" until the next rebuild. There is no public "refresh display values" call.
4. Fill data inside `BeginUpdate` / `EndUpdate`.
5. Apply state layouts and options, conditional formatting, then `Group` / calculations, then merges.

## State layouts: `Grid.CellAppearance`

Each is a `TTMSFNCDataGridCellLayout` with `Fill` (`Kind`, `Color`), `Stroke` (`Color`, `Width`), `Sides: TTMSFNCGraphicsSides` (`gsLeft, gsTop, gsRight, gsBottom`), `Font` (`Name`, `Size`, `Color`, `Style`), `TextAlign` (`gtaLeading`, `gtaCenter`, `gtaTrailing`), `TextMargins`.

| Layout | Used for |
|---|---|
| `NormalLayout` | data rows |
| `BandLayout` | alternate data rows when `Options.Banding.Enabled := True` |
| `FixedLayout` / `FixedSelectedLayout` | fixed rows (captions, band header, filter row, footer) |
| `SelectedLayout` / `FocusedLayout` | selected cells / focused cell |
| `GroupLayout` | group header (node) rows |
| `SummaryLayout` | group summary rows |

`CellAppearance.ShowFocus := False` hides the focus rectangle. Copy one layout to another with `Assign`.

Dashboard recipe (navy header, zebra rows, horizontal lines only, blue selection):

```delphi
procedure SetLayoutFont(ALayout: TTMSFNCDataGridCellLayout; AColor: TAlphaColor; ABold: Boolean);
begin
  ALayout.Font.Name := 'Segoe UI';
  ALayout.Font.Size := 13;            // FMX font size is in DIPs: 13-14 = about 10-10.5 pt
  ALayout.Font.Color := AColor;
  if ABold then ALayout.Font.Style := [TFontStyle.fsBold] else ALayout.Font.Style := [];
end;

procedure StyleLayout(ALayout: TTMSFNCDataGridCellLayout; AFill, ALine: TAlphaColor; ASides: TTMSFNCGraphicsSides);
begin
  ALayout.Fill.Kind := gfkSolid;
  ALayout.Fill.Color := AFill;
  ALayout.Stroke.Color := ALine;
  ALayout.Sides := ASides;
  ALayout.TextMargins.Left := 8;
  ALayout.TextMargins.Right := 10;
end;

// in the form:
var ca := FGrid.CellAppearance;
ca.ShowFocus := False;
StyleLayout(ca.NormalLayout, TAlphaColors.White, $FFE3E8EF, [gsBottom]);
SetLayoutFont(ca.NormalLayout, $FF1F2937, False);
StyleLayout(ca.BandLayout, $FFF3F6FA, $FFE3E8EF, [gsBottom]);
SetLayoutFont(ca.BandLayout, $FF1F2937, False);
StyleLayout(ca.FixedLayout, $FF1B3A63, $FF2E5283, [gsRight, gsBottom]);
SetLayoutFont(ca.FixedLayout, TAlphaColors.White, True);
ca.FixedSelectedLayout.Assign(ca.FixedLayout);
StyleLayout(ca.SelectedLayout, $FF1E7FC2, $FF1E7FC2, [gsBottom]);
SetLayoutFont(ca.SelectedLayout, TAlphaColors.White, False);
ca.FocusedLayout.Assign(ca.SelectedLayout);
StyleLayout(ca.GroupLayout, $FFDCE9F7, $FFB9D0EA, [gsTop, gsBottom]);
SetLayoutFont(ca.GroupLayout, $FF1B3A63, True);
StyleLayout(ca.SummaryLayout, $FFEEF3FA, $FFC9D8EA, [gsBottom]);
SetLayoutFont(ca.SummaryLayout, $FF1B3A63, True);

FGrid.Options.Banding.Enabled := True;
FGrid.Options.Selection.Mode := gsmSingleRow;
FGrid.DefaultRowHeight := 30;
FGrid.Options.Column.Stretching.Enabled := True;
FGrid.Options.Column.Stretching.Mode := gstmProportional;   // keep ColumnWidths ratios, fill the width
```

Sizes: `DefaultRowHeight`, `RowHeights[ARow]`, `ColumnWidths[AColumn]`. The frame around the grid: `Grid.Fill`, `Grid.Stroke`.

## Per-cell layout: `OnGetCellLayout`

`procedure(Sender: TObject; ACell: TTMSFNCDataGridCell)`. Change `ACell.Layout` for alignment, colours and fonts per row/column. Row tests: `ACell.Row`, `Grid.IsRowNode(r)` (group header), `Grid.IsRowSummary(r)`, `Grid.RowTypes[r]` (`grtDefault` for data rows). The footer is `Grid.RowCount - 1` when `FixedBottomRowCount = 1`.

```delphi
procedure TFormMain.GridGetCellLayout(Sender: TObject; ACell: TTMSFNCDataGridCell);
begin
  if ACell.Row = ROW_BAND then
    ACell.Layout.TextAlign := gtaCenter
  else if FGrid.IsRowNode(ACell.Row) then
    ACell.Layout.TextAlign := gtaLeading
  else if ACell.Column in [COL_QTY, COL_PRICE, COL_REVENUE, COL_MARGIN] then
    ACell.Layout.TextAlign := gtaTrailing                      // right-aligned numbers, captions too
  else if (ACell.Column = COL_PAID) and (ACell.Row >= FGrid.FixedRowCount) then
    ACell.Layout.Font.Color := TAlphaColors.Null;              // hide True/False behind the checkbox
end;
```

## Locale-proof formats

The display text uses the application's `FormatSettings`, so on a German/Dutch Windows `#,##0.00` shows `12.345,00` and a spec of "€ 12,345.00" is missed. Set the separators once at startup, before the grid is filled:

```delphi
FormatSettings.DecimalSeparator := '.';
FormatSettings.ThousandSeparator := ',';
FormatSettings.DateSeparator := '-';
FormatSettings.ShortDateFormat := 'dd-mm-yyyy';
```

Per-column formats with `OnGetCellFormatting` (`procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; AData: TTMSFNCDataGridCellValue; var AFormatting: TTMSFNCDataGridDataFormatting; var AConvertSettings: TFormatSettings; var ACanFormat: Boolean)`). Store real numbers / `TDateTime` in `Cells[]` (not pre-formatted strings) so sorting, filtering and calculations keep working:

```delphi
procedure TFormMain.GridGetCellFormatting(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AData: TTMSFNCDataGridCellValue; var AFormatting: TTMSFNCDataGridDataFormatting;
  var AConvertSettings: TFormatSettings; var ACanFormat: Boolean);
begin
  // group/summary/footer rows already hold formatted calculation text
  if (ACell.Row < FGrid.FixedRowCount) or (ACell.Row >= FGrid.RowCount - FGrid.FixedBottomRowCount)
    or (FGrid.RowTypes[ACell.Row] <> grtDefault) then
  begin
    ACanFormat := False;
    Exit;
  end;
  case ACell.Column of
    COL_DATE:    begin AFormatting.&Type := gdftDate;  AFormatting.Format := 'dd-mm-yyyy'; end;
    COL_PRICE, COL_REVENUE:
                 begin AFormatting.&Type := gdftFloat; AFormatting.Format := '"€ "#,##0.00'; end;
    COL_MARGIN:  begin AFormatting.&Type := gdftFloat; AFormatting.Format := '0.0"%"'; end;
  end;
end;
```

Calculation rows (group summaries, footer totals) are formatted by the calculation callback instead (`AOptions.CalculationFormatType := gcfNumber; AOptions.CalculationFormat := '€ %.2n'`, see grouping.md).

Non-ASCII literals such as `€` or `·` in a `.pas` file: save the unit as **UTF-8 with BOM**, or write them as `#$20AC` / `#$00B7`. Without a BOM the compiler reads the file as ANSI and the characters come out garbled.

## Checkbox, bar and "value + bar" columns

- Boolean column as checkbox: `AddDataCheckBoxColumn(AColumn)` (state follows the cell value). The value's `True`/`False` text is still drawn behind the checkbox. Hide it with `ACell.Layout.Font.Color := TAlphaColors.Null` in `OnGetCellLayout` (above), or in `OnBeforeDrawCell` with `ACell.DrawElements := ACell.DrawElements - [gcdText]`. Both keep the value, sorting and filtering intact; don't blank the value or the display text.
- A number plus a bar (e.g. Margin % with a bar): use a conditional-formatting **data bar** (`ConditionalFormatting.AddDataBar(AColumn, AColor)`, `DataBar.ShowValue = True`, fixed range with `DataBar.MinKind/MaxKind` + `MinValue/MaxValue`). The built-in progress-bar cell (`AddDataProgressBarColumn`) is a full-cell control that covers the value text.
- The data bar is drawn as a thin bar along the bottom of the cell, under the value. That's expected.

## Header bar and toolbar (FMX)

- A slim title/toolbar bar above the grid: a `TRectangle` (`Align := Top`, `Fill.Color`, `Stroke.Kind := TBrushKind.None`, unit `FMX.Objects` / `FMX.Graphics`) with `TLabel`s and `TButton`s. `TBrushKind` is FMX's own type. For FNC graphics (`Fill.Kind` on grid layouts) use `gfkSolid`/`gfkNone` from `*.TMSFNCGraphicsTypes`.
- With several `Align := Right` buttons, FMX orders them by their current `Position.X`, so creating them in reading order often shows them reversed. Set `Position.X` explicitly (increasing left to right) before setting `Align`, or put them in a right-aligned `TLayout`.
- `TLabel` / `TButton` ignore `Font`/`FontColor` until you remove the matching item from `StyledSettings` (e.g. `Lbl.StyledSettings := Lbl.StyledSettings - [TStyledSetting.Size, TStyledSetting.FontColor, TStyledSetting.Style]`).

## Checking the look

Look at the running app before declaring a visual task done. Plan for it in the first version of the code: a command-line switch (e.g. `-snapshot`) that saves the image, writes any self-checks to a text file and closes the app. Adding it later costs an extra build. Capture **only your own window**: have the app save an image of itself, for example a root `TLayout` that holds the whole UI (`RootLayout.MakeScreenshot.SaveToFile('shot.png')`, FMX `TControl.MakeScreenshot`, free the bitmap), or `Grid.SaveToImageData('grid.png')` for just the grid's data. `TForm` has no `MakeScreenshot`. Never take a full-desktop screenshot: it captures the user's other windows (mail, chats) and isn't needed.

Stop the running app before rebuilding, or the link step fails with `F2039 Could not create output file`.

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `Form.MakeScreenshot` | `SomeControl.MakeScreenshot` on a TControl (e.g. a root TLayout), or `Grid.SaveToImageData` |
| Full-screen screenshot to check the UI | App saves its own image (see above) |
| `Grid.Appearance.*`, `Grid.Font` | `CellAppearance.*Layout.Font`, `GlobalFont` |
| `FormatFloat` into `Cells[]` as strings | Store numbers, format with `OnGetCellFormatting` |
| Assigning `OnGetCellFormatting` after filling and expecting existing cells to change | Assign before filling (or refill / regroup) |
| Blanking the Paid cell's value to hide True/False | `Font.Color := TAlphaColors.Null` or `DrawElements - [gcdText]` |
| `AddDataProgressBarColumn` for "value + bar" | Conditional-formatting data bar |
