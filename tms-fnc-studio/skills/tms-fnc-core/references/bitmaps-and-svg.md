# Bitmaps, containers and SVG (TTMSFNCBitmap, TTMSFNCBitmapContainer, TTMSFNCURLBitmapContainer, TTMSFNCSVGImageCollection)
> Sections (line ranges): 6-17 Units and palette · 18-65 TTMSFNCBitmap: what it really is · 66-89 SVG engine and options · 90-144 TTMSFNCBitmapContainer · 145-168 TTMSFNCURLBitmapContainer · 169-191 TTMSFNCSVGImageCollection · 192-198 Platform notes · 199-215 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0: `VCL/FMX/WEBLib.TMSFNCTypes`, `*.TMSFNCBitmapContainer`, `*.TMSFNCURLBitmapContainer`, `*.TMSFNCGraphicsSVGEngine`, `*.TMSFNCGraphics.Win/General`, `*.TMSFNCBitmapContainerReg`, `VCL.TMSFNCGeneralRegDE`. Demos: `tms.fnc.core.demos\VCL\SVG VirtualImageList`, UI Pack `Shared Code\Business Logic\SVG\UBL.pas` and `PDFLib BMI\UBL.pas`.

## Units and palette

| Class | Unit | Palette page |
|---|---|---|
| `TTMSFNCBitmap`, `TTMSFNCBitmapHelper`, `TTMSFNCScaledBitmaps`, `TTMSFNCSVGBitmap`, `TTMSFNCSVGImageCollection` | `*.TMSFNCTypes` | |
| `TTMSFNCBitmapContainer` | `*.TMSFNCBitmapContainer` | `TMS FNC UI` |
| `TTMSFNCURLBitmapContainer` | `*.TMSFNCURLBitmapContainer` | `TMS FNC UI` |
| `TTMSFNCSVGImageCollection` | `VCL.TMSFNCTypes` (registered in `VCL.TMSFNCGeneralRegDE`) | `TMS FNC UI`, VCL only, Delphi 10.3+ |
| `TTMSFNCGraphicsSVGImport` (SVG parser/renderer) | `*.TMSFNCGraphicsSVGEngine` (VCL, FMX, LCL; **no WEB unit**) | |

The SVG engine unit is pulled in by `*.TMSFNCTypes` itself; you never add it for normal SVG use.

## TTMSFNCBitmap: what it really is

| Framework | Declaration | Notes |
|---|---|---|
| FMX | `TTMSFNCBitmap = class(TBitmap)` | `TTMSFNCBitmapHelperClass = TBitmap`. Adds `HasSVG`, `SVG`, `LoadFromSVG`, `LoadFromBase64`, `SaveToBase64`, `CreateFromFile`, `CreateFromStream` |
| VCL, LCL | `TTMSFNCBitmap = class(TPicture)` | `TTMSFNCBitmapHelperClass = TPicture`. PNG/JPEG/GIF/SVG via `Graphic`; `HasSVG`, `SVG` |
| WEB | `TTMSFNCBitmap = class(TBitmap)` (WEB Core) | `TTMSFNCBitmapHelperClass = TGraphic`. Browser decodes images (SVG too) asynchronously |

`TTMSFNCBitmapHelper` (class helper for `TTMSFNCBitmapHelperClass`, **VCL/FMX/LCL only**, not WEB):

```delphi
procedure LoadFromSVG(ASVG: string);
procedure LoadFromBase64(ABase64: string);
procedure LoadFromURL(AURL: String); overload;                       // synchronous download
procedure LoadFromResource(AResourceName: String); overload;         // RT_RCDATA resource of the module
procedure LoadFromResource(AResourceName: String; AInstance: NativeUInt); overload;
function SaveToBase64: string;
class function CreateFromResource(AResourceName: string): TTMSFNCBitmap; overload;
class function CreateFromURL(AURL: string): TTMSFNCBitmap; overload;
class function CreateFromBase64(ABase64: string): TTMSFNCBitmap;
class function CreateFromSVG(ASVG: string): TTMSFNCBitmap;
// VCL/LCL only (FMX has the TBitmap constructors CreateFromFile/CreateFromStream):
class function CreateFromFile(AFileName: string): TTMSFNCBitmap; overload;
class function CreateFromStream(AStream: TStream): TTMSFNCBitmap; overload;
```

Loading, all frameworks except where noted:

