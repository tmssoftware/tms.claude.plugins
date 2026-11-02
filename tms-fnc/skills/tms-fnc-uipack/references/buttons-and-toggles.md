# Buttons, toggles, sliders and indicators (TTMSFNCButton, TTMSFNCCheckBox, TTMSFNCRadioButton, TTMSFNCCheckGroup, TTMSFNCRadioGroup, TTMSFNCSwitch, TTMSFNCTrackBar, TTMSFNCRangeSlider, TTMSFNCProgressBar, TTMSFNCRating, TTMSFNCBadge, TTMSFNCSpinner, TTMSFNCWaitingIndicator)

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCButton`, `*.TMSFNCHTMLImageContainer`, `*.TMSFNCCheckBox`, `*.TMSFNCRadioButton`, `*.TMSFNCCustomGroup`, `*.TMSFNCCheckGroup`, `*.TMSFNCRadioGroup`, `*.TMSFNCSwitch`, `*.TMSFNCTrackBar`, `*.TMSFNCRangeSlider`, `*.TMSFNCProgressBar`, `*.TMSFNCBadge`, `*.TMSFNCSpinner`, `*.TMSFNCWaitingIndicator` (+ FNC Core 4.5.0.0).

## Units, palette, platforms

All registered on **`TMS FNC UI`**, all `TMSPlatformsWeb` (VCL, FMX, WEB). Prefix `VCL.` / `FMX.` / `WEBLib.`; Lazarus `LCLTMSFNC...` (no LCL unit for `TTMSFNCSpinner`).

| Class | Unit | Native or FNC-drawn |
|---|---|---|
| `TTMSFNCButton` | `TMSFNCButton` | **native**: VCL/FMX/LCL `TCustomButton`, WEB `TWebButton`; hosts a `TTMSFNCHTMLText` + `TTMSFNCImage` |
| `TTMSFNCCheckBox`, `TTMSFNCRadioButton` | `TMSFNCCheckBox`, `TMSFNCRadioButton` | FNC-drawn (`TTMSFNCHTMLImageContainer`) |
| `TTMSFNCCheckGroup`, `TTMSFNCRadioGroup` | `TMSFNCCheckGroup`, `TMSFNCRadioGroup` (base `TMSFNCCustomGroup`) | FNC panel creating **native** `TCheckBox` / `TRadioButton` + HTML text per item |
| `TTMSFNCSwitch` | `TMSFNCSwitch` | FNC-drawn |
| `TTMSFNCTrackBar`, `TTMSFNCRangeSlider` | `TMSFNCTrackBar`, `TMSFNCRangeSlider` | FNC-drawn |
| `TTMSFNCProgressBar`, `TTMSFNCRating` | both in `TMSFNCProgressBar` | FNC-drawn |
| `TTMSFNCBadge` | `TMSFNCBadge` | FNC-drawn |
| `TTMSFNCSpinner` | `TMSFNCSpinner` | FNC-drawn (iOS-style value wheel, **not** a busy indicator) |
| `TTMSFNCWaitingIndicator` | `TMSFNCWaitingIndicator` | FNC-drawn busy animation |

## TTMSFNCButton

Published (all frameworks): `Text` (HTML allowed), `Font: TTMSFNCGraphicsFont`, `WordWrapping`, `Bitmap: TTMSFNCBitmap`, `BitmapName` + `BitmapContainer`, `BitmapSize: integer default 30`, `ShowImage: Boolean default False`, `ShowText: Boolean default True`, `ImageAlign`/`TextAlign` (`TAlign` on VCL/WEB, default `alLeft`/`alClient`; `TAlignLayout` on FMX). Public: `function HTMLText: TTMSFNCHTMLText;`, `function Image: TTMSFNCImage;`. Everything else is the native button's: VCL `ModalResult`, `Default`, `Cancel`, `Style`, `DropDownMenu`, `OnClick`; FMX `StaysPressed`, `IsPressed`, `RepeatClick`, `ModalResult`.
```delphi
uses VCL.TMSFNCButton, VCL.TMSFNCBitmapContainer;

