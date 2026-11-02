# Timeline (TTMSFNCTimeline, TTMSFNCTimelineDatabaseAdapter)

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCTimeline`, `*.TMSFNCTimelineDatabaseAdapter`, `*.TMSFNCTimelineReg`, `*.TMSFNCTimelineDatabaseAdapterReg` and the demos `Timeline\Positions`, `Timeline\Custom Drawing`, `Timeline\Timeline Database Adapter` (VCL/FMX/WEB).

`TTMSFNCTimeline` is a scrollable/zoomable **axis** with point markers (**indicators**, each with an optional text **annotation**) and range bars (**sections**). It is not a Gantt chart or a scheduler; for appointments per resource use `TTMSFNCPlanner` (see planner.md).

## Units, palette, platforms

Palette page **`TMS FNC UI`**. Prefix `VCL.` / `FMX.` / `WEBLib.`; Lazarus `LCLTMSFNC...` (no dot).

| Class | Unit |
|---|---|
| `TTMSFNCTimeline` (and `TTMSFNCTimelineIndicator`, `TTMSFNCTimelineSection`, all enums/records) | `VCL.TMSFNCTimeline` |
| `TTMSFNCTimelineDatabaseAdapter` | `VCL.TMSFNCTimelineDatabaseAdapter` (+ `Data.DB`) |

Also typically needed: `VCL.TMSFNCGraphics`, `VCL.TMSFNCGraphicsTypes` (`gtaCenter`, `gcRed`, `gfkSolid`), `VCL.TMSFNCTypes`. `TTMSFNCTimeline` descends from `TTMSFNCCustomScrollControl` (FNC Core). Available on VCL, FMX, WEB and LCL (both units are in the WEB package).

## Values vs dates

Every position on the axis is a `Double`. `Range.RangeType` decides how it is labelled and spaced:

```delphi
TTMSFNCTimelineRangeType = (tlrDay, tlrMonth, tlrYear, tlrMilliSecond, tlrSecond, tlrMinute, tlrHour, tlrValue);
```
- Date range types (`tlrDay` default ... `tlrHour`): the axis runs from `Range.MinimumDate` to `Range.MaximumDate` (defaults `Int(Now - 10)` .. `Int(Now + 10)`); a value is a `TDateTime`.
- `tlrValue`: the axis runs from `Range.MinimumValue` to `Range.MaximumValue` (**Integer**, defaults 0..10); values are plain numbers (years, steps, ...).

`Indicator.TimelineDate` is just `TDateTime(TimelineValue)` (same storage). Sections: `StartTimelineValue/EndTimelineValue` or `StartTimelineDate/EndTimelineDate`.

```delphi
// TTMSFNCTimelineRange (Timeline.Range)
property RangeType: TTMSFNCTimelineRangeType default tlrDay;
property MinimumDate: TDateTime;  property MaximumDate: TDateTime;
property MinimumValue: Integer default 0;  property MaximumValue: Integer default 10;
property DivisionSpace: Integer default 40;   // pixels between division tick marks
property DivisionSpan: Single;                // range units per division (default 1; demo uses 50 = 50 years)

// TTMSFNCTimelineDivision (Timeline.Division)
property Position: TTMSFNCTimelinePosition default tlpMiddle;   // tlpMiddle, tlpTopLeft, tlpBottomRight
property DrawText, DrawTickMark: Boolean default True;  property TickMarkSize: Integer default 8;
property TextFormat: TTMSFNCTimelineDivisionFormat;   // ValueFormat '%.0n' (Format), YearFormat 'YYYY', MonthFormat 'MMM', DayFormat 'dd/MM', HourFormat 'hh:mm', MinuteFormat, SecondFormat, MilliSecondFormat
property TextOrientation: TTMSFNCTimelineTextOrientation default tltoHorizontal;  // tltoLeft, tltoRight, tltoUpsideDown
property TextWordWrap: Boolean default False;  property Size: Integer default -1;

