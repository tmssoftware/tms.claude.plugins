# FNC graphics and custom painting (TTMSFNCGraphics, TTMSFNCGraphicsFill / Stroke / Font, TTMSFNCCustomControl.Draw)
> Sections (line ranges): 8-19 Units · 20-75 Creating a graphics object · 76-126 Fill, stroke, font · 127-183 Drawing methods · 184-198 Bitmaps · 199-217 Text and HTML · 218-302 Custom control: override Draw · 303-318 Color helpers · 319-324 Platform notes · 325-347 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0: `VCL.TMSFNCGraphics`, `VCL.TMSFNCGraphicsTypes`, `VCL.TMSFNCGraphicsTools`, `VCL.TMSFNCHTMLEngine`, `VCL.TMSFNCCustomControl`, `VCL.TMSFNCTypes` (FMX/WEB copies checked for differences). Demo: `tms.fnc.core.demos\VCL\DataBinding` (`THTMLPaintBox.Paint`), UI Pack `Shared Code\Business Logic\SVG\UBL.pas`.

`TTMSFNCGraphics` is a framework-neutral drawing layer over the VCL/LCL `TCanvas` (GDI+ for the native context), the FMX `TCanvas`, or the HTML canvas on WEB. All FNC controls paint through it, and you can use it on any canvas.

## Units

```delphi
uses
  System.Types,           // TRectF, TPointF (VCL)
  VCL.TMSFNCTypes,        // InflateRectEx, ConvertToRectF, TTMSFNCBitmap
  VCL.TMSFNCGraphicsTypes,// TTMSFNCGraphicsColor, gcXXX, Fill/Stroke/Font/Path, enums, Lighter/Darker/Blend
  VCL.TMSFNCGraphics,     // TTMSFNCGraphics
  VCL.TMSFNCCustomControl;// TTMSFNCCustomControl (custom controls)
// FMX: FMX.TMSFNC...   WEB: WEBLib.TMSFNC...   Lazarus: LCLTMSFNC...
```

## Creating a graphics object

```delphi
constructor Create(ACanvas: TCanvas; ANative: Boolean = False); virtual;
constructor CreateNative(ACanvas: TCanvas); virtual;
constructor CreateBitmapCanvas(AWidth: Integer = 1; AHeight: Integer = 1; ANative: Boolean = False; AHighDPI: Boolean = True); virtual;
constructor CreateNativeBitmapCanvas(AWidth: Integer = 1; AHeight: Integer = 1); virtual;
function BeginScene: Boolean; virtual;
procedure EndScene; virtual;
property Bitmap: TBitmap;        // the backing bitmap of CreateBitmapCanvas
property Canvas: TCanvas;  property Context: TTMSFNCGraphicsContext;
property Fill: TTMSFNCGraphicsFill;  property Stroke: TTMSFNCGraphicsStroke;  property Font: TTMSFNCGraphicsFont;  // read-only refs, change their members
```

On an existing canvas (paint handler of a non-FNC control). From the DataBinding demo:

```delphi
procedure THTMLPaintBox.Paint;          // THTMLPaintBox = class(TPaintBox)
var
  g: TTMSFNCGraphics;
begin
  inherited;
  g := TTMSFNCGraphics.Create(Canvas);
  try
    g.DrawText(ClientRect, HTML, True, gtaLeading, gtaLeading);   // HTML text, word wrapped
  finally
    g.Free;
  end;
end;
```

Off-screen bitmap (pattern used in `TTMSFNCGraphics.InternalDrawBitmapPartSync`): `BeginScene`/`EndScene` are required for bitmap canvases.

```delphi
var
  g: TTMSFNCGraphics;
  bmp: TTMSFNCBitmap;
begin
  g := TTMSFNCGraphics.CreateBitmapCanvas(200, 100);
  try
    g.BeginScene;
    g.Fill.Color := gcSteelblue;
    g.Stroke.Kind := gskNone;
    g.DrawRoundRectangle(RectF(0, 0, 200, 100), 12);
    g.Font.Color := gcWhite;
    g.Font.Size := 14;
    g.DrawText(RectF(0, 0, 200, 100), 'Hello <b>FNC</b>', False, gtaCenter, gtaCenter);
    g.EndScene;
    bmp := TTMSFNCBitmap.Create;
    bmp.Assign(g.Bitmap);                 // keep a copy; g.Bitmap is freed with g
  finally
    g.Free;
  end;
end;
```

## Fill, stroke, font