```delphi
var
  bmp: TTMSFNCBitmap;
begin
  bmp := TTMSFNCBitmap.Create;
  try
    bmp.LoadFromFile('icon.svg');          // SVG, PNG, JPG, BMP, GIF (not WEB: use a URL)
    bmp.LoadFromResource('MYPNG');         // {$R} RCDATA resource, VCL/FMX/LCL
    bmp.LoadFromSVG('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><circle cx="5" cy="5" r="4" fill="red"/></svg>');
    if bmp.HasSVG then
      bmp.SVG.TintColor := gcSteelblue;    // recolor a monochrome icon
    TMSFNCImage1.Bitmaps.AddBitmap(bmp);   // UI Pack TTMSFNCImage: collection copies the bitmap
  finally
    bmp.Free;
  end;
end;
```

Every published `Bitmap: TTMSFNCBitmap` property of FNC controls is assigned with `Assign`: `Ctrl.Bitmap.Assign(bmp)` or `Ctrl.Bitmap.LoadFromFile(...)`. Do not replace the instance.

## SVG engine and options

`TTMSFNCBitmap.SVG: TTMSFNCSVGImport` (nil / no elements when the image is not SVG; check `HasSVG`). Published options on `TTMSFNCSVGImport`:

```delphi
property GrayScale: Boolean default False;
property CustomFillColor: TTMSFNCSVGImportColor;     // TAlphaColor on FMX, TColor on VCL/LCL
property CustomStrokeColor: TTMSFNCSVGImportColor;
property TintColor: TTMSFNCSVGImportColor;
property CustomOpacity: Single;
property RotationAngle: Single;
property ViewRect: TRectF;                           // public
function GenerateBitmap(AWidth: Single = -1; AHeight: Single = -1): TTMSFNCBitmap;  // rasterize (caller frees)
procedure LoadFromText(const AText: string);  procedure LoadFromFile(const AFile: string);
procedure LoadFromStream(const AStream: TStream);  procedure SaveToFile(const AFile: string);
function HasElements: Boolean;  function ElementCount: Integer;
```

- Drawing: `TTMSFNCGraphics.DrawBitmap(r, bmp, ...)` detects `HasSVG` and renders the vector (sharp at any size/DPI). FNC controls that show a `TTMSFNCBitmap` therefore scale SVG for free.
- Supported: paths, basic shapes, `<g>`/`<use>`/`<defs>`, linear/radial gradients, patterns, clip paths, CSS classes and `style=""`, transforms, text, embedded `<image>` (base64).
- Fill rules: `fill-rule` and `clip-rule` attributes are honored (inherited from parent elements; `inherit` resolves upward). The engine maps them to `TTMSFNCGraphicsPath.FillRule` (`gpfrNonZero` default per the SVG spec, `gpfrEvenOdd` for `evenodd`) and sets it explicitly so screen and PDF output match. Contexts: GDI+ `FillModeWinding`/`FillModeAlternate` on Windows, even-odd fills on macOS/iOS (`*.TMSFNCGraphics.Mac/iOS`), and the PDF engine (`*.TMSFNCGraphicsPDFEngine`). Paths you build yourself use the same property: `path.FillRule := gpfrEvenOdd`.
- VCL registers SVG as a `TPicture` format at startup (`TPicture.RegisterFileFormat('SVG', 'Scalable Vector Graphics', TTMSFNCSVGBitmap)`), so a plain VCL `TImage.Picture.LoadFromFile('x.svg')` works once `VCL.TMSFNCTypes` is used.
- `TTMSFNCGraphicsSVGEngine` (same unit) is the opposite direction: a `TTMSFNCGraphics` descendant that records drawing calls into SVG text. `constructor Create(AWidth: Single; AHeight: Single)`, draw with the normal API, then `Build: string` / `SVG: TStrings`.

## TTMSFNCBitmapContainer

Non-visual store of named bitmaps (`TTMSFNCCustomComponent`, `[ComponentPlatformsAttribute(TMSPlatformsWeb)]`).