// TTMSFNCTimelineLayout (Timeline.Layout)
property Orientation: TTMSFNCTimelineOrientation default tloHorizontal;   // tloVertical
property Position: TTMSFNCTimelinePosition default tlpMiddle;
property Size: Integer default 32;           // thickness of the axis bar
property Margins: TTMSFNCMargins;  property ShowScrollBar: Boolean default True;  property FullSize: Boolean default False;
property ZoomFactor: Single;  property MultiSelect: Boolean default False;
property IndicatorAnnotationSpacing: Single;
property IndicatorHoverBehavior: TTMSFNCTimelineItemBehavior default tlibAlwaysItem;  // tlibBoth, tlibAlwaysAnnotation, tlibSeperate (sic)
property OverlapSections: Boolean default True;  property DrawSectionsBeneathDivisions: Boolean default False;
property ShowHoveredItems: Boolean default True;

// TTMSFNCTimelineInteraction (Timeline.Interaction)
property CanMoveIndicator, CanMoveSection, CanSizeSectionStart, CanSizeSectionEnd: Boolean default True;
property CanMoveIndicatorWithAnnotation: Boolean default False;
property InvertedMouseScroll: Boolean default False;  property InvertedMouseDrag: Boolean default True;
```

## Indicators and sections

```delphi
// TTMSFNCTimelineIndicator = class(TCollectionItem)
property TimelineValue: Double;  property TimelineDate: TDateTime;   // public
property Annotation: TTMSFNCTimelineAnnotation;   // Text, Visible, Position (tlapMiddle, tlapTopLeft default, tlapBottomRight), Width, Height, Hint, ShowHint, Appearance
property Appearance: TTMSFNCTimelineIndicatorAppearance;  // Shape (tlisCircle default, tlisSquare, tlisDiamond, tlisTriangleUp/Down/Left/Right, tlisBitmap), Size, Fill, Stroke, Bitmap/BitmapName, Hover*/Selected* variants
property Fixed: Boolean default False;  property Selectable: Boolean default True;  property Selected: Boolean default False;
property Visible: Boolean default True;  property Hint: string;  property ShowHint: Boolean;  property Tag: NativeInt;
property DBKey: String;  // + DataPointer/DataBoolean/DataObject/DataString/DataInteger (public)
procedure BeginUpdate;  procedure EndUpdate;

// TTMSFNCTimelineSection = class(TCollectionItem)
property StartTimelineValue, EndTimelineValue: Double;  property StartTimelineDate, EndTimelineDate: TDateTime;
property Text: string;  property Row: Integer;  // public Row
property Appearance: TTMSFNCTimelineSectionAppearance;   // Fill, Stroke, Font, Hover*/Selected*, TextHorizontalAlign, TextVerticalAlign, TextOrientation, Rounding
property Fixed, Selectable, Selected, Visible, Hint, ShowHint, Tag, DBKey  // as indicator

