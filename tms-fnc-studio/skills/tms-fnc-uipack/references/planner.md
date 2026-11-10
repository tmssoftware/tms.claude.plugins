# Planner / scheduler (TTMSFNCPlanner, TTMSFNCPlannerDatabaseAdapter, TTMSFNCPlannerItemEditorRecurrency, TTMSFNCRecurrencyHandler, TTMSFNCPlannerToolBarPopup)
> Sections (line ranges): 6-21 Units, palette, platforms · 22-60 Core model: positions, resources, modes · 61-110 Items, resources, groups · 111-149 Example · 150-169 Interaction · 170-194 Key events · 195-198 Appearance · 199-204 Item editing dialog: three customisation levels · 205-231 Recurrency · 232-261 TTMSFNCPlannerDatabaseAdapter · 262-265 TTMSFNCPlannerToolBarPopup · 266-271 Platform notes · 272-285 Does not exist / common mistakes

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCPlanner`, `*.TMSFNCPlannerBase`, `*.TMSFNCPlannerData`, `*.TMSFNCPlannerDatabaseAdapter`, `*.TMSFNCPlannerItemEditorRecurrency`, `*.TMSFNCRecurrencyHandler`, `*.TMSFNCPlannerToolBarPopup`, the `*Reg.pas` units and the demos `Planner`, `Planner Database Adapter and PDFLib`, `Planner TV Guide` (VCL/FMX/WEB).

## Units, palette, platforms

All registered on palette page **`TMS FNC UI`**. Prefix `VCL.` / `FMX.` / `WEBLib.`; Lazarus `LCLTMSFNC...` (no dot).

| Class | Unit |
|---|---|
| `TTMSFNCPlanner` | `VCL.TMSFNCPlanner` + `VCL.TMSFNCPlannerData` (item/resource/group classes) + `VCL.TMSFNCPlannerBase` (`TTMSFNCPlannerCell`, `pomVertical`, ...) |
| `TTMSFNCPlannerDatabaseAdapter` | `VCL.TMSFNCPlannerDatabaseAdapter` (+ `Data.DB` for `TFields` in events) |
| `TTMSFNCPlannerItemEditorRecurrency` | `VCL.TMSFNCPlannerItemEditorRecurrency` |
| `TTMSFNCRecurrencyHandler` (plain `TObject`, not a component) | `VCL.TMSFNCRecurrencyHandler` |
| `TTMSFNCPlannerToolBarPopup` | `VCL.TMSFNCPlannerToolBarPopup` (needs the rich editor toolbar units) |

Colors/aligns (`gcRed`, `gtaCenter`, `gskNone`) come from `VCL.TMSFNCGraphicsTypes`; `TTMSFNCGraphics` from `VCL.TMSFNCGraphics`. The VCL demo `uses` list: `VCL.TMSFNCPlannerBase, VCL.TMSFNCPlannerData, VCL.TMSFNCPlanner, VCL.TMSFNCGraphics, VCL.TMSFNCGraphicsTypes, VCL.TMSFNCTypes, VCL.TMSFNCUtils`.

WEB: planner, database adapter, recurrency editor and handler are in the WEB package. **`TTMSFNCPlannerToolBarPopup` is not** (no `WEBLib.TMSFNCPlannerToolBarPopup.pas`; it depends on the rich editor, which has no WEB version).

## Core model: positions, resources, modes

`Positions.Count` is the number of **columns**. What a column means depends on `Mode` (`TTMSFNCPlannerMode`, default `pmMultiDay`):

| Mode | A position (column) is | Notes |
|---|---|---|
| `pmDay` | a resource (`Item.Resource` = column index) | one day; TV Guide / DB demo put each resource in a column |
| `pmDayPeriod`, `pmHalfDayPeriod` | resource | period from `ModeSettings.StartTime` to `ModeSettings.EndTime` |
| `pmMultiDay` | a day (`Positions.Count := 7` = week view) | `Item.Resource` ignored for layout |
| `pmMultiResDay` | day x resource; resource = `pos mod Resources.Count` | `Positions.Count` = days * resources. Falls back to `pmDay` when `Resources.Count = 0` |
| `pmMultiDayRes` | resource x day; resource = `pos div numDays` | falls back to `pmMultiDay` when no resources |
| `pmMonth` | resource; rows are the days of the month | `Positions.Format := 'mmmm'` in demo |
| `pmMultiMonth` | a month | |
| `pmCustom` | uses `CustomDateTimes` (list of `TDateTime`) | |

The first visible date is `ModeSettings.StartTime`. Rows come from `TimeLine` (`DisplayUnit` * `DisplayUnitType`, from `DisplayStart` to `DisplayEnd` row index). `OrientationMode: TTMSFNCPlannerOrientationMode` = `pomVertical` (default) / `pomHorizontal` (time runs horizontally, TV Guide demo).

```delphi
// TTMSFNCPlannerModeSettings (planner.ModeSettings)
property StartTime: TDateTime;
property EndTime: TDateTime;
property InActiveDays: TTMSFNCPlannerInActiveDays default [padSaturday, padSunday];  // padMonday..padSunday
property OverlappableItems: Boolean default True;

