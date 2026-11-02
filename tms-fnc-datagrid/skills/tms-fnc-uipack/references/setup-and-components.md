# TMS FNC UI Pack: component catalog and shared conventions (all UI Pack controls)

Verified against: `tms.fnc.uipack` 7.3.1.2 (`version.txt`), every `*Reg.pas` unit in `Source`, the packages `Packages\d13\VCLTMSFNCUIPackPkg.dpk`, `FMXTMSFNCUIPackPkg.dpk`, `Packages\web\TMSFNCUIPackWEB.dpk`, `Packages\lazarus\LCLTMSFNCUIPackPkg.lpk`, and `tms.fnc.core` 4.5.0.0 (`VCL.TMSFNCCustomControl`, `VCL.TMSFNCCustomComponent`, `VCL.TMSFNCBitmapContainer`, `VCL.TMSFNCHTMLEngine`).

## Install, packages, unit prefixes

This is already covered in `skills\tms-fnc-datagrid\references\setup-and-install.md`. It applies unchanged to every UI Pack component:
- Smart Setup id `tms.fnc.uipack`, which depends on `tms.fnc.core`. Install with `tms install tms.fnc.uipack`.
- Packages: `VCLTMSFNCUIPackPkg`, `FMXTMSFNCUIPackPkg`, `TMSFNCUIPackPkgDE` (design time), `Packages\web\TMSFNCUIPackWEB`, and `Packages\lazarus\LCLTMSFNCUIPackPkg.lpk`.
- Unit prefixes are `VCL.`, `FMX.` and `WEBLib.`. Lazarus units have **no dot**: `LCLTMSFNCPanel`, not `LCL.TMSFNCPanel`. Never mix VCL and FMX units in one unit.
- The command-line `.dproj` / msbuild notes in that file also apply.

Every UI Pack component (and the FNC Core visual components such as `TTMSFNCBitmapContainer`, `TTMSFNCPopupMenu`, `TTMSFNCStylesManager`) registers on the IDE palette page **`TMS FNC UI`**. The only exception is FNC Core's `TTMSFNCDataBinder`, which is on `TMS FNC DB`.

## Component catalog

Columns: class, unit (shown without prefix, so add `VCL.` / `FMX.` / `WEBLib.`, or `LCL` with no dot), Reg unit, and platforms. Platforms are **V**CL, **F**MX, **W**EB and **L**azarus, taken from which package actually contains the Reg unit. A `WEBLib.*` source file can exist without being in the WEB package; when it isn't, you can't drop the component on a WEB form. "desk" means the class has `ComponentPlatformsAttribute(TMSPlatformsDesktop / TMSPlatformsWebDesktop)`, so on FMX it targets Windows/macOS/Linux only, not iOS or Android.

### Editors, buttons, pickers

