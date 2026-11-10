# Containers & navigation (TTMSFNCPanel, TTMSFNCPageControl, TTMSFNCTabSet, TTMSFNCNavigationPanel, TTMSFNCPageSlider, TTMSFNCRibbon, TTMSFNCToolBar, TTMSFNCStatusBar, TTMSFNCSplitter, TTMSFNCTrayIcon)
> Sections (line ranges): 6-26 Units and palette · 27-58 TTMSFNCPanel · 59-128 TTMSFNCTabSet · 129-176 TTMSFNCNavigationPanel · 177-203 TTMSFNCPageSlider · 204-254 TTMSFNCRibbon · 255-287 TTMSFNCToolBar and pickers · 288-310 TTMSFNCStatusBar · 311-328 TTMSFNCSplitter · 329-355 TTMSFNCTrayIcon · 356-361 Platform notes · 362-377 Does not exist / common mistakes

Verified against TMS FNC UI Pack 7.3.1.2 source (`VCL.TMSFNCPanel`, `VCL.TMSFNCTabSet`, `VCL.TMSFNCPageControl`, `VCL.TMSFNCNavigationPanel`, `VCL.TMSFNCPageSlider`, `VCL.TMSFNCRibbon`, `VCL.TMSFNCToolBar`, `VCL.TMSFNCToolBars`, `VCL.TMSFNCToolBarPopup`, `VCL.TMSFNCStatusBar`, `VCL.TMSFNCSplitter`, `VCL.TMSFNCTrayIcon`) and the VCL demos `TabSet_PageControl`, `NavigationPanel`, `Ribbon`.

## Units and palette

Unit = `<prefix>.TMSFNC<Name>` with prefix `VCL.` / `FMX.` / `WEBLib.`; Lazarus units have **no dot**: `LCLTMSFNCPanel`, `LCLTMSFNCTabSet`, ...

| Class | Unit (VCL) | Palette | Frameworks |
|---|---|---|---|
| TTMSFNCPanel | VCL.TMSFNCPanel | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCTabSet | VCL.TMSFNCTabSet | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCPageControl | VCL.TMSFNCPageControl (+ VCL.TMSFNCTabSet) | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCNavigationPanel | VCL.TMSFNCNavigationPanel (+ VCL.TMSFNCPanel) | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCPageSlider | VCL.TMSFNCPageSlider | TMS FNC UI | VCL/FMX/WEB (no LCL) |
| TTMSFNCRibbon | VCL.TMSFNCRibbon (+ PageControl, TabSet, ToolBar) | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCToolBar, ...Button, ...Separator, ...FontNamePicker, ...FontSizePicker, ...ColorPicker, ...BitmapPicker, ...ItemPicker, TTMSFNCDockPanel | VCL.TMSFNCToolBar | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCFontToolBar, TTMSFNCParagraphToolBar, TTMSFNCInsertToolBar, TTMSFNCClipboardToolBar, TTMSFNCFileIOToolBar | VCL.TMSFNCToolBars | TMS FNC UI | VCL/FMX/WEB (no LCL) |
| TTMSFNCToolBarPopup | VCL.TMSFNCToolBarPopup | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCStatusBar | VCL.TMSFNCStatusBar | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCSplitter | VCL.TMSFNCSplitter | TMS FNC UI | VCL/FMX/WEB/LCL |
| TTMSFNCTrayIcon | VCL./FMX.TMSFNCTrayIcon, LCLTMSFNCTrayIcon | **not registered** | desktop only, no WEB |

Common: all visual classes descend from `TTMSFNCCustomControl` (accept child controls, `BeginUpdate/EndUpdate`, `Fill`, `Stroke`, `BitmapContainer` where image-capable). Text props render mini-HTML (`<b>`, `<font color="gcRed">`, `<a href>`) → `On...AnchorClick` events. Images come from `Bitmaps: TTMSFNCScaledBitmaps` + a `TTMSFNCBitmapContainer`: `Bitmaps.AddBitmapName('Home.png')`, `AddBitmap(ABitmap)`.

## TTMSFNCPanel