// TTMSFNCPlannerTimeLine (planner.TimeLine)
property DisplayUnit: Integer default 30;                                      // minutes per row with pduMinute
property DisplayUnitType: TTMSFNCPlannerDisplayUnitType default pduMinute;    // pduMilliSecond, pduSecond, pduMinute, pduHour, pduDay
property DisplayStart: Integer default 0;   property DisplayEnd: Integer default 47;   // ROW indexes, not hours
property ActiveStart: Integer default 16;   property ActiveEnd: Integer default 40;    // non-greyed rows
property DisplayUnitFormat: String;  property DisplaySubUnitFormat: String;
property DisplayUnitSize: Double;                   // row height
property ViewStart: TDateTime;                      // scroll position
property CurrentTimeMode: TTMSFNCPlannerCurrentTimeMode default pctmLine;   // pctmNone, pctmLine, pctmText
property CurrentTimePosition: TTMSFNCPlannerCurrentTimePosition default pctpUnderItems;  // pctpOverItems

// TTMSFNCPlannerPositions (planner.Positions)
property Count: Integer default 3;   property Format: String;   property ViewStart: Integer default 0;
```

## Items, resources, groups (unit `*.TMSFNCPlannerData`)

```delphi
// TTMSFNCPlannerItem = class(TCollectionItem) — published (selection)
property Title: String;  property Text: String;          // both support FNC mini-HTML
property StartTime: TDateTime;  property EndTime: TDateTime;
property Resource: Integer default 0;                     // INDEX (position/resource), not a name
property FullDay: Boolean default False;
property Visible, Enabled, Editable, Selectable, Deletable, Movable, Sizeable, ShowTitle: Boolean;  // default True
property FixedResource: Boolean default False;  property Overlappable: Boolean default True;
property Color, TitleColor, FontColor, TitleFontColor, StrokeColor: TTMSFNCGraphicsColor;
property ActiveColor, SelectedColor, DisabledColor: TTMSFNCGraphicsColor;  // + ...Title/Font variants
property UseDefaultAppearance: Boolean default False;
property MarkType: TTMSFNCPlannerItemMarkTypes;  property MarkColor: TTMSFNCGraphicsColor;  // imtLeft, imtTop, imtRight, imtBottom
property Hint: String;  property Tag: NativeInt;  property Rounding: Integer;
// public
property DBKey: String;  property Recurrency: string;  property Recurrent: Boolean;
property DataPointer: Pointer; DataBoolean: Boolean; DataObject: TObject; DataString: String; DataInteger: NativeInt;
property LinkedItem: TTMSFNCPlannerItem;  property LinkType: TTMSFNCPlannerItemLinkType default iltNone;
procedure BeginUpdate;  procedure EndUpdate(ADirty: Boolean = True; AUpdate: Boolean = True);