| Class | Unit | Reg | Platforms | Purpose |
|---|---|---|---|---|
| `TTMSFNCButton` | `TMSFNCButton` | ButtonReg | VFWL | Button. **It wraps the native `TCustomButton`/`TWebButton`, not a FNC-drawn control** |
| `TTMSFNCEdit` | `TMSFNCEdit` | EditReg | VFWL | Edit with input types and autocomplete. **Native `TCustomEdit` descendant** |
| `TTMSFNCEditButton` | `TMSFNCEdit` | EditReg | VFWL | Edit plus a drop-down button that shows a popup |
| `TTMSFNCLabelEdit` | `TMSFNCLabelEdit` | LabelEditReg | VFWL | Label that is edited in place by clicking it |
| `TTMSFNCIPEdit` | `TMSFNCIPEdit` | IPEditReg | VFWL | IPv4 / IPv6 / MAC address edit |
| `TTMSFNCSpinEdit` | `TMSFNCSpinEdit` | SpinEditReg | VFWL | Numeric spin edit |
| `TTMSFNCSearchEdit` | `TMSFNCSearchEdit` | SearchEditReg | VFL | Edit with a category button and a filtered drop-down list |
| `TTMSFNCSearchList` | `TMSFNCSearchList` | SearchListReg | VFL | Searchable, filterable multi-column list |
| `TTMSFNCDirectoryEdit` | `TMSFNCDirectoryEdit` | DirectoryEditReg | VF, desk | Folder picker edit |
| `TTMSFNCCheckBox`, `TTMSFNCRadioButton` | `TMSFNCCheckBox`, `TMSFNCRadioButton` | own Reg | VFWL | Check box / radio button with HTML text |
| `TTMSFNCCheckGroup`, `TTMSFNCRadioGroup` | `TMSFNCCheckGroup`, `TMSFNCRadioGroup` | own Reg | VFWL | Groups of check boxes / radio buttons |
| `TTMSFNCCheckGroupPicker`, `TTMSFNCRadioGroupPicker` | same names | own Reg | VFWL | Those groups in a drop-down |
| `TTMSFNCSwitch` | `TMSFNCSwitch` | SwitchReg | VFWL | Toggle switch |
| `TTMSFNCTrackBar`, `TTMSFNCRangeSlider` | `TMSFNCTrackBar`, `TMSFNCRangeSlider` | own Reg | VFWL | Slider; two-thumb range slider |
| `TTMSFNCComboBox` | `TMSFNCComboBox` | ComboBoxReg | VFWL | FNC-drawn combo box |
| `TTMSFNCControlPicker` | `TMSFNCControlPicker` | ControlPickerReg | VFWL | Picker that shows any other control in its drop-down |
| `TTMSFNCColorPicker` / `TTMSFNCColorSelector` / `TTMSFNCColorWheel` | same names | own Reg | VFWL | Color drop-down / color grid / color wheel |
| `TTMSFNCBitmapPicker` / `TTMSFNCBitmapSelector` | same names | own Reg | VFWL | Image drop-down / image grid |
| `TTMSFNCFontNamePicker` / `TTMSFNCFontSizePicker` | same names | own Reg | VFWL | Font name / size drop-downs |
| `TTMSFNCFillKindPicker` / `TTMSFNCFillKindSelector` | `TMSFNCFillKindPicker` / `...Selector` | FillKindReg | VFWL | Choose a `TTMSFNCGraphicsFillKind` |
| `TTMSFNCStrokeKindPicker` / `TTMSFNCStrokeKindSelector` | `TMSFNCStrokeKindPicker` / `...Selector` | StrokeKindReg | VFWL | Choose a stroke kind |
| `TTMSFNCDateTimePicker` | `TMSFNCDateTimePicker` | DateTimePickerReg | VFWL | Combined date and time picker |
| `TTMSFNCCalendar` / `TTMSFNCDatePicker` | `TMSFNCCalendar` / `TMSFNCDatePicker` | CalendarReg | VFWL | Month calendar / drop-down date picker |
| `TTMSFNCAnalogTimeSelector` / `TTMSFNCAnalogTimePicker` | `TMSFNCAnalogTimeSelector` / `...Picker` | AnalogTimeReg | VFWL | Clock-face time selection |
| `TTMSFNCDigitalTimeSelector` / `TTMSFNCDigitalTimePicker` | `TMSFNCDigitalTimeSelector` / `...Picker` | DigitalTimeReg | VFWL | Time-slot grid / drop-down |
| `TTMSFNCSpinner` | `TMSFNCSpinner` | SpinnerReg | VFW | Wheel-style spinner columns (numbers, dates, custom items) |
| `TTMSFNCPassLock` | `TMSFNCPassLock` | PassLockReg | VFWL | PIN / pattern lock |
| `TTMSFNCListEditor` | `TMSFNCListEditor` | ListEditorReg | VFWL | Editable "chip"/tag list |
| `TTMSFNCSignatureCapture` | `TMSFNCSignatureCapture` | SignatureCaptureReg | VFWL | Signature drawing pad |
| `TTMSFNCTouchKeyboard` / `TTMSFNCPopupTouchKeyboard` | `TMSFNCTouchKeyboard` | TouchKeyboardReg | VFW, desk | On-screen keyboard |

