# Kanban board (TTMSFNCKanbanBoard, TTMSFNCKanbanBoardDatabaseAdapter)
> Sections (line ranges): 8-17 Units and palette · 18-50 Columns · 51-83 Items · 84-100 Board-level members · 101-117 Events · 118-164 Example: board built in code · 165-208 TTMSFNCKanbanBoardDatabaseAdapter · 209-213 Platform notes · 214-227 Does not exist / common mistakes

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCKanbanBoard`, `*.TMSFNCKanbanBoardDatabaseAdapter`; demo `Shared Code\Business Logic\Kanban Board\UBL.pas` (used by `VCL\Kanban Board`, `FMX\Kanban Board`, LCL and WEB).

The board is a horizontal row of **columns**; each column owns its own `Items` collection and renders them with an embedded `TTMSFNCKanbanBoardTableView` (a `TTMSFNCTableView` descendant). There is no board-level `Items` list.

## Units and palette

```delphi
uses
  VCL.TMSFNCKanbanBoard,                  // TTMSFNCKanbanBoard, column/item classes, kb* enums
  VCL.TMSFNCKanbanBoardDatabaseAdapter,   // TTMSFNCKanbanBoardDatabaseAdapter
  VCL.TMSFNCGraphicsTypes;                // gc* colors, gta* alignment
```
Prefix rule: `VCL.` / `FMX.` / `WEBLib.` / `LCLTMSFNC...`. Palette **TMS FNC UI**: `TTMSFNCKanbanBoard`, `TTMSFNCKanbanBoardDatabaseAdapter`. Both exist on VCL, FMX, WEB, LCL.

## Columns (TTMSFNCKanbanBoardColumn)

```delphi
// TTMSFNCKanbanBoardColumns
function Add: TTMSFNCKanbanBoardColumn;
function Insert(Index: Integer): TTMSFNCKanbanBoardColumn;
property Items[Index: Integer]: TTMSFNCKanbanBoardColumn; default;

// TTMSFNCKanbanBoardColumn, published
property HeaderText: String;   property FooterText: String;   property Name: String;
property HeaderVisible: Boolean default True;   property FooterVisible: Boolean default False;
property HeaderHorizontalTextAlign: TTMSFNCGraphicsTextAlign default gtaCenter;
property Width: Double;   property CollapsedWidth: Double;   property Visible: Boolean;
property Expandable: Boolean default False;   property Expanded: Boolean default True;   // collapse whole column
property Items: TTMSFNCKanbanBoardItems;
property Sorting: TTMSFNCKanbanBoardSorting default kbsNone;   // kbsNone, kbsNormal, kbsNormalCaseSensitive
property ShowFilterButton: Boolean default False;
property Filter: TTMSFNCTableViewFilter;
property UseDefaultAppearance: Boolean default True;   // False -> Fill, Stroke, HeaderFill, HeaderFont, FooterFill...
// public
function AddItem(AText: string = ''): TTMSFNCKanbanBoardItem;
procedure RemoveItem(AItem: TTMSFNCKanbanBoardItem);
function MoveItem(AItem: TTMSFNCKanbanBoardItem; AToColumn: TTMSFNCKanbanboardColumn; AIndex: Integer = -1): TTMSFNCKanbanBoardItem;
function CopyItem(AItem: TTMSFNCKanbanBoardItem; AToColumn: TTMSFNCKanbanboardColumn; AIndex: Integer = -1): TTMSFNCKanbanBoardItem;
function FindItem(AIndex: Integer): TTMSFNCKanbanBoardItem;
property SelectedItem: TTMSFNCKanbanBoardItem;   property ItemIndex: Integer;
procedure SelectItem(AItemIndex: Integer);   procedure ClearSelection;   procedure ScrollToItem(AItemIndex: Integer);
procedure StartFiltering;  procedure StopFiltering;  procedure ApplyFilter;  procedure RemoveFilters;
procedure StartEditMode;   procedure StopEditMode;
property KanbanBoard: TTMSFNCCustomKanbanBoard;   property TableView: TTMSFNCKanbanBoardTableView;
property DataObject / DataString / DataInteger / DataPointer / DataBoolean; property DBKey: String;
```

## Items (TTMSFNCKanbanBoardItem)

```delphi
// TTMSFNCKanbanBoardItems (per column)
function Add: TTMSFNCKanbanBoardItem;
function Insert(Index: Integer): TTMSFNCKanbanBoardItem;
procedure Clear;
procedure Sort(ACaseSensitive: Boolean = True; ASortingMode: TTMSFNCKanbanBoardItemsSortMode = kbismAscending);
property Column: TTMSFNCKanbanBoardColumn;