// TTMSFNCPlannerItems: function Add: TTMSFNCPlannerItem; function Insert(Index: Integer); procedure Clear; Items[Index] default
// TTMSFNCPlannerResource: Name, Text, Hint, Tag, DBKey, Data*        Resources.Add
// TTMSFNCPlannerGroup:    Name, Text, StartPosition, EndPosition      Groups.Add (header spanning positions)
```

Planner helpers (public on `TTMSFNCCustomPlanner`):
```delphi
function AddItem(AStartTime, AEndTime: TDateTime): TTMSFNCPlannerItem;
function AddOrUpdateItem(AStartTime, AEndTime: TDateTime; ATitle: String; AText: String; AItemIndex: Integer = -1): TTMSFNCPlannerItem; overload;  // resource 0
function AddOrUpdateItem(AResource: Integer; AStartTime, AEndTime: TDateTime; ATitle: String = ''; AText: String = ''; AItemIndex: Integer = -1): TTMSFNCPlannerItem; overload;
function AddOrUpdateItem(AResourceName: String; AStartTime, AEndTime: TDateTime; ATitle: String = ''; AText: String = ''; AItemIndex: Integer = -1): TTMSFNCPlannerItem; overload;
function AddItemAtSelection: TTMSFNCPlannerItem;
function FindResourceByName(AName: String): TTMSFNCPlannerResource;  function FindResourceIndexByName(AName: String): Integer;
function FindItemWithDBKey(ADBKey: String): TTMSFNCPlannerItem;
function FindFirstItem(AStartTime, AEndTime: TDateTime; APosition: Integer): TTMSFNCPlannerItem;
function HasItem(AStartTime, AEndTime: TDateTime; APosition: Integer; ACompareWithItemIndex: Integer = -1; ACheckOverlap: Boolean = True): Boolean;
function XYToItem(X, Y: Double): TTMSFNCPlannerItem;   function XYToCell(X, Y: Double): TTMSFNCPlannerCell;   function XYToTime(X, Y: Double): TTMSFNCPlannerTime;
function PositionToDateTime(APosition: Integer): TDateTime;  function PositionToResource(APosition: Integer): Integer;  function ResourceToPosition(AResource: Integer): Integer;
function DisplayStartDateTime: TDateTime;  function DisplayEndDateTime: TDateTime;
function SelectedStartDateTime: TDateTime; function SelectedEndDateTime: TDateTime; function SelectedResource: Integer;
procedure SelectItem(AItem: TTMSFNCPlannerItem); overload;  procedure SelectItem(AItemIndex: Integer); overload;
procedure UnselectAllItems;  procedure EditItem(AItem: TTMSFNCPlannerItem); overload;  procedure StopEditing;  procedure CancelEditing;
procedure NavigateToNextDateTime(ADateTime: TDateTime = -1);  procedure NavigateToPreviousDateTime(ADateTime: TDateTime = -1);
procedure LinkItems(AItems: TTMSFNCPlannerLinkedItemArray; ACircular: Boolean = False; ALinkType: TTMSFNCPlannerItemLinkType = iltNone);
property ActiveItem: TTMSFNCPlannerItem;  property SelectedItems: TTMSFNCPlannerSelectedItems;  property HoverItem: TTMSFNCPlannerItem;
property DefaultItem: TTMSFNCPlannerItem;   // template for new items (colors etc.)
```
Wrap bulk changes in `Planner.BeginUpdate; ... Planner.EndUpdate;`. To delete an item: `Planner.Items.Delete(AItem.Index)` (what the planner itself does) or `AItem.Free`.

## Example (demo `Planner`, trimmed) — week view

```delphi
uses VCL.TMSFNCPlannerBase, VCL.TMSFNCPlannerData, VCL.TMSFNCPlanner, VCL.TMSFNCGraphicsTypes, DateUtils;