### Display, lists, data

| Class | Unit | Reg | Platforms | Purpose |
|---|---|---|---|---|
| `TTMSFNCHTMLText` | `TMSFNCHTMLText` | HTMLTextReg | VFWL | Label with HTML formatting, anchors (`OnAnchorClick`) and images |
| `TTMSFNCImage` | `TMSFNCImage` | ImageReg | VFWL | Image (bitmap/SVG) display |
| `TTMSFNCHotSpotImage` | `TMSFNCHotSpotImage` | HotSpotImageReg | VFWL | Image with clickable hot-spot regions |
| `TTMSFNCHotSpotImageEditor` | `TMSFNCHotSpotImageEditor` | HotSpotImageEditorReg | VFWL | Non-visual: dialog for editing hot spots |
| `TTMSFNCHTMLEditor` | `TMSFNCHTMLEditor` | HTMLEditorReg | VFL, desk | Non-visual: modal dialog for editing HTML text (`Execute`, `Text`) |
| `TTMSFNCBadge` | `TMSFNCBadge` | BadgeReg | VFW | Badge overlay anchored on another control |
| `TTMSFNCProgressBar`, `TTMSFNCRating` | `TMSFNCProgressBar` (both) | ProgressBarReg | VFWL | Progress bar; star rating |
| `TTMSFNCWaitingIndicator` | `TMSFNCWaitingIndicator` | WaitingIndicatorReg | VFWL | Animated busy indicator, with optional overlay |
| `TTMSFNCListBox`, `TTMSFNCCheckedListBox` | `TMSFNCListBox`, `TMSFNCCheckedListBox` | ListBoxReg | VFWL | FNC list box (built on the tree view) |
| `TTMSFNCTreeView`, `TTMSFNCCheckedTreeView` | `TMSFNCTreeView`, `TMSFNCCheckedTreeView` | TreeViewReg | VFWL | Multi-column, virtual tree view |
| `TTMSFNCTreeViewDatabaseAdapter` | `TMSFNCTreeViewDatabaseAdapter` | TreeViewDatabaseAdapterReg | **none** | Its Reg unit is in **no** package, so it is not on the palette. Create it in code |
| `TTMSFNCTableView` | `TMSFNCTableView` | TableViewReg | VFWL | iOS-style table view (sections, accessories, swipe) |
| `TTMSFNCTileList` | `TMSFNCTileList` | TileListReg | VFWL | Paged / scrolling tile grid |
| `TTMSFNCResponsiveList` | `TMSFNCResponsiveList` | ResponsiveListReg | VFL | List whose item template changes with available size |
| `TTMSFNCKanbanBoard` (+ `...DatabaseAdapter`) | `TMSFNCKanbanBoard` | KanbanBoard(DatabaseAdapter)Reg | VFWL | Kanban columns and cards |
| `TTMSFNCPlanner` (+ `...DatabaseAdapter`, `TTMSFNCPlannerItemEditorRecurrency`) | `TMSFNCPlanner` | Planner*Reg | VFWL | Scheduler / planner |
| `TTMSFNCPlannerToolBarPopup` | `TMSFNCPlannerToolBarPopup` | PlannerToolBarPopupReg | VFL | Context toolbar popup for the planner |
| `TTMSFNCTimeline` (+ `...DatabaseAdapter`) | `TMSFNCTimeline` | Timeline(DatabaseAdapter)Reg | VFW | Timeline |
| `TTMSFNCDataGrid`, `TTMSFNCDataGridRendererSource` | `TMSFNCDataGrid`, `TMSFNCDataGridRenderer` | DataGridReg | VFW | **The** grid. See the `tms-fnc-datagrid` skill |
| `TTMSFNCDataGridDatabaseAdapter` / `...PDFIO` / `...PrintIO` | `TMSFNCDataGrid*` | own Reg | VFW | DataGrid dataset binding / export |
| `TTMSFNCGrid` (+ `TTMSFNCGridDatabaseAdapter`, `TTMSFNCGridPDFIO`, `TTMSFNCGridPrintIO`) | `TMSFNCGrid`, ... | GridReg, GridIOReg, ... | VFWL | Legacy grid. See spreadgrid-and-legacy-grid.md |
| `TTMSFNCGridToolBarPopup` | `TMSFNCGridToolBarPopup` | GridToolBarPopupReg | VFL | Legacy grid context toolbar |
| `TTMSFNCSpreadGrid`, `TTMSFNCGridBinder`, `TTMSFNC*MathLib` | `TMSFNCSpreadGrid`, `TMSFNCFormulaParser`, `TMSFNCSpreadGridLibs` | SpreadGridReg | VFL | Spreadsheet grid with formulas |
| `TTMSFNCMemo`, `TTMSFNCMemoCustomLanguage`, `TTMSFNCMemoCustomTheme` | `TMSFNCMemo`, ... | MemoReg | VFWL | Code editor (Monaco), hosted in a web browser control |
| `TTMSFNCRichEditor` (+ `HorizontalRuler`, `EditToolBar`/`FormatToolBar`, `ToolBarPopup`, `HTMLIO`/`RTFIO`/`PDFIO`/`PrintIO`) | `TMSFNCRichEditor*` | RichEditor*Reg | VFL | Rich text editor and its IO components |
| `TTMSFNCChat` | `TMSFNCChat` | ChatReg | VFWL | Chat conversation view. See dialogs-and-misc.md |
| `TTMSFNCObjectInspector` | `TMSFNCObjectInspector` | ObjectInspectorReg | VFWL | Property inspector (a `TTMSFNCTreeView` descendant) |
| `TTMSFNCFilterView` | `TMSFNCFilterView` | FilterViewReg | VFW | Visual filter builder |