btn := TTMSFNCButton.Create(Self);
btn.Parent := Self;
btn.SetBounds(16, 16, 140, 36);              // FMX: Position.X/Y, Width, Height
btn.Text := '<b>Save</b> document';
btn.BitmapContainer := TMSFNCBitmapContainer1;
btn.BitmapName := 'save';
btn.ShowImage := True;                        // required in code (auto-set only at design time)
btn.OnClick := SaveClick;
```

## TTMSFNCCheckBox / TTMSFNCRadioButton

Shared published members (`TTMSFNCHTMLImageContainer`): `Checked: Boolean`, `Text` (HTML, anchors raise `OnAnchorClick`), `Font`, `WordWrapping`, `Trimming`, `HorizontalTextAlign` (`gtaLeading`), `VerticalTextAlign` (`gtaCenter`), `WidgetPosition: TTMSFNCHTMLImageContainerWidgetPosition = (hwpLeft, hwpRight)`, `BitmapName` + `BitmapContainer`.
```delphi
OnChange: TNotifyEvent;
OnCheckedStateChanged: TTMSFNCHTMLImageContainerCheckedStateChangedEvent; // procedure(Sender: TOBject; AChecked: Boolean) of object
OnAnchorClick: procedure(Sender: TObject; AAnchor: string) of object;
OnBeforeDrawWidget: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; AWidgetPosition: TTMSFNCHTMLImageContainerWidgetPosition; var AAllow: Boolean; var ADefaultDraw: Boolean) of object;
// + OnAfterDrawWidget, OnBeforeDrawText, OnAfterDrawText
```
`TTMSFNCRadioButton` adds `GroupName: string`: checking one unchecks the other `TTMSFNCRadioButton`s **with the same Parent and the same GroupName** (empty name = one group per parent).
```delphi
chk := TTMSFNCCheckBox.Create(Self);
chk.Parent := Self;
chk.Text := 'I accept the <a href="terms">terms</a>';
chk.OnCheckedStateChanged := AcceptChanged;

for i := 0 to 2 do
begin
  rb := TTMSFNCRadioButton.Create(Self);   // give it an Owner: grouping compares ComponentIndex
  rb.Parent := Panel1;
  rb.GroupName := 'size';
  rb.Text := Sizes[i];
  rb.SetBounds(8, 8 + i * 28, 120, 24);
end;
```

## TTMSFNCCheckGroup / TTMSFNCRadioGroup

One control per line of `Items: TStrings` (HTML allowed), laid out in `Columns` (default 1). Shared published: `Items`, `Columns`, `Font`, `Fill`, `Stroke`, `BitmapContainer`, `Title` (`Text`, `Font`, `Alignment`, `ShowCheckBox` (False), `Checked`, `CheckBoxMode`). Public: `Texts[AIndex]`, `Containers[AIndex]`, `HTMLTexts[AIndex]`.
```delphi
// TTMSFNCCheckGroup
property Checked[AIndex: Integer]: Boolean;      // public
property Value: Int64 default 0;                 // public bitmask, bit i = item i (max 64)
property CheckBoxes[AIndex: Integer]: TCheckBox;  // public, native
property TitleCheckBox: TCheckBox;
// Title.CheckBoxMode: TTMSFNCCheckGroupTitleCheckBoxMode = (cgtcmNone, cgtcmCheckAll, cgtcmToggleEnabled), default cgtcmCheckAll
OnCheckBoxClick, OnCheckBoxDblClick: TTMSFNCCheckGroupClickEvent;  // procedure(Sender: TObject; AItemIndex: Integer; AValue: Int64) of object
OnTitleCheckBoxClick: TNotifyEvent; OnTitleAnchorClick; OnCheckboxAnchorClick;

