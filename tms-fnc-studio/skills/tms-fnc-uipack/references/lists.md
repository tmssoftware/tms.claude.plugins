# List controls (TTMSFNCListBox, TTMSFNCCheckedListBox, TTMSFNCTableView, TTMSFNCTileList, TTMSFNCSearchList, TTMSFNCResponsiveList, TTMSFNCListEditor, TTMSFNCCategoryList)

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCListBox`, `*.TMSFNCCheckedListBox`, `*.TMSFNCTableView`, `*.TMSFNCTileList`, `*.TMSFNCSearchList`, `*.TMSFNCResponsiveList`, `*.TMSFNCListEditor`, `*.TMSFNCCategoryList`; demos `VCL\Listbox`, `VCL\TableView`, `VCL\TileList`, `VCL\SearchList`, `VCL\ResponsiveList`, `VCL\ListEditor`.

Each control has its **own item class and its own enum prefixes**; do not transfer names between them.

| Component | Unit | Item class / text member | Palette | Platforms |
|---|---|---|---|---|
| TTMSFNCListBox | `*.TMSFNCListBox` | `TTMSFNCListBoxItem.Text` | TMS FNC UI | VCL, FMX, WEB, LCL |
| TTMSFNCCheckedListBox | `*.TMSFNCCheckedListBox` | `TTMSFNCCheckedListBoxItem.Text/Checked` | TMS FNC UI | VCL, FMX, WEB, LCL |
| TTMSFNCTableView | `*.TMSFNCTableView` | `TTMSFNCTableViewItem.Text` | TMS FNC UI | VCL, FMX, WEB, LCL |
| TTMSFNCTileList | `*.TMSFNCTileList` | `TTMSFNCTileListItem.Title/Description` | TMS FNC UI | VCL, FMX, WEB, LCL |
| TTMSFNCSearchList | `*.TMSFNCSearchList` | `TSearchListItem.Captions[col]` | TMS FNC UI | VCL, FMX (no WEBLib unit) |
| TTMSFNCResponsiveList | `*.TMSFNCResponsiveList` | `TResponsiveListItem.Content` | TMS FNC UI | VCL, FMX (no WEBLib unit) |
| TTMSFNCListEditor | `*.TMSFNCListEditor` | `TTMSFNCCustomListEditorItem.Text/Value` | TMS FNC UI | VCL, FMX, WEB, LCL |
| TTMSFNCCategoryList | `*.TMSFNCCategoryList` | `TTMSFNCCategoryListItem` (bitmap tiles) | not registered | VCL, FMX, WEB, LCL |

Prefix rule: `VCL.` / `FMX.` / `WEBLib.` / `LCLTMSFNC...`. Also add `*.TMSFNCGraphicsTypes` for `gta*`/`gc*` constants. All support `BeginUpdate`/`EndUpdate`.

## TTMSFNCListBox

Internally hosts a `TTMSFNCTreeView` (public read-only `TreeView` property).
```delphi
// TTMSFNCListBoxItems
function Add: TTMSFNCListBoxItem; overload;
function Add(AText: string): TTMSFNCListBoxItem; overload;
procedure AddStrings(AItems: TStrings; AClear: Boolean = False);
function Insert(Index: Integer): TTMSFNCListBoxItem;
function FindItem(AText: string): TTMSFNCListBoxItem;
procedure Sort(ACaseSensitive: Boolean = True; ASortingMode: TTMSFNCListBoxItemsSortMode = ismAscending);
// TTMSFNCListBoxItem (published): Text, Bitmap, BitmapName, BitmapWidth, BitmapHeight, WordWrapping, Trimming,
//   TextAlign, TextColor, SelectedTextColor, DisabledTextColor, Enabled, Height, Tag
// public: DataPointer/DataBoolean/DataObject/DataString/DataInteger, DBKey, IsSelected, StrippedHTMLText
// TTMSFNCCustomListBox
function AddItem(AText: string = ''): TTMSFNCListBoxItem;
procedure RemoveItem(AItem: TTMSFNCListBoxItem);
property ItemIndex: Integer;   property SelectedItem: TTMSFNCListBoxItem;
property SelectedItems[AIndex: Integer]: TTMSFNCListBoxItem;  function SelectedItemCount: Integer;
procedure SelectItem(AItemIndex: Integer);  procedure SelectItems(AItemIndexes: TTMSFNCListBoxItemArray);  procedure UnSelectAllItems;
procedure ScrollToItem(AItemIndex: Integer);
function LookupItem(ALookupString: String; ACaseSensitive: Boolean = False; AAutoSelect: Boolean = False): TTMSFNCListBoxItem;
procedure LoadFromStrings(AStrings: TStrings);  procedure SaveToStrings(AStrings: TStrings);
procedure Sort(ACaseSensitive: Boolean = True; ASortingMode: TTMSFNCListBoxItemsSortMode = ismAscending);  procedure ClearSorting;
property Filter: TTMSFNCListBoxFilter;  procedure ApplyFilter;  procedure RemoveFilter;  procedure RemoveFilters;
```
- `Interaction`: `MultiSelect`, `Sorting` (`lcsNone, lcsNormal, lcsNormalCaseSensitive` = header-click sort), `Filtering.Enabled` (header dropdown), `Lookup.Enabled`, `DragDropMode` (`ldmNone, ldmMove, ldmCopy`), `Reorder`, `ClipboardMode` (`lcmNone, lcmTextOnly, lcmFull`).
- `ItemsAppearance`: `HeightMode` (`lihmFixed`/`lihmVariable`), `FixedHeight`, `Font`, `Fill`, `SelectedFill`, `ShowFocus`. `Header`: `Visible` (default False), `Text`, `Size`, `Fill`, `Font`, `HorizontalTextAlign`.
- Filter items: `Filter.Add` -> `Condition` (wildcards), `CaseSensitive`, `Prefix`, `Suffix`, `Operation` (`lfo...`); no `Column` property.
- Events: `OnItemSelected`, `OnItemClick`, `OnItemDblClick`: `procedure(Sender: TObject; AItem: TTMSFNCListBoxItem)`; `OnItemCompare(Sender; Item1, Item2: TTMSFNCListBoxItem; var ACompareResult: Integer)`; `OnBeforeDropItem(Sender; AFromItem, AToItem: TTMSFNCListBoxItem; var ACanDrop: Boolean)`, `OnAfterDropItem`, `OnItemAnchorClick`.

Demo (`VCL\Listbox`):
```delphi
TMSFNCListBox1.ItemsAppearance.HeightMode := lihmVariable;
TMSFNCListBox1.Header.Text := 'Birthday shopping list';
TMSFNCListBox1.Header.Visible := True;
TMSFNCListBox1.Interaction.DragDropMode := ldmMove;     // drag between two listboxes
TMSFNCListBox1.BitmapContainer := TMSFNCBitmapContainer1;
TMSFNCListBox1.BeginUpdate;
try
  TMSFNCListBox1.Items.Clear;
  for I := 0 to TMSFNCBitmapContainer1.ItemCount - 1 do
  begin
    it := TMSFNCListBox1.Items.Add;
    it.BitmapName := TMSFNCBitmapContainer1.BitmapNames[I];
    it.Text := it.BitmapName;
  end;
