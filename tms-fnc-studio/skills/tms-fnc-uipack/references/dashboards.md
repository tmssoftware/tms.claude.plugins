# Dashboards: KPI cards, custom charts and a consistent look with FNC UI Pack + Core
> Sections (line ranges): 6-19 Pick the parts · 20-60 Palette and base part · 61-100 KPI card with sparkline · 101-139 Bar chart and donut · 140-181 Styling the stock controls · 182-219 Snapshot and PDF · 220-232 Does not exist / common mistakes

A recipe for runtime-built, styled dashboards. Code is VCL and was compiled and screenshot-checked against UI Pack 7.3 / Core 4.5 (Win32). For FMX swap `TColor` for `TAlphaColor` (`$FFRRGGBB`, alpha first) and `Vcl.*` units for `FMX.*`. API details stay in the control's own reference; this file covers how the pieces fit and the visual traps found when building four test dashboards.

## Pick the parts

| Dashboard piece | Use | Reference |
|---|---|---|
| KPI card, sparkline, bar/line/donut chart, gauge | `TTMSFNCCustomControl` descendant that overrides `Draw` (no chart control in UI Pack) | core `graphics.md` |
| Title + subtitle, rich captions | `TTMSFNCHTMLText` (mini-HTML) | `html-text-and-images.md` |
| Status chip | `TTMSFNCBadge` (flat fill, below) | `buttons-and-toggles.md` |
| Table with bars / colours | `TTMSFNCDataGrid` + `ConditionalFormatting.AddDataBar` | datagrid `styling.md`, `conditional-formatting.md` |
| Progress list | `TTMSFNCTableView` with `tviaProgress`, or `TTMSFNCProgressBar` per row | `lists.md`, `buttons-and-toggles.md` |
| Hierarchy with values | `TTMSFNCTreeView` with 2 columns | `treeview.md` |
| Board / schedule / timeline | `TTMSFNCKanbanBoard`, `TTMSFNCPlanner` (`pmMultiDay`), `TTMSFNCTimeline` | `kanban.md`, `planner.md`, `timeline.md` |
| Navigation | `TTMSFNCTabSet`, `TTMSFNCPageControl`, `TTMSFNCNavigationPanel`, or HTMLText links | `containers-and-navigation.md` |
| Whole-app theme | `TTMSFNCStylesManager` (order below) | core `styles.md` |

## Palette and base part

Define the palette once. VCL `TColor` literals are **BGR** (`$00BBGGRR`): `$00E0763B` is blue, not orange.

```delphi
const
  BG = $00F7F2EE;  Surface = clWhite;  Ink = $00402A1E;  Muted = $00857266;
  Accent = $00E0763B;  Good = $0060A82E;  Bad = $004747D9;  Line = $00EEE6E0;

type
  // DrawBackground paints Fill + a default grey Stroke over the whole control before Draw.
  // Around rounded cards that rectangle shows, so make it the page colour and drop the stroke.
  TDashPart = class(TTMSFNCCustomControl)
  public
    constructor Create(AOwner: TComponent); override;
  end;

constructor TDashPart.Create(AOwner: TComponent);
begin
  inherited;
  Fill.Kind := gfkSolid;
  Fill.Color := BG;            // VCL: gfkNone is NOT see-through, the control is an opaque window
  Stroke.Kind := gskNone;
end;

procedure StyleText(G: TTMSFNCGraphics; ASize: Integer; AColor: TColor; ABold: Boolean);
begin
  G.Font.Name := 'Segoe UI';  G.Font.Size := ASize;  G.Font.Color := AColor;
  if ABold then G.Font.Style := [TFontStyle.fsBold] else G.Font.Style := [];
end;

procedure DrawCard(G: TTMSFNCGraphics; R: TRectF);
begin
  G.Fill.Kind := gfkSolid;  G.Fill.Color := Surface;
  G.Stroke.Kind := gskSolid;  G.Stroke.Color := Line;
  G.DrawRoundRectangle(R, 12);
end;
```

Don't call a helper `Text`, `Fill`, `Font` or `Color`: inside a control method the inherited member wins (E2066).

## KPI card with sparkline

