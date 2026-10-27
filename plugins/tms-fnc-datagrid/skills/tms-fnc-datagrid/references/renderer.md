# Renderer architecture, RendererSource, non-visual export

## Layering (class hierarchy)

```
TTMSFNCDataGridCore        (*.TMSFNCDataGridCore)      rows/columns/fixed counts, coordinates (TInterfacedPersistent)
  TTMSFNCDataGridData      (*.TMSFNCDataGridData)      cell data, merge info, sort/filter/group/calculations, CSV/JSON/XML IO, Options
    TTMSFNCDataGridRenderer (*.TMSFNCDataGridRenderer) drawing, input, editing, columns, appearance, conditional formatting,
                                                        HTML/image export  -- NOT a TControl
TTMSFNCDataGridBase (TTMSFNCCustomControl)             hosts a renderer: property Root: TTMSFNCDataGridRenderer
  TTMSFNCCustomDataGrid -> TTMSFNCDataGrid             the visual control; most members forward to Root
TTMSFNCDataGridRendererSource (TTMSFNCCustomComponent) wraps a standalone renderer "layer" for RendererSource
```

Consequences:
- Almost all grid API (Cells, Group, MergeCells, LoadFromCSVData, ConditionalFormatting, Options, CellAppearance, Columns...) also exists on `TTMSFNCDataGridRenderer`, so a renderer can be filled and exported **without any visual control**.
- `Grid.Root` gives the active renderer (escape hatch for members not surfaced on the grid). Nested grids from `AddGrid` are renderers too (see cell-controls.md).

```delphi
TTMSFNCDataGridRenderer = class(TTMSFNCDataGridData, ...)
  constructor Create(AHost: TObject = nil); reintroduce; virtual;
```

## Non-visual data + export (Advanced\Non-Visual Data Export)

A standalone renderer created with no host; you own and free it.

```delphi
uses VCL.TMSFNCDataGridData, VCL.TMSFNCDataGridRenderer, VCL.TMSFNCDataGridPDFIO,
  VCL.TMSFNCDataGridExcelIO, VCL.TMSFNCPDFIO, VCL.TMSFNCTypes;

type
  TForm1 = class(TForm)
    TMSFNCDataGridPDFIO1: TTMSFNCDataGridPDFIO;
    TMSFNCDataGridExcelIO1: TTMSFNCDataGridExcelIO;
  private
    r: TTMSFNCDataGridRenderer;
  end;

procedure TForm1.FormCreate(Sender: TObject);
begin
  r := TTMSFNCDataGridRenderer.Create;
  r.LoadFromCSVData('train.csv');
  r.Options.IO.OpenAfterCreation := True;   // open saved CSV/HTML file in associated app (default True)
  r.Options.IO.StartRow := 0;
  r.Options.IO.StartColumn := 0;
end;

procedure TForm1.FormDestroy(Sender: TObject);
begin
  r.Free;
end;

procedure TForm1.PDFClick(Sender: TObject);
begin
  TMSFNCDataGridPDFIO1.Renderer := r;                 // instead of DataGrid
  TMSFNCDataGridPDFIO1.Options.Header := 'Train Data';
  TMSFNCDataGridPDFIO1.Options.Footer := '';
  TMSFNCDataGridPDFIO1.Options.OpenInPDFReader := True;
  TMSFNCDataGridPDFIO1.Save('Export.pdf');
end;

procedure TForm1.XLSClick(Sender: TObject);           // VCL/FMX only
begin
  TMSFNCDataGridExcelIO1.Renderer := r;
  TMSFNCDataGridExcelIO1.Options.ExportOverwrite := TOverwriteMode.omAlways;
  TMSFNCDataGridExcelIO1.Options.ExportShowInExcel := True;
  TMSFNCDataGridExcelIO1.DataGridStartCol := 0;      // defaults are 1
  TMSFNCDataGridExcelIO1.DataGridStartRow := 0;
  TMSFNCDataGridExcelIO1.XLSExport('Export.xls');
end;

procedure TForm1.HTMLClick(Sender: TObject); begin r.SaveToHTMLData('Export.html'); end;
procedure TForm1.CSVClick(Sender: TObject);  begin r.SaveToCSVData('Export.csv'); end;
```

