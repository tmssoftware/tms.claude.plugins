# TMS FNC DataGrid: PDF, Excel and print export

There are three non-visual components, all on palette page `TMS FNC UI`, and all linked to the grid via a published **`DataGrid`** property:

| Component | Unit (VCL / FMX / WEB) | Base class (FNC Core) | Platforms |
|---|---|---|---|
| `TTMSFNCDataGridPDFIO` | `VCL.TMSFNCDataGridPDFIO` / `FMX.` / `WEBLib.` | `TTMSFNCCustomPDFIO` (`*.TMSFNCPDFIO`) | VCL, FMX, WEB |
| `TTMSFNCDataGridPrintIO` | `VCL.TMSFNCDataGridPrintIO` / `FMX.` / `WEBLib.` | `TTMSFNCCustomPrintIO` (`*.TMSFNCPrintIO`) | VCL, FMX, WEB |
| `TTMSFNCDataGridExcelIO` | `VCL.TMSFNCDataGridExcelIO` / `FMX.TMSFNCDataGridExcelIO` | `TTMSFNCCustomComponent` | VCL, FMX desktop only (`TMSPlatformsDesktop`). **No WEB** |

All three also have a public `Renderer: TTMSFNCDataGridRenderer`, which exports a non-visual `TTMSFNCDataGridRenderer` instead of a visible grid.

Where they come from: PDF and Print IO sources are in `tms.fnc.uipack\Source\`, and their base classes and PDF library (`*.TMSFNCPDFLib`) are in **TMS FNC Core**. Excel IO is in `tms.fnc.uipack\Source\xlsAdapter\`, together with its own bundled XLS engine units (`*.TMSFNCXLSAdapter`, `*.TMSFNCUExcelAdapter`, `*.TMSFNCUFlx*`, `*.TMSFNCUXls*`). All of these compile into `VCLTMSFNCUIPackPkg` / `FMXTMSFNCUIPackPkg`, so **Excel export needs no FlexCel or other product**, only the UI Pack + FNC Core.

When a project compiles the TMS **source** instead of the installed packages (for example a command-line build whose search path points at `tms.fnc.uipack\Source`), add `tms.fnc.uipack\Source\xlsAdapter` to the unit search path as well, or `FMX.TMSFNCDataGridExcelIO` is not found.

### File names for export

Build the path as a plain string next to the exe (or in a folder the user picks), then pass it to `Save` / `XLSExport`:

```delphi
var
  fn: string;
begin
  fn := ExtractFilePath(ParamStr(0)) + 'Report.pdf';
  PDFIO.Save(fn);
end;
```

In **FMX units, `TPath` usually means `FMX.Objects.TPath`** (a vector-shape control), not `System.IOUtils.TPath`, so `TPath.Combine` / `TPath.GetDocumentsPath` fail with "Undeclared identifier: 'Combine'". Write `System.IOUtils.TPath.Combine(...)` fully qualified (and add `System.IOUtils` to the uses clause), or use `ExtractFilePath` / `IncludeTrailingPathDelimiter` as above. Open the result with `TTMSFNCUtils.OpenFile(fn)` (`*.TMSFNCUtils`) or `Options.OpenInPDFReader := True` for PDF.

---

## PDF: TTMSFNCDataGridPDFIO

```delphi
TTMSFNCDataGridPDFIO = class(TTMSFNCCustomDataGridPDFIO)
published
  property DataGrid;            // TTMSFNCCustomDataGrid
  property Information;         // TTMSFNCPDFIOInformation: Author, Title, Subject, Keywords (TStringList), Creator
  property Options;             // TTMSFNCDataGridPDFIOOptions
  property OnGetHeader, OnGetFooter, OnRowIsPageBreak;
  property OnBeforeDrawHeader, OnAfterDrawHeader, OnBeforeDrawFooter, OnAfterDrawFooter;
  property OnBeforeDrawContent, OnAfterDrawContent;
  property Version;
public
  property Renderer;            // TTMSFNCDataGridRenderer