// TTMSFNCRadioGroup
property ItemIndex: Integer default -1;          // published
property RadioButtons[AIndex: Integer]: TRadioButton;  // public, native
property RadioTabStop: Boolean default True;
// Title.CheckBoxMode: TTMSFNCRadioGroupTitleCheckBoxMode = (rgtcmNone, rgtcmToggleEnabled)
OnRadioButtonClick, OnRadioButtonDblClick: TTMSFNCRadioGroupClickEvent; // procedure(Sender: TObject; AItemIndex: Integer) of object
```
```delphi
cg := TTMSFNCCheckGroup.Create(Self);
cg.Parent := Self;
cg.SetBounds(16, 60, 220, 120);
cg.BeginUpdate;
cg.Title.Text := 'Toppings';
cg.Title.ShowCheckBox := True;          // "check all"
cg.Columns := 2;
cg.Items.CommaText := 'Cheese,Ham,Olives,Onion';
cg.EndUpdate;
cg.Checked[0] := True;                  // after Items exist
cg.OnCheckBoxClick := ToppingClick;
```
Group demos fill items at design time only (`InitSample` runs in the IDE); a group created in code starts empty.

## TTMSFNCSwitch

```delphi
TTMSFNCCustomSwitchState = (ssOff, ssOn);
TTMSFNCCustomSwitchLayout = (sloSimple, sloExtended);   // extended draws On/Off text
TTMSFNCCustomSwitchOrientation = (soHorizontal, soVertical);
property State: TTMSFNCCustomSwitchState default ssOff;  // published
property Checked: Boolean;                                // public only (maps to State)
property AppearanceOn, AppearanceOff;   // Fill, Stroke, Font, Text
property ButtonAppearance;               // Fill, Stroke, OffFill, OffStroke, Margin
property Rounded: Boolean default False; property AnimationFactor: Integer default 15; property GlobalFont;
OnStateChange: TTMSFNCCustomSwitchStateChangeEvent; // procedure(Sender: TObject; ASwitchState: TTMSFNCCustomSwitchState) of object
OnChange: TNotifyEvent;
```
```delphi
sw := TTMSFNCSwitch.Create(Self);
sw.Parent := Self;
sw.Rounded := True;
sw.Layout := sloExtended;
sw.AppearanceOn.Text := 'ON';
sw.State := ssOn;
sw.OnStateChange := SwitchStateChange;
```

## TTMSFNCTrackBar / TTMSFNCRangeSlider (demo `TrackBar`)

Both descend from `TTMSFNCCustomTrackBarBase`: `Min`/`Max: Single` (0/100). Track bar: `Value: Single`; range slider: `ValueLeft`, `ValueRight: Single`.
```delphi
// Appearance (TTMSFNCCustomTrackBarAppearance / ...RangeSliderAppearance)
Orientation: TTMSFNCCustomTrackBarOrientation = (tboHorizontal, tboVertical);
ThumbShape: TTMSFNCCustomTrackBarBaseShape = (tsRectangle, tsEllipse, tsImage);
LineShape: TTMSFNCCustomTrackBarBaseLineShape = (lsRectangle, lsRoundedRectangle, lsImage);
TickMarkPosition: TTMSFNCTrackBarAppearanceTickMarkPosition = (tmpBoth, tmpBottomRight, tmpTopLeft, tmpNone);
TickMarkDivision (5), TickMarkLabel (False), TickMarkLabelFormat ('%g'), TickMarkSize, TickMarkSpacing;
TrackLabelPosition: TTMSFNCCustomTrackBarTrackLabelPosition = (tlpTopLeft, tlpTopCenter, tlpTopRight, tlpBottomLeft, tlpBottomCenter, tlpBottomRight, tlpNone);
TrackLabelFormat ('Pos: %g'), ThumbFill/ThumbStroke/ThumbWidth/ThumbHeight, LineFill/LineStroke/LineWidth;
ButtonShape: TTMSFNCTrackBarAppearanceButtonShape = (bsRounded, bsRectangle, bsImage, bsNoButton); // track bar only, default bsNoButton
// Interaction: Frequency (snap step); track bar also RepeatClick, RepeatInterval, JumpToExactValue
// TTMSFNCTrackBar events
OnValueChanged: TTMSFNCCustomTrackBarValueChangedEvent; // procedure(Sender: TObject; AValue: Single) of object
OnChanged: TNotifyEvent;  OnBefore/AfterDrawThumb, ...TrackLine, ...TickMarks, ...TickLabel, ...TrackLabel, ...Button
// public: procedure DecreaseByFrequency; procedure EncreaseByFrequency;   (sic: "Encrease")
// TTMSFNCRangeSlider events
OnValueChanged, OnValueChange: TTMSFNCCustomTrackBarBaseValueChanged; // procedure(Sender: TObject; AValue: Single; ALeft: Boolean) of object
```
```delphi
procedure TForm130.TMSFNCRangeSlider1ValueChanged(Sender: TObject; AValue: Single; ALeft: Boolean);
begin
  Label5.Caption := Format('%g - %g', [TMSFNCRangeSlider1.ValueLeft, TMSFNCRangeSlider1.ValueRight]);