// TTMSFNCKanbanBoardItem, published
property Title: String;          // bold first line
property Text: String;           // body (mini-HTML: <font>, <img src="name.png"> from BitmapContainer, <br/>)
property HTMLTemplateItems: TStringList;   // values for ItemsAppearance.HTMLTemplate '<#NAME>'
property Bitmap: TTMSFNCBitmap;  property BitmapName: string;
property Color: TTMSFNCGraphicsColor default gcWhite;
property UseDefaultAppearance: Boolean default True;   // set False for Color/TextColor/TitleColor/StrokeColor to apply
property TextColor, TitleColor, SelectedColor, StrokeColor: TTMSFNCGraphicsColor;
property MarkType: TTMSFNCKanbanBoardMarkTypes default [];   // set of kbmtLeft, kbmtTop, kbmtRight, kbmtBottom
property MarkColor: TTMSFNCGraphicsColor default gcRed;      // + MarkColorLeft/Top/Right/Bottom, MarkSizeLeft..., MarkRounding
property Rounding: Integer;  property RoundingCorners: TTMSFNCGraphicsCorners;
property Expandable: Boolean default False;  property Expanded: Boolean default True;  // collapse Text, keep Title
property Movable: Boolean default True;      // False = cannot be dragged
property Enabled, Visible: Boolean;  property Height: Double;  property Tag: NativeInt;
// public
function MoveItem(AToColumn: TTMSFNCKanbanBoardColumn; AIndex: Integer = -1): TTMSFNCKanbanBoardItem;  // returns the NEW item
function CopyItem(AToColumn: TTMSFNCKanbanBoardColumn; AIndex: Integer = -1): TTMSFNCKanbanBoardItem;
procedure SelectItem;   function IsSelected: Boolean;
property Column: TTMSFNCKanbanBoardColumn;
property DataObject / DataString / DataInteger / DataPointer / DataBoolean; property DBKey: String;
```
`Checked` / `CheckType` exist on the item but are **protected** (not usable from application code).

## Board-level members

```delphi
property Columns: TTMSFNCKanbanBoardColumns;
property ColumnsAppearance: TTMSFNCKanbanBoardColumnsAppearance;  // Margins, Spacing, HeaderSize, FooterSize, HeaderFont, HeaderFill, HeaderStroke, Fill, Stroke
property ItemsAppearance: TTMSFNCKanbanBoardItemsAppearance;      // Font, TitleFont, Fill, Stroke, SelectedFill, SelectedStroke, Spacing, Margins,
                                                                  // HeightMode (kbhmFixed, kbhmVariable default), FixedHeight, HTMLTemplate, ShowFocus