Header/footer panel with optional buttons and collapsible sections. Header/Footer are `TTMSFNCPanelElement` (Footer `Visible` default False).
```delphi
property Header: TTMSFNCPanelHeader;  property Footer: TTMSFNCPanelFooter;
// element: Text: string; Size: Single; Visible; Fill; Stroke; Font; HorizontalTextAlign/VerticalTextAlign (gtaCenter);
//          WordWrapping; Trimming; StretchText; ShowButtons; Buttons: TTMSFNCPanelButtons; ButtonSize; ButtonSpacing;
//          DropDownControl: TControl; DropDownWidth; DropDownHeight
TTMSFNCPanelButton = (pbCompact, pbClose, pbExpander, pbDropDown);
property CloseAction: TTMSFNCPanelCloseAction default pcaHide;          // pcaNone, pcaFree, pcaHide
property ExpandAction: TTMSFNCPanelExpandAction default peaExpand;      // peaNone, peaExpand
property CompactAction: TTMSFNCPanelCompactAction default pcCompact;    // pcNone, pcCompact
property DropDownAction: TTMSFNCPanelDropDownAction default pddaPopup;  // pddaNone, pddaPopup
property Sections: TTMSFNCPanelSections;   // item: Text, Size: Single, Control: TControl, Tag
property SectionsAppearance;  property ButtonsAppearance;  property GlobalFont;
procedure Expand(ACompact: Boolean = False);  procedure Collapse(ACompact: Boolean = False);
procedure Compact;  procedure CompactAndCollapse;  procedure Restore;
property ExpandState: TTMSFNCPanelExpandState;    // pesCollapsed, pesExpanded (public)
property CompactState: TTMSFNCPanelCompactState;  // pcsCollapsed, pcsExpanded (public)
// events: OnHeaderAnchorClick(Sender; AAnchor: String), OnHeaderCloseButtonClick, OnHeaderExpandButtonClick,
//         OnHeaderCompactButtonClick, OnHeaderDropDownButtonClick, same OnFooter...
```
```delphi
pnl := TTMSFNCPanel.Create(Self);
pnl.Parent := Self;
pnl.Align := alLeft;
pnl.Header.Text := '<b>Settings</b>';
pnl.Header.Buttons := [pbExpander, pbClose];
pnl.CloseAction := pcaHide;
btn := TButton.Create(pnl); btn.Parent := pnl;   // children go directly on the panel
```

## TTMSFNCTabSet (tabs only) and TTMSFNCPageControl (tabs + pages)

`TTMSFNCPageControl` descends from `TTMSFNCCustomTabSet`; it shares `TabAppearance`, `ButtonAppearance`, `TabSize`, `Layout`, `Options`, `Interaction`.
```delphi
// TabSet
property Tabs: TTMSFNCTabSetTabs;              // Tabs[i]: TTMSFNCTabSetTab (default), Add, Insert, Clear
property ActiveTabIndex: Integer default 0;    property ActiveTab: TTMSFNCTabSetTab (public)
function AddTab(AText: string = ''): TTMSFNCTabSetTab;
function InsertTab(ATabIndex: Integer; AText: string = ''): TTMSFNCTabSetTab;
procedure RemoveTab(ATabIndex: Integer);   procedure MoveTab(AFromTabIndex, AToTabIndex: Integer);
procedure SelectTab(ATabIndex: Integer);   procedure SelectNextTab;  procedure SelectPreviousTab;
procedure ScrollToTab(ATabIndex: Integer); function IsTabVisible(ATabIndex: Integer): Boolean;
OnChangeTab: procedure(Sender: TObject; APreviousTabIndex: Integer; ACurrentTabIndex: Integer) of object;
OnBeforeChangeTab: procedure(Sender: TObject; ACurrentTabIndex: Integer; ANewTabIndex: Integer; var ACanChange: Boolean) of object;
OnBeforeCloseTab: procedure(Sender: TObject; ATabIndex: Integer; var ACloseAction: TTMSFNCTabSetTabCloseAction) of object;
// also OnCloseTab, OnBeforeInsertTab, OnInsertTab, OnBeforeReorderTab, OnReorderTab, OnAnchorTabClick, OnBefore/AfterDrawTab*

// PageControl
property Pages: TTMSFNCPageControlPages;       // Add/Insert return TTMSFNCPageControlPage
property ActivePageIndex: Integer default 0;   property ActivePage: TTMSFNCPageControlPage (public)
property PageContainers[AIndex: Integer]: TTMSFNCPageControlContainer;   // public
property Collapsed: Boolean default False;
function AddPage(AText: string = ''): TTMSFNCPageControlPage;
function InsertPage(APageIndex: Integer; AText: String = ''): TTMSFNCPageControlPage;
procedure RemovePage(APageIndex: Integer);  procedure MovePage(AFromPageIndex, AToPageIndex: Integer);
// TTMSFNCPageControlPage = class(TTMSFNCTabSetTab): property Container: TTMSFNCPageControlContainer
OnChangePage: procedure(Sender: TObject; APreviousPageIndex: Integer; ACurrentPageIndex: Integer) of object;
OnBeforeChangePage(Sender; ACurrentPageIndex, ANewPageIndex: Integer; var ACanChange: Boolean)
OnBeforeClosePage(Sender; APageIndex: Integer; var ACloseAction: TTMSFNCPageControlPageCloseAction)
// also OnClosePage, OnBeforeInsertPage, OnInsertPage, OnBeforeReorderPage, OnReorderPage
```
Tab item (`TTMSFNCTabSetTab`) published: `Text`, `Badge`, `Hint`, `Enabled`, `Visible`/`TabVisible`, `CloseButton` (True), `Bitmaps`, `DisabledBitmaps`, `BitmapVisible`, `BitmapSize`, `Shape`, `Width`, `Progress`, `ProgressMax`, `ProgressKind` (`tpkNone, tpkCircular, tpkRectangular`), `ProgressMode` (`tpmNormal, tpmMarquee`), colors (`Color`, `ActiveColor`, `TextColor`, ... used only when `UseDefaultAppearance = False`, the default), `Tag`; public `DataPointer/DataObject/DataString/DataInteger/DataBoolean`.