Export components (all expose both `DataGrid` and `Renderer`):
- `TTMSFNCDataGridPDFIO` (`*.TMSFNCDataGridPDFIO`): `property Renderer: TTMSFNCDataGridRenderer`, `property DataGrid: TTMSFNCCustomDataGrid` (assigning DataGrid sets Renderer to `DataGrid.Root`), `Options: TTMSFNCDataGridPDFIOOptions` (inherits `Header`, `Footer`, `OpenInPDFReader`, fonts), `Save(const AFileName: String)` / `Save(const AStream: TStream)`.
- `TTMSFNCDataGridPrintIO` (`*.TMSFNCDataGridPrintIO`): same `Renderer`/`DataGrid`/`Options`; `Print`.
- `TTMSFNCDataGridExcelIO` (`Source\xlsAdapter\*.TMSFNCDataGridExcelIO`, **VCL and FMX only**): `Renderer`, `DataGrid`, `Options: TTMSFNCDataGridIOOptions` (`ExportOverwrite: TOverwriteMode` default `omNever`, `ExportShowInExcel` default False, ...), `DataGridStartRow/DataGridStartCol` (default 1), `XLSExport(const FileName: TFileName; const SheetName: UTF16String = ''; const SheetPos: integer = -1; const SelectSheet: integer = 1; const InsertInSheet: TInsertInSheet = InsertInSheet_Clear)`, `XLSImport(const FileName: TFileName)` (+ sheet number/name overloads).

Renderer/data file IO (each also has an `AEncoding: TEncoding` overload and a `...StreamData(AStream: TStream)` form):
```delphi
procedure LoadFromCSVData(AFileName: string); overload; virtual;
procedure LoadFromCSVData(AFileName: string; AEncoding: TEncoding); overload; virtual;
procedure SaveToCSVData(AFileName: string); overload; virtual;
procedure LoadFromJSONData / LoadFromJSONStreamData / LoadFromJSONTextData(AText: string ...)
procedure LoadFromXMLData / LoadFromXMLStreamData
procedure LoadFromFileData / SaveToFileData / LoadFromFileStreamData / SaveToFileStreamData   // native format
procedure SaveToHTMLData(AFileName: string); overload; virtual;          // renderer level
procedure SaveToHTMLStreamData(AStream: TStream); overload; virtual;
procedure SaveToImageData(AFileName: string); overload; virtual;         // bitmap snapshot
procedure SaveToImageStreamData(AStream: TStream); overload; virtual;
```
`Options.IO` (`TTMSFNCDataGridDataIOOptions`): `StartRow`, `StartColumn` (where import writes / export reads, default 0), `Delimiter`, `AlwaysQuotes`, `QuoteEmptyCells`, `TrimSpaces`, `MaxRows`, `ExportScale`, `OpenAfterCreation` (default **True** — set False in services/servers).

## RendererSource: swappable render "layers" (Advanced\Renderer Source)

```delphi
TTMSFNCDataGridRendererSource = class(TTMSFNCCustomComponent, ITMSFNCDataGridRendererSource)
public
  constructor Create(AOwner: TComponent); overload; override;
  constructor Create; reintroduce; overload;
  property Renderer: TTMSFNCDataGridRenderer read FRenderer;    // owned, never nil, never free it
published
  property ConditionalFormatting: TTMSFNCDataGridConditionalFormatting;  // = Renderer.ConditionalFormatting
end;
// on the grid:
property RendererSource: TTMSFNCDataGridRendererSource;   // published; nil = grid's own renderer
```

- While assigned, the grid renders **that renderer instance by reference**: its data, appearance, options and scroll behaviour. Live edits to `Source.Renderer` show immediately; grid calls (`Cells`, `RowCount`...) now operate on the source's renderer.
- The grid does **not own** the source. Setting `RendererSource := nil` or freeing the source reverts to the grid's own renderer and data (which were kept intact).
- Registered on the palette (`TMS FNC UI`) but `Renderer` is public only — fill data/appearance in code. `ConditionalFormatting` is published (editable at design time).
- Subclass and override `GetRendererInstanceClass: TTMSFNCDataGridRendererClass` (protected virtual) to inject a custom renderer class.
- Use cases: switch between datasets/themes in one grid without rebuilding; keep several pre-built views.