finally
  TMSFNCListBox1.EndUpdate;
end;
```

## TTMSFNCCheckedListBox

Descends from `TTMSFNCListBox`; every item shows a checkbox.
```delphi
function AddItem(AText: string = ''): TTMSFNCCheckedListBoxItem;   // reintroduced, typed result
property Checked[AItemIndex: Integer]: Boolean;
property CheckedItem[AItem: TTMSFNCCheckedListBoxItem]: Boolean;
function CheckedItems: TTMSFNCListBoxCheckedItems;   // array of TTMSFNCCheckedListBoxItem
procedure CheckAll;  procedure UncheckAll;
property OnItemCheckChanged: procedure(Sender: TObject; AItem: TTMSFNCCheckedListBoxItem) of object;
```
```delphi
lb := TTMSFNCCheckedListBox.Create(Self);
lb.Parent := Self;
lb.Align := alLeft;
lb.BeginUpdate;
lb.AddItem('Apples').Checked := True;
lb.AddItem('Pears');
lb.EndUpdate;
```

## TTMSFNCTableView (iOS-style list)

Also hosts an inner tree (`TreeView` property). Items can be grouped in alphabetic categories, have accessories, swipe "more options" and a detail control.
```delphi
// TTMSFNCTableViewItem (published): Text, Bitmap, BitmapName, HTMLTemplateItems, Checked, CheckType (tvictNone/tvictCheckBox/tvictRadioButton),
//   Accessory (tviaNone, tviaDetail, tviaProgress, tviaButton, tviaBadge, tviaCustom), AccessoryText, AccessoryProgress,
//   CategoryID, GroupIndex, DetailControl, Enabled, Visible, Height, TextColor, WordWrapping, HorizontalTextAlign, VerticalTextAlign
// public: Title, TitleExpanded, Data*, DBKey, IsSelected
function AddItem(AText: string = ''): TTMSFNCTableViewItem;   // or Items.Add
procedure RemoveItem(AItem: TTMSFNCTableViewItem);
property SelectedItem: TTMSFNCTableViewItem;  property ItemIndex;  function SelectedItemCount: Integer;
property Checked[AItemIndex: Integer]: Boolean;  function GetCheckedItems: TTMSFNCTableViewCheckedItems;  procedure CheckAllItems;  procedure UnCheckAllItems;
procedure StartEditMode;  procedure StopEditMode;  procedure ToggleEditMode;  function IsEditMode: Boolean;
procedure StartFiltering;  procedure StopFiltering;  procedure ApplyFilter;  procedure RemoveFilters;  property Filter: TTMSFNCTableViewFilter;
procedure ShowDetailControl(AItemIndex: Integer = -1);  procedure HideDetailControl;
procedure StartReload;  procedure StopReload;   // pull-to-reload (Reload property)
procedure Sort(ACaseSensitive: Boolean = True; ASortingMode: TTMSFNCTableViewItemsSortMode = tvismAscending);
procedure LookupCategory(ACategory: String);  procedure ScrollToItem(AItemIndex: Integer);
```
Published: `Header`, `Footer` (`Text`, `Visible`, `Font`, `Fill`), `ItemAppearance` (`HTMLTemplate`, `HeightMode` default `tvhmVariable`, `FixedHeight`, `Font`, `SelectedFill`), `CategoryType` (`tvctNone, tvctAlphaBetic, tvctAlphaNumericFirst, tvctAlphaNumericLast, tvctCustom`), `Categories` (custom: `Add` -> `Id`, `Text`, `LookupText`; items use `CategoryID`), `LookupBar`, `MoreOptions` (`Add` -> `Text`, `Color`, `BorderColor`, `FontColor`, `Width`), `DefaultItem`, `LayoutMode`, `Reload`, `Interaction` (`MultiSelect`, `ShowEditButton`, `ShowFilterButton`, `SwipeToShowMoreOptions`, `ShowDetailMode` `tvdtNone/tvdtAfterSelectItem`, `DragDropMode` `tvdmNone/tvdmMove/tvdmCopy`, `Reorder`, `Sorting` `tvcsNone/...`, `Lookup`, `Filtering`).

Events: `OnItemSelected`, `OnItemClick`, `OnItemDblClick`, `OnItemCheckChanged`, `OnItemAccessoryClick`: `(Sender: TObject; AItem: TTMSFNCTableViewItem)`; `OnItemSelectionChanged(Sender: TObject)`; `OnItemMoreOptionClick(Sender; AItem: TTMSFNCTableViewItem; AMoreOption: TTMSFNCTableViewMoreOption)`; `OnBeforeItemShowDetailControl(Sender; AItem; ADetailControl: TControl; var AAllow: Boolean)`; `OnItemCompare(Sender; Item1, Item2; var ACompareResult: Integer)`; `OnGetHTMLTemplateValue`.

Demo (`VCL\TableView`):
```delphi
TMSFNCTableView1.BeginUpdate;
try
  TMSFNCTableView1.BitmapContainer := TMSFNCBitmapContainer1;
  TMSFNCTableView1.Header.Text := 'Car List';
  TMSFNCTableView1.Items.Clear;
  TMSFNCTableView1.CategoryType := tvctAlphaBetic;
  TMSFNCTableView1.ItemAppearance.HTMLTemplate := '<b><#NAME></b><br/><font size="14" color="gcGray"><#DESCRIPTION></font>';
  it := TMSFNCTableView1.Items.Add;
  it.BitmapName := 'audi.png';
  it.HTMLTemplateItems.Values['NAME'] := 'Audi';
  it.HTMLTemplateItems.Values['DESCRIPTION'] := 'German manufacturer';
  it.CheckType := tvictCheckBox;
  it.Accessory := tviaBadge;
  it.AccessoryText := '5';
  TMSFNCTableView1.Items.Sort;
  mo := TMSFNCTableView1.MoreOptions.Add;   // swipe/edit-mode buttons
  mo.Text := 'Delete';
  mo.Color := gcRed;
  TMSFNCTableView1.Interaction.ShowEditButton := True;
  TMSFNCTableView1.DefaultItem.DetailControl := Panel1;