```delphi
property Items: TTMSFNCBitmapCollection;      // TTMSFNCBitmapItem: Bitmap: TTMSFNCBitmap; Name: string; Tag: NativeInt
function FindBitmap(s: string): TTMSFNCBitmap; overload; virtual;   // case-insensitive Name lookup, nil if missing
procedure FindBitmap(i: Integer; ABitmap: TTMSFNCBitmap); overload; virtual;
function GetItem(AIndex: Integer): TTMSFNCBitmapItem; virtual;
function ItemCount: Integer;
procedure AddFromFile(FileName, BitmapName: String);
procedure AddFromResource(ResourceName, BitmapName: string); overload;
procedure AddFromResource(ResourceName, BitmapName: string; AInstance: NativeUInt); overload;
procedure AddFromURL(URL, BitmapName: string); virtual;      // WEB ONLY: empty method on VCL/FMX/LCL
procedure AddFromFolder(AFolder: string);                    // not on WEB; Name = file name incl. extension
property BitmapNames[AIndex: Integer]: String;  property Bitmaps[AIndex: Integer]: TTMSFNCBitmap;
function RandomBitmapName: string;  function RandomBitmap: TTMSFNCBitmap;
property OnBitmapChanged: TNotifyEvent;
property OnResolveBitmapName: TTMSFNCResolveBitmapNameEvent;
// procedure(Sender: TObject; const ABitmapName: string; var AResolvedBitmapName: string) of object
```

Controls register themselves with the container (`RegisterControl`) when you assign their `BitmapContainer`, and are invalidated when it changes.

### Referencing images by name

Pattern used across FNC: a control has `BitmapContainer: TTMSFNCBitmapContainer` plus a name property, or HTML `<img src="name">`:

```delphi
// UI Pack SVG demo (Shared Code\Business Logic\SVG\UBL.pas)
b := TTMSFNCBitmapContainer.Create(FForm);
b.AddFromFile(pth + '/' + IconNames[I] + '.svg', IconNames[I] + '.svg');

pnl1 := TTMSFNCPanel.Create(FForm);
pnl1.Parent := FForm;
pnl1.BitmapContainer := b;
pnl1.Header.Text := '<img src="' + IconNames[6] + '.svg"/> <font size="18">SVG</font>';  // HTML image by name

img2 := TTMSFNCImage.Create(pnl2);
img2.BitmapContainer := b;
img2.Bitmaps.AddBitmapName(IconNames[0] + '.svg');     // TTMSFNCScaledBitmaps entry by name
```

Other shapes of the same pattern: `TTMSFNCButton.BitmapName`, `TTMSFNCListBox` item `BitmapName`, `TTMSFNCScaledBitmap.BitmapName`, `TTMSFNCGraphics.DrawBitmapWithName(r, 'name')` (uses `g.BitmapContainer`). `OnResolveBitmapName` lets one name map to theme variants:

```delphi
procedure TForm1.BCResolve(Sender: TObject; const ABitmapName: string; var AResolvedBitmapName: string);
begin
  if FDarkMode then
    AResolvedBitmapName := ABitmapName + '_dark';
end;
```

`TTMSFNCScaledBitmaps` (used by `Bitmaps` properties): `Add(Scale: Single = 1.0)`, `AddBitmap(Bitmap: TTMSFNCBitmap; Scale = 1.0)`, `AddBitmapName(BitmapName: string; Scale = 1.0)`, `AddBitmapFromFile(FileName; Scale)` (not WEB), `AddBitmapFromResource(ResourceName; Scale)`, `GetBitmapByScale(Scale)`, `Bitmaps[Scale]`, `Items[Index]`, `Clear`. The drawing code picks the item matching the current DPI scale.

## TTMSFNCURLBitmapContainer

`class(TTMSFNCBitmapContainer)`; downloads in a background thread on VCL/FMX/LCL (WinINet on Windows, NSURL on Apple, curl on Linux) and via the browser on WEB.

```delphi
property Items: TTMSFNCURLBitmapCollection;   // TTMSFNCURLBitmapItem adds URL: string, Loaded: Boolean
property DefaultBitmap: TTMSFNCBitmap;        // returned by FindBitmap while the image is not downloaded yet
procedure AddFromURL(URL, BitmapName: String); override;
function FindBitmapByURL(AURL: string): TTMSFNCBitmap;
function Download(URL: string): TMemoryStream;
property OnDownloadComplete: TTMSFNCURLBitmapContainerDownloadCompleteEvent;  // (Sender: TObject; ItemIndex: integer)
property OnDownloadProgress: TTMSFNCURLBitmapContainerDownloadProgressEvent;  // (Sender: TObject; ItemIndex: integer; Position, TotalSize: Int64)
```

From the UI Pack `PDFLib BMI` demo:

```delphi
b := TTMSFNCURLBitmapContainer.Create(FForm);
b.AddFromURL('https://www.tmssoftware.com/site/img/TMS_LOGO_rgb_high.jpg', 'TMS_LOGO_rgb_high.jpg');
b.OnDownloadComplete := DoDownloadComplete;     // repaint / export once the image is there
```

`TTMSFNCURLBitmapContainer.FindBitmap` does not call `OnResolveBitmapName`.