### Containers, navigation, dialogs

See containers-and-navigation.md and dialogs-and-misc.md for their APIs.

| Class | Unit | Platforms | Purpose |
|---|---|---|---|
| `TTMSFNCPanel` | `TMSFNCPanel` | VFWL | Panel with header/footer, collapse, compact mode |
| `TTMSFNCPageControl` / `TTMSFNCTabSet` | `TMSFNCPageControl` / `TMSFNCTabSet` | VFWL | Pages with tabs / tabs only |
| `TTMSFNCNavigationPanel` | `TMSFNCNavigationPanel` | VFWL | Outlook-style navigation panel |
| `TTMSFNCPageSlider` | `TMSFNCPageSlider` | VFW | Sliding pages |
| `TTMSFNCRibbon` | `TMSFNCRibbon` | VFWL | Office-style ribbon |
| `TTMSFNCToolBar`, `TTMSFNCToolBarButton`, `TTMSFNCToolBarSeparator`, `TTMSFNCToolBar{FontName,FontSize,Color,Bitmap,Item}Picker`, `TTMSFNCDockPanel` | `TMSFNCToolBar` | VFWL | Toolbar and its items; dock panel hosts toolbars |
| `TTMSFNCFontToolBar`, `TTMSFNCParagraphToolBar`, `TTMSFNCInsertToolBar`, `TTMSFNCClipboardToolBar`, `TTMSFNCFileIOToolBar` | `TMSFNCToolBars` | VFW | Prebuilt toolbars |
| `TTMSFNCToolBarPopup` | `TMSFNCToolBarPopup` | VFWL | Popup toolbar |
| `TTMSFNCStatusBar` / `TTMSFNCSplitter` | `TMSFNCStatusBar` / `TMSFNCSplitter` | VFWL | Status bar / splitter |
| `TTMSFNCTrayIcon` | `TMSFNCTrayIcon` (VCL/FMX/LCL only) | **no Reg, no package**, desk | Must be created in code; add the unit to the project yourself |
| `TTMSFNCTaskDialog`, `TTMSFNCFontDialog` | same names | VFWL | Task dialog; font dialog |
| `TTMSFNCFindDialog`, `TTMSFNCReplaceDialog` | same names | VFW, desk | Find / replace dialogs |
| `TTMSFNCDataSetFilterDialog` | `TMSFNCFilterDialog` | VF, desk | Dataset filter dialog. Generic `TTMSFNCFilterDialog` is in the same unit but not registered |

