# Date and time controls (TTMSFNCCalendar, TTMSFNCDatePicker, TTMSFNCDateTimePicker, TTMSFNCAnalogTimePicker/Selector, TTMSFNCDigitalTimePicker/Selector)
> Sections (line ranges): 6-21 Units, palette, platforms · 22-115 TTMSFNCCalendar · 116-144 TTMSFNCDatePicker · 145-163 TTMSFNCDateTimePicker · 164-189 Analog time: TTMSFNCAnalogTimeSelector · 190-217 Digital time: TTMSFNCDigitalTimeSelector · 218-223 Platform notes · 224-238 Does not exist / common mistakes

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCCalendar`, `*.TMSFNCDatePicker`, `*.TMSFNCDateTimePicker`, `*.TMSFNCAnalogTimePicker`, `*.TMSFNCAnalogTimeSelector`, `*.TMSFNCDigitalTimePicker`, `*.TMSFNCDigitalTimeSelector`, `*.TMSFNCCustomPicker`, the `*Reg.pas` units and the demos `Calendar` and `Pickers` (VCL/FMX).

## Units, palette, platforms

All on palette page **`TMS FNC UI`**. Prefix `VCL.` / `FMX.` / `WEBLib.`; Lazarus `LCLTMSFNC...` (no dot). All are in the WEB package.

| Class | Unit | Kind |
|---|---|---|
| `TTMSFNCCalendar` | `VCL.TMSFNCCalendar` | month grid control |
| `TTMSFNCDatePicker` | `VCL.TMSFNCDatePicker` (+ `VCL.TMSFNCCalendar` for appearance types) | edit/button + calendar dropdown |
| `TTMSFNCDateTimePicker` | `VCL.TMSFNCDateTimePicker` | date picker + time picker side by side |
| `TTMSFNCAnalogTimeSelector` | `VCL.TMSFNCAnalogTimeSelector` | clock face control |
| `TTMSFNCAnalogTimePicker` | `VCL.TMSFNCAnalogTimePicker` | dropdown with clock |
| `TTMSFNCDigitalTimeSelector` | `VCL.TMSFNCDigitalTimeSelector` (+ `VCL.TMSFNCCustomSelector`) | grid of time slots |
| `TTMSFNCDigitalTimePicker` | `VCL.TMSFNCDigitalTimePicker` | dropdown with time-slot grid |

Colors/aligns from `VCL.TMSFNCGraphicsTypes` (`gcDodgerblue`, `gtaCenter`). Dates are `TDate`, times `TTime`; use `DateUtils`/`SysUtils` (`EncodeDate`, `StrToTime`).

## TTMSFNCCalendar

```delphi
// published
property Date: TDate;                  // the displayed (navigated) date; setting it does NOT select it
property Day, Month, Year: Integer;    // displayed month/year
property MinDate, MaxDate: TDate;      // 0 = no limit
property FirstDay: Integer default 1;  // DayOfWeek numbering: 1 = Sunday, 2 = Monday, ...
property Events: TTMSFNCCalendarEvents;          // badge items
property BadgeSize: Integer default 14;
property Header: TTMSFNCCalendarHeader;          // Visible, Height (25), Fill, Font, Stroke, Arrow
property Footer: TTMSFNCCalendarFooter;          // Visible, Caption, DateCaption (fdNone, fdSelected, fdToday default)
property DateAppearance: TTMSFNCCalendarDateAppearance;   // Fill/Font/Stroke, Selected*, Disabled*, Today*, DateBefore*/DateAfter*, Badge*, ShowDaysBefore, ShowDaysAfter, ShowFocus
property DayNameAppearance, LineAppearance, WeekNumberAppearance;   // WeekNumberAppearance.Visible default False
property Interaction: TTMSFNCCalendarInteraction;
property Fill, Stroke, BitmapContainer, GlobalFont;
// public
procedure SelectDate(ADate: TDate);              // ADDS ADate to SelectedDates (respects Min/MaxDate)
procedure SelectADate(ADate: TDate);             // clears selection, selects and shows ADate
procedure SelectDateIfAvailable(ADate: TDate);   // clears selection, selects if within Min/MaxDate
procedure SelectMultiDates(AStartDate: TDate; AEndDate: TDate);
procedure SelectEvent(ADate: TDate);
function SelectedDate: TDate;                    // last selected; a FUNCTION (read-only)
property SelectedDates: TTMSFNCCalendarDates;    // Count, Items[i].Date, SelectDate, SelectDateInterval, UnselectDate, UnselectAll, InCollection
property FocusedDate: TDate;
procedure PreviousDate; procedure NextDate;      // navigate one step (month/year by NavigationMode)
function CurrentDay, CurrentMonth, CurrentYear: Integer;   // of today
function XYToDate(AX, AY: Single): TDate;
```

`Header.Arrow` (`TTMSFNCCalendarArrow`): `Color`, `Size` (15), `Visibility` ([alvLeft, alvRight]), `ArrowLeftType`/`ArrowRightType: TTMSFNCCalendarArrowType` = `atTriangle, atArrow` (default)`, atBitmap, atCustom` (draw in `OnCustomArrowDraw`), `ArrowLeftBitmap`/`ArrowRightBitmap`.

`Interaction` (`TTMSFNCCalendarInteraction`): `MultiSelect` (False), `ReadOnlyMode` (False), `KeyboardSupport` (True), `SwipeOnHeader` (False), `AllowMonthSelection`/`AllowYearSelection` (False; header popups), `YearOptions.ItemsBeforeCurrentYear/ItemsAfterCurrentYear` (5), `NavigationMode: TTMSFNCCalendarNavigationMode` = `nmMonth` (default), `nmYear`, `nmFocusedDate`, `nmCustom` (handle `OnCustomNavigation`).

`Events` items (`TTMSFNCCalendarEventItem`): `Date`, `BadgeValue: Integer`, `ShowBadge` (True), `BadgeColor`, `BadgeFontColor`, `Hint` (shown when the control's `ShowHint := True`). `Events.Add: TTMSFNCCalendarEventItem`.

Events:
```delphi
OnSelectDate:      procedure(Sender: TObject; ADate: TDate) of object;
OnBeforeSelectDate: procedure(Sender: TObject; ADate: TDate) of object;
OnSelectMultiDate: procedure(Sender: TObject; AStartDate: TDate; AEndDate: TDate) of object;
OnMonthChanged:    procedure(Sender: TObject; AMonth: Integer) of object;
OnYearChanged:     procedure(Sender: TObject; AYear: Integer) of object;
OnCustomNavigation: procedure(Sender: TObject; ADate: TDate; AFocusedDate: TDate; ADirection: Boolean) of object;
OnCustomArrowDraw: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; ADirection: Boolean) of object;
OnBeforeDrawDayNumbers: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; ADate: TDate; var AAllow: Boolean; var ADefaultDraw: Boolean) of object;
OnBeforeDrawBadge: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; ABadge: TTMSFNCCalendarEventItem; var AAllow: Boolean; var ADefaultDraw: Boolean) of object;
```
Plus `OnBeforeDraw/AfterDraw` for `Header`, `Footer`, `DayNames`, `DayNumbers`, `Lines`, `WeekNumbers`, `ArrowLeft`, `ArrowRight` (and `...Text` variants), `OnNavigateBack`, `OnNavigateForward`, `OnNavigateFooter`, `OnMonthPopupValueSelected`, `OnYearPopupValueSelected`.

Example (demo `Calendar`):
```delphi
uses VCL.TMSFNCCalendar, VCL.TMSFNCGraphicsTypes, DateUtils;