finally
  TMSFNCTableView1.EndUpdate;
end;

procedure TForm5.TMSFNCTableView1ItemMoreOptionClick(Sender: TObject; AItem: TTMSFNCTableViewItem; AMoreOption: TTMSFNCTableViewMoreOption);
begin
  if AMoreOption.Index = 0 then
    TMSFNCTableView1.RemoveItem(AItem);
end;
```

## TTMSFNCTileList (paged tile grid)

```delphi
// TTMSFNCTileListItem (published): Title, Description, Image, ImageName, ImagePosition (tipLeft, tipRight, tipTop, tipBottom, tipClient, tipCustom),
//   ImageWidth, ImageHeight, Badge, Control, ControlPosition (tcpBottom...), ColumnSpan, RowSpan, Empty, Visible, Enabled, CanSelect, Hint
// public: Selected, DataObject/DataString/DataInteger/DataBoolean, State
property Rows: Integer;  property Columns: Integer;            // grid per page
property NavigationMode: TTMSFNCTileListNavigationMode default tlnmPage;  // tlnmPage, tlnmScroll
property Orientation;  property PageIndex: Integer;  property PageCount: Integer;  // read-only
property MultiSelect: Boolean;  property SelectedItemIndex: Integer;   // SelectedItemIndex is public, not published
property ReorderMode: TTMSFNCTileListReorderMode default rmNone;  // rmRearrange, rmSwap, rmShift
property Filtering: TTMSFNCTileListFiltering default tlfAny;      // tlfAny, tlfStart
procedure ApplyFilter(AFilter: string);  procedure ClearFilter;
procedure SelectItem(AIndex: Integer);  procedure DeselectItem(AIndex: Integer);  procedure DeselectAllItems;  procedure SelectAllItems;
procedure NextPage;  procedure PreviousPage;  procedure FirstPage;  procedure LastPage;  procedure GoToPage(APageIndex: Integer);
function XYToItemIndex(X, Y: Single): Integer;
// events use an index, not an item:
OnItemClick / OnItemSelected / OnItemDeselected / OnItemDoubleClick: procedure(Sender: TObject; AItemIndex: Integer)
OnFilter: procedure(Sender: TObject; var AFilter: string; var AAllow: Boolean)
```
`Appearance`: `Fill`, `FillHover`, `FillDown`, `FillSelected`, `Stroke...`, `TitleFont`, `DescriptionFont`. `Header`/`Footer`: `Visible`, `Fill`, `ArrowLeft`/`ArrowRight`, `Bullets`.

Demo (`VCL\TileList`):
```delphi
TMSFNCTileList1.BeginUpdate;
try
  TMSFNCTileList1.Appearance.FillSelected.Color := gcDeepskyblue;
  TMSFNCTileList1.Items.Clear;
  for I := 0 to 13 do
  begin
    itm := TMSFNCTileList1.Items.Add;
    itm.Title := ' ';
    itm.Description := TileElements[I];
    itm.ImagePosition := tipTop;
    itm.ImageName := LowerCase(TileElements[I]) + '.svg';   // from BitmapContainer
    if I = 3 then
      itm.ColumnSpan := 2;
  end;
