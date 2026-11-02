# PDF generation, PDF export and printing (TTMSFNCPDFLib, TTMSFNCGraphicsPDFIO, TTMSFNCGraphicsPrintIO, TTMSFNCPrinter)

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCPDFLib`, `*.TMSFNCPDFGraphicsLib`, `*.TMSFNCPDFCoreLibBase`, `*.TMSFNCPDFRichTextLib`, `*.TMSFNCPDFIO`, `*.TMSFNCGraphicsPDFEngine`, `*.TMSFNCPrintIO`, `*.TMSFNCPrinters`.

## Units and palette

| Class | Unit (`VCL.` / `FMX.` / `WEBLib.` prefix; LCL = `LCLTMSFNC...`) | Palette |
|---|---|---|
| `TTMSFNCPDFLib` | `*.TMSFNCPDFLib` | TMS FNC UI |
| `ITMSFNCCustomPDFGraphicsLib` (type of `PDF.Graphics`) | `*.TMSFNCPDFGraphicsLib` | - |
| `TTMSFNCPDFGraphicsLibFont`, `dmPathStroke`, `itJPG`, `TTMSFNCPDFPageInfo` | `*.TMSFNCPDFCoreLibBase` | - |
| `TTMSFNCGraphicsPDFIO` (export any FNC control) | `*.TMSFNCGraphicsPDFEngine` (options/events types in `*.TMSFNCPDFIO`) | TMS FNC UI |
| `TTMSFNCGraphicsPrintIO` | `*.TMSFNCPrintIO` | TMS FNC UI |
| `TTMSFNCPrinter` + global function `TMSFNCPrinter` | `*.TMSFNCPrinters` | not a component |

Colors (`gcRed`), fill/stroke kinds (`gfkSolid`, `gskDash`) and `gtaCenter` come from `*.TMSFNCGraphicsTypes`. Grid-specific exporters (`TTMSFNCDataGridPDFIO`, `TTMSFNCDataGridPrintIO`) live in UI Pack, see the datagrid `export.md`.

## TTMSFNCPDFLib: generating a PDF

Non-visual; usually created in code. Both constructors exist: `constructor Create;` and `constructor Create(AOwner: TComponent);`.

```delphi
procedure BeginDocument(FileName: String = '');
procedure NewPage;
function Graphics: ITMSFNCCustomPDFGraphicsLib;
function EndDocument(AOpenInPDFReader: Boolean = False): TMemoryStream;
function GetPageCount: Integer;   function GetPageIndex: Integer;
function GetHeaderRect: TRectF;   function GetFooterRect: TRectF;   function GetPageNumberRect: TRectF;
property PageSize: TTMSFNCPDFLibPageSize;            // psLetter default; psA0..psA8, psB0..psB10, psLegal, psLedger, psTabloid, psExecutive, ..., psCustom
property PageOrientation: TTMSFNCPDFLibPageOrientation; // poPortrait, poLandscape
property PageWidth: Single;  property PageHeight: Single;   // points (72/inch); used with PageSize := psCustom
property MediaBox, TrimBox, ArtBox, BleedBox, CropBox: TRectF;
property EmbedFonts: Boolean;  property EmbedFontType: TTMSFNCPDFEmbedFontType; // eftNative, eftCustom
property FontFallBackList: TStrings;
property BitmapContainer: TTMSFNCBitmapContainer;   // for DrawImageWithName and <img src="name"> in HTML text
```

`EndDocument` contract (from `TTMSFNCGeneralPDFLib.EndDocument`):
- `BeginDocument('file.pdf')` writes the file and `EndDocument` returns **nil** (`True` opens the file with the default viewer).
- `BeginDocument` / `BeginDocument('')` returns a new `TMemoryStream` you must free.
- `EndDocument` raises if no page was added (`NewPage` never called).

### Header, footer, page number, metadata

```delphi
property Header: UnicodeString;  property HeaderSize: Single;  property HeaderMargins: TTMSFNCMargins;
property HeaderAlignment: TTMSFNCGraphicsTextAlign;  property HeaderFont: TTMSFNCPDFGraphicsLibFont;
property Footer: UnicodeString;  property FooterSize: Single;  property FooterMargins: TTMSFNCMargins;
property FooterAlignment: TTMSFNCGraphicsTextAlign;  property FooterFont: TTMSFNCPDFGraphicsLibFont;
property PageNumber: TTMSFNCPDFLibPageNumber;         // pnNone, pnHeader, pnFooter
property PageNumberFormat: UnicodeString;             // default '%d'
property PageNumberSize, PageNumberMargins, PageNumberAlignment, PageNumberFont;
property Title, Subject, Author, Creator, Producer, CreationDate, ModificationDate: String;
property Keywords: TStrings;
```
Header/footer/page number are drawn when a page starts, so set them **before** `NewPage` (change them between pages for per-page text). Header text accepts HTML formatting. Events (all with `AGraphics: ITMSFNCCustomPDFGraphicsLib` to custom-draw):
```delphi
TTMSFNCPDFLibBeforeDrawHeaderEvent = procedure(Sender: TObject; APageIndex: Integer; AHeader: UnicodeString; ARect: TRectF; AGraphics: ITMSFNCCustomPDFGraphicsLib; var ADefaultDraw: Boolean) of object;
TTMSFNCPDFLibAfterDrawHeaderEvent = procedure(Sender: TObject; APageIndex: Integer; AHeader: UnicodeString; ARect: TRectF; AGraphics: ITMSFNCCustomPDFGraphicsLib) of object;
TTMSFNCPDFLibNewPageStartedEvent = procedure(Sender: TObject; APageIndex: Integer) of object;
// same pattern: OnBeforeDrawFooter/OnAfterDrawFooter, OnBeforeDrawPageNumber/OnAfterDrawPageNumber, OnNewPageStarted
```

### ITMSFNCCustomPDFGraphicsLib (PDF.Graphics)

Properties: `Fill: TTMSFNCPDFGraphicsFill` (`Color`, `ColorTo`, `Kind`), `Stroke: TTMSFNCPDFGraphicsStroke` (`Color`, `Width`, `Kind`), `Font: TTMSFNCPDFGraphicsLibFont` (`Name`, `Size`, `SizeNoScale`, `Color`, `Style`, `FileName`), `URLFont`, `Alignment: TTMSFNCGraphicsTextAlign`, `LineBreakMode` (`bmLineBreakModeWordWrap`, `bmLineBreakModeCharacterWrap`, `bmLineBreakModeClip`), `LineHeightFactor`, `BitmapContainer`.

```delphi
procedure DrawRectangle(Rect: TRectF);
procedure DrawEllipse(Rect: TRectF);
procedure DrawLine(StartPoint, EndPoint: TPointF);
function DrawText(Text: UnicodeString; Point: TPointF; Calculate: Boolean = False): TRectF; overload;
function DrawText(Text: UnicodeString; Rect: TRectF; Calculate: Boolean = False): TRectF; overload;
function DrawText(Text: UnicodeString; Rect: TRectF; Columns: Integer; Padding: Single = 5.0; DetectOverflow: Boolean = False): Integer; overload;
function DrawHTMLText(Text: UnicodeString; Point: TPointF; Scale: Single = 1.0; Calculate: Boolean = False): TRectF; overload;
function DrawHTMLText(Text: UnicodeString; Rect: TRectF; Paging: Boolean = False; Scale: Single = 1.0; Calculate: Boolean = False): TRectF; overload;
function CalculateText(Text: UnicodeString; Rect: TRectF): TRectF; overload;
function CalculateHTMLText(Text: UnicodeString; Rect: TRectF; Scale: Single = 1.0): TRectF; overload;
function DrawImageFromFile(AFileName: String; Rect: TRectF; Stretch: Boolean = True; AspectRatio: Boolean = True; ImageType: TTMSFNCPDFGraphicsLibImageType = itOriginal; Quality: Single = 1.0; Center: Boolean = True): TRectF; overload;
function DrawImage(ABitmap: TTMSFNCBitmapHelperClass; Rect: TRectF; Stretch: Boolean = True; ...): TRectF; overload;
function DrawImageWithName(AName: string; Rect: TRectF; ...): TRectF; overload;   // name from BitmapContainer
procedure AddURL(AText: UnicodeString; AURL: UnicodeString; ARect: TRectF);
procedure AddGoTo(AText: Unicodestring; APageIndex: Integer; AOptions: UnicodeString; ARect: TRectF); overload;
procedure DrawPathBegin; DrawPathMoveToPoint(Point: TPointF); DrawPathAddLineToPoint(Point: TPointF);
procedure DrawPathAddCurveToPoint(FirstControlPoint, SecondControlPoint, EndPoint: TPointF);
procedure DrawPathAddRectangle(Rect: TRectF); DrawPathAddEllipse(Rect: TRectF); DrawPathClose;
procedure DrawPathEnd(DrawingMode: TTMSFNCPDFGraphicsLibPathDrawingMode = dmPathFillStroke); // dmPathFill, dmPathEOFill, dmPathStroke, ...
procedure DrawPathBeginClip; DrawPathEndClip; DrawPathEndLinearGradient(StartPoint, EndPoint: TPointF);
procedure DrawSaveState; DrawRestoreState;
procedure DrawSetTransform(m11, m12, m21, m22, dx, dy: Double); overload;
```
Coordinates are PDF points, origin top-left. Converters in `*.TMSFNCPDFLib`: `MillimeterToPixel`, `MillimeterRect(AX, AY, AWidth, AHeight)`, `InchToPixel`, `InchRect`, `PixelToMillimeter`.

**Font size:** `Font.Size` is rescaled per platform (on VCL/WEB the setter stores `Size * 96 / 72`, rounded down). Use `Font.SizeNoScale` for an exact point size, as every demo does.

Rounded rectangles, arcs, shadows, radial gradients and rich text are on a second interface, `ITMSFNCCustomPDFGraphicsExLib` (implemented by every backend):
```delphi
var gx: ITMSFNCCustomPDFGraphicsExLib;
if Supports(PDF.Graphics, ITMSFNCCustomPDFGraphicsExLib, gx) then
begin
  gx.DrawRoundedRectangle(RectF(50, 50, 250, 120), 8);
  gx.RichText.Text := 'Bold part and normal part';
  gx.RichText.SetBold(True, 0, 9);            // SetBold(AValue, AStart, ALength)
  gx.RichText.SetForegroundColor(gcRed, 0, 4);
  gx.DrawRichText(RectF(50, 140, 400, 300));