procedure TForm1.FormCreate(Sender: TObject);
var
  P: TTMSFNCPlanner;
  it: TTMSFNCPlannerItem;
  dt: TDateTime;
begin
  P := TTMSFNCPlanner.Create(Self);
  P.Parent := Self;
  P.Align := alClient;
  dt := Int(Now);
  P.BeginUpdate;
  try
    P.Mode := pmMultiDay;
    P.Positions.Count := 7;
    P.Positions.Format := 'dddd d';
    P.ModeSettings.StartTime := StartOfTheWeek(dt);
    P.TimeLine.DisplayUnit := 30;                       // 30-minute rows
    P.Interaction.MouseInsertMode := pmimDialogAfterSelection;
    P.Interaction.KeyboardInsertMode := pkimSelection;
    P.Interaction.UpdateMode := pumDialog;
    P.Items.Clear;
    it := P.AddOrUpdateItem(dt + EncodeTime(9, 30, 0, 0), dt + EncodeTime(12, 0, 0, 0),
      'Meeting with John', '<u>Bring</u><ul><li>Notebook</ul>');
    it.Color := MakeGraphicsColor(255, 246, 210);
    it.TitleColor := MakeGraphicsColor(255, 211, 39);
  finally
    P.EndUpdate;
  end;
  P.TimeLine.ViewStart := dt + EncodeTime(8, 0, 0, 0);   // scroll after EndUpdate (demo does this)