## Shared FNC conventions

Most UI Pack controls descend from `TTMSFNCCustomControl` (unit `*.TMSFNCCustomControl`, FNC Core). Non-visual ones (dialogs, `TTMSFNCHTMLEditor`, `TTMSFNCHotSpotImageEditor`, IO components) descend from `TTMSFNCCustomComponent` (`*.TMSFNCCustomComponent`). **Exceptions:** `TTMSFNCButton` and `TTMSFNCEdit` are native control descendants. They have no `Fill`/`Stroke`, no `SaveSettingsToFile` and no `BeginUpdate`. `TTMSFNCMemo` descends from `TTMSFNCCustomWEBControl`, a web browser control, so on Windows VCL/FMX it needs the Edge WebView2 runtime.

Members inherited from `TTMSFNCCustomControl` (copied from `VCL.TMSFNCCustomControl.pas`):

```delphi
procedure BeginUpdate; virtual;
procedure EndUpdate; virtual;
property Fill: TTMSFNCGraphicsFill read FFill write SetFill;          // background
property Stroke: TTMSFNCGraphicsStroke read FStroke write SetStroke;  // border
procedure DisableBackground;   procedure EnableBackground;
procedure DisableFill;         procedure EnableFill;
procedure DisableStroke;       procedure EnableStroke;
property AdaptToStyle: Boolean ... default False;        // FMX style / VCL style adaptation
property Transparent: Boolean ... default False;
property ShowAcceleratorChar: Boolean ... default True;
procedure SaveSettingsToFile(AFileName: string; AAppearanceOnly: Boolean = False); virtual;
procedure LoadSettingsFromFile(AFileName: string); virtual;
procedure SaveSettingsToStream(AStream: TStream; AAppearanceOnly: Boolean = False); virtual;
procedure LoadSettingsFromStream(AStream: TStream); virtual;
function IsDesignTime: Boolean; virtual;
property DataPointer: Pointer;  property DataBoolean: Boolean;  property DataObject: TObject;  // free-use tags
```
`TTMSFNCCustomComponent` has the same `BeginUpdate/EndUpdate`, `AdaptToStyle` and `Save/LoadSettingsToFile/Stream` members. Settings are saved as JSON. Pass `AAppearanceOnly = True` to save only the look, which works like a theme file.