end;
```

### Example (demo `VCL\PDFLib` and `VCL\PDFCapabilities`)

```delphi
uses VCL.TMSFNCPDFLib, VCL.TMSFNCPDFCoreLibBase, VCL.TMSFNCPDFGraphicsLib,
  VCL.TMSFNCGraphicsTypes, System.Types;

procedure TForm1.CreatePDF(const AFileName: string);
var
  p: TTMSFNCPDFLib;
  rh, tr: TRectF;
begin
  p := TTMSFNCPDFLib.Create;
  try
    p.PageSize := psA4;
    p.BeginDocument(AFileName);
    p.Title := 'Report';
    p.Author := 'TMS Software';
    p.Header := 'TMS PDF Library';
    p.Footer := 'Generated with TTMSFNCPDFLib';
    p.PageNumber := pnFooter;
    p.PageNumberFormat := 'Page %d';
    p.NewPage;
    rh := p.GetHeaderRect;
    p.Graphics.Font.Name := 'Arial';
    p.Graphics.Font.SizeNoScale := 12;
    p.Graphics.Font.Style := [TFontStyle.fsBold];
    tr := p.Graphics.DrawText('Drawing primitives', PointF(rh.Left, rh.Bottom + 10));
    p.Graphics.Fill.Color := gcOrange;
    p.Graphics.Stroke.Color := gcSteelblue;
    p.Graphics.DrawRectangle(RectF(rh.Left + 10, tr.Bottom + 10, rh.Left + 50, tr.Bottom + 50));
    p.Graphics.Font.SizeNoScale := 10;
    p.Graphics.Font.Style := [];
    p.Graphics.DrawHTMLText('Some <b>bold</b> and <font color="gcRed">red</font> text',
      RectF(rh.Left, tr.Bottom + 70, rh.Right, 400));
    p.Graphics.AddURL('TMS website', 'https://www.tmssoftware.com', RectF(72, 420, 300, 440));
    p.EndDocument(True);   // file written; True opens it
  finally
    p.Free;
  end;