end;

tb := TTMSFNCTrackBar.Create(Self);
tb.Parent := Self;
tb.BeginUpdate;
tb.Min := 0; tb.Max := 50; tb.Value := 10;
tb.Interaction.Frequency := 5;
tb.Appearance.TickMarkLabel := True;
tb.Appearance.TrackLabelPosition := tlpTopCenter;
tb.EndUpdate;
tb.OnValueChanged := TrackValueChanged;
```

## TTMSFNCProgressBar / TTMSFNCRating (demo `ProgressBar and Rating`)

`Minimum`, `Maximum`, `Value: Double` (0/100), `CustomValue: string` (ProgressBar), `Levels` (collection: `LevelPosition: Double` = value where the level starts, `Fill`, `Stroke`, `ActiveFont`), `Appearance`, `Layout`, `GlobalFont`.
```delphi
// Layout (TTMSFNCProgressBarLayout / TTMSFNCRatingLayout)
Shape: TTMSFNCProgressBarShape = (psHorizontalLine, psVerticalLine);
ValueType: TTMSFNCProgressBarValueType = (pvtValue, pvtPercentage, pvtCustom);  // default pvtPercentage
TextPosition: TTMSFNCProgressBarTextPosition = (ptpStart, ptpCenter, ptpEnd, ptpProgressEnd, ptpFollowCenter, ptpFollowEnd, ptpProgressCenter);
TextOrientation: (ptoHorizontal, ptoLeft, ptoRight, ptoUpsideDown);
ShowValue, Blocks (1), Spacing, Rounding, RoundProgressEnd, Prefix, Suffix, Decimals (2), Min/MaximumBitmap; Interval (Rating only)
// Appearance: Fill, Stroke, Font, DefaultLevelFill/Font/Stroke, Stacked (ProgressBar);
//             Rating: ActiveBitmap, InActiveBitmap, ShowActiveBitmaps, ShowInActiveBitmaps
// TTMSFNCRating only: Interaction (ReadOnlyMode, SnapToValue, SlideToValue, KeyboardSupport) and value events:
OnValueChange: procedure(Sender: TObject; AValue: Single; var AAllow: Boolean) of object;
OnValueChanged: procedure(Sender: TObject; AValue: Single) of object;
// + OnSlideValueChange(d), OnSnapValueChange(d), OnKeyboardValueChange(d)
```
```delphi
procedure TForm2.TMSFNCRating4ValueChange(Sender: TObject; AValue: Single; var AAllow: Boolean);
begin
  if AValue < 3 then AAllow := False;
end;