end;
```

Resource view (demo `Planner Database Adapter and PDFLib`): `Mode := pmDay; Resources.Clear;` add `Resources.Add` with `Name`/`Text` (HTML, `<img src="name">` from a `BitmapContainer`), then `Positions.Count := Resources.Count`. Multi-day timeline in `pmDay`: `TimeLine.DisplayUnit := 240; TimeLine.DisplayEnd := Round((MinsPerDay * 7) / TimeLine.DisplayUnit) - 1;`. For `pmMultiResDay` set `Positions.Count := Days * Resources.Count`.

## Interaction (planner.Interaction: TTMSFNCPlannerInteraction)

```delphi
property ReadOnly: Boolean default False;
property MouseInsertMode: TTMSFNCPlannerMouseInsertMode default pmimNone;          // pmimNone, pmimAfterSelection, pmimDialogAfterSelection
property KeyboardInsertMode: TTMSFNCPlannerKeyboardInsertMode default pkimNone;    // pkimNone, pkimSelection, pkimSelectionDialog
property UpdateMode: TTMSFNCPlannerUpdateMode default pumInplace;                  // pumNone, pumInplace, pumDialog
property MouseEditMode: TTMSFNCPlannerMouseEditMode default pmemSingleClickOnSelectedItem;  // pmemDoubleClick, pmemSingleClick
property InplaceEditorMode: TTMSFNCPlannerInplaceEditorMode default piemText;      // piemTitle, piemItem
property KeyboardDelete: Boolean default False;  property KeyboardEdit: Boolean default True;
property MoveMode: TTMSFNCPlannerMoveMode default pmmAuto;      // pmmDesktop, pmmMobile, pmmAuto
property SizeMode: TTMSFNCPlannerSizeMode default psmAuto;      // psmDesktop, psmMobile, psmAuto
property DeleteMode: TTMSFNCPlannerDeleteMode default pdmAuto;  // pdmDesktop, pdmMobile, pdmAuto
property MultiSelect: Boolean default False;  property KeepSelection, ShowSelection, TouchScrolling: Boolean;  // True
property TopNavigationButtons, BottomNavigationButtons: TTMSFNCPlannerNavigationButtons default [];  // [pnbPrevious, pnbNext]
property SwipeToNextDateTime, SwipeToPreviousDateTime: Boolean default True;
property AutoSelectLinkedItems, AutoDeleteLinkedItems: Boolean default False;
```
There is no global "allow move/size" flag: disable per item (`Item.Movable`, `Item.Sizeable`, `Item.Editable`, `Item.Deletable`) or veto in `OnBeforeMoveItem` / `OnBeforeSizeItem` (`ACanMove`/`ACanSize := False`). The move/size grips are `ItemsAppearance.ShowMoveArea`/`ShowSizeArea`; `ShowDeleteArea` (default False) shows a delete button.

## Key events (exact signatures)

```delphi
OnBeforeInsertItem: procedure(Sender: TObject; AStartTime, AEndTime: TDateTime; APosition: Integer; var ATitle: String; var AText: String; var ACanInsert: Boolean) of object;
OnAfterInsertItem:  procedure(Sender: TObject; AStartTime, AEndTime: TDateTime; APosition: Integer; AItem: TTMSFNCPlannerItem) of object;
OnBeforeUpdateItem: procedure(Sender: TObject; AStartTime, AEndTime: TDateTime; APosition: Integer; AItem: TTMSFNCPlannerItem; var ATitle: String; var AText: String; var ACanUpdate: Boolean) of object;
OnAfterUpdateItem:  procedure(Sender: TObject; AStartTime, AEndTime: TDateTime; APosition: Integer; AItem: TTMSFNCPlannerItem) of object;
OnBeforeDeleteItem: procedure(Sender: TObject; AItem: TTMSFNCPlannerItem; AMode: TTMSFNCPlannerItemDeleteMode; var ACanDelete: Boolean) of object;
OnAfterDeleteItem:  procedure(Sender: TObject; AItemIndex: Integer; ADBKey: String; AMode: TTMSFNCPlannerItemDeleteMode) of object;   // item already gone
OnBeforeMoveItem:   procedure(Sender: TObject; AItem: TTMSFNCPlannerItem; var ANewStartTime: TDateTime; var ANewEndTime: TDateTime; var ANewPosition: Integer; var ACanMove: Boolean) of object;
OnAfterMoveItem / OnAfterSizeItem: procedure(Sender: TObject; AItem: TTMSFNCPlannerItem; ANewStartTime, ANewEndTime: TDateTime; ANewPosition: Integer) of object;
OnBeforeSizeItem:   same as OnBeforeMoveItem with var ACanSize
OnItemClick / OnItemDblClick / OnItemRightClick: procedure(Sender: TObject; AItem: TTMSFNCPlannerItem) of object;
OnItemAnchorClick:  procedure(Sender: TObject; AItem: TTMSFNCPlannerItem; AAnchor: String) of object;
OnSelectTime:       procedure(Sender: TObject; AStartTime, AEndTime: TDateTime; APosition: Integer) of object;
OnGetItemText:      procedure(Sender: TObject; AItem: TTMSFNCPlannerItem; AMode: TTMSFNCPlannerGetTextMode; var AText: String) of object;   // pgtmDrawing, pgtmEditing
OnGetItemTitleText: procedure(Sender: TObject; AItem: TTMSFNCPlannerItem; AMode: TTMSFNCPlannerGetTextMode; var ATitle: String) of object;
OnIsDateTimeDisabled: procedure(Sender: TObject; ADateTime: TDateTime; APosition: Integer; var ADisabled: Boolean) of object;
OnAfterNavigateToDateTime: procedure(Sender: TObject; ADirection: TTMSFNCPlannerNavigationDirection; ACurrentDateTime: TDateTime; ANewDateTime: TDateTime) of object;
OnBeforeDrawItem: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; AItem: TTMSFNCPlannerItem; var AAllow: Boolean; var ADefaultDraw: Boolean) of object;
OnBeforeDrawPositionText: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; APosition: Integer; AKind: TTMSFNCPlannerCacheItemKind; AText: String; var AAllow: Boolean) of object;
OnBeforeDrawTimeText: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; AValue: Double; ARow: Integer; ASubUnit: Boolean; AKind: TTMSFNCPlannerCacheItemKind; AText: String; var AAllow: Boolean) of object;
```
Also: `OnItemChanged`, `OnBeforeSelectItem`/`OnAfterSelectItem`, `OnBeforeOpenInsertDialog`/`OnBeforeOpenUpdateDialog` (`var ACanOpen`), `OnCloseInsertDialog`/`OnCloseUpdateDialog`, `OnGetInplaceEditor`, `OnBeforeDrawCell`, `OnGetPositionText`, `OnItemPopupMenuPrepare`.

## Appearance

Sub-objects: `ItemsAppearance` (Fill/Stroke/Font, TitleFill/TitleFont, Selected*/Active*/Disabled* variants, `MoveAreaColor`, `SizeAreaColor`, `ShowLinks`, `WordWrap`), `GridCellAppearance` (`Fill`, `InActiveFill`, `DisabledFill`, `VerticalStroke`, `HorizontalStroke`, `HorizontalSubStroke`), `TimeLineAppearance` (`Layouts` [ptlLeft, ptlRight], `LeftSize`, `LeftFont`, `LeftSubUnitFontSize`, `CurrentTimeColor`), `PositionsAppearance` (`Layouts` [pplTop, pplBottom], `TopSize`, `TopFont`, `TopFill`, `Stretch`, `Size`), `GroupsAppearance` (`Layouts` [pglTop, pglBottom]), `FullDaysAppearance` (`Layouts` [pfdlTop, pfdlBottom], `AutoSize`), `SelectionAppearance`, plus `Fill`, `Stroke`, `GlobalFont`, `BitmapContainer` (for `<img src>` in HTML).

## Item editing dialog: three customisation levels

1. **Built-in dialog** — `Interaction.UpdateMode := pumDialog` and/or `MouseInsertMode := pmimDialogAfterSelection`. Open in code: `OpenEditingDialog(AStartTime, AEndTime: TDateTime; AResource: Integer; ATitle, AText: String; AUpdateItem: Integer = -1; ACustomParent = nil)`; close with `CloseEditingDialog(ACancel: Boolean)`.
2. **Custom content panel** inside the built-in dialog: assign `Planner.ItemEditor` (a `TTMSFNCPlannerCustomItemEditor` descendant, e.g. `TTMSFNCPlannerItemEditorRecurrency`), or handle `OnGetCustomContentPanel` / `OnInitializeCustomContentPanel` / `OnItemToCustomContentPanel` / `OnCustomContentPanelToItem` (`AContentPanel: TTMSFNCPlannerEditingDialogContentPanel` = `TControl` on FMX, `TWinControl` on VCL/WEB). Descendants override `CreateInstance`, `CreateCustomContentPanel`, `InitializeCustomContentPanel`, `GetCustomContentPanel`, `ItemToCustomContentPanel`, `CustomContentPanelToItem`.
3. **Own form**: `Planner.CustomItemEditorForm := TMyEditorForm;` (a **class**, `TTMSFNCPlannerCustomItemEditorFormClass`). Inherit from `TTMSFNCPlannerCustomItemEditorForm` (`TForm`; `TWebForm` on WEB), override `procedure Initialize; override;` (abstract) to load `PlannerTitle`, `PlannerText`, `PlannerStartTime`, `PlannerEndTime`, `PlannerResource`, `PlannerFullDay` (also `PlannerItem`, `PlannerMode` = `pemInsert`/`pemUpdate`, `Planner`). The planner shows it with `ShowModal`; in your OK/Cancel buttons write the `Planner*` properties back and call `Planner.CloseEditingDialog(False)` / `(True)` — the planner reads the values in `CloseEditingDialog`.

## Recurrency

**The planner itself never expands `Item.Recurrency`.** Expansion into occurrences happens only in `TTMSFNCPlannerDatabaseAdapter` (it runs a `TTMSFNCRecurrencyHandler` per record). `TTMSFNCPlannerItemEditorRecurrency` only edits the RRULE string (`Item.Recurrency`) in the dialog: `Planner.ItemEditor := TMSFNCPlannerItemEditorRecurrency1;`.

Rule format is iCal RRULE text, e.g. `'RRULE:FREQ=WEEKLY;BYDAY=TU,TH'`, `'RRULE:FREQ=WEEKLY'` (demo data). Without the adapter, expand manually:

```delphi
uses VCL.TMSFNCRecurrencyHandler;
var h: TTMSFNCRecurrencyHandler; s, e: TDateTime;
begin
  h := TTMSFNCRecurrencyHandler.Create;
  try
    h.Recurrency := 'RRULE:FREQ=DAILY;COUNT=5';
    h.StartTime := Int(Now) + EncodeTime(9, 0, 0, 0);
    h.EndTime := Int(Now) + EncodeTime(10, 0, 0, 0);
    h.Generate;
    Planner.BeginUpdate;
    while h.NextDate(s, e) do
      Planner.AddOrUpdateItem(s, e, 'Stand-up', '').Recurrency := h.Recurrency;
    Planner.EndUpdate;
  finally
    h.Free;
  end;