end;
```

### Form fields, opening and editing existing PDFs

- `PDF.FormFields` (`ITMSFNCCustomPDFFormFieldsLib`): `AddEdit(AFieldName, ARect, ...)`, `AddMemo`, `AddPasswordEdit`, `AddComboBox(AFieldName, ARect, AItems: TTMSFNCPDFLibStringArray or TStrings, ...)`, `AddListBox`, `AddCheckBox(AFieldName, ARect, AIsChecked, ...)`, `AddRadioGroup(AFieldName, AGroupID)` then `AddRadioButton(AFieldName, ARect, AGroupID, ...)`. Demo `VCL\PDFLibFormFields`. Declared `{$IFNDEF USENATIVE}`: **not available on FMX macOS/iOS/Android**.
- Editing (demos `PDFCapabilities`, `PDFLibWatermark`, `PDFLibManipulation`): `OpenDocument(FileName)`, metadata properties, `BeginPageEdit(PageIndex, pelOverlay | pelUnderlay)` + draw on `Graphics` + `EndPageEdit` / `CancelPageEdit`, `DeletePage`, `MovePage`, `DuplicatePage`, `RotatePage(PageIndex, Degrees)`, `ExtractPages([0, 1]): TMemoryStream`, `MergeDocument(FileOrStream)`, `InsertPages`, `ReplacePage`, `GetDocumentPageText(I)`, `GetDocumentPageInfo(I)`, `SaveDocument(FileName)`, `CloseDocument`. Page indexes are zero-based.

```delphi
p.OpenDocument(ASource);
for I := 0 to p.GetPageCount - 1 do
begin
  p.BeginPageEdit(I, pelUnderlay);       // watermark under existing content
  try
    p.Graphics.Font.SizeNoScale := 64;
    p.Graphics.Font.Color := MakeGraphicsColor(220, 220, 220);
    p.Graphics.Alignment := gtaCenter;
    p.Graphics.DrawText('CONFIDENTIAL', RectF(0, p.PageHeight / 2 - 40, p.PageWidth, p.PageHeight / 2 + 40));
    p.EndPageEdit;
  except
    p.CancelPageEdit;
    raise;
  end;