```delphi
// TTMSFNCGraphicsFill (TTMSFNCCustomGraphicsFill)
constructor Create(const AKind: TTMSFNCGraphicsFillKind = gfkSolid; const AColor: TTMSFNCGraphicsColor = gcWhite;
  const AColorTo: TTMSFNCGraphicsColor = gcGray; const AColorMirror: TTMSFNCGraphicsColor = gcNull;
  const AColorMirrorTo: TTMSFNCGraphicsColor = gcNull); virtual;
property Kind: TTMSFNCGraphicsFillKind;          // gfkNone, gfkSolid, gfkGradient, gfkTexture
property Color, ColorTo, ColorMirror, ColorMirrorTo: TTMSFNCGraphicsColor;
property Orientation: TTMSFNCGraphicsFillOrientation default gfoVertical;   // gfoHorizontal, gfoVertical, gfoCustom
property Opacity: Single;
property Texture: TTMSFNCBitmap;  property TextureMode: TTMSFNCGraphicsTextureMode default gtmStretch; // gtmOriginal, gtmFit, gtmStretch, gtmCenter, gtmTile
property GradientType: TTMSFNCGraphicsFillGradientType default gfgtLinear;  // gfgtLinear, gfgtRadial
property GradientMode: TTMSFNCGraphicsFillGradientMode default gfgmDefault; // gfgmDefault (Color..ColorTo), gfgmCollection (GradientItems)
property GradientAngle: Single;  property GradientCenterPoint: TPointF;  property GradientCenterColor: TTMSFNCGraphicsColor;
property GradientItems: TTMSFNCGraphicsFillGradientItems;   // items: Color, Position (0..1), Opacity
function AddGradientItem(AColor: TTMSFNCGraphicsColor; APosition: Single; AOpacity: Single = 1.0): TTMSFNCGraphicsFillGradientItem; virtual;
procedure ClearGradientItems; virtual;
procedure BeginUpdate; procedure EndUpdate;  property OnChanged: TNotifyEvent;

// TTMSFNCGraphicsStroke
constructor Create(const AKind: TTMSFNCGraphicsStrokeKind = gskSolid; const AColor: TTMSFNCGraphicsColor = gcSilver; const AWidth: Single = 1.0); virtual;
property Kind: TTMSFNCGraphicsStrokeKind;   // gskNone, gskSolid, gskDash, gskDot, gskDashDot, gskDashDotDot
property Color: TTMSFNCGraphicsColor;  property Width: Single;  property Opacity: Single;

// TTMSFNCGraphicsFont = class(TFont)  (Size is Integer on VCL, Single on FMX)
property Color: TTMSFNCGraphicsColor default gcBlack;   // + inherited Name, Size, Style
procedure Assign(Source: TPersistent); override;       // AssignSource(Source) just calls Assign
property OnChanged: TNotifyEvent;
```

On FMX, `Opacity` and the gradient properties are published; on VCL/WEB/LCL they are public only (not in the Object Inspector). Cross-framework font size: `TTMSFNCUtils.SetFontSize(AFont: TFont; ASize: Single; AScaleFactor: Single = 1)` or `g.SetFontSize(ASize: Integer)`.

Gradient example:

```delphi
g.Fill.Kind := gfkGradient;
g.Fill.Color := gcWhite;
g.Fill.ColorTo := gcLightgray;
g.Fill.Orientation := gfoVertical;
g.DrawRectangle(r);

g.Fill.GradientMode := gfgmCollection;   // multi-stop
g.Fill.ClearGradientItems;
g.Fill.AddGradientItem(gcRed, 0);
g.Fill.AddGradientItem(gcYellow, 0.5);
g.Fill.AddGradientItem(gcGreen, 1);
```

Setter shortcuts on `TTMSFNCGraphics`: `SetFill(AFill)`, `SetStroke(AStroke)`, `SetFillKind`, `SetFillColor`, `SetStrokeKind`, `SetStrokeColor`, `SetStrokeWidth(AWidth: Single)`, `SetFont(AFont: TTMSFNCGraphicsFont)`, `SetFontColor`, `SetFontName`, `SetFontSize(ASize: Integer)`, `SetFontStyles(AStyle: TFontStyles)`.

## Drawing methods (TRectF/Double overloads shown; TRect/Integer overloads exist too)

Every shape is filled with `Fill` and outlined with `Stroke`. Set `Stroke.Kind := gskNone` or `Fill.Kind := gfkNone` to skip one.

