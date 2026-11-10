# HTML text and images (TTMSFNCHTMLText, FNC mini-HTML, TTMSFNCImage, TTMSFNCHotSpotImage)
> Sections (line ranges): 6-19 Units, palette, platforms · 20-46 FNC mini-HTML · 47-101 TTMSFNCHTMLText · 102-115 TTMSFNCImage · 116-160 TTMSFNCHotSpotImage · 161-190 TTMSFNCPDFImageBook · 191-196 Platform notes · 197-210 Does not exist / common mistakes

Verified against TMS FNC UI Pack 7.3.1.2 source (`*.TMSFNCHTMLText`, `*.TMSFNCImage`, `*.TMSFNCHotSpotImage`, `*.TMSFNCHotSpotImageEditor`, `*.TMSFNCHTMLImageContainer`, `*.TMSFNCPDFImageBook`, `*.TMSFNCTextView`) and the HTML engine in FNC Core 4.5.0.0 (`*.TMSFNCHTMLEngine`, used by `TTMSFNCGraphics.DrawText`).

## Units, palette, platforms

| Class | Unit | Palette (`TMS FNC UI`) | Platforms |
|---|---|---|---|
| `TTMSFNCHTMLText` | `VCL.TMSFNCHTMLText` | yes | VCL, FMX, WEB, LCL |
| `TTMSFNCImage` | `VCL.TMSFNCImage` | yes | VCL, FMX, WEB, LCL |
| `TTMSFNCHotSpotImage` | `VCL.TMSFNCHotSpotImage` | yes | VCL, FMX, WEB, LCL |
| `TTMSFNCHotSpotImageEditor` (dialog) | `VCL.TMSFNCHotSpotImageEditor` | yes | VCL, FMX, WEB, LCL |
| `TTMSFNCHTMLImageContainer` | `VCL.TMSFNCHTMLImageContainer` | no — base class of `TTMSFNCCheckBox`/`TTMSFNCRadioButton`, all members protected | — |
| `TTMSFNCPDFImageBook` | `VCL.TMSFNCPDFImageBook` | no — plain `class` (not a component) | VCL, FMX, LCL (no WEB unit) |
| `TTMSFNCTextView` | `VCL.TMSFNCTextView` | no — not registered and not in any package | — |

Prefix `VCL.` / `FMX.` / `WEBLib.`; Lazarus `LCLTMSFNCHTMLText` etc. Typical extra units: `VCL.TMSFNCTypes`, `VCL.TMSFNCGraphics`, `VCL.TMSFNCGraphicsTypes`, `VCL.TMSFNCBitmapContainer`.

## FNC mini-HTML (what TTMSFNCHTMLText and any FNC DrawText render)

Parsed by the FNC Core HTML engine. Tag names are case-insensitive. **Attribute values must be in double quotes** (the parser looks for `"`). Line breaks in the string are not breaks — use `<br>`.

| Tag | Attributes / notes |
|---|---|
| `<b>` `<i>` `<u>` `<s>` | bold, italic, underline, strikeout |
| `<br>` | line break |
| `<p>` | `align="left|center|right"`, `indent="n"`, `bgcolor="..."`, `bgcolorto="..."` (gradient) |
| `<font>` | `face="Arial"`, `color="#FF0000"` or `color="red"`, `bgcolor="..."`, `size="n"` (1..5 map to 8/10/12/14/16 pt, other values = pt), `style="font-size:14pt"` |
| `<a href="value">` | anchor; drawn with `URLColor`/`URLUnderline`; click delivers the `href` value |
| `<img>` | `src="name"` (name in `BitmapContainer`), `src="file://c:\x.png"` (not WEB), `src="url://https://..."` (WEB only), `src="data:image/png;base64,..."`, `src="idx:n"` (VCL/LCL ImageList only); `width`, `height`, `align="middle|top"`, `alt` |
| `<ul>` + `<li>` | bullets; `<li type="square|circle" color="...">` (no `<ol>`) |
| `<hr>` | `color="..."` |
| `<sub>` `<sup>` | subscript / superscript |
| `<hi>` | highlight; `<e>` marks text as error |
| `<shad>` | shadow (uses `ShadowColor`/`ShadowOffset` on TTMSFNCHTMLText) |
| `<ind x="n">` | indent to x pixels; `<ofs x="n">` horizontal offset |
| `<z>` | hidden text |
| `<blink>` | blink color |
| `<body>` | `bgcolor`, `bgcolorto`, `dir`, `background="..."` |
| entities | `&lt;` `&gt;` `&amp;` `&nbsp;` `&#nnn;` `&#xhh;` |