procedure TForm1.FormCreate(Sender: TObject);
var
  Cal: TTMSFNCCalendar;
  y, m: Integer;
begin
  Cal := TTMSFNCCalendar.Create(Self);
  Cal.Parent := Self;
  Cal.SetBounds(10, 10, 250, 250);
  Cal.BeginUpdate;
  try
    Cal.FirstDay := 2;                                   // Monday
    Cal.Interaction.MultiSelect := True;
    Cal.WeekNumberAppearance.Visible := True;
    Cal.DateAppearance.SelectedFill.Color := gcLimegreen;
    Cal.ShowHint := True;
    y := Cal.CurrentYear; m := Cal.CurrentMonth;
    with Cal.Events.Add do
    begin
      Date := EncodeDate(y, m, 14);
      BadgeValue := 2;
      Hint := 'Tom''s birthday';
    end;
    Cal.SelectADate(EncodeDate(y, m, Cal.CurrentDay));
  finally
    Cal.EndUpdate;
  end;
  Cal.OnSelectDate := CalSelectDate;
end;

procedure TForm1.CalSelectDate(Sender: TObject; ADate: TDate);
var
  I: Integer;
  Cal: TTMSFNCCalendar;
begin
  Cal := Sender as TTMSFNCCalendar;
  for I := 0 to Cal.SelectedDates.Count - 1 do
    ListBox1.Items.Add(DateToStr(Cal.SelectedDates.Items[I].Date));