TMSFNCProgressBar1.Layout.ShowValue := True;
TMSFNCProgressBar1.Value := 70;
```

## TTMSFNCBadge

Floats over another control: `Control: TControl` (the badge must have the **same Parent** as that control; position uses `Control.Left/Top`), `HorizontalPosition: TTMSFNCBadgeHorizontalPosition = (bhpCustom, bhpLeft, bhpCenter, bhpRight)` (bhpRight), `VerticalPosition: TTMSFNCBadgeVerticalPosition = (bvpCustom, bvpTop, bvpCenter, bvpBottom)` (bvpTop), `Text`, `Bitmap`, `DisabledBitmap`, `AutoSize`, `Visible`, `Appearance` (`Fill`, `Stroke`, `Font`, `Rounding` (15), `Hover*`, `Down*`, `Disabled*`, `TextAlignHorizontal/Vertical`). Public: `procedure ShowBadge;`, `procedure HideBadge;`. Events: `OnPositionChange(Sender; var AX, AY: Integer; var AAllow: Boolean)`, `OnSizeChange`, `OnPositionChanged`, `OnSizeChanged`, `OnBeforeDrawText`, `OnBeforeDrawImage`, `OnBeforeDrawBackGround`, ...
```delphi
bd := TTMSFNCBadge.Create(Self);
bd.Parent := Button1.Parent;
bd.Control := Button1;
bd.Text := '3';
bd.Appearance.Fill.Color := gcRed;
bd.Appearance.Font.Color := gcWhite;
```

## TTMSFNCSpinner (value wheel)

`Columns: TTMSFNCSpinnerColumns`; each `TTMSFNCSpinnerColumn`: `RangeType: TTMSFNCSpinnerRangeType = (rtNumber, rtDateTime, rtCustom)`, `RangeFrom`, `RangeTo`, `Step`, `StepType: TTMSFNCSpinnerStepType = (stNumber, stSecond, stMinute, stHour, stDay, stMonth, stYear)`, `DateRangeFrom/To`, `ValueFormat`, `DateTimeValueFormat`, `CustomItems` (`Text`, `Value`, `PictureName`), `Cyclic`, `Width`, `Font`, `SelectedFont`, `SelectedValue: Double`; public `SelectedDateTime`, `SelectedCustomIndex`, `ScrollToValue(AValue: Double; AAnimation: Boolean = True; AAnimationSpeed: Integer = 4)`, `Next`, `Previous`. Control: `Appearance` (SelectedFill/Stroke/Height), `ColumnAppearance`, `ReadOnly`, `SmoothScrolling`, `BitmapContainer`.
```delphi
OnSelectedValueChanged: procedure(Sender: TObject; AColumn, ASelectedCustomIndex: Integer; ASelectedValue: Double; ARangeType: TTMSFNCSpinnerRangeType) of object;
```
```delphi
sp := TTMSFNCSpinner.Create(Self);       // empty at runtime (3 sample columns only in the IDE)
sp.Parent := Self;
sp.BeginUpdate;
col := sp.Columns.Add;
col.RangeType := rtNumber;
col.RangeFrom := 0; col.RangeTo := 23; col.Step := 1;
col.ValueFormat := '%g';
sp.EndUpdate;
sp.Columns[0].SelectedValue := 8;
```

## TTMSFNCWaitingIndicator (demo `ProgressBar and Rating`)

`Active: Boolean` (start/stop), `AnimationSpeed: Double` (4), `OverlayParent: Boolean` (False: dim the parent), `Appearance`: `IndicatorShape: TTMSFNCWaitingIndicatorIndicatorShape = (wisCircle, wisSquare, wisImage, wisProgress)`, `MoveShape: TTMSFNCWaitingIndicatorMoveShape = (wmsCircle, wmsLine)`, `Indicators`, `IndicatorFill`, `IndicatorStroke`, `IndicatorBitmap`, `CenterBitmap`, `OverlayFill`, `RotateIndicators`, `RotateClockWise`, `ChangeIndicatorSize`.
```delphi
TMSFNCWaitingIndicator1.Active := True;
TTask.Run(procedure
  begin
    DoLongWork;
    TThread.Queue(nil, procedure begin TMSFNCWaitingIndicator1.Active := False; end);
  end);