end;
p.SaveDocument(ATarget);
```

## TTMSFNCGraphicsPDFIO: export FNC controls to PDF

Exports any object implementing `ITMSFNCGraphicsExport` (every `TTMSFNCCustomControl` descendant does) by letting it paint on a PDF page.

```delphi
property ExportObject: TTMSFNCPDFIOExportObject;   // = TObject
property Options: TTMSFNCPDFIOOptions;   // OpenInPDFReader, Header, Footer, Margins, PageSize, PageOrientation,
                                         // PageWidth, PageHeight, HeaderFont, FooterFont, DefaultFont, PageNumber (default pnHeader),
                                         // PageNumberFormat ('%d'), EmbedFonts, FontFallBackList, ExportImages
property Information: TTMSFNCPDFIOInformation;    // Author, Title, Subject, Keywords, Creator
procedure Save(const AFileName: String); overload;                // exports ExportObject
procedure Save(const AStream: TStream); overload;
procedure Save(const AFileName: String; AExportObject: TTMSFNCPDFIOExportObject; AExportRect: TRectF); overload;
procedure Save(const AFileName: String; AExportObjects: TTMSFNCPDFIOExportObjectArray); overload;  // one page per object
procedure Save(const AFileName: String; AExportObjects: TTMSFNCPDFIOExportObjectArray; AExportRects: TTMSFNCPDFIOExportRectArray); overload;
// events: OnGetHeader/OnGetFooter(Sender; AExportObject: TObject; APageIndex: Integer; var AHeader: UnicodeString),
// OnBeforeDrawContent/OnAfterDrawContent, OnGetExportRect, OnCanCreateNewPage, OnAfterDraw(Sender; APDFLib: TTMSFNCPDFLib)
```
Without an explicit rect, the export rect is the page `MediaBox` minus `Options.Margins`.

```delphi
uses VCL.TMSFNCGraphicsPDFEngine, VCL.TMSFNCPDFIO, VCL.TMSFNCPDFLib;

procedure TForm1.ExportClick(Sender: TObject);
var
  io: TTMSFNCGraphicsPDFIO;
begin
  io := TTMSFNCGraphicsPDFIO.Create(Self);
  try
    io.Options.Header := 'Chart export';
    io.Options.PageOrientation := poLandscape;
    io.Options.OpenInPDFReader := True;
    io.Information.Title := 'Sales';
    io.ExportObject := TMSFNCChart1;
    io.Save('chart.pdf');
    // several controls, one page each:
    // io.Save('all.pdf', [TMSFNCChart1, TMSFNCPlanner1]);
  finally
    io.Free;
  end;