```delphi
procedure DrawRectangle(ARect: TRectF; AModifyRectMode: TTMSFNCGraphicsModifyRectMode = gcrmShrinkAll); overload;
procedure DrawRectangle(ARect: TRectF; ASides: TTMSFNCGraphicsSides; AModifyRectMode: ... = gcrmShrinkAll); overload; // [gsLeft, gsTop, gsRight, gsBottom]
procedure DrawRectangle(ALeft, ATop, ARight, ABottom: Double; AModifyRectMode: ... = gcrmShrinkAll); overload;
procedure DrawRoundRectangle(ARect: TRectF; ARounding: Single = 10;
  ACorners: TTMSFNCGraphicsCorners = [gcTopLeft, gcTopRight, gcBottomLeft, gcBottomRight]; AModifyRectMode: ... = gcrmShrinkAll); overload;
procedure DrawEllipse(ARect: TRectF; AModifyRectMode: ... = gcrmShrinkAll); overload;
procedure DrawLine(AFromPoint: TPointF; AToPoint: TPointF; AModifyPointModeFrom: TTMSFNCGraphicsModifyPointMode = gcpmRightDown;
  AModifyPointModeTo: TTMSFNCGraphicsModifyPointMode = gcpmRightDown); overload;
procedure DrawArc(const Center, Radius: TPointF; StartAngle, SweepAngle: Single); overload;
procedure DrawPolygon(APolygon: TTMSFNCGraphicsPathPolygon);    // array of TPointF
procedure DrawPolyline(APolyline: TTMSFNCGraphicsPathPolygon);
procedure DrawPath(APath: TTMSFNCGraphicsPath; APathMode: TTMSFNCGraphicsPathDrawMode = pdmPolygon); // pdmPolygon, pdmPolyline, pdmPath
procedure DrawFocusRectangle(ARect: TRectF; AColor: TTMSFNCGraphicsColor = gcBlack; AModifyRectMode: ... = gcrmShrinkAll); overload;
procedure ClipRect(ARect: TRectF); overload;
function SaveState(ACanvasOnly: Boolean = False): TTMSFNCGraphicsSaveState;
procedure RestoreState(AState: TTMSFNCGraphicsSaveState; ACanvasOnly: Boolean = False);   // FREES AState
procedure SetMatrix(const AMatrix: TTMSFNCGraphicsMatrix);  function GetMatrix: TTMSFNCGraphicsMatrix;
```

Built-in UI elements: `DrawCheckBox(ARect; AChecked; AFocused; AEnabled; AScaleFactor)`, `DrawRadioButton(...)`, `DrawButton(ARect; ADown; AFocused; AEnabled; AAdaptToStyle; AScaleFactor)`, `DrawCloseButton`, `DrawDropDownButton(ARect; ADown; AFocused; AEnabled; ACenter; AAdaptToStyle; AScaleFactor)`, `DrawExpanderButton(ARect; AState: TTMSFNCGraphicsExpanderState = gesExpanded; ...)`, `DrawCompactButton(ARect; AState = gcsExpanded; ...)`, `DrawProgressBar(ARect; AValue: Single; AFormat: string = '%.0f%%'; AMax: Single = 100; AColor = gcYellowgreen; ATextColor = gcBlack; AShowText = True; AEnabled = True; AScaleFactor = 1.0)`.

Clipping and paths:

```delphi
var
  st: TTMSFNCGraphicsSaveState;
  p: TTMSFNCGraphicsPath;
begin
  st := g.SaveState;
  try
    g.ClipRect(RectF(10, 10, 110, 60));
    g.DrawText(RectF(10, 10, 110, 60), 'long text that gets clipped');
  finally
    g.RestoreState(st);     // restores clip/fill/stroke/font and frees st
  end;

  p := TTMSFNCGraphicsPath.Create;
  try
    p.MoveTo(PointF(10, 10));
    p.LineTo(PointF(100, 10));
    p.CurveTo(PointF(120, 40), PointF(80, 80), PointF(10, 60));
    p.ClosePath;
    p.FillRule := gpfrEvenOdd;        // gpfrDefault, gpfrNonZero, gpfrEvenOdd
    g.DrawPath(p);
  finally
    p.Free;
  end;
end;
```

`TTMSFNCGraphicsPath` also has `AddRectangle(ARect; ARoundingX = 0; ARoundingY = 0; ACorners)`, `AddEllipse`, `AddArc(Center, Radius: TPointF; StartAngle, SweepAngle)`, `AddLine`, `AddPolygon`, `QuadCurveTo`, `SmoothCurveTo`, `AddPath`, `ApplyMatrix`, `GetBounds`, `Clear`, `Flatten`.