Demo (condensed):
```delphi
private
  FSalesLayer: TTMSFNCDataGridRendererSource;

procedure TFormRendererSource.FormCreate(Sender: TObject);
var r: TTMSFNCDataGridRenderer;
begin
  FSalesLayer := TTMSFNCDataGridRendererSource.Create(Self);
  r := FSalesLayer.Renderer;
  r.BeginUpdate;
  try
    r.CellAppearance.FixedLayout.Fill.Color := gcSteelblue;
    r.CellAppearance.FixedLayout.Font.Color := gcWhite;
    r.CellAppearance.NormalLayout.Fill.Color := gcAliceblue;
    r.CellAppearance.SelectedLayout.Fill.Color := gcLightsteelblue;
    r.Options.Column.Stretching.Enabled := True;
    r.FixedRowCount := 1;
    r.ColumnCount := 6;
    r.RowCount := 6;
    r.Cells[0, 0] := 'Region';
    // ...
  finally
    r.EndUpdate;
  end;
end;

procedure TFormRendererSource.btnSalesClick(Sender: TObject);
begin
  TMSFNCDataGrid1.RendererSource := FSalesLayer;    // show external layer
end;

procedure TFormRendererSource.btnDefaultClick(Sender: TObject);
begin
  TMSFNCDataGrid1.RendererSource := nil;            // back to the grid's own data
end;

procedure TFormRendererSource.btnAddRowClick(Sender: TObject);
var newRow: Integer;
begin
  TMSFNCDataGrid1.BeginUpdate;
  try
    newRow := TMSFNCDataGrid1.RowCount;
    TMSFNCDataGrid1.RowCount := newRow + 1;          // affects whichever layer is active
    TMSFNCDataGrid1.Cells[0, newRow] := Format('Added row %d', [newRow]);
  finally
    TMSFNCDataGrid1.EndUpdate;
  end;
end;
```

## Platform notes

- WEB (TMS WEB Core) PDF export needs fonts in the PDF font cache; the WEB demo does:
```delphi
Application.OnFontCacheReady := DoFontCacheReady;   // enable the export button there
AddFontToCache('https://download.tmssoftware.com/tmsweb/pdf/fonts/Roboto-Regular.ttf');  // + Bold, Italic, BoldItalic
r := TTMSFNCDataGridRenderer.Create;
r.GlobalFont.Name := 'Roboto';
r.LoadFromCSVData('train.csv', TEncoding.UTF8);
// before Save:
TMSFNCDataGridPDFIO1.Options.DefaultFont.Name := 'Roboto';
TMSFNCDataGridPDFIO1.Options.HeaderFont.Name := 'Roboto';
TMSFNCDataGridPDFIO1.Options.FooterFont.Name := 'Roboto';
TMSFNCDataGridPDFIO1.Options.PageNumberFont.Name := 'Roboto';
TMSFNCDataGridPDFIO1.Options.FontFallBackList.Insert(0, 'Roboto');
```
  (uses `WEBLib.TMSFNCPDFLib`). No ExcelIO on WEB. File-based load/save maps to browser download/URL loading.
- RendererSource demo is identical on VCL/FMX/WEB.

## Does not exist / common mistakes

- `TTMSFNCDataGridRenderer` is not a control: no `Parent`, `Align`, `Visible` on screen. Display it via `Grid.RendererSource` (wrapped in `TTMSFNCDataGridRendererSource`) or inside a cell via `AddGrid`.
- `Grid.Renderer := r` / `Grid.DataSource := r` / `Grid.Data` — no such assignment; use `RendererSource` with a `TTMSFNCDataGridRendererSource`.
- Freeing `RendererSource.Renderer` — owned by the source.
- Forgetting to free a standalone `TTMSFNCDataGridRenderer.Create` — it has no owner.
- `PDFIO.Grid` / `ExcelIO.Grid` — the properties are `DataGrid` or `Renderer`.
- `TTMSFNCDataGridExcelIO` in a WEB project — not available.
- `SaveToCSVData` popping open Excel/Notepad on a server — `Options.IO.OpenAfterCreation` defaults to True; set False.
- `SaveToXLS`, `SaveToPDF`, `ExportToPDF` methods on the grid — use the IO components (`PDFIO.Save`, `ExcelIO.XLSExport`).