// TTMSFNCTimelineIndicators / TTMSFNCTimelineSections (Timeline.Indicators / Timeline.Sections)
function Add: TTMSFNCTimelineIndicator; overload;
function AddIndicator(ATimelineValue: Double; AAnnotationText: string = ''): TTMSFNCTimelineIndicator; overload;
function AddIndicator(ATimelineDate: TDateTime; AAnnotationText: string = ''): TTMSFNCTimelineIndicator; overload;
function AddSection(AStartTimelineValue: Double; AEndTimelineValue: Double; AText: string = ''): TTMSFNCTimelineSection; overload;
function AddSection(AStartTimelineDate: TDateTime; AEndTimelineDate: TDateTime; AText: string = ''): TTMSFNCTimelineSection; overload;
procedure Delete(Index: Integer);  procedure UnSelectAll;  function Insert(Index: Integer): ...;  Items[Index] default
```
The same `AddIndicator` / `AddSection` overloads exist directly on `TTMSFNCTimeline`. Both overloads store the same Double; with an untyped literal, pass a typed variable or cast (`Double(1492)` / `EncodeDate(...)`) if the compiler reports an ambiguous overload.

## Timeline control members (public)

```delphi
procedure BeginUpdate; override;  procedure EndUpdate; override;
procedure CenterValue(AValue: Double);
procedure ValueVisibleStart(AValue: Double; AOffset: Single = 0);  procedure ValueVisibleEnd(AValue: Double; AOffset: Single = 0);
function IsValueVisible(AValue: Double): Boolean;
procedure ResetZoomFactor;
function IncreaseZoomFactor(APercentage: Single = 10): Single;  function DecreaseZoomFactor(APercentage: Single = 10): Single;
function FindIndicatorWithDBKey(ADBKey: string): TTMSFNCTimelineIndicator;
function FindSectionWithDBKey(ADBKey: string): TTMSFNCTimelineSection;
function IsIndicatorHovered(AIndicator: TTMSFNCTimelineIndicator): Boolean; overload;
property TimelineRect, WorkspaceRect, DivisionsRect;  property DivisionSpace;   // read-only geometry, used in custom drawing
// published: Adapter, Appearance, BitmapContainer, Division, Fill, GlobalFont, Indicators, Interaction, Layout, Range, Sections, Stroke
```
`Appearance` (`TTMSFNCTimelineAppearance`): `TimelineFill`, `TimelineStroke`, `DivisionFont`, `DivisionTickmarkStroke`, `Rounding` (4), `DefaultIndicatorAppearance`, `DefaultAnnotationAppearance`, `DefaultSectionAppearance` (templates for new items).

## Example (runtime creation)

```delphi
uses VCL.TMSFNCTimeline, VCL.TMSFNCGraphicsTypes;

procedure TForm1.FormCreate(Sender: TObject);
var
  TL: TTMSFNCTimeline;
  ind: TTMSFNCTimelineIndicator;
  sec: TTMSFNCTimelineSection;
  v, v2: Double;
begin
  TL := TTMSFNCTimeline.Create(Self);
  TL.Parent := Self;
  TL.Align := alTop;
  TL.Height := 200;
  TL.BeginUpdate;
  try
    TL.Range.RangeType := tlrValue;          // numeric axis: years
    TL.Range.MinimumValue := 450;
    TL.Range.MaximumValue := 2050;
    TL.Range.DivisionSpan := 50;
    TL.Division.TextFormat.ValueFormat := '%.0f';
    TL.Layout.Orientation := tloHorizontal;

    v := 1492;
    ind := TL.AddIndicator(v, 'Columbus discovers America');
    ind.Annotation.Position := tlapTopLeft;
    ind.Annotation.Appearance.Alignment := gtaCenter;

    v := 1485; v2 := 1603;
    sec := TL.AddSection(v, v2, 'The Tudors');
    sec.Appearance.Fill.Color := gcMagenta;
    sec.Fixed := True;                       // not movable/sizable
  finally
    TL.EndUpdate;
  end;
  TL.CenterValue(1492);
end;
```

Date axis variant: `TL.Range.RangeType := tlrDay; TL.Range.MinimumDate := Date - 30; TL.Range.MaximumDate := Date + 30; TL.AddIndicator(Date, 'Today');` (`Date` is a `TDateTime`, so the date overload is picked).

## Events (exact signatures)

```delphi
OnGetValueText: procedure(Sender: TObject; AValue: Double; ARangeType: TTMSFNCTimelineRangeType; var AText: string) of object;
OnIndicatorMove:  procedure(Sender: TObject; AIndicator: TTMSFNCTimelineIndicator; var AMoveParams: TTMSFNCTimelineIndicatorMoveParameters; var AAllow: Boolean) of object;
OnIndicatorMoved: procedure(Sender: TObject; AIndicator: TTMSFNCTimelineIndicator; AMoveParams: TTMSFNCTimelineIndicatorMoveParameters) of object;
  // record: PreviousTimelineValue, NewTimelineValue: Double