end;
```
Handler members: `Parse`, `Generate`, `Compose: string`, `IsRecurrent`, `NextDate(var AStartDate, AEndDate: TDateTime): Boolean`, `RecurrentMinDate`, `RecurrentMaxDate`, `Frequency: TTMSFNCRecurrencyFrequency` (`rfHourly, rfDaily, rfWeekly, rfMonthly, rfYearly, rfNone`), `Interval`, `RepeatCount`, `RepeatUntil`, `Days`, `ExDates`, `Dates`, `TimeSpan` (upper bound when no COUNT/UNTIL; 0 = many years).

## TTMSFNCPlannerDatabaseAdapter (demo `Planner Database Adapter and PDFLib`)

Field mapping is by **field name strings** on `Adapter.Item` (`TTMSFNCPlannerDatabaseAdapterItemSource`): `DataSource`, `DBKey`, `StartTime`, `EndTime`, `Title`, `Text`, `Resource`, `Recurrency`, `AutoIncrementDBKey: Boolean default True`. `DBKey`, `StartTime`, `EndTime` are required. `Resource` field is read with `AsInteger` (a resource index).

```delphi
TMSFNCPlanner1.Adapter := TMSFNCPlannerDatabaseAdapter1;
TMSFNCPlanner1.ItemEditor := TMSFNCPlannerItemEditorRecurrency1;   // optional
with TMSFNCPlannerDatabaseAdapter1.Item do
begin
  AutoIncrementDBKey := False;        // we generate GUID keys ourselves
  DataSource := DataSource1;
  DBKey := 'Id'; StartTime := 'StartTime'; EndTime := 'EndTime';
  Title := 'Title'; Text := 'Text'; Resource := 'Resource'; Recurrency := 'Recurrency';