end;
```

## Printing

### TTMSFNCGraphicsPrintIO (print FNC controls)

Same shape as the PDF IO, but drawing goes to a `TTMSFNCGraphics` on the printer.
```delphi
procedure Print; overload;                          // prints ExportObject
procedure Print(AExportObject: TTMSFNCPrintIOExportObject; AExportRect: TRectF); overload;
procedure Print(AExportObjects: TTMSFNCPrintIOExportObjectArray); overload;
procedure Print(AExportObjects: TTMSFNCPrintIOExportObjectArray; AExportRects: TTMSFNCPrintIOExportRectArray); overload;
property Options: TTMSFNCPrintIOOptions;  // Header, Footer, HeaderFont, FooterFont (TTMSFNCGraphicsFont), Margins,
  // HeaderHorizontalAlignment/HeaderVerticalAlignment, PageNumber (TTMSFNCPrintPageNumber: pnNone default, pnHeader, pnFooter),
  // PageNumberFormat, PageOrientation: TPrinterOrientation, Device (not settable on Android/iOS/WEB), DefaultFont;
  // read-only DPI, PageWidth, PageHeight, PageIndex; PageSize: TPrintSize only on Android
```
Demo (UI Pack `VCL\PrintIO`):
```delphi
if PrintDialog1.Execute then
begin
  TMSFNCGraphicsPrintIO1.Options.Footer := 'My Footer Text';
  TMSFNCGraphicsPrintIO1.Options.PageNumber := pnHeader;
  TMSFNCGraphicsPrintIO1.Options.PageNumberFormat := 'Page %d';
  r := RectF(TMSFNCGraphicsPrintIO1.Options.Margins.Left, TMSFNCGraphicsPrintIO1.Options.Margins.Top,
    TMSFNCGraphicsPrintIO1.Options.Margins.Left + TMSFNCDataGrid1.Width,
    TMSFNCGraphicsPrintIO1.Options.Margins.Top + TMSFNCDataGrid1.Height);
  TMSFNCGraphicsPrintIO1.Print(TMSFNCDataGrid1, r);
end;
```

### TTMSFNCPrinter (free-form printing)

Use the global singleton function `TMSFNCPrinter` (unit `*.TMSFNCPrinters`).
```delphi
procedure BeginDoc;  procedure EndDoc;  procedure NewPage;
property Graphics: TTMSFNCGraphics;            // valid between BeginDoc and EndDoc
property PageWidth, PageHeight: Integer;       // settable only on WEB
property PageNumber: Integer;  property DPI: Integer;
property Orientation: TPrinterOrientation;
property Device: string;                       // read-only on Android/iOS/WEB
property OnDrawContent: TTMSFNCPrinterDrawContentCallBack; // reference to procedure (LCL: procedure of object)
```
`BeginDoc` creates `Graphics` and then **calls `OnDrawContent` itself** (on Android later, from the print adapter). Draw inside `OnDrawContent` and call `EndDoc` at its end. Demo `VCL\TMSFNCPrinter` (same code on WEB):
```delphi
uses VCL.TMSFNCPrinters, VCL.TMSFNCGraphics, VCL.TMSFNCGraphicsTypes;

procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCPrinter.OnDrawContent :=
    procedure
    begin
      TMSFNCPrinter.Graphics.Font.Color := gcBlue;
      TMSFNCPrinter.Graphics.Font.Size := 40;
      TMSFNCPrinter.Graphics.DrawText(0, 20, TMSFNCPrinter.PageWidth, 100, 'Hello', False, gtaCenter, gtaCenter);
      TMSFNCPrinter.Graphics.Fill.Color := gcRed;
      TMSFNCPrinter.Graphics.DrawEllipse(100, 200, TMSFNCPrinter.PageWidth - 100, 300);
      TMSFNCPrinter.EndDoc;
    end;
end;

procedure TForm1.PrintButtonClick(Sender: TObject);
begin
  if PrintDialog1.Execute then
    TMSFNCPrinter.BeginDoc;