end;
```

## TTMSFNCDatePicker

A `TTMSFNCDefaultPicker` (button/edit + popup) with a calendar inside. Shares the calendar appearance properties.

```delphi
property SelectedDate: TDate;                   // read/write PROPERTY here (on the calendar it is a function)
property AllowNumericNullValue: Boolean default True;  // SelectedDate := 0 -> empty text
property Editable: Boolean default False;       // typed input (validate with OnValidate)
property CloseOnSelection: Boolean default True;
property MinDate, MaxDate: TDate;  property FirstDay: Integer;  property Events;  property BadgeSize;
property Header, Footer, DateAppearance, DayNameAppearance, LineAppearance, WeekNumberAppearance;
property CalendarFill, CalendarStroke: ...;     // calendar background (not Fill/Stroke)
property DropDownWidth, DropDownHeight: Single;
property Interaction: TTMSFNCDatePickerInteraction;  // ReadOnlyMode, SwipeOnHeader, KeyboardSupport, NavigationMode (NO MultiSelect)
property Day, Month, Year: Integer;  procedure Clear;  procedure DropDown;   // public
OnDateSelected: procedure(Sender: TObject; ADate: TDate) of object;
OnValidate: procedure(Sender: TObject; AEditText: string; var ADate: TDateTime; var ADefault: Boolean) of object;
```
The displayed text is `DateToStr(SelectedDate)` (current `FormatSettings`); there is no format property.

```delphi
DP := TTMSFNCDatePicker.Create(Self);
DP.Parent := Self;
DP.SetBounds(10, 280, 150, 26);
DP.SelectedDate := Date;
DP.MinDate := Date;                // no past dates
DP.OnDateSelected := DPDateSelected;   // procedure TForm1.DPDateSelected(Sender: TObject; ADate: TDate);
```

## TTMSFNCDateTimePicker

Composite of a `TTMSFNCDatePicker` and an analog or digital time picker.

```delphi
property SelectedDateTime: TDateTime;
property TimePickerMode: TTMSFNCDateTimePickerMode default dtpmDigital;   // dtpmAnalog, dtpmDigital
property Editable: Boolean default False;  property CloseOnSelection: Boolean default True;
property AllowNumericNullValue: Boolean default True;
OnDateTimeChanged: procedure(Sender: TObject; ADateTime: TDateTime) of object;
// public sub-controls for fine tuning
property DatePicker: TTMSFNCDatePicker;  property AnalogTimePicker: TTMSFNCAnalogTimePicker;  property DigitalTimePicker: TTMSFNCDigitalTimePicker;
procedure Clear;
// FMX only:
property Native: Boolean default False;   // use FMX TDateEdit + TTimeEdit
property DateEdit: TDateEdit;  property TimeEdit: TTimeEdit;
```
Demo `Pickers`: `TMSFNCDateTimePicker1.TimePickerMode := dtpmAnalog;` and `FormatDateTime('ddddd tt', TMSFNCDateTimePicker1.SelectedDateTime)`.

## Analog time: TTMSFNCAnalogTimeSelector / TTMSFNCAnalogTimePicker

```delphi
// TTMSFNCAnalogTimeSelector (control)
property Time: TTime;  property AM: Boolean;   // public AM
property Style: TTMSFNCAnalogTimeSelectorStyle default wsClassic;  // wsClassic, wsFluorescent, wsEmerald, wsTower, wsFuchsia, wsBlack, wsBlackWhite, wsSuperNova, wsSports, wsSmooth, wsCustom
property FollowMouse: Boolean default True;
property Settings: TTMSFNCAnalogTimeSelectorSettings;   // Auto (False: True = running clock), TimeOffset (0), ReadOnly (False)
property Appearance: TTMSFNCAnalogTimeSelectorAppearance;
  // Shape (wsCircle, wsRect, wsRoundRect), TickMarks (tmAll, tmHours, tmNone, tmQuartHours), HourMarkStyle (hmsLine, hmsQuartDblLine),
  // PointerStyle (psLine, psShortLine, psPointer, psLineArrow), ShowSecondPointer (False), ShowNumbers (True), ShowAMPM (True),
  // HourPointer/MinutePointer/SecondPointer (strokes), HourFont, Fill, Stroke, CenterPoint*; procedure InitializeDefault;
function XYToHour(X: Single; Y: Single): Integer;  function XYToMinute(X: Single; Y: Single): Integer;
OnTimeChanged / OnHourChanged / OnMinuteChanged / OnSecondChanged: procedure(Sender: TObject; ATime: TTime) of object;