end;
TMSFNCPlannerDatabaseAdapter1.Active := True;   // Active is on the adapter (inherited TTMSFNCPlannerAdapter)

// load the new period after navigation (adapter only loads DisplayStartDateTime..DisplayEndDateTime)
procedure TForm3.TMSFNCPlanner1AfterNavigateToDateTime(Sender: TObject; ADirection: TTMSFNCPlannerNavigationDirection; ACurrentDateTime, ANewDateTime: TDateTime);
begin
  TMSFNCPlannerDatabaseAdapter1.LoadItems;
end;

// extra columns
procedure TForm3.TMSFNCPlannerDatabaseAdapter1FieldsToItem(Sender: TObject; AFields: TFields; AItem: TTMSFNCPlannerItem);
begin
  AItem.Color := AFields.FieldByName('Color').AsLongWord;
end;
```
Events: `OnFieldsToItem`, `OnItemToFields(Sender; AItem; AFields: TFields)`, `OnFieldsToResource(Sender; AFields: TFields; AColumnField: TField; var AResource: Integer; var AAcceptItem: Boolean)`, `OnResourceToFields`, `OnItemCreateDBKey(Sender; AItem; var ADBKey: string)`, `OnItemInserted`, `OnItemUpdated`, `OnItemRead`, `OnItemsLoaded`, `OnItemLocate`. Methods: `LoadItems`, `GetItems(PeriodFrom, PeriodTo: TDateTime)`.

## TTMSFNCPlannerToolBarPopup (VCL/FMX/LCL)

Drop it and set `Planner.ToolBarPopup := TMSFNCPlannerToolBarPopup1;`. When the user clicks the already-active (non full-day) item, the planner sets the popup's `Planner`/`PlannerItem` and shows a rich-editor format toolbar above the item (bold/italic/underline/strikeout, alignment, font name/size, text and background color applied to the item). `Options: TTMSFNCRichEditorFormatToolBarOptions` default `AllPlannerFormatOptions`.

## Platform notes

- Same API on VCL, FMX, WEB, LCL. `TTMSFNCPlannerCustomItemEditorForm` derives from `TWebForm` on WEB (created with `CreateNew` and shown as popup).
- WEB DB adapter demo uses `TWebClientDataSet` with `Data.DB, WEBLib.DB, WEBLib.CDS`.
- `TTMSFNCPlannerToolBarPopup`: not on WEB.

## Does not exist / common mistakes

- `pmWeek`, `pmWorkWeek`, `pmTimeline`, `pmMonthView`, `pmAgenda` — week = `pmMultiDay` + `Positions.Count := 7` and `ModeSettings.StartTime := StartOfTheWeek(...)` (work week: `Positions.Count := 5` starting Monday; `ModeSettings.InActiveDays` only greys days via `IsDateTimeInActive`, it does not hide them); horizontal timeline = `OrientationMode := pomHorizontal`. Full list: `pmDay, pmDayPeriod, pmHalfDayPeriod, pmMultiDay, pmMultiResDay, pmMultiDayRes, pmMonth, pmMultiMonth, pmCustom`.
- `Planner.Date`, `GoToDate`, `Display.StartDate`, `Day` (TAdvPlanner/TPlanner) — use `ModeSettings.StartTime` and `TimeLine.ViewStart`; navigate with `NavigateToNextDateTime` / `NavigateToPreviousDateTime`.
- `Items.Add(Start, End, ...)` with parameters — `Items.Add` takes none; use `AddItem(AStart, AEnd)` or `AddOrUpdateItem(...)`.
- `Item.ItemStartTime`/`ItemEndTime`/`Start`/`Finish`, `Item.Caption`/`Subject`/`Notes`/`Location`, `Item.AllDay`, `Item.ResourceName` — use `StartTime`, `EndTime`, `Title`, `Text`, `FullDay`, `Resource` (Integer index; resolve names with `FindResourceIndexByName` or the `AddOrUpdateItem(AResourceName, ...)` overload).
- `Planner.SelectedItem` — use `ActiveItem` or `SelectedItems[i]`. `DeleteItem`/`RemoveItem` on the planner — use `Items.Delete(AItem.Index)`.
- `Interaction.AllowMove` / `AllowSize` / `AllowInsert` — per-item `Movable`/`Sizeable`, insert via `MouseInsertMode`/`KeyboardInsertMode`, global lock `Interaction.ReadOnly`.
- `TimeLine.DisplayStart := 8` meaning 8:00 — it is a **row index**; with 30-minute rows 8:00 is row 16 (= default `ActiveStart`).
- Expecting `Item.Recurrency := 'RRULE:...'` to repeat the item in a non-DB planner — nothing happens; expand with `TTMSFNCRecurrencyHandler` or use the DB adapter.
- `Adapter.Item.Location`/`Color`/`AllDay` field mappings — not available; map extra fields in `OnFieldsToItem`/`OnItemToFields`.
- `CustomItemEditorForm := TMyForm.Create(...)` — the property takes the **class**, not an instance.
- `TTMSFNCPlannerItemEditor` is a design-time helper form, not the runtime editor component; the runtime ones are `TTMSFNCPlannerItemEditorRecurrency` or your `TTMSFNCPlannerCustomItemEditor` descendant.