finally
  TMSFNCTileList1.EndUpdate;
end;
TMSFNCTileList1.ReorderMode := rmSwap;
```

## TTMSFNCSearchList (VCL/FMX; type names have NO TTMSFNC prefix)

Multi-column filterable list with category rows; used by `TTMSFNCSearchEdit`.
```delphi
// Items: TSearchList (collection of TSearchListItem)
function Add: TSearchListItem; overload;
function Add(ACaption: string; ADescription: string = ''): TSearchListItem; overload;
function Add(ACaption: string; ADescription: string; AObject: TObject = nil): TSearchListItem; overload;
procedure LoadStrings(Value: TStrings);
procedure Sort(AColumn: Integer; ADirection: TSortDirection = sdUp; CaseSensitive: boolean = true);   // sdDown, sdUp
// TSearchListItem: Captions[AIndex], Descriptions[AIndex], ImageIndexes[AIndex], &Object, CategoryID, ItemType (itItem, itCategory), Columns[i].Picture
// Columns: TColumnItems (Add -> TColumnItem: Width, Font, ControlFont, Color, Alignment, WordWrap)
// Categories: TCategoryList: function Add(Caption: string; ID: integer): TCategoryItem;  TCategoryItem.Filter: Boolean
property FilterCondition: TFilterCondition;   // Text, Column, FilterType (mText, mEntireWord, mStartWord, mEndWord), FilterData (fdText, fdDescription, fdAll),
                                              // CaseSensitive, AllColumns, Categories, CategoryItems, MaxCategoryItems, AutoSelect