Not supported: CSS classes/stylesheets, `<div>`, `<span>`, `<table>`, `<h1>`..`<h6>`, `<ol>`, `<strong>`/`<em>` (use `<b>`/`<i>`). Strip tags: `TTMSFNCUtils.HTMLStrip(AHTML: string): string`; detect: `TTMSFNCUtils.IsHTML(AValue: string): Boolean`.

The same markup works in captions/texts of most FNC controls and in custom drawing: `TTMSFNCGraphics.DrawText(ARect: TRectF; AText: String; AWordWrapping: Boolean = False; AHorizontalAlign: TTMSFNCGraphicsTextAlign = gtaLeading; AVerticalAlign: TTMSFNCGraphicsTextAlign = gtaCenter; ATrimming: TTMSFNCGraphicsTextTrimming = gttNone; AAngle: Single = 0; AMinWidth: Single = -1; AMinHeight: Single = -1; ASupportHTML: Boolean = True; ATestAnchor: Boolean = False; AX: Single = -1; AY: Single = -1): String` — with `ATestAnchor = True` it returns the anchor at (AX, AY). `TTMSFNCGraphics.BitmapContainer` resolves `<img src="name">`.

## TTMSFNCHTMLText

`TTMSFNCHTMLText = class(TTMSFNCCustomControl, ITMSFNCBitmapContainer)`. Published (beyond Align/Anchors/Fill/Stroke/...):
```delphi
property Text: String;
property Font: TTMSFNCGraphicsFont;
property BitmapContainer: TTMSFNCBitmapContainer;
property WordWrapping: Boolean default False;
property HorizontalTextAlign: TTMSFNCGraphicsTextAlign default gtaCenter;   // gtaLeading, gtaCenter, gtaTrailing
property VerticalTextAlign: TTMSFNCGraphicsTextAlign default gtaCenter;
property Trimming: TTMSFNCGraphicsTextTrimming default gttNone;
property AutoSize: Boolean default False;  property AutoWidth: Boolean default True;  property AutoHeight: Boolean default True;
property AutoSizeSpacing: Single;
property TextIndentMargins: TTMSFNCMargins;
property DisplayHTML: Boolean default True;          // False shows the raw markup
property AutoOpenURL: Boolean default True;
property URLColor: TTMSFNCGraphicsColor default gcBlue;
property URLUnderline: Boolean default True;
property ShadowColor: TTMSFNCGraphicsColor default gcGray;  property ShadowOffset: integer default 1;
property OnAnchorClick: TTMSFNCHTMLTextAnchorClickEvent;
// TTMSFNCHTMLTextAnchorClickEvent = procedure(Sender: TObject; AAnchor: string) of object;
```
Public: `function IsHTML: boolean;`. Anchor behavior: if `OnAnchorClick` is assigned it is called **instead of** opening the URL; otherwise, with `AutoOpenURL`, `TTMSFNCUtils.OpenURL(Anchor)` runs.

```delphi
procedure TForm1.FormCreate(Sender: TObject);
var
  ht: TTMSFNCHTMLText;
begin
  ht := TTMSFNCHTMLText.Create(Self);
  ht.Parent := Self;
  ht.Align := alTop;
  ht.Height := 80;
  ht.WordWrapping := True;
  ht.HorizontalTextAlign := gtaLeading;
  ht.Fill.Kind := gfkSolid;            // VCL: gfkNone is NOT transparent (opaque window, shows white);
  ht.Fill.Color := Self.Color;         // use the parent's colour. FMX/WEB: gfkNone works.
  ht.Stroke.Kind := gskNone;
  ht.BitmapContainer := TMSFNCBitmapContainer1;
  ht.Text := '<b>Status:</b> <font color="#008000">online</font><br>' +
             '<img src="logo" width="16" height="16"> Visit <a href="https://www.tmssoftware.com">our site</a> ' +
             'or <a href="settings">open settings</a>';
  ht.OnAnchorClick := HTMLTextAnchorClick;
end;

procedure TForm1.HTMLTextAnchorClick(Sender: TObject; AAnchor: string);
begin
  if AAnchor = 'settings' then
    ShowSettings
  else
    TTMSFNCUtils.OpenURL(AAnchor);   // handler replaces AutoOpenURL, so open it yourself
end;
```
Use `TTMSFNCHTMLEditor` (`VCL.TMSFNCHTMLEditor`, see rich-editor.md) to let users edit this markup in a dialog.

## TTMSFNCImage