```

Save methods (inherited from `TTMSFNCCustomPDFIO`, FNC Core):

```delphi
procedure Save(const AFileName: String); overload;
procedure Save(const AStream: TStream); overload;
procedure Save(const AFileName: String; AExportObject: TTMSFNCPDFIOExportObject; AExportRect: TRectF); overload;
procedure Save(const AFileName: String; AExportObjects: TTMSFNCPDFIOExportObjectArray); overload;   // several objects, one PDF
// + TStream variants and (AExportObjects, AExportRects: TTMSFNCPDFIOExportRectArray)
```

`TTMSFNCPDFIOExportObject = TObject`.

Grid-specific options on `TTMSFNCDataGridPDFIOOptions`, which descends from `TTMSFNCPDFIOOptions`:

```delphi
property Scale: Single;                              // stored only when changed
property FitToPage: Boolean default True;
property RepeatFixedRows: Boolean default False;     // repeat header rows on every page
property RepeatFixedColumns: Boolean default False;
```

Inherited `TTMSFNCPDFIOOptions` properties that are commonly used: `OpenInPDFReader: Boolean` (default False), `Header`, `Footer: UnicodeString`, `HeaderFont`, `FooterFont`, `DefaultFont`, `PageNumberFont: TTMSFNCPDFGraphicsLibFont`, `Margins`, `HeaderMargins`, `FooterMargins`, `PageNumberMargins: TTMSFNCMargins`, `HeaderAlignment`, `FooterAlignment`, `PageNumberAlignment`, `PageSize: TTMSFNCPDFLibPageSize` (default `psLetter`, e.g. `psA4`), `PageOrientation: TTMSFNCPDFLibPageOrientation` (`poPortrait`/`poLandscape`), `PageWidth`, `PageHeight`, `PageNumber: TTMSFNCPDFLibPageNumber` (`pnNone`/`pnHeader`/`pnFooter`, default `pnHeader`), `PageNumberFormat` (e.g. `'%d'`), `ExportImages` (default True), `EmbedFonts` (default True), `FontFallBackList: TStrings`.

Events:

```delphi
TTMSFNCPDFIOGetFooterEvent = procedure(Sender: TObject; AExportObject: TObject; APageIndex: Integer; var AFooter: UnicodeString) of object;
TTMSFNCPDFIOGetHeaderEvent = procedure(Sender: TObject; AExportObject: TObject; APageIndex: Integer; var AHeader: UnicodeString) of object;
TTMSFNCDataGridPDFIORowIsPageBreakEvent = procedure(Sender: TObject; AExportObject: TTMSFNCPDFIOExportObject; ARow: Integer; var IsPageBreak: Boolean) of object;
```

### VCL demo (`VCL\DataGrid\Basic\PDF Export`)

Uses: `VCL.TMSFNCPDFIO, VCL.TMSFNCDataGridPDFIO` plus the usual grid units. In the DFM: `DataGrid = TMSFNCDataGrid1`, `OnGetFooter = TMSFNCDataGridPDFIO1GetFooter`.

```delphi
procedure TForm130.FormCreate(Sender: TObject);
begin
  // ... fill grid ...
  TMSFNCDataGridPDFIO1.Options.OpenInPDFReader := True;
  TMSFNCDataGridPDFIO1.Options.Header := 'TMS FNC Data Grid PDF Export';
end;

procedure TForm130.Button2Click(Sender: TObject);
begin
  TMSFNCDataGridPDFIO1.Save('gridexport.pdf');
end;

procedure TForm130.TMSFNCDataGridPDFIO1GetFooter(Sender, AExportObject: TObject;
  APageIndex: Integer; var AFooter: string);
begin
  AFooter := 'Page ' + IntToStr(APageIndex + 1);
end;

// change appearance only in the export:
procedure TForm130.TMSFNCDataGrid1BeforeDrawCell(Sender: TObject; AGraphics: TTMSFNCGraphics;
  ACell: TTMSFNCDataGridCell; var ACanDraw: Boolean);
begin
  if ACell.IsExporting then
    ACell.DrawElements := [gcdText, gcdStroke];   // no fill when exporting
end;
```

Code-only setup:

```delphi
PDF := TTMSFNCDataGridPDFIO.Create(Self);
PDF.DataGrid := TMSFNCDataGrid1;
PDF.Options.PageOrientation := TTMSFNCPDFLibPageOrientation.poLandscape;  // qualify: poLandscape also exists in Printers.TPrinterOrientation
PDF.Options.RepeatFixedRows := True;
PDF.Information.Title := 'Customers';
PDF.Save('customers.pdf');
```

The database grid works the same way. The Master_Detail_FireDac_SQLite demo exports the adapter-bound grid:

```delphi
TMSFNCDataGridPDFIO1.Options.Header := 'Master Detail';
TMSFNCDataGridPDFIO1.Options.Footer := '';
TMSFNCDataGridPDFIO1.Options.OpenInPDFReader := True;
TMSFNCDataGridPDFIO1.Save('Export.pdf');
```

With the default `LoadMode = almBuffered` only buffered records are in the grid. Before exporting a whole dataset, consider `Adapter.LoadMode := almAllRecords` or `Adapter.LoadAllData`.

### WEB Core (`WEB\DataGrid\Basic\PDF Export`)

The PDF needs fonts in the font cache before saving. The demo enables the button only after `OnFontCacheReady` fires:

```delphi
implementation
uses WEBLib.TMSFNCPDFLib;