## Bitmaps

```delphi
procedure DrawBitmap(ARect: TRectF; ABitmap: TTMSFNCBitmapHelperClass; AAspectRatio: Boolean = True;
  AStretch: Boolean = False; ACenter: Boolean = True; ACropping: Boolean = False); overload;
procedure DrawBitmap(ALeft, ATop: Single; ABitmap: TTMSFNCBitmapHelperClass); overload;
procedure DrawBitmapPart(ASourceRect: TRectF; ADestinationRect: TRectF; ABitmap: TTMSFNCBitmapHelperClass; ...); overload;
procedure DrawBitmapWithName(ARect: TRectF; ABitmapName: string; AApplyScale: Boolean = False; AScale: Single = 0;
  AAspectRatio: Boolean = True; AStretch: Boolean = False; ACenter: Boolean = True; ACropping: Boolean = False); overload; // uses g.BitmapContainer
procedure DrawScaledBitmap(ARect: TRectF; ABitmaps: TTMSFNCScaledBitmaps; AScale: Single = 0; ...); overload;
function GetBitmapDrawRectangle(ARect: TRectF; ABitmap: TTMSFNCBitmapHelperClass; AAspectRatio: Boolean = True; ...): TRectF; overload;
```

`TTMSFNCBitmapHelperClass` is `TBitmap` on FMX, `TPicture` on VCL/LCL, `TGraphic` on WEB, so pass a `TTMSFNCBitmap`. SVG bitmaps are rendered as vectors (see bitmaps-and-svg.md). Example from the UI Pack SVG demo: `AGraphics.DrawBitmap(ARect, BitmapContainer.FindBitmap(n), True, True);`

## Text and HTML

```delphi
function DrawText(ARect: TRectF; AText: String; AWordWrapping: Boolean = False;
  AHorizontalAlign: TTMSFNCGraphicsTextAlign = gtaLeading; AVerticalAlign: TTMSFNCGraphicsTextAlign = gtaCenter;
  ATrimming: TTMSFNCGraphicsTextTrimming = gttNone; AAngle: Single = 0; AMinWidth: Single = -1; AMinHeight: Single = -1;
  ASupportHTML: Boolean = True; ATestAnchor: Boolean = False; AX: Single = -1; AY: Single = -1): String; overload;
function DrawText(APoint: TPointF; AText: String; AAngle: Single = 0; ASupportHTML: Boolean = True; ...): String; overload;
function CalculateText(AText: String; ARect: TRectF; AWordWrapping: Boolean = False; ASupportHTML: Boolean = True): TRectF; overload;
function CalculateTextSize(AText: string): TSizeF; overload;
function CalculateTextWidth(AText: string): Single; overload;     function CalculateTextHeight(AText: string): Single; overload;
// also CalculateTextSize/Width/Height(AText; ARect; AWordWrapping; ASupportHTML) and *Int variants returning TSize/Integer
```

- Alignment enum: `gtaCenter`, `gtaLeading`, `gtaTrailing`. Trimming: `gttNone`, `gttCharacter`, `gttWord`.
- HTML is on by default (`ASupportHTML = True`): the mini-HTML engine (`*.TMSFNCHTMLEngine`, function `HTMLDrawEx`) handles `<b> <i> <u> <s> <br> <p> <font color="..." bgcolor="..." size="..." face="..."> <a href="..."> <img src="..."> <ul>/<li> <sub> <sup> <shad> <hr>`. Use `ASupportHTML := False` to draw a literal `<`.
- Hit-testing an anchor: `s := g.DrawText(r, html, True, gtaLeading, gtaLeading, gttNone, 0, -1, -1, True, True, X, Y);` returns the `href` under (X, Y) (draws nothing when `ATestAnchor` is True).
- `<img src="name">` looks the name up in `g.BitmapContainer`; also `src="data:image/png;base64,..."`, `src="file://..."` (not WEB), `src="idx:N"` with `g.ImageList` (VCL/LCL only). Related properties: `URLColor` (default `gcBlue`), `URLUnderline`, `HighlightColor`, `HighlightTextColor`, `OptimizedHTMLDrawing`. Strip tags with `TTMSFNCUtils.HTMLStrip(AHTML)`.

## Custom control: override Draw