Settings:
- `Layout.Position: TTMSFNCTabSetLayoutPosition` = `tlpLeft, tlpTop, tlpBottom, tlpRight`; `Layout.Multiline` = `tlmNone, tlmEnabled, tlmEnabledActiveTab`.
- `Options.CloseMode` = `tcmNone, tcmTab, tcmMenu`; `Options.InsertMode` = `timNone, timTab, timMenu`; `Options.CloseAction` (`ttcaNone, ttcaFree, ttcaHide`, default ttcaHide); `Options.TabListButton`.
- `Interaction.Editing` (in-place rename), `Interaction.Reorder` (drag), `SelectTabOnFocus`, `SelectTabOnInsert`, `CloseTabWithKeyboard`, `AutoOpenURL`.
- `TabSize.Mode: TTMSFNCTabSetTabSizeMode` = `tsmAutoSize, tsmFixedSize, tsmFixedSizeAutoShrink, tsmAutoTabSize`; `TabSize.Width/Height/Spacing/Margins`.
- `TabAppearance`: `Font`, `Fill/ActiveFill/HoverFill/DownFill/DisabledFill` (+Stroke), `TextColor/ActiveTextColor/...`, `Shape` (`tsRectangle, tsPyramidLeft, tsPyramidRight, tsPyramid, tsRoundLeft, tsRoundRight, tsRound`), `BadgeFill`, `BadgeFont`, `ProgressFill`.