procedure TForm130.FormCreate(Sender: TObject);
begin
  Application.OnFontCacheReady := DoFontCacheReady;
  AddFontToCache('https://download.tmssoftware.com/tmsweb/pdf/fonts/Roboto-Regular.ttf');
  AddFontToCache('https://download.tmssoftware.com/tmsweb/pdf/fonts/Roboto-Bold.ttf');
  AddFontToCache('https://download.tmssoftware.com/tmsweb/pdf/fonts/Roboto-BoldItalic.ttf');
  AddFontToCache('https://download.tmssoftware.com/tmsweb/pdf/fonts/Roboto-Italic.ttf');
  TMSFNCDataGrid1.GlobalFont.Name := 'Roboto';
  TMSFNCDataGridPDFIO1.Options.OpenInPDFReader := True;
end;

procedure TForm130.DoFontCacheReady(Sender: TObject);
begin
  Button2.Enabled := True;
end;

procedure TForm130.Button2Click(Sender: TObject);
begin
  TMSFNCDataGridPDFIO1.Options.DefaultFont.Name := 'Roboto';
  TMSFNCDataGridPDFIO1.Options.HeaderFont.Name := 'Roboto';
  TMSFNCDataGridPDFIO1.Options.FooterFont.Name := 'Roboto';
  TMSFNCDataGridPDFIO1.Options.PageNumberFont.Name := 'Roboto';
  TMSFNCDataGridPDFIO1.Options.FontFallBackList.Insert(0, 'Roboto');
  TMSFNCDataGridPDFIO1.Save('gridexport.pdf');
end;
```

### Non-visual export (`WEB\DataGrid\Advanced\Non-Visual Data Export`)

```delphi
r := TTMSFNCDataGridRenderer.Create;
r.LoadFromCSVData('train.csv', TEncoding.UTF8);
r.Options.IO.OpenAfterCreation := True;
TMSFNCDataGridPDFIO1.Renderer := r;      // instead of DataGrid
TMSFNCDataGridPDFIO1.Save('Export.pdf');
r.SaveToHTMLData('Export.html');
r.SaveToCSVData('Export.csv');
// r.Free in FormDestroy
```

---

## Excel (.xls): TTMSFNCDataGridExcelIO

The bundled engine reads and writes **binary Excel `.xls` (BIFF)**. Nothing in the UI Pack source handles `.xlsx`.

```delphi
[ComponentPlatformsAttribute(TMSPlatformsDesktop)]
TTMSFNCDataGridExcelIO = class(TTMSFNCCustomComponent)
public
  procedure XLSImport(const FileName: TFileName); overload;
  procedure XLSImport(const FileName: TFileName; const SheetNumber: integer); overload;
  procedure XLSImport(const FileName: TFileName; const SheetName: UTF16String); overload;
  procedure XLSExport(const FileName: TFileName; const SheetName: UTF16String = ''; const SheetPos: integer = -1;
    const SelectSheet: integer = 1; const InsertInSheet: TInsertInSheet = InsertInSheet_Clear);
  procedure LoadSheetNames(const FileName: string);
  property SheetNames[index: integer]: UTF16String;   // read-only
  property SheetNamesCount: integer;
  property Renderer: TTMSFNCDataGridRenderer;
published
  property DataGrid: TTMSFNCCustomDataGrid;
  property AutoResizeDataGrid: Boolean default true;
  property Options: TTMSFNCDataGridIOOptions;
  property UseUnicode: boolean;
  property DataGridStartRow: integer default 1;  property DataGridStartCol: integer default 1;  // 1 = skip grid row 0 / column 0!
  property XlsStartRow: integer default 1;       property XlsStartCol: integer default 1;
  property ZoomSaved: boolean default true;      property Zoom: integer default 100;
  property DateFormat, TimeFormat: UTF16String;
  property Version: string;
  property OnProgress: TTMSFNCDataGridIOProgressEvent;
  property OnDateTimeFormat, OnCellFormat, OnExportColumnFormat, OnGetCellFormula;  // not on FMX mobile
end;

TOverwriteMode = (omNever, omAlways, omWarn);
TInsertInSheet = (InsertInSheet_Clear, InsertInSheet_OverwriteCells, InsertInSheet_InsertRows,
  InsertInSheet_InsertCols, InsertInSheet_InsertRowsExceptFirstAndSecond, InsertInSheet_InsertColsExceptFirstAndSecond);