- **Create / Parent / Align**: `X := TTMSFNCxxx.Create(Self); X.Parent := Self;`. Alignment is `alClient` on VCL/WEB and `TAlignLayout.Client` on FMX.
- **BeginUpdate / EndUpdate** around bulk changes (adding items, tabs, nodes, pages). Pair them in `try..finally`.
- **Fill / Stroke** are FNC Core graphics types (`TTMSFNCGraphicsFill.Kind := gfkSolid/gfkGradient/gfkNone`, `.Color`, `.ColorTo`; `TTMSFNCGraphicsStroke.Kind := gskSolid/gskNone`, `.Color`, `.Width`). Colors use `gcXxx` constants from `*.TMSFNCGraphicsTypes`, such as `gcWhite` and `gcSteelBlue`. Many controls have an extra `Appearance`-style class property for item/tab/button states. Its name differs per control, so check the control's reference.
- **GlobalFont** (`TTMSFNCAppearanceGlobalFont`) exists on controls that implement `ITMSFNCAppearanceGlobalFont` (Calendar, Chat, TaskDialog, AnalogTimeSelector, Switch, ...). It sets the font for all elements at once.
- **BitmapContainer**: `TTMSFNCBitmapContainer` (FNC Core, `*.TMSFNCBitmapContainer`, palette `TMS FNC UI`) holds named images. Controls that implement `ITMSFNCBitmapContainer` have `property BitmapContainer: TTMSFNCBitmapContainer` and refer to images **by name**: `BitmapName` on button-like items, or `<img src="name">` in HTML text. Fill it with `AddFromFile(FileName, BitmapName: String)` or `AddFromResource(ResourceName, BitmapName: string)`, and look images up with `FindBitmap(s: string): TTMSFNCBitmap`.
- **HTML-capable text**: Text, captions, items and tabs of most controls go through the FNC Core mini-HTML engine (`*.TMSFNCHTMLEngine`). Supported tags include `<b> <i> <u> <s> <br> <font color="..." size=".." face=".."> <a href="..."> <img src="..."> <ul><li> <sub> <sup>`. Anchors fire control-specific events such as `TTMSFNCHTMLText.OnAnchorClick`. This is not a browser: CSS and tables are not supported.
- **Styles**: `TTMSFNCStylesManager` (FNC Core, `*.TMSFNCStyles`) has `LoadStyleFromFile(AFile: string)` / `LoadStyleFromText(AText: string)` to style all FNC controls on a form.

## Example: building a small UI in code (VCL)

```delphi
uses
  VCL.TMSFNCTypes, VCL.TMSFNCGraphics, VCL.TMSFNCGraphicsTypes, VCL.TMSFNCCustomControl,
  VCL.TMSFNCBitmapContainer, VCL.TMSFNCHTMLText, VCL.TMSFNCButton;

procedure TForm1.FormCreate(Sender: TObject);
var
  bc: TTMSFNCBitmapContainer;
  lbl: TTMSFNCHTMLText;
  btn: TTMSFNCButton;
begin
  bc := TTMSFNCBitmapContainer.Create(Self);
  bc.AddFromFile('save.png', 'save');           // (FileName, BitmapName)

  lbl := TTMSFNCHTMLText.Create(Self);
  lbl.Parent := Self;
  lbl.Align := alTop;                           // FMX: TAlignLayout.Top
  lbl.BitmapContainer := bc;
  lbl.Text := '<img src="save"> Click <a href="go"><b>here</b></a> to save';
  lbl.Fill.Kind := gfkSolid;
  lbl.Fill.Color := gcLightyellow;
  lbl.Stroke.Kind := gskNone;
  lbl.OnAnchorClick := LabelAnchorClick;        // (Sender: TObject; AAnchor: string)

  btn := TTMSFNCButton.Create(Self);            // native button: no Fill/Stroke
  btn.Parent := Self;
  btn.BitmapContainer := bc;
  btn.BitmapName := 'save';
  btn.ShowImage := True;                        // default False
  btn.Text := 'Save';
end;

// persist the look/state of any TTMSFNCCustomControl descendant
TMSFNCPanel1.SaveSettingsToFile('panel.json', True);   // appearance only
TMSFNCPanel1.LoadSettingsFromFile('panel.json');
```

## Platform notes