OnSectionMove / OnSectionSize: procedure(Sender: TObject; ASection: TTMSFNCTimelineSection; var AMoveParams: TTMSFNCTimelineSectionMoveParameters; var AAllow: Boolean) of object;
OnSectionMoved / OnSectionSized: procedure(Sender: TObject; ASection: TTMSFNCTimelineSection; AMoveParams: TTMSFNCTimelineSectionMoveParameters) of object;
  // record: PreviousStartValue, NewStartValue, PreviousEndValue, NewEndValue, MoveValue: Double
OnIndicatorSelectionChanged: procedure(Sender: TObject; AIndicator: TTMSFNCTimelineIndicator; ASelectionParameters: TTMSFNCTimelineIndicatorSelectionParameters) of object;  // Annotation, Selected, MultiSelect
OnSectionSelectionChanged: procedure(Sender: TObject; ASection: TTMSFNCTimelineSection; ASelectionParameters: TTMSFNCTimelineSectionSelectionParameters) of object;
OnIndicatorAnnotationAnchorClick: procedure(Sender: TObject; AIndicator: TTMSFNCTimelineIndicator; AAnchor: string) of object;
OnBeforeDrawIndicator: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; AIndicator: TTMSFNCTimelineIndicator; var ADrawingParams: TTMSFNCTimelineIndicatorDrawingParams; var AAllow: Boolean; var ADefaultDraw: Boolean) of object;
OnBeforeDrawIndicatorAnnotation: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; AIndicator: TTMSFNCTimelineIndicator; var ADrawingParams: TTMSFNCTimelineAnnotationDrawingParams; var AAllow: Boolean; var ADefaultDraw: Boolean) of object;
OnBeforeDrawSection: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ASection: TTMSFNCTimelineSection; var ADrawingParams: TTMSFNCTimelineSectionDrawingParams; var AAllow: Boolean; var ADefaultDraw: Boolean) of object;
OnUpdateIndicatorDisplay: procedure(Sender: TObject; AIndicator: TTMSFNCTimelineIndicator; var AIndicatorDrawingParams: TTMSFNCTimelineIndicatorDrawingParams; var AAdd: Boolean) of object;
OnRangeChanged: procedure(Sender: TObject; ARangeParams: TTMSFNCTimelineRangeChangeParameters) of object;
```
Also `OnHoveredIndicatorChanged`, `OnHoveredSectionChanged`, `OnIndicatorsChanged`, `OnSectionsChanged`, `OnSectionAnchorClick`, `OnBeforeDrawDivision(Text/Tickmark)`, `OnBeforeDrawTimeline`, and matching `OnAfterDraw...`.

Custom drawing (demo `Custom Drawing`): in `OnBeforeDrawIndicatorAnnotation` replace `ADrawingParams.Text` (HTML allowed) and adjust `ADrawingParams.Rect`/`TextRect`; in `OnUpdateIndicatorDisplay` move `AIndicatorDrawingParams.AnnotationDrawingParams.Rect` and `AnnotationLineDrawingParams.StartPoint/EndPoint` (use `TimelineRect` / `WorkspaceRect`).

## TTMSFNCTimelineDatabaseAdapter (demo `Timeline Database Adapter`)

One dataset holds both kinds of item. Mapping by field-name strings on `Adapter.Item`: `DataSource`, `DBKey` (required), `Text`, `StartValue`/`EndValue` (numeric fields) **or** `StartDate`/`EndDate` (date fields), `Fixed`, `Selectable` (Boolean fields), `AutoIncrementDBKey: Boolean default True`. A record becomes an **indicator** when there is no end field or start = end (or the end date is NULL); otherwise a **section**.

```delphi
TMSFNCTimeline1.Adapter := TMSFNCTimelineDatabaseAdapter1;
with TMSFNCTimelineDatabaseAdapter1.Item do
begin
  AutoIncrementDBKey := False;
  DataSource := DataSource1;
  DBKey := 'Id';
  StartValue := 'Start';     // ftInteger fields, Range.RangeType = tlrValue
  EndValue := 'End';
  Text := 'Text';
