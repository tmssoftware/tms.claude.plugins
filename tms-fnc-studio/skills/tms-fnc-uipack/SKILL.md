---
name: tms-fnc-uipack
description: >
  Accurate API knowledge for the TMS FNC UI Pack controls (tms.fnc.uipack) other than TTMSFNCDataGrid, in Delphi VCL,
  FMX and TMS WEB Core. Use whenever code references a TTMSFNC UI Pack control (TreeView, Planner, Timeline, Calendar,
  DatePicker, RichEditor, HTMLEditor, Memo, HTMLText, KanbanBoard, ListBox, TableView, TileList, Edit, SpinEdit,
  ComboBox, pickers and selectors, Button, Switch, TrackBar, ProgressBar, Badge, Panel, PageControl, TabSet,
  NavigationPanel, Ribbon, ToolBar, StatusBar, TaskDialog, Chat, SpreadGrid, the older TTMSFNCGrid), or when the user
  asks to build a tree view, scheduler, rich text or code editor, kanban board, list, form inputs, navigation, dialogs
  or a dashboard with TMS FNC. Read it before writing or reviewing UI Pack code: the real API differs from VCL/FMX
  standard controls and TMS VCL UI Pack (TAdv*).
metadata:
  version: "0.3.1"
---

# TMS FNC UI Pack API knowledge

TMS FNC UI Pack (product id `tms.fnc.uipack`, version 7.3, depends on TMS FNC Core) is a set of framework-neutral controls. The same API works in VCL, FMX and TMS WEB Core (and Lazarus). Only the unit prefix (`VCL.`, `FMX.`, `WEBLib.`; Lazarus `LCLTMSFNC...`) and a few classes differ. For **TTMSFNCDataGrid** load the `tms-fnc-datagrid` skill instead. For graphics, bitmaps, PDF, printing, popups, styles, JSON and persistence load `tms-fnc-core`.

## Ground rules

- **Never guess member names.** Use only members in these references. If one isn't covered, don't read component source (many installs are trial/DCU-only): check https://doc.tmssoftware.com/fnc/uipack/ if web access is available (these references win on conflicts), else compile the smallest use and let the compiler confirm it, else tell the user the member is unverified.
- **Don't carry over names** from VCL/FMX standard controls (`TTreeView`, `TListBox`, `TRichEdit`, `TPageControl`, ...), TMS VCL UI Pack (`TAdv*`) or another FNC control. Each control has its own item class and enum prefix. Each reference file ends with a "Does not exist / common mistakes" list; check it.
- **Match the framework**, and check that the control exists for it. These are **not available on TMS WEB Core**: RichEditor (and its toolbars and IO), HTMLEditor, SpreadGrid, SearchEdit, SearchList, ResponsiveList, DirectoryEdit, DirectoryTreeView, DataSetFilterDialog, and the Grid and Planner toolbar popups.
- **New project from code**: a hand-written `.dpr` must not contain `{$R *.res}` unless the `.res` exists (E1026). Non-FNC types need their own units: VCL `TPngImage` → `Vcl.Imaging.pngimage`; FMX `TBrushKind`/`TBitmap` → `FMX.Graphics`, `TAlignLayout` → `FMX.Types`, `TAlphaColors`/`TFontStyle` → `System.UITypes`; `TRectF`/`PointF` → `System.Types`.
- **Bracket bulk changes** with `BeginUpdate` / `EndUpdate` where the class has them.
- Prefer patterns from the reference files (derived from the official demos) over invented approaches.

## The pitfalls that matter most