Demo `TabSet_PageControl` (DFM settings, reproduced in code):
```delphi
pc := TTMSFNCPageControl.Create(Self);
pc.Parent := Self;
pc.Align := alClient;
pc.BitmapContainer := TMSFNCBitmapContainer1;
pc.BeginUpdate;
try
  pc.Pages.Clear;
  pg := pc.AddPage('Mercedes');
  pg.Bitmaps.AddBitmapName('Tools.png');
  pg.BitmapVisible := True;
  pg.ProgressKind := tpkRectangular;
  pg.Progress := 50;
  pc.AddPage('BMW').Badge := 'Hello';
  pc.Interaction.Editing := True;
  pc.Interaction.Reorder := True;
  pc.Options.CloseMode := tcmTab;
  pc.Options.InsertMode := timTab;
  pc.Options.TabListButton := True;
finally
  pc.EndUpdate;
end;
grid := TTMSFNCDataGrid.Create(Self);
grid.Parent := pc.PageContainers[0];       // or pg.Container
grid.Align := alClient;
pc.ActivePageIndex := 0;
```
`AddPage` creates the `TTMSFNCPageControlContainer` automatically (owned by the page control's Owner); `RemovePage` frees it. A runtime-created TabSet/PageControl starts empty (`InitSample` only runs at design time).

## TTMSFNCNavigationPanel

Outlook-style bar. Items are **Panels**; each has an auto-created `Container: TTMSFNCNavigationPanelContainer` (a `TTMSFNCPanel`, so it has `Sections`).
```delphi
property Panels: TTMSFNCNavigationPanelItems;    // Panels[i]: TTMSFNCNavigationPanelItem; Add; Insert; Clear
property ActivePanelIndex: Integer default 0;
property PanelContainers[AIndex: Integer]: TTMSFNCNavigationPanelContainer;   // public, read-only
property Mode: TTMSFNCNavigationPanelMode default npmMixed;   // npmItems, npmButtons, npmMixed
property CompactMode: Boolean default False;  property CompactModeSize: Single;  property ShowCompactModeButton: Boolean default True;
property ShowHeader: Boolean default True;    property ShowFooter: Boolean default False;
property MaxItemCount: Integer default -1;    property MaxButtonCount: Integer default -1;
property Splitter: TTMSFNCNavigationPanelSplitter;  property ItemsAppearance;  property ButtonsAppearance;
function AddPanel(AText: string = ''): TTMSFNCNavigationPanelItem;
function InsertPanel(APanelIndex: Integer; AText: String = ''): TTMSFNCNavigationPanelItem;
procedure RemovePanel(APanelIndex: Integer);  procedure MovePanel(AFromPanelIndex, AToPanelIndex: Integer);
procedure SelectPanel(APanelIndex: Integer);  procedure SelectNextPanel;  procedure SelectPreviousPanel;
procedure SplitItems(ANumberOfItems: Integer);
OnItemClick / OnCompactItemClick: procedure(Sender: TObject; AItemIndex: Integer) of object;
OnItemAnchorClick(Sender; AItemIndex: Integer; AAnchor: String);  OnSplitterMove(Sender; AOldPosition, ANewPosition: Integer)
// item: Text, CompactText, Hint, Badge, Enabled, Visible, Kind (pikItem, pikButton), Bitmaps
```
Demo `NavigationPanel` (abridged):
```delphi
for I := 0 to Length(pnls) - 1 do
  with TMSFNCNavigationPanel1.Panels.Add do
  begin
    Text := pnls[I];
    CompactText := pnls[I];
    if I = 0 then Kind := pikButton;
    Bitmaps.AddBitmapName(pnls[I]);
    if I = 1 then Badge := '5';
    with Container.Sections.Add do
    begin
      Text := 'Settings';
      Size := TMSFNCNavigationPanel1.ScalePaintValue(250);
      pnl := TTMSFNCPanel.Create(Self);
      pnl.Header.Visible := False;
      Control := pnl;                      // section hosts any TControl
    end;
  end;
TMSFNCNavigationPanel1.ActivePanelIndex := 0;

procedure TForm5.TMSFNCNavigationPanel1CompactItemClick(Sender: TObject; AItemIndex: Integer);
begin
  TMSFNCNavigationPanel1.CompactMode := False;
end;
```

## TTMSFNCPageSlider

Horizontally sliding pages, each a `TTMSFNCPageSliderContainer` with `Header`/`Footer` (`Text`, `Size` (40), `Visible`, `Fill`, `Stroke`, `Font`) and `MinimumWidth` (200).
```delphi
function AddPage(APageCaption: string): TTMSFNCPageSliderContainer; overload;
function AddPage(APageCaption, AFooterCaption: string): TTMSFNCPageSliderContainer; overload;
function AddSimplePage: TTMSFNCPageSliderContainer;      // header + footer hidden
procedure RemovePage(AIndex: Integer);  procedure MovePage(AFromPageIndex, AToPageIndex: Integer);
procedure NextPage;  procedure PreviousPage;
function IndexOfPage(APage: TTMSFNCPageSliderContainer): Integer;
property PageCount: Integer;  property PageContainers[Index: Integer]: TTMSFNCPageSliderContainer;
property ActivePageIndex: Integer;  property Pages: TTMSFNCPageSliderPages;
property AnimateScroll: Boolean default True;  property AnimationFactor: Integer default 5;
property KeyboardInteraction: Boolean default True;
OnPageChanging: procedure(Sender: TObject; AFromPage, AToPage: Integer; var AAllowChange: Boolean) of object;
OnPageMoved: procedure(Sender: TObject; AFromPos: Integer; AToPos: Integer) of object;
OnPageChange: TNotifyEvent;
```
```delphi
ps := TTMSFNCPageSlider.Create(Self);
ps.Parent := Self;
ps.Align := alClient;
c := ps.AddPage('Step 1', 'Next >');
lbl := TLabel.Create(Self); lbl.Parent := c;
ps.NextPage;
```

## TTMSFNCRibbon

Composite: `Caption`, `QAT` (quick access toolbar), `SystemMenu`, `ToolBarWrapper`, `PageControl: TTMSFNCRibbonPageControl` (all public, read-only). Pages hold `TTMSFNCRibbonToolBar` groups.
```delphi
property Theme: TTMSFNCRibbonTheme default rbtLightBlue;  // rbtLightBlue, rbtBlue, rbtCrimson, rbtGreen, rbtSeaGreen,
                                                          // rbtOrange, rbtPurple, rbtDarkGray, rbtBlack, rbtWhite, rbtCustom
property CustomThemeColor: TTMSFNCGraphicsColor;          // used with rbtCustom
property Mode: TTMSFNCRibbonMode default rmToolBarAndPageControl;  // rmToolBarOnly, rmToolBarAndPageControl, rmPageControlOnly
property QATMode: TTMSFNCRibbonQATMode default rqmToolBar;         // rqmToolBar, rqmBelowRibbon
property Groups: TTMSFNCRibbonGroups;   // contextual tab groups: Text, StartPageIndex, EndPageIndex, Color, TextColor
procedure Rebuild;  procedure ApplyTheme;
procedure SetTheme(ATheme: TTMSFNCRibbonTheme; ACustomThemeColor: TTMSFNCGraphicsColor);
// PageControl: AddPage(AText): TTMSFNCRibbonPage; Pages[i]: TTMSFNCRibbonPage; PageContainers[i];
//              FileButton: TTMSFNCRibbonFileButton; Collapsable: Boolean
// TTMSFNCRibbonPage / TTMSFNCRibbonPageControlContainer:
function AddToolBar(AText: string = ''; AIndex: Integer = -1): TTMSFNCRibbonToolBar;
property ToolBars[AIndex: Integer]: TTMSFNCRibbonToolBar;
// TTMSFNCRibbonToolBar.AddButton(...): TTMSFNCRibbonToolBarButton; AddFontNamePicker, AddFontSizePicker,
//   AddColorPicker, AddItemPicker, AddBitmapPicker, AddSeparator (Ribbon* subclasses); ShortCutHint
```
Demo `Ribbon` (abridged):
```delphi
rb := TMSFNCRibbon1;
rb.SystemMenu.Visible := False;
rb.Rebuild;                                  // creates/refreshes the sub-controls
rb.PageControl.Collapsable := True;
rb.PageControl.Pages.Clear;
rb.PageControl.AddPage('Home').ShortCutHint := 'H';
rb.PageControl.AddPage('Insert').ShortCutHint := 'I';
rb.Caption.Text := 'Document 1.txt';
tb := rb.PageControl.PageContainers[0].AddToolBar('Clipboard');
btn := tb.AddButton;
btn.Text := 'Paste';
btn.Layout := bblLarge;
btn.MinimumLayout := bblLarge;
btn.BitmapContainer := TMSFNCBitmapContainer1;
btn.Bitmaps.AddBitmapName('Paste.png');
btn.LargeLayoutBitmaps.AddBitmapName('Paste_LARGE.png');
btn.OnClick := DoPasteClick;
fnp := tb.AddFontNamePicker;
fnp.OnFontNameSelected := DoFontNameSelected;    // procedure(Sender: TObject; AFontName: String)
rb.PageControl.FileButton.OnClick := DoFileButtonClick;
ip := rb.QAT.AddItemPicker;
ip.Items.Add('Light Blue');
ip.OnItemSelected := DoItemSelected;             // procedure(Sender: TObject; AItemIndex: Integer)
rb.QATMode := rqmBelowRibbon;
g := rb.Groups.Add;  g.Text := 'Tools';  g.StartPageIndex := 1;  g.EndPageIndex := 2;
rb.ApplyTheme;
```
For runtime creation: `rb := TTMSFNCRibbon.Create(Self); rb.Parent := Self; rb.Rebuild;` before touching `rb.PageControl`. `TTMSFNCRibbonForm` (same unit) is an optional `TForm` descendant for borderless ribbon chrome; the demo uses a plain `TForm`.

## TTMSFNCToolBar and pickers

```delphi
function AddButton(AWidth: Single = -1; AHeight: Single = -1; AResource: String = ''; AResourceLarge: String = ''; AText: String = '';
  AIndex: Integer = -1): TTMSFNCToolBarButton;
function AddSeparator(AIndex: Integer = -1): TTMSFNCToolBarSeparator;
function AddFontNamePicker / AddFontSizePicker / AddColorPicker / AddItemPicker / AddBitmapPicker(AIndex: Integer = -1): ...;
procedure AddCustomControl(AControl: TControl; AIndex: Integer = -1);
function AddCustomControlClass(AControlClass: TControlClass; AIndex: Integer = -1): TControl;
// published: Text (group caption), AutoSize, AutoAlign, AutoWidth, AutoHeight, CanCompact, Compact, OptionsMenu
//   (ShowButton, ShowItemBitmap, ShowItemText), Appearance (Fill, Stroke, DragGrip, Separator, HorizontalSpacing,...)
```
Button (`TTMSFNCToolBarButton`): `Text`, `Action`, `Bitmaps`, `LargeLayoutBitmaps`, `DisabledBitmaps`, `HoverBitmaps`, `DownBitmaps`, `BitmapSize`, `AutoBitmapSize`, `BitmapPosition` (`bbpLeft, bbpTop`), `Layout`/`MinimumLayout`/`MaximumLayout`/`CompactLayout` (`bblNone, bblBitmap, bblLabel, bblLarge`), `DropDownKind` (`ddkNormal, ddkDropDown, ddkDropDownButton`), `DropDownPosition` (`ddpRight, ddpBottom`), `DropDownControl: TControl`, `DropDownWidth/Height`, `OnDropDown`, `OnCloseDropDown`, `LastElement`, `Appearance`; public `DropDown`, `CloseDropDown`, `Hidden`. Click = `OnClick`.
Pickers: ItemPicker `Items: TStringList`, `SelectedItemIndex`, `SelectedItem`, `OnItemSelected`; FontNamePicker `SelectedFontName`, `OnFontNameSelected`; FontSizePicker `SelectedFontSize: Single`, `OnFontSizeSelected(Sender; AFontSize: Single)`; ColorPicker `SelectedColor`, `OnColorSelected(Sender; AColor: TTMSFNCGraphicsColor)`; BitmapPicker `SelectedBitmap`, `OnBitmapSelected`. `TTMSFNCDockPanel.AddToolBar(AIndex: Integer = -1): TTMSFNCToolBar` hosts several toolbars.
```delphi
tb := TTMSFNCToolBar.Create(Self);
tb.Parent := Self;
tb.Align := alTop;
b := tb.AddButton(-1, -1, '', '', 'Save');
b.OnClick := SaveClick;
tb.AddSeparator;
tb.AddColorPicker.OnColorSelected := ColorSelected;
```

**Prebuilt toolbars** (`*.TMSFNCToolBars`): each has `Options` (set) and per-action events; the `Control: TComponent` link only works for components implementing `ITMSFNCFontToolBar` etc. (`*.TMSFNCToolBarInterfaces`). Otherwise handle the events:
- `TTMSFNCFontToolBar`: `Options` (`ftoFontName, ftoFontSize, ftoBold, ftoItalic, ftoUnderline, ftoStrikeout, ftoTextColor, ftoBackgroundColor`), `OnApplyBold/Italic/Underline/Strikeout: TNotifyEvent`, `OnApplyFontName(Sender; AFontName: String)`, `OnApplyFontSize(Sender; AFontSize: Integer)`, `OnApplyTextColor/OnApplyBackgroundColor(Sender; AColor)`; accessors `FontNamePicker`, `FontSizePicker`, `BoldButton`, ...
- `TTMSFNCParagraphToolBar`: `ptoAlignLeft, ptoAlignCenter, ptoAlignRight, ptoBullets, ptoNumbering, ptoUnindent, ptoIndent`; `OnAlignLeft/Center/Right`, `OnApplyBullets(Sender; AIndex: Integer)`, `OnApplyNumbering`, `OnApplyIndent`, `OnApplyUnindent`.
- `TTMSFNCInsertToolBar`: `ftiImage, ftiHyperlink`; `OnInsertBitmap`, `OnInsertHyperlink`.
- `TTMSFNCClipboardToolBar`: `etoCut, etoCopy, etoPaste, etoUndo, etoRedo`; `OnCut/OnCopy/OnPaste/OnUndo/OnRedo`.
- `TTMSFNCFileIOToolBar`: `itoOpenFile, itoSaveFile`; `OnOpenFile`, `OnSaveFile`.

**TTMSFNCToolBarPopup** (non-focusable popup with a toolbar): `Buttons` collection (item: `Text`, `Bitmap`, `Left/Top/Width/Height`, `Enabled`, `Visible`, `LastElement`, public `Button: TTMSFNCToolBarButton`), `PlacementControl`, `Placement` (`ppBottom, ppTop, ...`), `OnButtonClick(Sender; AButton: TTMSFNCToolBarPopupButton)`, `Activate`, `Deactivate`, `Activated`, `ToolBar`.

## TTMSFNCStatusBar

Default `Align = alBottom` (FMX `TAlignLayout.Bottom`).
```delphi
property Panels: TTMSFNCStatusBarPanels;     // Add; Items[Index] (NOT a default property)
property PanelAppearance;  property ShowSplitter: Boolean default True;  property BitmapContainer;
TTMSFNCStatusBarPanelStyle = (spsHTML, spsText, spsOwnerDraw, spsTime, spsDate, spsProgress, spsImage, spsImageList, spsEllipsText);
// panel: Text, Style (spsHTML), Width: Integer, MinWidth (20), AutoSize, Alignment: TAlignment, ImageIndex (-1), ImageCount,
//        DateFormat, TimeFormat, Progress (Position, Min, Max, Indication...), Control: TControl, ControlAlign, Button, Hint, Visible
OnPanelLeftClick / OnPanelRightClick: procedure(Sender: TObject; PanelIndex: Integer) of object;
OnAnchorClick: procedure(Sender: TObject; APanel: TTMSFNCStatusBarPanel; AAnchor: string) of object;
OnDrawCustomPanel(Sender; AGraphics; ARect: TRectF; APanel)   // for spsOwnerDraw
```
Ribbon demo:
```delphi
sb.Panels.Items[0].Text := '<b>Selected text: </b>';
sb.Panels.Items[1].Style := spsImage;              // image from BitmapContainer by ImageIndex
sb.Panels.Items[1].ImageIndex := 42;
sb.Panels.Items[2].Style := spsTime;
sb.Panels.Items[2].Alignment := taRightJustify;
```
A runtime-created status bar has no panels: call `Panels.Add` first.

## TTMSFNCSplitter

Works like VCL `TSplitter`: place it next to an aligned control with the same `Align`; it resizes the neighbour.
```delphi
property Align;  property MinSize: Single;  property ResizeStyle: TTMSFNCSplitterResizeStyle default rsContinuous; // rsOnce
property ShowIndicator: Boolean default True;
property SplitterIndicator: TTMSFNCSplitterIndicator default siCircle; // siCircles, siLine, siSquare, siSquares, siImage
property Appearance;   // SplitterFill/Stroke, SplitterHoverFill, IndicatorFill, IndicatorBitmap, ...
OnSplitterMove / OnSplitterMoved: procedure(Sender: TObject; AResizeStyle: TTMSFNCSplitterResizeStyle; ADownPos: TPointF; ACurrentPos: TPointF; ASplit: Single) of object;
```
```delphi
spl := TTMSFNCSplitter.Create(Self);
spl.Parent := Self;
spl.Align := alLeft;
spl.Left := NavPanel.Left + NavPanel.Width + 1;   // must sit right of the alLeft control
spl.MinSize := 100;
```

## TTMSFNCTrayIcon

Non-visual (`TTMSFNCCustomComponent`), `ComponentPlatformsAttribute(TMSPlatformsDesktop)`; Windows (Shell_NotifyIcon) and macOS (FMX). There is **no Reg unit and it is in no package**: add `VCL.TMSFNCTrayIcon` (or FMX./LCL) to the project/uses and create it in code.
```delphi
property Active: Boolean default False;   property Icon: TTMSFNCBitmap;   property Hint: string;
property BitmapContainer;  property IconIndex: Integer default 0;
property Animate: Boolean default False;  property AnimateInterval: Integer default 1000;  // cycles BitmapContainer items
property MessageTitle, MessageHint: string;  property MessageTimeout: Integer default 10000;
property MessageFlags: TTMSFNCTrayIconMessageFlags default bfNone;   // bfNone, bfInfo, bfWarning, bfError (Windows)
property PopupMenu: TPopupMenu;
procedure ShowMessageHint;  procedure ShowPopupMenu(X, Y: Integer);
// events: OnClick, OnDblClick, OnMessageClick, OnMouseDown/Up/Move, OnAnimate
```
```delphi
uses VCL.TMSFNCTrayIcon;
FTray := TTMSFNCTrayIcon.Create(Self);
FTray.Icon.LoadFromFile('app.png');
FTray.Hint := 'My app';
FTray.PopupMenu := PopupMenu1;
FTray.OnDblClick := TrayDblClick;
FTray.Active := True;
FTray.MessageTitle := 'Done';
FTray.MessageHint := 'Export finished';
FTray.MessageFlags := bfInfo;
FTray.ShowMessageHint;
```

## Platform notes

- WEB: no TrayIcon. Ribbon on a `TWebForm` switches itself to `Mode := rmPageControlOnly` on `Rebuild`. Page/panel containers are created the same way.
- FMX: use `TAlignLayout.Client/Top/...` instead of `alClient`; StatusBar default align `TAlignLayout.Bottom`. TrayIcon works on Windows and macOS.
- LCL: no PageSlider and no prebuilt `TMSFNCToolBars`; unit names have no dot (`LCLTMSFNCRibbon`).

## Does not exist / common mistakes

- `TTMSFNCPageControl.Pages[i].Container` does not compile: `TTMSFNCPageControlPages` inherits the default `Tabs[]` (returns `TTMSFNCTabSetTab`). Use `PageContainers[i]`, the result of `AddPage(...)`, or `TTMSFNCPageControlPage(Pages[i]).Container`. (The Ribbon's `Pages[]` does return `TTMSFNCRibbonPage`.)
- `TabSheet`, `TTMSFNCTabSheet`, `TabIndex`, `Pages[i].Caption`, `ActivePage := TabSheet1`: use `AddPage('...')`, `ActivePageIndex`, `Text`. TabSet: `ActiveTabIndex`, `OnChangeTab` (no `OnChange`/`OnChanging`).
- `ttcaNone/ttcaFree/ttcaHide` are declared in **both** `TTMSFNCTabSetTabCloseAction` and `TTMSFNCPageControlPageCloseAction`; the last unit in `uses` wins. In `OnBeforeClosePage` write `ACloseAction := TTMSFNCPageControlPageCloseAction.ttcaNone`.
- `TTMSFNCToolBarPopup` is declared in **both** `*.TMSFNCToolBar` (internal `TTMSFNCPopup` descendant) and `*.TMSFNCToolBarPopup` (the component). Put `VCL.TMSFNCToolBarPopup` after `VCL.TMSFNCToolBar` in `uses`, or qualify the unit name.
- `StatusBar.Panels[0]`, `SimpleText`, `SimplePanel`: there is no default indexer and no simple mode. Use `Panels.Items[0].Text`, and `Panels.Add` at runtime.
- `TTMSFNCPanel.Caption`, `Collapsed`, `Collapsible`, `BevelOuter`: use `Header.Text`, `Header.Buttons := [pbExpander]`, `Collapse`/`Expand`, and `ExpandState`.
- `NavigationPanel.Items`, `ActiveItem`, `ActivePanel`, `AddItem`: use `Panels`, `ActivePanelIndex`, `AddPanel`, `PanelContainers[i]`. Content goes in `Panels[i].Container` (sections or children).
- `PageSlider.ActivePage` is protected: use `PageContainers[ActivePageIndex]`. Page caption is `Header.Text`, not `Caption`.
- Toolbar `Buttons[]`, `Images`/`ImageIndex`, `Down`, `GroupIndex`, `ShowCaptions`, `Caption`: the toolbar has none of these. Use `AddButton` results, `Bitmaps.AddBitmapName` + `BitmapContainer`, `Text`, and `Layout`. There is no toggle/down state.
- `TTMSFNCRibbon.AddPage`, `Tabs`, `RibbonPage.Groups`, `ApplicationMenu`: pages and groups live on `rb.PageControl.AddPage(...).AddToolBar('Group')`. `rb.Groups` are contextual tab-group headers spanning `StartPageIndex..EndPageIndex`, not button groups. `rb.PageControl` is nil until `Rebuild` on a runtime-created ribbon.
- Splitter `AutoSnap`, `Beveled`, `Control`/`ResizeControl`, `OnMoved`: the neighbour is found by position and align. Use `OnSplitterMoved`. `OnBefore/AfterDrawIndicator` are not published.
- TrayIcon `Visible`, `BalloonHint`, `ShowBalloonHint`, `Icons`/`ImageList`, dropping it from the palette: use `Active`, `MessageHint` + `MessageTitle` + `ShowMessageHint`, `BitmapContainer` + `IconIndex`, and create it in code.
- `TTMSFNCFontToolBar.Control := RichEdit1/Memo1` does nothing unless that component implements `ITMSFNCFontToolBar`. Handle `OnApplyBold`, `OnApplyFontName`, etc. instead. (For TTMSFNCRichEditor use its own `TTMSFNCRichEditorFormatToolBar` etc.)