// TTMSFNCAnalogTimePicker (dropdown)
property SelectedTime: TTime;
property TimeFormat: string;                    // default 'hh:nn:ss' (FormatDateTime)
property Mode: TTMSFNCTimePickerMode default tpmAnalog;   // tpmAnalog, tpmDigital
property CloseOnSelection: Boolean default False;         // note: False here, True on the other pickers
property Editable, AllowNumericNullValue, DropDownWidth, DropDownHeight, Font;
property SelectorAppearance: TTMSFNCAnalogTimeSelectorAppearance;
OnTimeSelected: procedure(Sender: TObject; ATime: TTime) of object;
```
Demo `Pickers`: `TMSFNCAnalogTimeSelector1.Settings.Auto := True; TMSFNCAnalogTimeSelector1.Appearance.ShowSecondPointer := True;` / `Style := wsBlackWhite` / `Appearance.InitializeDefault` to reset.

## Digital time: TTMSFNCDigitalTimeSelector / TTMSFNCDigitalTimePicker

Pages of time slots from `StartTime` to `EndTime` every `TimeInterval` `IntervalUnit`, laid out in `Rows` x `Columns` (default 4 x 3) with header arrows to page.

```delphi
property StartTime, EndTime: TTime;
property TimeInterval: Integer default 5;
property IntervalUnit: TTMSFNCDigitalTimeSelectorIntervalUnit default tsuMinutes;   // tsuMilliseconds, tsuSeconds, tsuMinutes, tsuHours
property TimeFormat: string;  property HeaderSize: Integer default 24;  property Rows, Columns;
property SelectedTime: TTime;     // public on the selector, published on the picker
OnTimeSelected / OnTimeDeselected: procedure(Sender: TObject; ATime: TTime) of object;
// selector only: procedure NavigateBack; procedure NavigateForth; procedure InitializePage(ATime: TTime);
//                function FindItemByTime(ATime: TTime): Integer; function FindTimeByItem(AItem: Integer): TTime; OnNavigation
// picker only:   CloseOnSelection (True), Editable, DropDownWidth/Height, property TimeSelector: TTMSFNCDigitalTimeSelector (public)
```
Demo `Pickers`:
```delphi
TMSFNCDigitalTimePicker1.StartTime := StrToTime('08:00:00');
TMSFNCDigitalTimePicker1.EndTime := StrToTime('16:30:00');
TMSFNCDigitalTimePicker1.TimeFormat := 'hh:nn';
TMSFNCDigitalTimeSelector1.TimeInterval := 15;

procedure TForm1.TMSFNCDigitalTimePicker1TimeSelected(Sender: TObject; ATime: TTime);
begin
  Label1.Caption := FormatDateTime('hh:nn', ATime);
end;
```

## Platform notes

- Same API on VCL, FMX, WEB, LCL, except `TTMSFNCDateTimePicker.Native`, `DateEdit`, `TimeEdit` (FMX only).
- WEB: calendar month/year popups use `TWebPopupMenu`; `Header.Arrow` bitmaps are not bitmap-container aware on WEB.
- Picker popups are FNC `TTMSFNCPopup`s, so they work identically on all frameworks.

## Does not exist / common mistakes

- `Calendar.SelectedDate := X` — `SelectedDate` is a function on `TTMSFNCCalendar`; use `SelectADate(X)` (replace) or `SelectDate(X)` (add). On `TTMSFNCDatePicker` `SelectedDate` *is* a writable property.
- `Calendar.Date := X` to select — it only navigates; the old selection stays.
- `SelectDate` in a loop to "move" the selection — it accumulates; call `SelectedDates.UnselectAll` or use `SelectADate`.
- `FirstDay := 1` meaning Monday — it uses `DayOfWeek` numbering (1 = Sunday); Monday is 2. Not `StartOfWeek`/`WeekStartDay`/`FirstDayOfWeek`.
- `ShowWeekNumbers`, `ShowToday`, `TodayButton`, `MultiSelect` on the calendar root — use `WeekNumberAppearance.Visible`, `Footer.DateCaption := fdToday`, `Interaction.MultiSelect`.
- `Calendar.Events.Add(Date, 'text')` / `Event.Caption` — `Add` has no parameters; set `Date`, `BadgeValue`, `Hint`.
- `DatePicker.Date`, `DateTime`, `Value`, `Format`/`DateFormat`, `ShowCheckBox`/`Checked`, `Kind` (VCL `TDateTimePicker` habits) — use `SelectedDate` / `SelectedDateTime` / `SelectedTime`; formatting follows `FormatSettings` for dates and `TimeFormat` for time pickers; "no value" = `AllowNumericNullValue` + `0`.
- `DatePicker.OnChange` / `OnCloseUp` — use `OnDateSelected` (date picker), `OnDateTimeChanged` (date-time picker), `OnTimeSelected` (time pickers), `OnTimeChanged` (analog selector).
- `DatePicker.Interaction.MultiSelect` — not published on the picker; use a `TTMSFNCCalendar`.
- `TTMSFNCTimePicker`, `TTMSFNCTimeEdit`, `TTMSFNCDateEdit`, `TTMSFNCMonthCalendar` — do not exist; use the classes above.
- `AnalogTimeSelector.Hour/Minute`, `.SelectedTime` — the selector property is `Time` (plus `AM`); `SelectedTime` is on the pickers and the digital selector.
- `DigitalTimeSelector.Interval`/`Step` — `TimeInterval` + `IntervalUnit`.