1. **Native wrappers**: `TTMSFNCButton` and `TTMSFNCEdit` wrap native controls. They have no `Fill`, `Stroke`, `Caption`-style FNC appearance, `BeginUpdate` or `SaveSettings`. `TTMSFNCEdit` uses `EditType` plus `IntValue`/`FloatValue`; a button image needs `BitmapName` and `ShowImage := True`.
2. **TreeView**: node text is per column (`Node.Text[0]`). Add children with `AddNode(Parent)` or `Parent.Nodes.Add`; use `GetParent`, `Nodes.Count`. Collection and virtual mode (`OnGetNumberOfNodes`, which first gets a root with `Level = -1`) can't be mixed. `Clear` also deletes columns; use `ClearNodes`. Columns aren't editable by default. The TreeView database adapter isn't in the installed packages, so fill the tree from the dataset in code (see `treeview.md`).
3. **Planner**: modes are `pmDay, pmDayPeriod, pmHalfDayPeriod, pmMultiDay, pmMultiResDay, pmMultiDayRes, pmMonth, pmMultiMonth, pmCustom`. There is no `pmWeek`: use `pmMultiDay` with `Positions.Count := 7`. `Item.Resource` is an integer index. `Items.Add` takes no parameters; use `AddItem`. The planner never expands recurrency itself (the database adapter or `TTMSFNCRecurrencyHandler` does). The adapter loads only the visible period, so call `LoadItems` in `OnAfterNavigateToDateTime`.
4. **Timeline**: points are `Indicators`, ranges are `Sections`; there is no `Items`. `Orientation`/`ZoomFactor` are on `Layout`.
5. **Date/time**: `Calendar.SelectedDate` is a read-only function (`SelectADate` replaces the selection). `DatePicker.SelectedDate` is writable. The pickers raise `OnDateSelected` / `OnDateTimeChanged` / `OnTimeSelected`, not `OnChange`.
6. **RichEditor**: `LoadFromFile` reads only the native format; RTF and HTML go through `TTMSFNCRichEditorRTFIO` / `TTMSFNCRichEditorHTMLIO`. There's no `Lines`, `SelAttributes` or `Paragraph`; use `AddText`/`AddLineBreak` and the `SetSelection*` methods. In `SelectText(FromChar, ALength)` a line break counts as 2 characters. Print with `TTMSFNCRichEditorPrintIO`.
7. **Memo** is Monaco inside a web control: it needs WebView2 on Windows, and anything that runs JavaScript only works after `OnInitialized`. Settings go through `Options`. Save with `Lines.SaveToFile`.
8. **Mini-HTML** text (HTMLText, captions, items): attribute values are double-quoted; no `<div>`, `<span>`, `<table>` or CSS; use `<br>`. Assigning `OnAnchorClick` replaces `AutoOpenURL`. A literal `&` must be written `&&` (VCL and FMX, in HTMLText, TableView, TreeView and other FNC text): a single `&` is a hotkey prefix, so `R&D` loses the `&`, and `&amp;` shows as `amp;`.
9. **Lists and Kanban**: each list has its own item class and prefix (`l*` ListBox, `tv*` TableView, `tl*` TileList). TileList items use `Title`/`Description`. Templates are `<#NAME>` in TableView/Kanban but `(#NAME)` in ResponsiveList. Kanban drag/drop is off until `Interaction.DragDropMode := kbdmMove`. Item colours need `UseDefaultAppearance := False`. `MoveItem` frees the original item.
10. **Inputs**: SpinEdit uses `Min`/`Max`/`Value`/`Interaction.Frequency`, not `MinValue`/`Increment`. TrackBar uses `Value`, not `Position`. ProgressBar uses `Minimum`/`Maximum` and has no marquee mode (use TTMSFNCWaitingIndicator). TTMSFNCSpinner is a value wheel, not a busy indicator. Qualify `TTMSFNCCustomComboBoxStyle.csDropDownList`.
11. **Pickers/selectors** created in code are empty until `InitializeDefault`. Use `SelectedColor`/`OnColorSelected` style names, not `Color`/`OnChange`. On CheckGroupPicker set `Value` (bitmask) or `SelectedItems`.
12. **Containers**: `PageControl.Pages[i]` is a tab; add controls to `PageContainers[i]`. `ttcaNone` exists in both the TabSet and PageControl units, so qualify it. Call `Ribbon.Rebuild` before using a runtime-created ribbon's page control. `StatusBar.Panels.Items[i]` (no default indexer).
13. **Dialogs**: results arrive asynchronously on WEB (and for TaskDialog on FMX mobile). TaskDialog custom buttons return 100+i. Find/Replace dialogs don't search; you search in `OnFind`. `Chat.AddMessage` triggers the send event unless `ATriggerSendEvent = False`.
14. **SpreadGrid**: `Cells` holds the formula; read results from `CalcValues` after `Recalc`. Use `;` as argument separator. There's no `IF` and no `<`/`>`/`=` operators (`LT`/`ST`/`EQ`/`CHOOSE`).
15. **TTMSFNCGrid** is the older grid. Maintain existing code with it, but write new code with TTMSFNCDataGrid (mapping table in `spreadgrid-and-legacy-grid.md`).
16. **Look on VCL**: FNC controls are opaque windows, so `Fill.Kind := gfkNone` shows white, not the parent; use a solid fill in the parent colour. Badge fills default to a gradient (set `Fill.Kind := gfkSolid`). A style load overwrites earlier customisation. See `dashboards.md`.