```delphi
type
  TMyGauge = class(TTMSFNCCustomControl)
  private
    FValue: Single;
    FFont: TTMSFNCGraphicsFont;
    procedure SetValue(const AValue: Single);
    procedure SetValueFont(const AValue: TTMSFNCGraphicsFont);
    procedure FontChanged(Sender: TObject);
  protected
    procedure Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF); override;
    procedure ApplyStyle; override;              // optional: AdaptToStyle support
  public
    constructor Create(AOwner: TComponent); override;
    destructor Destroy; override;
  published
    property Fill;                               // protected in the base: publish them
    property Stroke;
    property ValueFont: TTMSFNCGraphicsFont read FFont write SetValueFont;  // not "Font": VCL already publishes TControl.Font
    property Value: Single read FValue write SetValue;
  end;

constructor TMyGauge.Create(AOwner: TComponent);
begin
  inherited;
  FFont := TTMSFNCGraphicsFont.Create;
  FFont.OnChanged := FontChanged;
  Width := 200;
  Height := 40;
end;

destructor TMyGauge.Destroy;
begin
  FFont.Free;
  inherited;
end;

procedure TMyGauge.FontChanged(Sender: TObject);
begin
  Invalidate;
end;

procedure TMyGauge.SetValueFont(const AValue: TTMSFNCGraphicsFont);
begin
  FFont.Assign(AValue);
end;

procedure TMyGauge.SetValue(const AValue: Single);
begin
  if FValue <> AValue then
  begin
    FValue := AValue;
    Invalidate;
  end;
end;

procedure TMyGauge.Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF);
var
  r: TRectF;
begin
  inherited;                                     // background (Fill/Stroke) was already drawn by DrawBackground
  r := ARect;
  InflateRectEx(r, -4, -4);
  r.Right := r.Left + (r.Right - r.Left) * FValue / 100;
  AGraphics.Fill.Kind := gfkSolid;
  AGraphics.Fill.Color := Lighter(gcSteelblue, 20);
  AGraphics.Stroke.Kind := gskNone;
  AGraphics.DrawRoundRectangle(r, 4);
  AGraphics.Font.Assign(FFont);
  AGraphics.DrawText(ARect, Format('%.0f %%', [FValue]), False, gtaCenter, gtaCenter);
end;

procedure TMyGauge.ApplyStyle;
begin
  inherited;                                     // base sets Fill.Color / Stroke.Color from the active style
end;
```

Paint order in `TTMSFNCCustomControl.DrawControl`: `OnBeforeDraw(Sender, AGraphics, ARect, ADefaultDraw)` → if `ADefaultDraw`: `DrawBackground` → `Draw` → `OnAfterDraw`. Use `OnAfterDraw` to decorate an existing FNC control without subclassing. Call `Invalidate` to repaint; `BeginUpdate/EndUpdate` around bulk changes.

- `DrawBackground` fills the whole control with `Fill` and outlines it with the default grey `Stroke`. When `Draw` paints a rounded card, that rectangle shows in the corners. In the constructor set `Fill.Kind := gfkSolid; Fill.Color := <parent/page colour>; Stroke.Kind := gskNone;`. On VCL, `gfkNone` does **not** make the control see-through (it is an opaque window); only `TTMSFNCPanel`, `TTMSFNCToolBar` and `TTMSFNCFilterView` publish `Transparent`.
- Don't name a drawing helper `Text`, `Fill`, `Font`, `Color` or `Width`: inside a method of a control descendant the inherited member wins, and calls like `Text(G, R, 'x')` fail with E2066.

## Color helpers

In `*.TMSFNCGraphicsTypes` (plain functions):

```delphi
function MakeGraphicsColor(ARed, AGreen, ABlue: Byte {FMX only: ; AAlpha: Byte = 255}): TTMSFNCGraphicsColor;
function Lighter(AColor: TTMSFNCGraphicsColor; APercent: Byte): TTMSFNCGraphicsColor;
function Darker(AColor: TTMSFNCGraphicsColor; APercent: Byte): TTMSFNCGraphicsColor;
function Blend(AColor1: TTMSFNCGraphicsColor; AColor2: TTMSFNCGraphicsColor; ALevel: Byte): TTMSFNCGraphicsColor;
function MatrixCreateRotation(const AAngle: Single): TTMSFNCGraphicsMatrix;   // + MatrixCreateScaling, MatrixCreateTranslation, MatrixMultiply, MatrixIdentity
```