```

## Platform notes

- `TTMSFNCButton` on WEB is a `TWebButton` rendered as HTML (`<font>` tags converted to spans); VCL inherits `TCustomButton` (no `Caption` access, `Text` is the caption); FMX uses `StyleLookup 'buttonstyle'`.
- Check/radio groups use the framework's native `TCheckBox`/`TRadioButton` (`CheckBoxes[i]`, `RadioButtons[i]` are those types per framework).
- Positioning: VCL/WEB `SetBounds`/`Align := alTop`; FMX `Position`, `Align := TAlignLayout.Top`.

## Does not exist / common mistakes

- `TTMSFNCButton.Caption`, `.Images`/`.ImageIndex`, `.Glyph`, `.Fill`, `.Stroke`, `.Appearance`, `.Down`, `.GroupIndex` — it is a native button with `Text`, `Bitmap`/`BitmapName`+`BitmapContainer`; for a fully FNC-drawn/styleable button use `TTMSFNCToolBarButton` (unit `*.TMSFNCToolBar`). Setting `BitmapName` at runtime without `ShowImage := True` shows no image.
- `TTMSFNCCheckBox.Caption`, `.State`, `.AllowGrayed`, `cbGrayed`, `OnClick` for state — use `Text`, `Checked`, `OnCheckedStateChanged`/`OnChange`; there is no third state.
- `TTMSFNCRadioButton.GroupIndex` — use `GroupName` (and the same Parent).
- `TTMSFNCRadioGroup.Buttons[]`, `.Caption`, `OnClick` for selection; `TTMSFNCCheckGroup.ItemChecked[]`, `.Caption` — use `RadioButtons[]`, `Title.Text`, `OnRadioButtonClick`; `Checked[]`/`Value`, `OnCheckBoxClick`.
- `TTMSFNCSwitch.IsChecked` (FMX TSwitch), `.Value`, `OnSwitch`, `OnToggle`; `Checked` in the Object Inspector — use `State` (published) / `Checked` (public only), `OnStateChange`.
- `TTMSFNCTrackBar.Position`, `.Frequency`, `.TickStyle`, `OnChange` — use `Value`, `Interaction.Frequency`, `Appearance.TickMark*`, `OnValueChanged`. `TTMSFNCTrackBar` does **not** publish `OnValueChange` (only `TTMSFNCRangeSlider` does). `IncreaseByFrequency` does not exist — the method is spelled `EncreaseByFrequency`.
- `Appearance.ButtonShape := bsNone` (the `TrackBar` demo does this) — the value is `bsNoButton`; `bsNone` is the VCL `TBorderStyle` constant.
- `TTMSFNCRangeSlider.Value` / `.MinValue` / `.MaxValue` — use `ValueLeft` / `ValueRight` (and `Min`/`Max` for the range).
- `TTMSFNCProgressBar.Position`, `.Max`, `.Min`, `.StepIt`, `.Marquee`, `.Style := pbstMarquee`, `OnValueChanged` — use `Value`, `Maximum`, `Minimum`; indeterminate = `TTMSFNCWaitingIndicator` (`Appearance.IndicatorShape := wisProgress`); the progress bar publishes no value-change events (`TTMSFNCRating` does).
- `TTMSFNCRatingBar`, `TTMSFNCStarRating` — the class is `TTMSFNCRating` in unit `*.TMSFNCProgressBar`.
- `TTMSFNCBadge.Value`, `.Count`, `.Caption`, `ShowBadge('5')` — use `Text`; only parameterless `ShowBadge`/`HideBadge` are public on `TTMSFNCBadge`.
- `TTMSFNCSpinner.Active` / `.Spinning` as a loading animation — `TTMSFNCSpinner` is a value-picking wheel; for a busy animation use `TTMSFNCWaitingIndicator.Active`.
- `TTMSFNCWaitingIndicator.Start` / `.Stop` / `.Animate` — use `Active := True/False`.
- `TAdvGlowButton`, `TAdvToggleSwitch`, `TAdvTrackBar`, `TAdvProgressBar`, `TAdvBadge` property names (`Picture`, `Position`, `ProgressBarStyle`) do not carry over to FNC.