end;
```

## Platform notes

- **Backends:** VCL, FMX Windows/Linux, LCL and WEB use the built-in "General" PDF writer; FMX macOS/iOS/Android use the native OS PDF engine (`USENATIVE`). `FormFields` does not exist on the native backends.
- **WEB output:** `BeginDocument('x.pdf')` + `EndDocument(True)` opens the PDF in the browser (`'application/pdf'`); with a file name and `EndDocument(False)` nothing is produced and the result is nil. Use `BeginDocument` without a name to get the stream. `TTMSFNCGraphicsPDFIO.Save(FileName)` likewise only opens the PDF in the browser when `Options.OpenInPDFReader` is True.
- **WEB fonts:** fonts must be loaded first: `AddFontToCache('https://.../Roboto-Regular.ttf')` (global procedure in `WEBLib.TMSFNCPDFLib`, also `AddFontToCache(AFontFile: TJSBlob)`), wait for `Application.OnFontCacheReady`, then use `Graphics.Font.Name := 'Roboto'` and `PDF.FontFallBackList.Insert(0, 'Roboto')` (UI Pack demo `WEB\Planner Database Adapter and PDFLib`).
- **WEB:** `OpenDocument`, `SaveDocument`, `MergeDocument`, `AddPages`, `InsertPages` exist only with `TStream` parameters (file-name overloads are `{$IFNDEF WEBLIB}`).
- Printing DPI constant: FMX 72, VCL/LCL 96, WEB 1. `TPrinterOrientation` comes from `Vcl.Printers` / `FMX.Printer`.
- `TTMSFNCGraphicsPrintIO`, `TTMSFNCPDFLib`, `TTMSFNCGraphicsPDFIO` are available on all frameworks including WEB.

## Does not exist / common mistakes

- `TTMSFNCPDFIO` / `TTMSFNCPrintIO` components: the concrete classes are `TTMSFNCGraphicsPDFIO` (unit `*.TMSFNCGraphicsPDFEngine`) and `TTMSFNCGraphicsPrintIO`. `TTMSFNCCustomPDFIO` / `TTMSFNCCustomPrintIO` are abstract bases.
- `PDF.SaveToFile`, `PDF.SaveToStream`, `PDF.Save` on `TTMSFNCPDFLib`: pass the file to `BeginDocument(FileName)`, or take the stream from `EndDocument`. `SaveDocument` is only for documents opened with `OpenDocument`.
- `PDF.AddPage` to start a new blank page: use `NewPage`. `AddPage(FileName, PageIndex)` exists but imports a page from another PDF.
- `Graphics.TextOut`, `DrawString`, `Canvas.TextOut`, `Graphics.DrawRoundRect`: use `DrawText`, `DrawHTMLText`, and `DrawRoundedRectangle` on `ITMSFNCCustomPDFGraphicsExLib`.
- `Graphics.Font.Size := 10` expecting 10 pt: on VCL/WEB it becomes 13. Use `SizeNoScale`.
- `Graphics.Brush` / `Graphics.Pen` / `Fill.Style`: use `Fill` / `Stroke` with `Kind` (`gfkSolid`, `gfkGradient`, `gfkNone`; `gskSolid`, `gskDash`, `gskNone`).
- `PDF.OwnerPassword`, `UserPassword`, `AllowsPrinting`, `AllowsCopying`, `PDFStandard`: declared **protected** on `TTMSFNCCustomPDFLib`, not reachable on `TTMSFNCPDFLib`.
- `PDF.Graphics` before `NewPage`: no page exists yet. Header/Footer set after `NewPage` only apply from the next page.
- `PDFIO.ExportToPDF(...)` / `PDFIO.Export`: use `Save(FileName)` or one of the `Save` overloads.
- `TTMSFNCPrinter.Create` + `Printer.Canvas` VCL style: use the `TMSFNCPrinter` function and draw on `TMSFNCPrinter.Graphics` inside `OnDrawContent`. Drawing after `BeginDoc` returns, without `OnDrawContent`, or forgetting `EndDoc`, leaves the print job open.
- `TMSFNCPrinter.Graphics.DrawText('x', RectF(...))` VCL `TCanvas` style: `TTMSFNCGraphics.DrawText` takes `(Left, Top, Right, Bottom, Text, WordWrap, HorzAlign, VertAlign)` or a `TRectF` first.
- `Options.PageSize` on `TTMSFNCGraphicsPrintIO`: Android only. On desktop pick the paper in the print dialog.