`TTMSFNCImage = class(TTMSFNCCustomImage)`; published `Bitmap: TTMSFNCBitmap`, `Bitmaps: TTMSFNCScaledBitmaps`, `BitmapContainer`, `AspectRatio` (default True), `Stretch` (False), `Cropping` (False), `Center` (True), `AutoSize` (False), `BitmapMargins: TTMSFNCMargins`, `Fill`, `Stroke`. Public: `procedure Clear;`, `function GetPaintRectangle: TRectF;`, `function GetBitmap: TTMSFNCBitmap;`, `OnBitmapChanged: TNotifyEvent` (public, not published).
```delphi
img := TTMSFNCImage.Create(Self);
img.Parent := Self;
img.Align := alClient;
img.Stretch := True;           // scale to the control
img.AspectRatio := True;       // keep proportions while stretching
img.Bitmap.LoadFromFile('photo.jpg');               // VCL/FMX/LCL
// WEB: img.Bitmap.LoadFromURL('images/photo.jpg');
// SVG/base64/resource: Bitmap.LoadFromSVG / LoadFromBase64 / LoadFromResource
```

## TTMSFNCHotSpotImage

Descends from `TTMSFNCCustomImage` (so has all image properties) and adds clickable polygon hotspots. Demo: `VCL\HotSpotImage` (Europe capitals quiz). Hotspots are usually drawn at design time with the hotspot editor (`TTMSFNCHotSpotImageEditor.Execute`, property `HotSpotImage`).

Published: `HotSpots: TTMSFNCHotSpotCollection`, `DefaultHotSpotAppearance: TTMSFNCHotSpotAppearance`, `HotSpotNameLocation: TTMSFNCHotSpotNameLocation` (`nlNone` default, `nlPolygonCenter, nlCenter, nlTopLeft, nlCenterLeft, nlBottomLeft, nlTopCenter`), `HoverBitmap`, `SelectedBitmap`, `MultiSelect` (False), `SelectedHotSpot: Integer`, `GlobalFont`.

`TTMSFNCHotSpot` (collection item), published: `Name`, `DataString`, `Selectable` (True), `Selected`, `Hovered` (read-only), `Appearance` (`HoverFill/HoverStroke/HoverFont`, `DownFill/...`, `SelectedFill/SelectedStroke/SelectedFont`), `ShowOnHover`, `ShowOnDown`, `ShowOnSelect` (True), `ShowHoverName`, `ShowDownName`, `ShowSelectedName` (False). Public: `HotSpotPolygon: TTMSFNCGraphicsPathPolygon` (`array of TPointF`), `SetRectangle(ARect: TRectF)`, `SetEllipse(ABounds: TRectF)`, `SetPath(APath: TTMSFNCGraphicsPath)`.

Image-level public methods:
```delphi
function AddRectangleHotSpot(ARect: TRectF; AName: string = ''; AAppearance: TTMSFNCHotSpotAppearance = nil): TTMSFNCHotSpot; virtual;
function AddEllipseHotSpot(ABounds: TRectF; AName: string = ''; AAppearance: TTMSFNCHotSpotAppearance = nil): TTMSFNCHotSpot; virtual;
function AddPolygonHotSpot(APolygon: TTMSFNCGraphicsPathPolygon; AName: string = ''; AAppearance: TTMSFNCHotSpotAppearance = nil): TTMSFNCHotSpot; virtual;
function AddPathHotSpot(APath: TTMSFNCGraphicsPath; AName: string = ''; AAppearance: TTMSFNCHotSpotAppearance = nil): TTMSFNCHotSpot; virtual;
function GetHotSpotIndexByName(AName: string): Integer;
function GetHotSpotByName(AName: string): TTMSFNCHotSpot;
```
Events (index-based, no "click" event — clicking selects):
```delphi
OnSelectedHotSpotChange / OnHoveredHotSpotChange:  procedure(Sender: TObject; AIndex: Integer; var Allow: Boolean) of object;
OnSelectedHotSpotChanged / OnHoveredHotSpotChanged: procedure(Sender: TObject; AIndex: Integer) of object;
OnHotSpotAppearanceChanged, OnHotSpotShapeChanged;  OnBefore/AfterDrawHoveredHotSpot, ...SelectedHotSpot, ...DownHotSpot, ...HotSpotName
```
```delphi
procedure TForm1.FormCreate(Sender: TObject);
var
  hs: TTMSFNCHotSpot;
begin
  TMSFNCHotSpotImage1.Bitmap.LoadFromFile('floorplan.png');
  TMSFNCHotSpotImage1.HotSpotNameLocation := nlPolygonCenter;
  hs := TMSFNCHotSpotImage1.AddRectangleHotSpot(RectF(10, 10, 120, 90), 'Kitchen');
  hs.DataString := 'room=1';
  hs.ShowHoverName := True;
  hs.Appearance.HoverFill.Color := gcLavender;
  TMSFNCHotSpotImage1.AddEllipseHotSpot(RectF(150, 20, 230, 100), 'Garden');
end;

procedure TForm1.TMSFNCHotSpotImage1SelectedHotSpotChanged(Sender: TObject; AIndex: Integer);
begin
  if AIndex >= 0 then
    Caption := TMSFNCHotSpotImage1.HotSpots[AIndex].Name + ' ' + TMSFNCHotSpotImage1.HotSpots[AIndex].DataString;
end;
```
Hotspot coordinates are in image (bitmap) space; the polygons are rescaled with the drawn image when it stretches/centers. Reset selection with `SelectedHotSpot := -1` and `HotSpots[i].Selected := False` (demo).