property Interaction: TTMSFNCKanbanBoardInteraction;
property BitmapContainer: TTMSFNCBitmapContainer;   property GlobalFont;   property Adapter: TTMSFNCKanbanBoardAdapter;
property SelectedItem: TTMSFNCKanbanBoardItem;
procedure SelectItem(AItem: TTMSFNCKanbanBoardItem);
procedure ClearSelection;   procedure ClearItems;   // ClearItems empties all columns
function XYToColumn(X, Y: Single): TTMSFNCKanbanBoardColumn;
function FindItemWithDBKey(ADBKey: String): TTMSFNCKanbanBoardItem;
```
`Interaction` (TTMSFNCKanbanBoardInteraction): `DragDropMode: TTMSFNCKanbanBoardDragDropMode default kbdmNone` (`kbdmNone`, `kbdmMove`, `kbdmCopy`), `DirectDrag` (default False: long-press/delayed drag), `MultiSelect`, `Editing` (default False), `MouseEditMode` (`kbemDoubleClick`, `kbemSingleClick`, `kbemSingleClickOnSelectedItem`), `KeyboardEdit`, `TouchScrolling`, `AutoOpenURL`.

## Events

```delphi
OnSelectItem:    procedure(Sender: TObject; AColumn: TTMSFNCKanbanBoardColumn; AItem: TTMSFNCKanbanBoardItem) of object;
OnItemClick, OnItemDblClick: procedure(Sender: TObject; AColumn: TTMSFNCKanbanBoardColumn; AItem: TTMSFNCKanbanBoardItem) of object;
OnBeforeDropItem: procedure(Sender: TObject; AFromColumn, AToColumn: TTMSFNCKanbanBoardColumn; AFromItem, AToItem: TTMSFNCKanbanBoardItem; var ACanDrop: Boolean) of object;
OnAfterDropItem:  procedure(Sender: TObject; AFromColumn, AToColumn: TTMSFNCKanbanBoardColumn; AFromItem, AToItem: TTMSFNCKanbanBoardItem) of object;
OnUpdateItemText: procedure(Sender: TObject; AColumn: TTMSFNCKanbanBoardColumn; AItem: TTMSFNCKanbanBoardItem; AText: String) of object;
OnItemCompare:   procedure(Sender: TObject; AColumn: TTMSFNCKanbanBoardColumn; Item1, Item2: TTMSFNCKanbanBoardItem; var ACompareResult: Integer) of object;
OnColumnCollapse, OnColumnExpand, OnItemCollapse, OnItemExpand: column/item notifications
OnCustomizeColumn: procedure(Sender: TObject; AColumn: TTMSFNCKanbanBoardColumn; ATableView: TTMSFNCKanbanBoardTableView) of object;
OnItemCustomDrawMark: procedure(Sender: TObject; AGraphics: TTMSFNCGraphics; ARect: TRectF; AMarkType: TTMSFNCKanbanBoardMarkType; AColumn: TTMSFNCKanbanBoardColumn; AItem: TTMSFNCKanbanBoardItem) of object;
OnDoneButtonClicked: procedure(Sender: TObject; AColumn: TTMSFNCKanbanBoardColumn) of object;
// also OnBefore/AfterDrawItem, ...DrawItemText, ...DrawItemTitle, ...DrawItemIcon, OnItemTextAnchorClick, OnItemTitleAnchorClick, OnColumnAnchorClick, OnBefore/AfterApplyFilter
```
`OnAfterDropItem` resolves `AFromItem`/`AToItem` by index (`Column.FindItem(Index)`) after the inner table view has processed the drop, so either can be `nil`: always test `Assigned(...)`, and rely on `AFromColumn`/`AToColumn` for the move itself.

## Example: board built in code

```delphi
procedure TForm1.FormCreate(Sender: TObject);
var
  kb: TTMSFNCKanbanBoard;
  c: TTMSFNCKanbanBoardColumn;
  it: TTMSFNCKanbanBoardItem;
begin
  kb := TTMSFNCKanbanBoard.Create(Self);
  kb.Parent := Self;
  kb.Align := alClient;                        // FMX: TAlignLayout.Client
  kb.BeginUpdate;
  try
    kb.Interaction.DragDropMode := kbdmMove;   // default kbdmNone: no dragging!
    c := kb.Columns.Add;
    c.HeaderText := 'TO DO';
    c.Expandable := True;
    it := c.Items.Add;                         // or c.AddItem('...')
    it.Title := 'Fix issue';
    it.Text := 'Fix issue in FNC Core';
    it.MarkType := [kbmtLeft];
    it.MarkColor := gcRed;
    c := kb.Columns.Add;
    c.HeaderText := 'IN PROGRESS';
    c.Sorting := kbsNormal;
    c.ShowFilterButton := True;
    c := kb.Columns.Add;
    c.HeaderText := 'DONE';
  finally
    kb.EndUpdate;
  end;
  kb.OnAfterDropItem := KanbanAfterDropItem;
end;

procedure TForm1.KanbanAfterDropItem(Sender: TObject; AFromColumn, AToColumn: TTMSFNCKanbanBoardColumn;
  AFromItem, AToItem: TTMSFNCKanbanBoardItem);
begin
  if Assigned(AToColumn) then
    Caption := 'Dropped in ' + AToColumn.HeaderText;
end;