procedure UpdateFilter;  procedure ClearFilter;
property ItemIndex: integer;  function SelectedItem: TSearchListItem;  property ItemHeight;  property Images: TCustomImageList;
OnItemClick / OnItemChange: procedure(Sender: TObject; ItemIndex: Integer; Item: TSearchListItem)
OnFilterItem: procedure(Sender: TObject; AItem: TSearchListItem; var Retain: boolean)
```
Demo (`VCL\SearchList`):
```delphi
TMSFNCSearchList1.BeginUpdate;
for i := 0 to sl.Count - 1 do
begin
  sli := TMSFNCSearchList1.Items.Add(sl[i]);
  sli.CategoryID := catid;
end;
TMSFNCSearchList1.EndUpdate;
TMSFNCSearchList1.FilterCondition.FilterType := mStartWord;
TMSFNCSearchList1.FilterCondition.CaseSensitive := False;

procedure TForm1.Edit1Change(Sender: TObject);
begin
  TMSFNCSearchList1.FilterCondition.Text := Edit1.Text;
  TMSFNCSearchList1.UpdateFilter;              // filter is NOT applied until UpdateFilter
end;
```

## TTMSFNCResponsiveList (VCL/FMX; type names have NO TTMSFNC prefix)

HTML-template card list whose layout switches by width/height via `Conditions`.
```delphi
// Items: TResponsiveListItems.Add -> TResponsiveListItem: Content (HTML), HeaderText, FooterText, Values[AName]: variant,
//   Color, HeaderColor, Width/WidthType, Height/HeightType (isAuto, isFixed, isPerc, isFill), Selected, Control
// Conditions: TResponsiveConditions.Add -> TResponsiveCondition: WidthFrom, WidthTo, HeightFrom, HeightTo, Columns, Rows,
//   ItemWidth, ItemHeight, Template, HeaderTemplate, FooterTemplate, Category
property FilterCondition: TResponsiveListItemFilter;  // Text, FilterData [fdContent, fdHeader, fdFooter], FilterType, CaseSensitive
procedure UpdateFilter;  procedure ClearFilter;  property ItemIndex: Integer;  property MultiSelect: boolean;
OnItemClick / OnItemDblClick / OnAfterSelectItem: procedure(Sender: TObject; AItem: TResponsiveListItem)
```
A condition `Template` uses `(#NAME)` placeholders replaced from `Item.Values['NAME']`. Demo (`VCL\ResponsiveList`):
```delphi
TMSFNCResponsiveList1.BeginUpdate;
try
  TMSFNCResponsiveList1.Items.Add.Content := '<B>' + Name + '</B><BR>' + Description;
finally
  TMSFNCResponsiveList1.EndUpdate;
end;
```

## TTMSFNCListEditor (tag/token editor)

```delphi
// Items: TTMSFNCCustomListEditorItems.Add -> TTMSFNCCustomListEditorItem: Text, Value, LeftImage, RightImage, LeftImageName, RightImageName, Tag; public DataString/DataInteger/DataObject
property SelectedItemIndex: Integer default -1;  property ReadOnly: Boolean;
property ItemAppearance;   // FillNormal, FillSelected, FontColorNormal, FontColorSelected, StrokeNormal, StrokeSelected, RoundingNormal, RoundingSelected, Font, DefaultLeftImageName...
OnItemClick / OnItemLeftImageClick / OnItemRightImageClick / OnItemDelete / OnItemInsert: procedure(Sender: TObject; AItemIndex: Integer)
OnItemCanDelete: (Sender; AItemIndex: Integer; var ACanDelete: Boolean)
OnItemUpdate:    (Sender; AItemIndex: Integer; var AText: String)
```
Demo (`VCL\ListEditor`): `TMSFNCListEditor2.SelectedItemIndex := 0; Label4.Caption := TMSFNCListEditor2.Items[0].Value;` and `OnItemClick` reads `Items[AItemIndex].Value`.

## TTMSFNCCategoryList (not on palette)

Bitmap category bar (vertical/horizontal) with optional popup per item. `Items.Add`, `AddCategoryItem(ABitmapName: string)`, item `Bitmaps`, `PopupControl`, `CanSelect`, `Separator`; `Mode` (`clmHorizontal`, `clmVertical`), `SelectedItemIndex`, `OnItemClick/OnItemSelected(Sender; AItemIndex: Integer)`. Item `Text` is protected (no caption text in the published API).

## Platform notes

- ListBox, CheckedListBox, TableView, TileList, ListEditor, CategoryList: VCL/FMX/WEB/LCL. `LoadFromFile/SaveToFile/LoadFromStream/SaveToStream` on ListBox and TableView are `{$IFNDEF WEBLIB}` (TableView's `SaveToStrings` too).
- SearchList and ResponsiveList: no `WEBLib.` unit. They use `TFont`/`TCustomImageList`/`TColor`-style members (`clNone`, `clGray`), unlike the gc*/TTMSFNCGraphicsFont API of the others.
- `Sort` is `reintroduce` on FMX for ListBox/TableView (same call syntax).

## Does not exist / common mistakes

- `ListBox.Items.Add('x')` returning an index / `Items.AddObject` / `Items.Strings[i]` / `Items.Text` — `Items.Add(AText)` returns a `TTMSFNCListBoxItem`; use `Items[i].Text`, `DataObject`, `LoadFromStrings`/`SaveToStrings`.
- `ListBox.Sorted`, `ListBox.MultiSelect`, `ListBox.Selected[i]` — use `Interaction.Sorting` / `Sort`, `Interaction.MultiSelect`, `Items[i].IsSelected` / `SelectedItems[]`.
- `OnClickCheck` / `OnCheckChanged` on the checked listbox — it is `OnItemCheckChanged`. Plain `TTMSFNCListBox` items have a public `Checked` but no checkbox; use `TTMSFNCCheckedListBox`.
- Editing a ListBox item in place — there is no inplace editing in TTMSFNCListBox; use TTMSFNCTreeView (one column) or TTMSFNCTableView edit mode.
- `TileListItem.Text`/`Caption` — use `Title` and `Description`. Tile list events give `AItemIndex: Integer`, not an item.
- `TTMSFNCSearchListItem`, `TTMSFNCSearchListColumn` — the real classes are `TSearchListItem`, `TColumnItem`, `TCategoryItem`; `Items.Add.Caption` does not exist, use `Captions[0]`.
- Setting `SearchList.FilterCondition.Text` and expecting the list to filter — call `UpdateFilter`.
- `ResponsiveList.Items.Add.Text` / `.HTML` — use `Content`; template placeholders are `(#NAME)` not `<#NAME>` (the `<#NAME>` form belongs to TableView/Kanban `HTMLTemplate`).
- TableView enum prefixes are `tv...` (`tvictCheckBox`, `tviaBadge`, `tvctAlphaBetic`), not the TreeView `tvnt...`/`tcs...` ones; ListBox uses `l...` (`ldmMove`, `lcsNormal`, `lihmVariable`).