TTMSFNCDataGridIOProgressEvent = procedure(Sender: TObject; SheetNum, SheetTot, RowNum, RowTot: integer) of object;
TExportColumnFormatEvent = procedure(Sender: TObject; DataGridCol, DataGridRow, XlsCol, XlsRow: integer; const Value: WideString; var ExportCellAsString: boolean) of object;
TFlxGetCellFormulaEvent = procedure(Sender: TObject; const DataGridCol, DataGridRow: integer; const Value: WideString; var Formula: WideString) of object;
```

`TTMSFNCDataGridIOOptions` (published, with defaults):
- Import: `ImportFormulas` (True), `ImportImages` (True), `ImportCellFormats` (True), `ImportCellProperties` (**False**), `ImportCellSizes` (True), `ImportClearCells` (True), `ImportLockedCellsAsReadonly` (False), `ImportPrintOptions` (True).
- Export: `ExportOverwrite: TOverwriteMode` (default **`omNever`**), `ExportOverwriteMessage: string`, `ExportFormulas` (True), `ExportCellFormats` (True), `ExportCellProperties` (True), `ExportCellSizes` (True), `ExportHiddenColumns` (False), `ExportImages` (True), `ExportReadonlyCellsAsLocked` (False), `ExportWordWrapped` (False), `ExportHTMLTags` (True), `ExportShowInExcel` (False), `ExportHardBorders` (False), `ExportShowGridLines` (True), `ExportPrintOptions` (True), `ExportSummaryRowsBelowDetail` (False), `ExportCellMargins` (False), `UseExcelStandardColorPalette` (True).

### Demo (`VCL\DataGrid\Basic\XLS Export`)

Uses `VCL.TMSFNCDataGridExcelIO` (plus `VCL.TMSFNCUtils` for `TTMSFNCUtils.OpenFile`). DFM: `DataGrid = TMSFNCDataGrid1`.

```delphi
procedure TForm130.FormCreate(Sender: TObject);
begin
  TMSFNCDataGridExcelIO1.Options.ImportCellProperties := True;
  TMSFNCDataGridExcelIO1.Options.ExportCellProperties := True;
  TMSFNCDataGridExcelIO1.Options.ExportOverwrite := omAlways;   // default omNever: an existing file is NOT overwritten
  TMSFNCDataGridExcelIO1.Options.ExportImages := True;
  // Not in the demo, but almost always wanted: the defaults (1) leave out grid row 0
  // (the column captions) and column 0 (often an ID column) from the .xls.
  TMSFNCDataGridExcelIO1.DataGridStartRow := 0;
  TMSFNCDataGridExcelIO1.DataGridStartCol := 0;
end;

procedure TForm130.Button1Click(Sender: TObject);
begin
  TMSFNCDataGridExcelIO1.XLSImport('CARS.xls');
end;

procedure TForm130.Button2Click(Sender: TObject);
begin
  TMSFNCDataGridExcelIO1.XLSExport('gridexport.xls');
  TTMSFNCUtils.OpenFile('gridexport.xls');
end;
```

Export into a named sheet: `XLSExport('report.xls', 'Customers');`. Pick a sheet before import with `LoadSheetNames(f)`, iterate `SheetNames[i]` for `i := 0 to SheetNamesCount - 1`, then call `XLSImport(f, SheetName)`.

---

## Printing: TTMSFNCDataGridPrintIO

```delphi
[ComponentPlatformsAttribute(TMSPlatformsWeb)]
TTMSFNCDataGridPrintIO = class(TTMSFNCCustomDataGridPrintIO)
public
  property Renderer;
published
  property DataGrid;
  property Options;              // TTMSFNCDataGridPrintIOOptions
  property OnBeforeDrawContent, OnAfterDrawContent, OnRowIsPageBreak;
  property Version;