```delphi
type
  TKPICard = class(TDashPart)
  private
    FCaption, FValue, FDelta: string;  FUp: Boolean;  FSeries: TArray<Single>;
  protected
    procedure Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF); override;
  public
    procedure Setup(const ACaption, AValue, ADelta: string; AUp: Boolean; const ASeries: TArray<Single>);
  end;

procedure TKPICard.Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF);
var R, Spark: TRectF; I: Integer; MinV, MaxV: Single; Pts: TTMSFNCGraphicsPathPolygon;
begin
  R := ARect;
  DrawCard(AGraphics, R);
  R.Inflate(-18, -14);                                   // TRectF: use R.Inflate, not InflateRect
  StyleText(AGraphics, 9, Muted, False);
  AGraphics.DrawText(RectF(R.Left, R.Top, R.Right, R.Top + 20), FCaption);
  StyleText(AGraphics, 22, Ink, True);
  // last argument False = no HTML parsing, so '%', '<', '&' in values draw literally
  AGraphics.DrawText(RectF(R.Left, R.Top + 22, R.Right, R.Top + 62), FValue, False, gtaLeading, gtaCenter, gttNone, 0, -1, -1, False);
  if FUp then StyleText(AGraphics, 9, Good, True) else StyleText(AGraphics, 9, Bad, True);
  AGraphics.DrawText(RectF(R.Left, R.Bottom - 20, R.Right, R.Bottom), FDelta + ' vs. last year', False, gtaLeading, gtaCenter, gttNone, 0, -1, -1, False);
  if Length(FSeries) < 2 then Exit;
  MinV := MinValue(FSeries); MaxV := MaxValue(FSeries);   // System.Math
  if MaxV = MinV then MaxV := MinV + 1;
  Spark := RectF(R.Right - 90, R.Top + 26, R.Right, R.Top + 56);
  SetLength(Pts, Length(FSeries));
  for I := 0 to High(FSeries) do
    Pts[I] := PointF(Spark.Left + I * Spark.Width / High(FSeries),
      Spark.Bottom - (FSeries[I] - MinV) / (MaxV - MinV) * Spark.Height);
  AGraphics.Stroke.Color := Accent;
  AGraphics.Stroke.Width := 2;
  AGraphics.DrawPolyline(Pts);
end;
```

## Bar chart and donut

```delphi
// bars with gridlines and axis labels (inside a TDashPart.Draw, after DrawCard)
Plot := RectF(ARect.Left + 44, ARect.Top + 50, ARect.Right - 18, ARect.Bottom - 30);
StyleText(AGraphics, 8, Muted, False);
AGraphics.Stroke.Color := Line;
for I := 0 to 4 do
begin
  Y := Plot.Bottom - I * Plot.Height / 4;
  AGraphics.DrawLine(PointF(Plot.Left, Y), PointF(Plot.Right, Y));
  AGraphics.DrawText(RectF(ARect.Left + 8, Y - 8, Plot.Left - 6, Y + 8), IntToStr(I * 40), False, gtaTrailing);
end;
W := Plot.Width / Length(Values);
AGraphics.Stroke.Kind := gskNone;
for I := 0 to High(Values) do
begin
  Bar := RectF(Plot.Left + I * W + W * 0.18, Plot.Bottom - Values[I] / MaxScale * Plot.Height,
    Plot.Left + (I + 1) * W - W * 0.18, Plot.Bottom);
  AGraphics.Fill.Color := Accent;
  AGraphics.DrawRoundRectangle(Bar, 4, [gcTopLeft, gcTopRight]);     // round only the top corners
  AGraphics.DrawText(RectF(Bar.Left - 6, Plot.Bottom + 4, Bar.Right + 6, Plot.Bottom + 22), Labels[I], False, gtaCenter);
end;

// donut: thick stroked arcs, angles in degrees, -90 = 12 o'clock, positive sweep = clockwise
C := PointF(ARect.Left + ARect.Height / 2, ARect.Top + ARect.Height / 2);
Rad := ARect.Height / 2 - 30;
AGraphics.Fill.Kind := gfkNone;
AGraphics.Stroke.Width := 18;
Start := -90;
for I := 0 to High(Parts) do                       // Parts in percent
begin
  AGraphics.Stroke.Color := Colors[I];
  AGraphics.DrawArc(C, PointF(Rad, Rad), Start, Parts[I] * 3.6 - 2);   // -2 leaves a small gap
  Start := Start + Parts[I] * 3.6;
end;
AGraphics.Stroke.Width := 1;                       // reset: state carries over to later drawing
```

## Styling the stock controls