## TTMSFNCPDFImageBook (helper class)

Not a component — create/free it yourself. Builds a PDF with one image file per page.
```delphi
TTMSFNCPDFImageBookPageNumberPosition = (pnNone, pnTopLeft, pnTopCenter, pnTopRight, pnBottomLeft, pnBottomCenter, pnBottomRight);
constructor Create;
procedure GenerateBook(FileName: string; Images: TStrings);      // Images = file names; raises if empty
property Title: UnicodeString;
property PageNumberFormat: UnicodeString;                        // default 'Page %d of %d'
property PageNumberPosition: TTMSFNCPDFImageBookPageNumberPosition default pnBottomCenter;
property OnGetPageInfo: procedure(Sender: TObject; PageIndex: integer; var Header, Footer: UnicodeString) of object;
property OnBeforePageDraw / OnAfterPageDraw: procedure(Sender: TObject; PageIndex: integer; Graphics: ITMSFNCCustomPDFGraphicsLib) of object;
```
```delphi
var book: TTMSFNCPDFImageBook; files: TStringList;
begin
  book := TTMSFNCPDFImageBook.Create;
  files := TStringList.Create;
  try
    files.Add('page1.jpg');
    files.Add('page2.jpg');
    book.Title := 'Photo album';
    book.GenerateBook('album.pdf', files);
  finally
    files.Free;
    book.Free;
  end;
end;
```

## Platform notes

- WEB: `<img src="file://...">` is ignored, use `url://` or `data:` or a `BitmapContainer` name; load images with `Bitmap.LoadFromURL` (the browser has no local file system). `TTMSFNCPDFImageBook` has no WEB unit.
- `idx:n` image sources need a VCL/LCL ImageList and do nothing on FMX/WEB.
- `TTMSFNCHTMLText` property defaults are not stored as `default` on WEB (`{$IFNDEF WEBLIB}`), behavior is the same.

## Does not exist / common mistakes

- `&amp;` / `&#38;` / a bare `&` for an ampersand: FNC text treats `&` as a hotkey prefix (VCL and FMX; HTMLText, TableView, TreeView item text). A bare `&` disappears and underlines the next character, `&amp;` renders as `amp;`. Write `&&` (verified: `'R&&D'` shows `R&D`).
- `TTMSFNCHTMLText.Caption`, `.HTML`, `.HTMLText`, `OnLinkClick`, `OnAnchorHint` — use `Text` and `OnAnchorClick`.
- `TTMSFNCLabel`, `TTMSFNCHTMLLabel`, `THTMLabel`/`TAdvHTMLLabel` equivalents — use `TTMSFNCHTMLText`.
- Unquoted attributes (`<font color=red>`, `<a href=x>`) — values must be double-quoted.
- `<div>`, `<span style=...>`, `<table>`, `<h1>`, `<ol>`, `<strong>`, CSS — not supported by the FNC engine.
- `#13#10` inside `Text` for new lines — use `<br>` (or `<p>`).
- Expecting both `OnAnchorClick` and auto-open — assigning the event disables `AutoOpenURL` behavior.
- `TTMSFNCImage.Picture`, `Proportional`, `Transparent`, `Picture.LoadFromFile` (TImage API) — use `Bitmap`, `AspectRatio`, `Fill.Kind := gfkNone`, `Bitmap.LoadFromFile`.
- `OnHotSpotClick`, `OnClickHotSpot`, `HotSpots[i].Hint`, `HotSpots[i].Shape`, `TImageMap` — use `OnSelectedHotSpotChanged(Sender; AIndex)`, `DataString`/`Name`, and `SetRectangle`/`SetEllipse`/`HotSpotPolygon`.
- Dropping `TTMSFNCHTMLImageContainer` or `TTMSFNCTextView` on a form — neither is a palette component (`TTMSFNCTextView` is not even in a package).
- `TTMSFNCPDFImageBook.Create(Self)` / dropping it — it is a plain class with a parameterless `Create`; free it yourself.