end;
```

Methods (from `TTMSFNCCustomPrintIO`, FNC Core):

```delphi
procedure Print; overload;
procedure Print(AExportObject: TTMSFNCPrintIOExportObject; AExportRect: TRectF); overload;
procedure Print(AExportObjects: TTMSFNCPrintIOExportObjectArray); overload;
procedure Print(AExportObjects: TTMSFNCPrintIOExportObjectArray; AExportRects: TTMSFNCPrintIOExportRectArray); overload;
```

`TTMSFNCDataGridPrintIOOptions` adds `Scale`, `FitToPage` (True), `RepeatFixedRows` (False) and `RepeatFixedColumns` (False) to `TTMSFNCPrintIOOptions`, which provides `Header`, `Footer: string`, `HeaderFont`, `FooterFont`, `DefaultFont`, `PageNumberFont: TTMSFNCGraphicsFont`, `Margins`, `PageNumber: TTMSFNCPrintPageNumber` (default **`pnNone`**), `PageNumberFormat`, `PageOrientation: TPrinterOrientation`, `PageSize: TPrintSize`, `Device: string`, and read-only `DPI`, `PageWidth`, `PageHeight`, `PageIndex`.

Demo (`VCL\PrintIO\UPrintIODemo.pas`, uses `VCL.TMSFNCPrintIO, VCL.TMSFNCDataGridPrintIO`):

```delphi
procedure TForm3.FormCreate(Sender: TObject);
begin
  TMSFNCDataGridPrintIO1.DataGrid := TMSFNCDataGrid1;
end;

procedure TForm3.Button2Click(Sender: TObject);
begin
  if PrintDialog1.Execute then
  begin
    TMSFNCDataGridPrintIO1.Options.Footer := 'My Footer Text';
    TMSFNCDataGridPrintIO1.Options.PageNumber := pnHeader;
    TMSFNCDataGridPrintIO1.Options.PageNumberFormat := 'Page %d';
    TMSFNCDataGridPrintIO1.Print;
  end;
end;
```

The same demo also prints the grid as a picture with FNC Core's `TTMSFNCGraphicsPrintIO.Print(TMSFNCDataGrid1, r)`. Use `TTMSFNCDataGridPrintIO` when you want paginated rows. FMX and WEB have the same demo (`FMX\PrintIO`, `WEB\PrintIO`), and both call `TMSFNCDataGridPrintIO1.Print`.

---

## Other built-in export (no extra component)

On the grid and renderer (verified): `SaveToCSVData(AFileName: string)`, `SaveToCSVData(AFileName; AEncoding: TEncoding)`, `SaveToHTMLData(AFileName: string)`, `SaveToFileData(AFileName: string)`, `LoadFromCSVData(...)`. These work on WEB too.

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `Grid.ExportToPDF`, `Grid.SaveToPDF`, `Grid.SaveToXLS`, `Grid.Print` | Use the IO components: `TTMSFNCDataGridPDFIO.Save`, `TTMSFNCDataGridExcelIO.XLSExport`, `TTMSFNCDataGridPrintIO.Print` |
| `PDFIO.Grid := ...` / `PDFIO.Export(...)` / `PDFIO.SaveToFile(...)` | `PDFIO.DataGrid := Grid; PDFIO.Save('x.pdf')` |
| `TPath.Combine(...)` in an FMX unit | `System.IOUtils.TPath.Combine(...)` (FMX's `TPath` is the shape control) or `ExtractFilePath(ParamStr(0)) + 'x.pdf'` |
| `ExcelIO.SaveToFile` / `ExcelIO.Export` / `ExcelIO.XLSXExport` | `XLSExport(FileName, ...)` / `XLSImport(FileName, ...)`. `.xls` only |
| Expecting `XLSExport` to include the header row and first column | Defaults `DataGridStartRow = 1` and `DataGridStartCol = 1` skip grid row 0 (column captions) and column 0. Set both to `0` before `XLSExport` to export the whole grid |
| Expecting `XLSExport` to overwrite an existing file | Default `Options.ExportOverwrite = omNever`. Set `omAlways` or `omWarn` |
| `TTMSFNCGridExcelIO` / `TTMSFNCGridPDFIO` with `TTMSFNCDataGrid` | Those are for the older `TTMSFNCGrid`. Use the `TTMSFNCDataGrid...IO` classes |
| `TAdvGridExcelIO`, FlexCel `TXlsFile` for the FNC data grid | Not needed. Excel IO is bundled in the UI Pack (`Source\xlsAdapter`) |
| Excel IO in TMS WEB Core / iOS / Android | Desktop only (`TMSPlatformsDesktop`). Not in the WEB package |
| Print page numbers appear by default | Print default `PageNumber = pnNone` (the PDF default is `pnHeader`). The enums differ: `TTMSFNCPrintPageNumber` vs `TTMSFNCPDFLibPageNumber` |
| `Options.Orientation` / `Options.Landscape` | `Options.PageOrientation` |
| WEB PDF saved before fonts load (missing glyphs or wrong font) | Call `AddFontToCache(...)` and wait for `Application.OnFontCacheReady` |
| A database-bound export misses records or values (default `almBuffered` buffers only visible rows) | Try `Adapter.LoadMode := almAllRecords` or `Adapter.LoadAllData` before exporting (not verified end-to-end here) |