// programmatic move (returns the new item instance in the target column):
// it := kb.Columns[0].Items[0].MoveItem(kb.Columns[2]);
```
Delete an item: `it.Column.Items.Delete(it.Index)` (demo) or `it.Column.RemoveItem(it)`.

## TTMSFNCKanbanBoardDatabaseAdapter

Loads one record per item and puts it in the column whose **index** equals the integer value of the `Column` field.
```delphi
property KanbanBoard: TTMSFNCCustomKanbanBoard;     // assigns board.Adapter
property Active: Boolean;
property Item: TTMSFNCKanbanBoardDatabaseAdapterItemSource;
//   Item.DataSource: TDataSource; Item.Title, Item.Text, Item.Column, Item.DBKey: String (field names);
//   Item.AutoIncrementDBKey: Boolean default True
OnFieldsToItem:   procedure(Sender: TObject; AFields: TFields; AItem: TTMSFNCKanbanBoardItem) of object;     // extra fields -> item
OnItemToFields:   procedure(Sender: TObject; AItem: TTMSFNCKanbanBoardItem; AFields: TFields) of object;     // item -> extra fields
OnFieldsToColumn: procedure(Sender: TObject; AFields: TFields; AColumnField: TField; var AColumn: Integer; var AAcceptItem: Boolean) of object;
OnColumnToFields: procedure(Sender: TObject; AColumn: Integer; AFields: TFields; AColumnField: TField) of object;
OnItemCreateDBKey: procedure(Sender: TObject; AItem: TTMSFNCKanbanBoardItem; var ADBKey: string) of object;
OnItemInserted, OnItemUpdated, OnItemRead: procedure(Sender: TObject; AItem: TTMSFNCKanbanBoardItem) of object;
procedure LoadItems;
```
Demo (`UBL.pas`, condensed): fields ID, Title, Description, Priority, Status (0..2), Color.
```delphi
FKanbanBoard.Interaction.DragDropMode := kbdmMove;
FAdapter := TTMSFNCKanbanBoardDatabaseAdapter.Create(AForm);
FAdapter.KanbanBoard := FKanbanBoard;
FAdapter.Item.DataSource := FDataSource;
FAdapter.Item.Title := 'Title';
FAdapter.Item.Text := 'Description';
FAdapter.Item.DBKey := 'ID';
FAdapter.Item.Column := 'Status';            // integer field = column index
FKanbanBoard.Columns.Add.HeaderText := 'TO DO';        // columns must exist for every Status value
FKanbanBoard.Columns.Add.HeaderText := 'IN PROGRESS';
FKanbanBoard.Columns.Add.HeaderText := 'DONE';
FAdapter.OnFieldsToItem := DoFieldsToItem;
FAdapter.Active := True;
FDataSet.Active := True;

procedure TKanbanBoardLogic.DoFieldsToItem(Sender: TObject; AFields: TFields; AItem: TTMSFNCKanbanBoardItem);
begin
  AItem.UseDefaultAppearance := False;
  AItem.Color := AFields.FieldByName('Color').AsInteger;
  if AFields.FieldByName('Priority').AsInteger = 1 then
    AItem.MarkType := [kbmtLeft];
end;
```
Dragging an item to another column writes the new column index back to the `Column` field.

## Platform notes

- Same API on VCL, FMX, WEB, LCL. On FMX the internal key handlers carry `var KeyChar: WideChar`; this does not affect the public events above.
- WEB demo uses `WEBLib.CDS` (`TClientDataSet`) with the same adapter code; LCL uses `TMemDataSet`.

## Does not exist / common mistakes

- `KanbanBoard.Items`, `KanbanBoard.AddItem(Column, ...)`, `Columns[i].Cards` — items live in `Columns[i].Items` (`Add`) or `Columns[i].AddItem(AText)`.
- `Column.Caption` / `Column.Title` / `Column.Header` — use `HeaderText` (and `FooterText` + `FooterVisible := True`).
- `Item.Caption` / `Item.Description` / `Item.Header` — use `Title` and `Text`.
- `Item.Color` ignored — set `Item.UseDefaultAppearance := False` first (same for `TextColor`, `TitleColor`).
- Dragging does nothing — `Interaction.DragDropMode` defaults to `kbdmNone`; set `kbdmMove` (or `kbdmCopy`). There is no `AllowDrag`/`DragMode`/`AllowMove` property; block per item with `Movable := False` or `ACanDrop := False` in `OnBeforeDropItem`.
- `OnItemMoved` / `OnDragDrop` / `OnItemDropped` — use `OnAfterDropItem` (and `OnBeforeDropItem` to veto).
- `Item.Column := OtherColumn` to move — `Column` is read-only; use `Item.MoveItem(OtherColumn)` and continue with the returned item (the original is freed).
- `Item.Checked` / checkboxes on cards — protected; not available.
- `OnItemSelected` / `OnSelectionChanged` on the board — it is `OnSelectItem(Sender, AColumn, AItem)`.
- `Item.Priority` / `Item.DueDate` / `Item.Tags` — no such fields; store data in `DataObject`/`DataString`/`DBKey` or `HTMLTemplateItems`, and visualize with `MarkType`/`MarkColor`.
- DB adapter `DataSource`, `FieldTitle`, `FieldColumn` at top level — the field mapping is under `Adapter.Item` (`Item.DataSource`, `Item.Title`, `Item.Text`, `Item.Column`, `Item.DBKey`); the column field is an **integer index**, map strings with `OnFieldsToColumn`/`OnColumnToFields`.