Class functions on `TTMSFNCGraphics`: `ColorToHTML(AColor): string`, `HTMLToColor(AHTML: string)`, `TextToColor(AText: string)`, `GetColorRed/Green/Blue(AColor): Byte`, `GetColorAlpha` (FMX only), `PointInRect`, `PointInPolygon`, `PointInPath`, `PointInCircle`, `GetBitmapFromBitmapContainer(ABitmapContainer; AName; AApplyScale = False; AScale = 0)`.

`*.TMSFNCGraphicsTools` has only bitmap/polygon helpers: `GetPixel(ABitmap: TTMSFNCBitmap; AX, AY: Single): TTMSFNCGraphicsColor`, `GetMagicWandPolygon`, `GetPolygonBoundsRect`, `InsertPointInPolygon`, `RemovePointInPolygon`.

## Platform notes

- VCL: `TTMSFNCGraphics.Create(Canvas)` uses the general context (`*.TMSFNCGraphics.General`); `ANative = True` / `CreateNative` uses the platform context (`TTMSFNCGraphicsContextWin` in `*.TMSFNCGraphics.Win` on Windows). Controls switch with the protected `NativeCanvas` property. The low-level context is reachable through `g.Context`.
- FMX: inside an FMX `OnPaint` the canvas is already in a scene, so do not call `BeginScene`; colors are `TAlphaColor` (alpha matters: `$FF0000` is transparent red, use `gcRed`).
- WEB: draws on an HTML canvas; `DrawBitmapPartSync` is `async` and images load asynchronously (repaint in `Application.OnImageCacheReady`, as in the UI Pack SVG demo). `ImageList` property and `file://` image sources are not available.

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `g.FillRect(r)` / `g.FillRectangle` / `g.FillEllipse` | `g.DrawRectangle(r)` / `g.DrawEllipse(r)` with `Stroke.Kind := gskNone` (`FillRect`/`FillEllipse` exist only on the low-level `g.Context`, with an explicit fill argument) |
| `g.DrawRoundRect(r, 5, 5)` | `g.DrawRoundRectangle(r, 5)` |
| `g.TextOut(x, y, s)` / `g.TextRect` | `g.DrawText(PointF(x, y), s)` / `g.DrawText(r, s, ...)` |
| `g.TextWidth(s)` / `g.MeasureText` | `g.CalculateTextWidth(s)`, `g.CalculateTextSize(s)`, `g.CalculateText(s, r, True)` |
| `g.DrawImage(...)` / `g.StretchDraw` | `g.DrawBitmap(r, bmp, AAspectRatio, AStretch)` |
| `g.DrawHTMLText(...)` / `HTMLDraw(...)` | `g.DrawText(...)` (HTML is on by default); low level: `HTMLDrawEx` |
| `g.DrawCircle(cx, cy, r)` | `g.DrawEllipse(RectF(cx - r, cy - r, cx + r, cy + r))` |
| `g.DrawBezier` / `g.DrawPie` / `g.DrawGradient` | build a `TTMSFNCGraphicsPath` (`CurveTo`, `AddArc`) and `DrawPath`; gradients via `Fill.Kind := gfkGradient` |
| `g.Rotate(angle)` / `g.Translate(x, y)` | `g.SetMatrix(MatrixCreateRotation(a))` / `MatrixCreateTranslation(dx, dy)`, or `DrawText(..., AAngle)` |
| `g.ResetClip` / `g.RestoreClip` | `st := g.SaveState; g.ClipRect(r); ... g.RestoreState(st);` |
| Freeing the state after `RestoreState` | `RestoreState` already frees it (double free) |
| `g.Fill := MyFill` | `g.Fill` is read-only: `g.Fill.Assign(MyFill)` or `g.SetFill(MyFill)` |
| `Fill.Kind := fkSolid` / `bkSolid` / `TBrushKind.Solid` | `gfkSolid` (`gfkNone`, `gfkGradient`, `gfkTexture`) |
| `Stroke.Kind := psSolid` / `skSolid`, `Stroke.Thickness` | `gskSolid`, `Stroke.Width` |
| `taCenter` / `TTextAlign.Center` in DrawText | `gtaCenter` (`gtaLeading`, `gtaTrailing`) |
| `procedure Paint; override;` in a `TTMSFNCCustomControl` descendant | `procedure Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF); override;` |
| `TTMSFNCGraphicsTools.Lighter(...)` / `TTMSFNCUtils.Lighter` | plain function `Lighter(...)` in `*.TMSFNCGraphicsTypes` |
| Forgetting `BeginScene` on `CreateBitmapCanvas` | `g.BeginScene; ... g.EndScene;` then copy `g.Bitmap` before `g.Free` |