end;
TMSFNCTimelineDatabaseAdapter1.Active := True;

procedure TForm1.TMSFNCTimelineDatabaseAdapter1FieldsToSection(Sender: TObject; AFields: TFields;
  ASection: TTMSFNCTimelineSection; var ADefaultSet: TTMSFNCTimelineDatabaseAdapterSectionFieldsParams);
begin
  ASection.Appearance.Fill.Color := AFields.FieldByName('Color').AsLongWord;
end;

procedure TForm1.TMSFNCTimelineDatabaseAdapter1IndicatorRead(Sender: TObject; AIndicator: TTMSFNCTimelineIndicator);
begin
  AIndicator.Fixed := True;
end;
```
Events: `OnFieldsToIndicator` / `OnIndicatorToFields` (`var ADefaultSet: TTMSFNCTimelineDatabaseAdapterIndicatorFieldsParams` = Text, Date, Value, Fixed, Selectable flags), `OnFieldsToSection` / `OnSectionToFields` (`...SectionFieldsParams` = Text, StartDate, EndDate, StartValue, EndValue, Fixed, Selectable), `OnReadFields(Sender; AFields; var AIndicator; var ASection; var AFieldParams)`, `OnIndicatorRead`/`OnSectionRead`, `OnIndicatorInserted`/`OnSectionInserted`, `OnIndicatorUpdated`/`OnSectionUpdated`, `OnIndicatorCreateDBKey`/`OnSectionCreateDBKey`, `OnSetIndicatorDateFromField`, `OnSetFieldFromIndicatorDate`, `OnSetSectionStartDateFromField`, `OnItemsLoaded`. `LoadItems` clears `Indicators` and `Sections` and reloads.

## Platform notes

Same API on VCL, FMX, WEB, LCL. WEB DB demo uses `TWebClientDataSet` instead of `TClientDataSet`.

## Does not exist / common mistakes

- `Timeline.Items`, `Events`, `AddEvent`, `AddItem` — the collections are `Indicators` (points) and `Sections` (ranges); use `AddIndicator` / `AddSection`.
- `Indicator.Date` / `Indicator.Value` / `Indicator.Caption` / `Indicator.Text` — use `TimelineDate` / `TimelineValue` and `Annotation.Text`.
- `Section.StartDate`/`EndDate`/`Caption`/`Color` — use `StartTimelineDate`/`EndTimelineDate` (or `...TimelineValue`), `Text`, `Appearance.Fill.Color`.
- `Timeline.Orientation`, `Timeline.StartDate`/`EndDate`, `Timeline.Zoom` — use `Layout.Orientation`, `Range.MinimumDate`/`MaximumDate`, `Layout.ZoomFactor` / `IncreaseZoomFactor`.
- Setting `Range.MinimumDate`/`MaximumDate` while `RangeType = tlrValue` (or vice versa) has no visible effect — set the pair that matches `RangeType`. `MinimumValue`/`MaximumValue` are Integer.
- `ScrollToDate`, `GotoDate` — use `CenterValue(ADate)` or `ValueVisibleStart(...)`.
- `Indicators.Clear` exists (TCollection), but there is no `Timeline.Clear`.
- Disabling drag per item: `Fixed := True` (and `Selectable := False`); globally via `Interaction.CanMove...` flags. There is no `ReadOnly` property.
- `Adapter.Item.StartTime`/`EndTime`/`Title` — timeline adapter fields are `StartDate`/`EndDate` or `StartValue`/`EndValue`, and `Text` (the planner adapter uses StartTime/EndTime/Title).