- VCL, FMX and WEB sources are copies with different prefixes, so class and member names are identical. Differences sit behind `{$IFDEF WEBLIB}` and `{$IFDEF FMXLIB}`. The biggest one is that dialogs are asynchronous on WEB, with result callbacks (see dialogs-and-misc.md).
- **Not in the WEB package:** SearchEdit, SearchList, ResponsiveList, RichEditor (all parts), SpreadGrid, HTMLEditor, DirectoryEdit, DataSetFilterDialog, GridToolBarPopup, PlannerToolBarPopup and TrayIcon. Some of them have an orphan `WEBLib.*Reg.pas` file that no package uses.
- **Not in the Lazarus package:** the DataGrid family, Badge, Spinner, PageSlider, prebuilt ToolBars, Timeline, TouchKeyboard, FilterView, Find/Replace dialogs, DataSetFilterDialog.
- Desktop-only on FMX (`TMSPlatformsDesktop`/`TMSPlatformsWebDesktop`): DirectoryEdit, Find/Replace dialogs, FilterDialog/DataSetFilterDialog, HTMLEditor, TouchKeyboard/PopupTouchKeyboard, TrayIcon.
- `TTMSFNCTreeViewDatabaseAdapter` has a Reg unit, but no package (VCL, FMX, WEB or LCL) includes it. It never appears on the palette.

## Does not exist / common mistakes

| Wrong guess | Correct |
|---|---|
| `TTMSFNCLabel` | `TTMSFNCHTMLText` (unit `*.TMSFNCHTMLText`) |
| `TTMSFNCGroupBox`, `TTMSFNCRadioGroupBox` | `TTMSFNCPanel` (with `Header`), `TTMSFNCCheckGroup`, `TTMSFNCRadioGroup` |
| `TTMSFNCImageList` | `TTMSFNCBitmapContainer` (FNC Core), with images referenced by name |
| `TTMSFNCSpeedButton`, `TTMSFNCToggleSwitch` | `TTMSFNCToolBarButton` / `TTMSFNCButton`, `TTMSFNCSwitch` |
| `TTMSFNCMainMenu` | No FNC main menu. Use `TTMSFNCRibbon` / `TTMSFNCToolBar`, or `TTMSFNCPopupMenu` (FNC Core) for popups |
| `TTMSFNCScrollBox` | No such class. FNC Core has `TTMSFNCScrollBar` only |
| `TTMSFNCStringGrid`, `TTMSFNCDBGrid` | `TTMSFNCDataGrid` (+ `TTMSFNCDataGridDatabaseAdapter`) |
| `TTMSFNCDateEdit`, `TTMSFNCTimePicker` | `TTMSFNCDatePicker`, `TTMSFNCDateTimePicker`, `TTMSFNCAnalogTimePicker`, `TTMSFNCDigitalTimePicker` |
| `TTMSFNCMaskEdit`, `TTMSFNCNumericEdit` | `TTMSFNCEdit` (`EditType: TTMSFNCEditType`, default `etString`) or `TTMSFNCSpinEdit` |
| `TTMSFNCAccordion`, `TTMSFNCTreeList` | `TTMSFNCNavigationPanel` / `TTMSFNCPanel` collapse; `TTMSFNCTreeView` (multi-column) |
| `TTMSFNCStyleManager` | `TTMSFNCStylesManager` (plural, FNC Core `*.TMSFNCStyles`) |
| `TTMSFNCFilterDialog` on the palette | Only `TTMSFNCDataSetFilterDialog` is registered |
| `TTMSFNCTrayIcon` on the palette | It isn't registered or packaged. Create it in code |
| `TAdvButton`, `TAdvEdit`, `TAdvPanel`, `TAdvStringGrid` (TMS VCL UI Pack) | FNC classes start with `TTMSFNC` and use FNC units; the APIs differ |
| `Button1.Fill.Color`, `Edit1.BeginUpdate` | `TTMSFNCButton`/`TTMSFNCEdit` are native controls without FNC `Fill`/`Stroke`/`BeginUpdate` |
| `Control.Images := ImageList1` / `ImageIndex` | `BitmapContainer := ...` and `BitmapName` / `<img src="name">` |
| `uses LCL.TMSFNCPanel` | `uses LCLTMSFNCPanel` (no dot) |
| `SaveSettingsToFile` expecting INI/XML | It writes JSON; the second parameter `AAppearanceOnly` limits it to the look |
| Palette page "TMS FNC UI Pack" | `TMS FNC UI` |