```delphi
// Header text: opaque on VCL, so paint it in the page colour.
Head := TTMSFNCHTMLText.Create(Self);  Head.Parent := Self;  Head.SetBounds(24, 16, 700, 56);
Head.Fill.Kind := gfkSolid;  Head.Fill.Color := BG;  Head.Stroke.Kind := gskNone;
Head.HorizontalTextAlign := gtaLeading;
Head.Text := '<font size="20" color="#1E2A40"><b>Sales Performance</b></font><br>' +
  '<font size="10" color="#667285">January - December 2025</font>';     // HTML colours are #RRGGBB

// Flat status chip: the badge default is a red gradient, set Kind before Color.
Badge := TTMSFNCBadge.Create(Self);  Badge.Parent := Self;
Badge.AutoSize := False;  Badge.HorizontalPosition := bhpCustom;  Badge.VerticalPosition := bvpCustom;
Badge.SetBounds(1056, 28, 120, 26);  Badge.Text := 'On track';
Badge.Appearance.Fill.Kind := gfkSolid;  Badge.Appearance.Fill.Color := $00E2F1DA;
Badge.Appearance.Stroke.Kind := gskNone;  Badge.Appearance.Font.Color := Good;

// Progress list: default accessory colour is yellow-green.
List.ItemAppearance.HeightMode := tvhmFixed;  List.ItemAppearance.FixedHeight := 40;
List.ItemAppearance.AccessoryFill.Color := Accent;  List.ItemAppearance.AccessoryFont.Color := clWhite;
It := List.Items.Add;  It.Accessory := tviaProgress;  It.AccessoryProgress := 93;   // 0..100
It.AccessoryColor := Bad;                                                            // per-item override

// Tree: Expanded := True while filling (Expand/ExpandAll only work after EndUpdate).
Region := Tree.AddNode;  Region.Text[0] := 'Europe';  Region.Text[1] := '$612K';  Region.Expanded := True;
// Column header keeps the style's grey: set it after the style load.
Tree.ColumnsAppearance.TopFill.Kind := gfkSolid;  Tree.ColumnsAppearance.TopFill.Color := BG;
Tree.ColumnsAppearance.TopFont.Color := Muted;

// Grid: fill inside BeginUpdate/EndUpdate, then layouts, then data bars
// (uses VCL.TMSFNCDataGridConditionalFormatting for bbkNumber).
Grid.CellAppearance.FixedLayout.Fill.Color := BG;
Grid.CellAppearance.FixedLayout.Font.Style := [TFontStyle.fsBold];
Grid.Options.Banding.Enabled := True;  Grid.CellAppearance.BandLayout.Fill.Color := $00FCF9F7;
with Grid.ConditionalFormatting.AddDataBar(2, Accent).DataBar do
begin
  MinKind := bbkNumber;  MaxKind := bbkNumber;  MinValue := 0;  MaxValue := 120;   // fixed scale
end;
```

With a built-in theme, set `StylesManager.Options.AdaptFormColor := False` (otherwise the form colour is replaced even for a restricted load), load with an explicit component array, and apply your own colours **after** the load. Details in core `styles.md`.

## Snapshot and PDF

Give the app a snapshot switch from the first build so the look can be checked without manual clicking. VCL: copy your own window's client DC (`PaintTo` / `GetFormImage` can miss FNC child controls):

```delphi
// FSnapTimer: TTimer, Interval 1500, enabled when FindCmdLineSwitch('snap'); uses Winapi.Windows, Vcl.Imaging.pngimage
procedure TDashForm.SnapTick(Sender: TObject);
var B: TBitmap; P: TPngImage; DC: HDC;
begin
  FSnapTimer.Enabled := False;
  B := TBitmap.Create;  P := TPngImage.Create;
  try
    B.SetSize(ClientWidth, ClientHeight);
    DC := GetDC(Handle);
    try
      BitBlt(B.Canvas.Handle, 0, 0, B.Width, B.Height, DC, 0, 0, SRCCOPY);
    finally
      ReleaseDC(Handle, DC);
    end;
    P.Assign(B);  P.SaveToFile(ChangeFileExt(Application.ExeName, '.png'));
  finally
    P.Free;  B.Free;
  end;
  Application.Terminate;
end;
```

The form must be visible and on screen. FMX: put the UI in a root `TLayout` and save `RootLayout.MakeScreenshot` (`TForm` has no `MakeScreenshot`). From Git Bash, a `/snap` argument becomes a path; pass `-snap`.

`TTMSFNCGraphicsPDFIO` exports one control through its own `DrawBackground` + `Draw`; **child controls are not exported**. Export each part (one page each) or make a surface that draws all content itself into the export `ARect`. Without rects every part is stretched to the page (a donut turns into an ellipse), so pass rects with the control's aspect ratio:

```delphi
io.Options.PageOrientation := poLandscape;
io.Save('report.pdf', [Card, Chart],
  [RectF(30, 80, 762, 80 + 732 * Card.Height / Card.Width),
   RectF(30, 80, 762, 80 + 732 * Chart.Height / Chart.Width)]);   // each rect must fit the page
```

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `Fill.Kind := gfkNone` for a see-through FNC control on VCL | solid fill in the parent colour (`Transparent` is published only on Panel, ToolBar, FilterView) |
| Rounded card with the default background | set the descendant's `Fill` to the page colour and `Stroke.Kind := gskNone` in the constructor |
| `Badge.Appearance.Fill.Color` alone for a flat chip | `Fill.Kind := gfkSolid` first |
| `Node.Expand(True)` inside `BeginUpdate` | `Node.Expanded := True` there, or `Expand` after `EndUpdate` |
| Styling controls, then loading a built-in style | load first (with `AdaptFormColor := False`), then customise |
| A chart component from UI Pack (`TTMSFNCChart`) | TMS FNC Chart is a separate product; in UI Pack/Core draw charts with `TTMSFNCGraphics` |
| `InflateRect(R, ...)` on a `TRectF` | `R.Inflate(dx, dy)` |
| `RGB(...)`-style reading of VCL hex literals | `$00BBGGRR` (blue first) |