## TTMSFNCSVGImageCollection (VCL, Delphi 10.3+)

A `TCustomImageCollection` for VCL `TVirtualImageList`, so standard VCL controls (toolbars, menus, tree views) get DPI-sharp SVG icons. Demo `VCL\SVG VirtualImageList`: drop `TTMSFNCSVGImageCollection` + `TVirtualImageList` (`ImageCollection` = the collection), set `Images := VirtualImageList1` on the controls.

```delphi
property Images: TTMSFNCSVGImageCollectionItems;   // items: Data: TPicture; Name: String; GrayScale; TintColor;
                                                   // CustomFillColor; CustomStrokeColor; CustomOpacity; RotationAngle
function GetIndexByName(const AName: String): Integer; override;
function GetNameByIndex(AIndex: Integer): String; override;
function GetItemByIndex(AIndex: Integer): TTMSFNCSVGImageCollectionItem; virtual;
function GetBitmap(AIndex: Integer; AWidth, AHeight: Integer): TBitmap; overload; override;

// runtime
with TMSFNCSVGImageCollection1.Images.Add do
begin
  Name := 'save';
  Data.LoadFromFile('save.svg');
  TintColor := clNavy;
end;
```

Uses: `Vcl.BaseImageCollection, System.ImageList, Vcl.ImgList, Vcl.VirtualImageList, VCL.TMSFNCTypes`.

## Platform notes

- VCL: `TTMSFNCBitmap` is a `TPicture`; use `bmp.Graphic`, `bmp.Width/Height`. There is no `bmp.Canvas`; draw into a `TTMSFNCGraphics.CreateBitmapCanvas` and `bmp.Assign(g.Bitmap)`.
- FMX: `TTMSFNCBitmap` is a real `TBitmap` (has `Canvas`, `SetSize`, `BitmapScale`).
- WEB: no `TTMSFNCBitmapHelper`, no SVG engine, no `AddFromFolder`, no `file://`. Use `AddFromURL` on either container (relative URLs are relative to the page) or `LoadFromURL` on the bitmap (WEB Core `TBitmap`). Images arrive asynchronously; repaint in `Application.OnImageCacheReady` (UI Pack SVG demo) or the URL container's `OnDownloadComplete`.
- LCL: same API as VCL (`LCLTMSFNC*` units).

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `TTMSFNCBitmapContainer.AddFromURL(...)` on VCL/FMX | it is an empty method there; use `TTMSFNCURLBitmapContainer` |
| `BitmapContainer.Bitmaps['name']` / `.GetBitmap('name')` / `.Items.Find` | `FindBitmap('name')` (`Bitmaps[]` is index-based) |
| `BitmapContainer.Add(bmp, 'name')` / `AddBitmap` | `with BC.Items.Add do begin Name := 'x'; Bitmap.Assign(bmp); end;` or `AddFromFile/AddFromResource` |
| `Control.Images := BitmapContainer` / `ImageIndex` on FNC controls | `Control.BitmapContainer := BC` + `BitmapName` / `Bitmaps.AddBitmapName` / `<img src="name">` |
| `TTMSFNCSVGBitmap` / `TTMSFNCSVGImage` component on FMX | load the `.svg` into any `TTMSFNCBitmap`; `TTMSFNCSVGBitmap` is the VCL/LCL `TGraphic` behind `TPicture` |
| `TTMSFNCSVGImageCollection` on FMX/WEB, or Delphi < 10.3 | VCL 10.3+ only |
| `uses VCL.TMSFNCSVGEngine` / `TMSFNCSVG` | not needed; the unit is `*.TMSFNCGraphicsSVGEngine` and is used automatically |
| `bmp.SVG.FillColor` / `bmp.SVG.Color` | `CustomFillColor`, `CustomStrokeColor`, `TintColor`, `GrayScale`, `CustomOpacity` |
| `bmp.SVG.FillRule` / `SVGOptions.FillMode` | fill rule comes from the SVG's `fill-rule`; for own paths set `TTMSFNCGraphicsPath.FillRule` |
| `TTMSFNCBitmap.Canvas` on VCL | not a `TBitmap` there; use `TTMSFNCGraphics.CreateBitmapCanvas` |
| `bmp.LoadFromResource('X', RT_RCDATA)` | resources are always looked up as RCDATA: `LoadFromResource('X')` |
| `TTMSFNCImageList` / `TTMSFNCImageCollection` | `TTMSFNCBitmapContainer` (all frameworks) or `TTMSFNCSVGImageCollection` (VCL) |