## Reference files

How to read them (saves most of the tokens and time): line 2 of every file is a section map, `> Sections (line ranges): 6-26 Units · 27-58 ...`. Read the first 2 lines, then only the line ranges you need (Read with offset/limit, `sed -n '27,58p'`, or `Get-Content f | Select-Object -Skip 26 -First 32`), plus the last section ("Does not exist / common mistakes") when you write code for that control. Every command is another full model round trip, so batch: read the maps of all files you need in one command, then all needed ranges in one or two commands (keep each output under ~40 KB). Never dump whole files: long outputs get truncated and re-read.

| File | Covers |
|---|---|
| `references/setup-and-components.md` | Catalog of every registered control (unit, palette, VCL/FMX/WEB/LCL availability), shared FNC control conventions. Install details are in the datagrid skill's `setup-and-install.md` |
| `references/treeview.md` | TTMSFNCTreeView (collection and virtual mode), CheckedTreeView, DirectoryTreeView, TreeView database adapter |
| `references/lists.md` | ListBox, CheckedListBox, TableView, TileList, SearchList, ResponsiveList, ListEditor, CategoryList |
| `references/kanban.md` | KanbanBoard and its database adapter |
| `references/planner.md` | Planner modes, items, resources, interaction, item editors, recurrency, database adapter, toolbar popup |
| `references/timeline.md` | Timeline and its database adapter |
| `references/date-time.md` | Calendar, DatePicker, DateTimePicker, analog and digital time pickers/selectors |
| `references/rich-editor.md` | RichEditor, toolbars, ruler, HTML/RTF/PDF/print/e-mail IO, HTMLEditor |
| `references/memo.md` | Memo (Monaco code editor), custom languages and themes |
| `references/html-text-and-images.md` | Mini-HTML tags, HTMLText, Image, HotSpotImage, PDFImageBook |
| `references/edits.md` | Edit, SpinEdit, ComboBox, SearchEdit, IPEdit, LabelEdit, DirectoryEdit, PassLock, SignatureCapture, TouchKeyboard |
| `references/pickers-and-selectors.md` | Colour, font, bitmap, fill/stroke kind pickers and selectors, ColorWheel, ControlPicker, group pickers |
| `references/buttons-and-toggles.md` | Button, CheckBox, RadioButton, Check/RadioGroup, Switch, TrackBar, RangeSlider, ProgressBar, Rating, Badge, Spinner, WaitingIndicator |
| `references/containers-and-navigation.md` | Panel, PageControl, TabSet, NavigationPanel, PageSlider, Ribbon, ToolBar(s), StatusBar, Splitter, TrayIcon |
| `references/dialogs-and-misc.md` | TaskDialog, FontDialog, Find/Replace, FilterView, filter dialogs, ObjectInspector, Chat |
| `references/spreadgrid-and-legacy-grid.md` | SpreadGrid formulas and math libs, the older TTMSFNCGrid and its companions, TTMSFNCGrid → TTMSFNCDataGrid mapping |
| `references/dashboards.md` | Building a styled dashboard: which control for which piece, KPI cards and charts drawn with `TTMSFNCGraphics`, flat/opaque styling traps on VCL, style-loading order, snapshot and PDF. Read this first for any dashboard, admin overview or "make it look good" task |

## Related skills

- `tms-fnc-datagrid`: TTMSFNCDataGrid.
- `tms-fnc-core`: graphics, bitmaps, PDF, printing, popups, styles, JSON, persistence.
- `/get-started`, `/unlock-feature`, `/review`.
