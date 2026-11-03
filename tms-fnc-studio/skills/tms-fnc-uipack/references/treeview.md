# Tree view (TTMSFNCTreeView, TTMSFNCCheckedTreeView, TTMSFNCDirectoryTreeView, TTMSFNCTreeViewDatabaseAdapter)

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCTreeView`, `*.TMSFNCCustomTreeView`, `*.TMSFNCTreeViewData`, `*.TMSFNCTreeViewBase`, `*.TMSFNCCheckedTreeView`, `*.TMSFNCDirectoryTreeView`, `*.TMSFNCTreeViewDatabaseAdapter`, demo `VCL\TreeView`.

TTMSFNCTreeView is a multi-column, multi-level tree. Class chain: `TTMSFNCTreeViewBase` -> `TTMSFNCTreeViewData` (nodes, columns, filter, navigation) -> `TTMSFNCCustomTreeView` (events, selection, editing) -> `TTMSFNCTreeViewPublished` -> `TTMSFNCTreeView`. It works in **two modes** that share one rendering engine:

- **Collection mode**: you fill `Nodes` (persistent `TTMSFNCTreeViewNode` objects with per-column `Values`).
- **Virtual mode**: you assign `OnGetNumberOfNodes` + `OnGetNodeText` and keep the data yourself. Events receive `TTMSFNCTreeViewVirtualNode`; its `.Node` is `nil` in virtual mode.

## Units and palette

```delphi
uses
  VCL.TMSFNCTreeView,          // TTMSFNCTreeView
  VCL.TMSFNCTreeViewData,      // TTMSFNCTreeViewNode, TTMSFNCTreeViewColumn, TTMSFNCTreeViewVirtualNode, tcet*/tvnt*/nsm*/tcs* enums
  VCL.TMSFNCCustomTreeView,    // event types, tnhm*/tsa*/tcm*/tdm*/tmem* enums
  VCL.TMSFNCTreeViewBase,
  VCL.TMSFNCGraphicsTypes;     // gta*, gc* colors
// + VCL.TMSFNCCheckedTreeView, VCL.TMSFNCDirectoryTreeView, VCL.TMSFNCTreeViewDatabaseAdapter
```
Prefix rule: `VCL.` / `FMX.` / `WEBLib.` / `LCLTMSFNC...` (Lazarus has no dot). Palette **TMS FNC UI**: `TTMSFNCTreeView`, `TTMSFNCCheckedTreeView`. `TTMSFNCDirectoryTreeView` is in the runtime package but **not registered on the palette**: create it in code. `TTMSFNCTreeViewDatabaseAdapter` is **not in any installed package** in 7.3.1.2 (VCL, FMX, WEB, LCL): it is not on the palette and its unit is not compiled, so `uses ...TMSFNCTreeViewDatabaseAdapter` usually fails. Show dataset data by filling the nodes in code (see the adapter section below).

## Columns (TTMSFNCTreeViewColumn, `TreeView.Columns`)

```delphi
function Add: TTMSFNCTreeViewColumn;            // Columns.Add
function Insert(Index: Integer): TTMSFNCTreeViewColumn;
// published on the column:
property Text: String;                          // header caption (Name is an identifier, not the caption)
property Name: String;
property Width: Double;   property MinimumWidth: Double;   property Visible: Boolean;
property HorizontalTextAlign / VerticalTextAlign: TTMSFNCGraphicsTextAlign;  // gtaLeading, gtaCenter, gtaTrailing
property WordWrapping: Boolean;  property Trimming: TTMSFNCGraphicsTextTrimming;
property EditorType: TTMSFNCTreeViewColumnEditorType default tcetNone;  // tcetEdit, tcetComboBox, tcetMemo, tcetNone
property EditorItems: TStringList;              // combobox items
property CustomEditor: Boolean;                 // use OnGetInplaceEditor
property Sorting: TTMSFNCTreeViewColumnSorting default tcsNone; // tcsNormal, tcsRecursive, tcsNormalCaseSensitive, tcsRecursiveCaseSensitive
property Filtering: TTMSFNCTreeViewColumnFiltering;  // .Enabled, .DropDownWidth, .DropDownHeight, .MultiColumn, .ButtonSize
property UseDefaultAppearance: Boolean default True; // set False to use Fill/Stroke/Font/TopFill/TopFont/... below
property Fill, TopFill, BottomFill: TTMSFNCGraphicsFill;  property Font, TopFont, BottomFont: TTMSFNCGraphicsFont;
property HTMLTemplate: string;
procedure Sort(ARecurse: Boolean = False; ACaseSensitive: Boolean = True; ASortingMode: TTMSFNCTreeViewNodesSortMode = nsmAscending);
```
Tree-level: `ClearColumns`, `FindColumnByName(AName)`, `FindColumnIndexByName(AName)`. `ColumnsAppearance`: `Stretch`, `StretchColumn` (default -1), `StretchAll` (default True), `Layouts: [tclTop, tclBottom]`, `TopSize`, `TopFont`, `TopFill`, `FillEmptySpaces`, `SortIndicatorColor`. `Groups.Add` gives a `TTMSFNCTreeViewGroup` (`Text`, `StartColumn`, `EndColumn`) spanning header columns.

## Collection mode: nodes

```delphi
// TTMSFNCTreeViewData
function AddNode(AParentNode: TTMSFNCTreeViewNode = nil): TTMSFNCTreeViewNode;
function InsertNode(AIndex: Integer; AParentNode: TTMSFNCTreeViewNode = nil): TTMSFNCTreeViewNode;
procedure RemoveNode(ANode: TTMSFNCTreeViewNode);
procedure ClearNodes;          // nodes only
procedure ClearNodeList;       // rebuilds the internal display structure (not the data)
procedure MoveNode(ANode, ADestinationNode: TTMSFNCTreeViewNode; AIndex: Integer = -1);
procedure CopyNode(ANode, ADestinationNode: TTMSFNCTreeViewNode; AIndex: Integer = -1);
property Nodes: TTMSFNCTreeViewNodes;  // root collection; Nodes.Add / Nodes.Insert(i) / Nodes[i]; Nodes.Sort(...)

// TTMSFNCTreeViewNode (TCollectionItem)
property Text[AColumn: Integer]: String;          // auto-creates Values up to AColumn
property Checked[AColumn: Integer]: Boolean;
property CheckTypes[AColumn: Integer]: TTMSFNCTreeViewNodeCheckType;   // tvntNone, tvntCheckBox, tvntRadioButton
property CollapsedIconNames[AColumn: Integer; ALarge: Boolean]: String; // names from BitmapContainer
property ExpandedIconNames[AColumn: Integer; ALarge: Boolean]: String;
property CollapsedIcons / ExpandedIcons[AColumn: Integer; ALarge: Boolean]: TTMSFNCBitmap;
property Values: TTMSFNCTreeViewNodeValues;   // one TTMSFNCTreeViewNodeValue per column (Text, Checked, CheckType, icons, HTMLTemplateItems)
property Nodes: TTMSFNCTreeViewNodes;         // children: Node.Nodes.Add
property Expanded: Boolean;  property Enabled: Boolean;  property Extended: Boolean;  // Extended = full-width category row
property DataPointer / DataBoolean / DataObject / DataString / DataInteger; property DBKey: String; property Tag: NativeInt;
property VirtualNode: TTMSFNCTreeViewVirtualNode;
function GetParent: TTMSFNCTreeViewNode;  function GetChildCount: Integer;
function GetFirstChild / GetLastChild / GetNext / GetPrevious / GetNextSibling / GetPreviousSibling: TTMSFNCTreeViewNode;
procedure Expand(ARecurse: Boolean = False);  procedure Collapse(ARecurse: Boolean = False);
procedure MoveTo(ADestination: TTMSFNCTreeViewNode; AIndex: Integer = -1);
procedure CopyTo(ADestination: TTMSFNCTreeViewNode; AIndex: Integer = -1);
```
Lookup: `FindNodeByTextAndColumn(AText: string; AColumn: Integer; ARecurse: Boolean = False; ACaseSensitive: Boolean = True)`, `FindNodeByDBKey(ADBKey)`, `GetFirstRootNode`, `GetRootNodeByIndex(AIndex)`, `GetTotalNodeCount`.

Demo (`VCL\TreeView`, condensed):
```delphi
procedure TForm1.FormCreate(Sender: TObject);
var
  pn, n: TTMSFNCTreeViewNode;
  c: TTMSFNCTreeViewColumn;
begin
  TMSFNCTreeView1.BeginUpdate;
  try
    TMSFNCTreeView1.ClearColumns;
    TMSFNCTreeView1.ClearNodes;
    TMSFNCTreeView1.NodesAppearance.HeightMode := tnhmVariable;   // needed for WordWrapping rows
    c := TMSFNCTreeView1.Columns.Add;
    c.Text := 'Item';
    c.Width := TMSFNCTreeView1.ScalePaintValue(120);
    c := TMSFNCTreeView1.Columns.Add;
    c.Text := 'Amount';
    c.EditorType := tcetEdit;                                     // column is NOT editable otherwise
    c := TMSFNCTreeView1.Columns.Add;
    c.Text := 'Delivery';
    c.EditorType := tcetComboBox;
    c.EditorItems.Add('Standard');
    c.EditorItems.Add('Express');

    pn := TMSFNCTreeView1.AddNode;          // root
    pn.Text[0] := 'Cakes';
    pn.Extended := True;
    n := TMSFNCTreeView1.AddNode(pn);       // child (same as pn.Nodes.Add)
    n.Text[0] := 'Chocolate';
    n.Text[1] := '12';
    n.Text[2] := 'Standard';
    n.CheckTypes[0] := tvntCheckBox;
    n.Checked[0] := True;
    n.CollapsedIconNames[0, False] := 'cake1.png';   // requires TreeView.BitmapContainer
    n.ExpandedIconNames[0, False] := 'cake1.png';
    TMSFNCTreeView1.ExpandAll;
  finally
    TMSFNCTreeView1.EndUpdate;
  end;
end;
```
Runtime creation: `TV := TTMSFNCTreeView.Create(Self); TV.Parent := Self; TV.Align := alClient;` (FMX: `TAlignLayout.Client`), then the code above.

## Virtual mode

```delphi
TTMSFNCTreeViewGetNumberOfNodesEvent = procedure(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode; var ANumberOfNodes: Integer) of object;
TTMSFNCTreeViewGetNodeTextEvent = procedure(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode; AColumn: Integer; AMode: TTMSFNCTreeViewNodeTextMode; var AText: String) of object;  // AMode: tntmDrawing, tntmEditing
TTMSFNCTreeViewIsNodeExpandedEvent = procedure(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode; var AExpanded: Boolean) of object;
TTMSFNCTreeViewGetNodeCheckTypeEvent = procedure(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode; AColumn: Integer; var ACheckType: TTMSFNCTreeViewNodeCheckType) of object;
TTMSFNCTreeViewIsNodeCheckedEvent = procedure(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode; AColumn: Integer; var AChecked: Boolean) of object;
// also: OnGetNodeIcon, OnIsNodeExtended, OnIsNodeVisible, OnIsNodeEnabled, OnGetNodeColor, OnGetNodeTextColor, OnGetNodeHeight, OnGetNodeData
```
How it is driven (from `BuildInternalNodeList`): the tree first calls `OnGetNumberOfNodes` with a hidden **root** virtual node whose `Level = -1` (root count), then once per node for its child count. `TTMSFNCTreeViewVirtualNode` read-only info: `Level`, `Index` (index among siblings), `Row`, `ParentNode` (**Integer row** of the parent, not an object), `Children`, `TotalChildren`, `Expanded`, `Node` (nil in virtual mode), plus writable `DataPointer/DataObject/DataString/DataInteger/DataBoolean`. Use `GetParentVirtualNode(ANode)` to get the parent object.

```delphi
procedure TForm1.TreeGetNumberOfNodes(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode; var ANumberOfNodes: Integer);
begin
  if ANode.Level = -1 then
    ANumberOfNodes := Length(FCustomers)                     // root nodes
  else if ANode.Level = 0 then
    ANumberOfNodes := Length(FCustomers[ANode.Index].Orders) // children of a customer
  else
    ANumberOfNodes := 0;
end;

procedure TForm1.TreeGetNodeText(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode; AColumn: Integer;
  AMode: TTMSFNCTreeViewNodeTextMode; var AText: String);
var p: TTMSFNCTreeViewVirtualNode;
begin
  if ANode.Level = 0 then
    AText := FCustomers[ANode.Index].Name
  else
  begin
    p := TMSFNCTreeView1.GetParentVirtualNode(ANode);
    AText := FCustomers[p.Index].Orders[ANode.Index].Caption;
  end;
end;
```
After the underlying data changes call `TMSFNCTreeView1.ClearNodeList` (inside BeginUpdate/EndUpdate) to rebuild. Virtual API counterparts: `AddVirtualNode`, `InsertVirtualNode`, `RemoveVirtualNode`, `ExpandVirtualNode/CollapseVirtualNode/ToggleVirtualNode(ANode; ARecurse)`, `CheckVirtualNode/UnCheckVirtualNode(ANode; AColumn; ARecurse)`, `SelectVirtualNode`, `SelectedVirtualNode`, `FocusedVirtualNode`, `EditVirtualNode`, `ScrollToVirtualNode`, `FindVirtualNodeByRow`, `GetFirstRootVirtualNode`, `GetNextVirtualNode`, `GetVirtualNodeText(ANode, AColumn)`, `ExpandAllVirtual/CollapseAllVirtual`. Persist user check / edit changes yourself in `OnAfterCheckNode`, `OnAfterUnCheckNode`, `OnBeforeUpdateNode` (`var AText`).

**Collection vs virtual — key differences**
| | Collection | Virtual |
|---|---|---|
| Data | `Nodes`, `TTMSFNCTreeViewNode.Text[col]` | your arrays + `OnGetNumberOfNodes`/`OnGetNodeText` |
| Selected item | `SelectedNode` / `FocusedNode` (TTMSFNCTreeViewNode) | `SelectedVirtualNode` (`SelectedNode` returns nil) |
| Events | all events receive a `TTMSFNCTreeViewVirtualNode`; use `ANode.Node` | `ANode.Node = nil`; use `Level`/`Index`/`Row` |
| Change data | edit node properties (auto refresh) | call `ClearNodeList` |
Assigning `OnGetNumberOfNodes` makes `DoGetNumberOfNodes` **clear `Nodes`** on every rebuild: you cannot mix both modes.

## Selection, expand/collapse, checks, editing

```delphi
property SelectedNode: TTMSFNCTreeViewNode;   property SelectedVirtualNode: TTMSFNCTreeViewVirtualNode;
property FocusedNode: TTMSFNCTreeViewNode;    property SelectedNodes[AIndex: Integer]: TTMSFNCTreeViewNode;
function SelectedNodeCount: Integer;          function IsNodeSelected(ANode: TTMSFNCTreeViewNode): Boolean;
procedure SelectNode(ANode: TTMSFNCTreeViewNode);   procedure SelectNodes(ANodes: TTMSFNCTreeViewNodeArray);
procedure UnSelectAllNodes;  procedure SelectAllNodes;  procedure RemoveSelectedNodes;
procedure ExpandAll;  procedure CollapseAll;
procedure ExpandNode(ANode: TTMSFNCTreeViewNode; ARecurse: Boolean = False);
procedure CollapseNode(ANode: TTMSFNCTreeViewNode; ARecurse: Boolean = False);
procedure CheckNode(ANode: TTMSFNCTreeViewNode; AColumn: Integer; ARecurse: Boolean = False);
procedure UnCheckNode(ANode: TTMSFNCTreeViewNode; AColumn: Integer; ARecurse: Boolean = False);
procedure ToggleCheckNode(ANode: TTMSFNCTreeViewNode; AColumn: Integer; ARecurse: Boolean = False);
procedure EditNode(ANode: TTMSFNCTreeViewNode; AColumn: Integer);  procedure StopEditing;  procedure CancelEditing;  function IsEditing: Boolean;
procedure ScrollToNode(ANode: TTMSFNCTreeViewNode; AScrollIfNotVisible: Boolean = False; AScrollPosition: TTMSFNCTreeViewNodeScrollPosition = tvnspTop; AForceScroll: Boolean = False);
function XYToNode(X, Y: Double; OffsetX: Single = 0): TTMSFNCTreeViewVirtualNode;
function LookupNode(ALookupString: String; ARootNodesOnly: Boolean = False; AColumn: Integer = -1; ACaseSensitive: Boolean = False; AAutoSelect: Boolean = False; AAutoExpand: Boolean = False): TTMSFNCTreeViewVirtualNode;
procedure Clear;   // ClearNodes + ClearColumns + ClearSorting (removes columns too!)
```
`Interaction` (TTMSFNCTreeViewInteraction): `MultiSelect`, `MultiSelectStyle`, `ReadOnly`, `MouseEditMode` (`tmemDoubleClick`, `tmemSingleClick`, `tmemSingleClickOnSelectedNode`), `KeyboardEdit`, `ExpandCollapseOnDblClick`, `ColumnSizing`, `ClipboardMode` (`tcmNone/tcmTextOnly/tcmFull`), `Reorder`, `DragDropMode` (`tdmNone/tdmMove/tdmCopy`), `Lookup` (`Enabled`, `Incremental`, `Column`, `AutoSelect`, `AutoExpand`), `SelectionFollowsFocus`.

Key events (all `Sender: TObject` first):
```delphi
OnAfterSelectNode / OnNodeClick / OnNodeDblClick: procedure(Sender: TObject; ANode: TTMSFNCTreeViewVirtualNode)
OnBeforeSelectNode:  (Sender; ANode: TTMSFNCTreeViewVirtualNode; var ACanSelect: Boolean)
OnNodeValueClick:    (Sender; ANode: TTMSFNCTreeViewVirtualNode; AColumn: Integer)
OnBeforeExpandNode / OnBeforeCollapseNode: (Sender; ANode; var ACanExpand / ACanCollapse: Boolean)
OnAfterExpandNode / OnAfterCollapseNode:   (Sender; ANode)
OnBeforeCheckNode:   (Sender; ANode; AColumn: Integer; var ACanCheck: Boolean)
OnAfterCheckNode / OnAfterUnCheckNode: (Sender; ANode; AColumn: Integer)
OnBeforeOpenInplaceEditor: (Sender; ANode; AColumn: Integer; var ACanOpen: Boolean)
OnCloseInplaceEditor: (Sender; ANode; AColumn: Integer; AInplaceEditor: TTMSFNCTreeViewInplaceEditor; ACancelled: Boolean; var ACanClose: Boolean)
OnBeforeUpdateNode:  (Sender; ANode; AColumn: Integer; var AText: String; var ACanUpdate: Boolean)
OnAfterUpdateNode:   (Sender; ANode; AColumn: Integer)
OnNodeCompare:       (Sender; Node1, Node2: TTMSFNCTreeViewNode; AColumn: Integer; var ACompareResult: Integer)
OnBeforeDropNode:    (Sender; AFromNode, AToNode: TTMSFNCTreeViewVirtualNode; var ACanDrop: Boolean)
OnAfterDropNode:     (Sender; AFromNode, AToNode: TTMSFNCTreeViewVirtualNode)
OnFocusedNodeChanged / OnNodeChanged: (Sender; ANode)
```
User clicks on a checkbox do **not** cascade to children; call `CheckNode(n, 0, True)` in `OnAfterCheckNode` if you need that. Radio buttons (`tvntRadioButton`) are exclusive among siblings.

## Sorting and filtering

- Header-click sorting: set `Columns[i].Sorting := tcsNormal` (or `tcsRecursive`). Code: `TreeView.Sort(AColumn: Integer = 0; ARecurse: Boolean = False; ACaseSensitive: Boolean = True; ASortingMode: TTMSFNCTreeViewNodesSortMode = nsmAscending; AClearNodeList: Boolean = True)`; `ClearSorting`; current mode in `SortMode`, column in `SortColumn`. Custom order: `OnNodeCompare` (demo checks `TreeView.SortMode = nsmDescending` and negates).
- Header filter dropdown: `Columns[i].Filtering.Enabled := True`.
- Code filter: `Filter` collection of `TTMSFNCTreeViewFilterData` (`Column: smallint`, `Condition` with wildcards like `'*abc*'`, `CaseSensitive` default True, `Prefix`, `Suffix`, `Operation`: `tfoSHORT, tfoNONE, tfoAND, tfoXOR, tfoOR`), then `ApplyFilter`. `RemoveFilter` hides the filter but keeps conditions; `RemoveFilters` clears them.
```delphi
TMSFNCTreeView1.Filter.Clear;
with TMSFNCTreeView1.Filter.Add do
begin
  Column := 0;
  Condition := '*cake*';
  CaseSensitive := False;
end;
TMSFNCTreeView1.ApplyFilter;
```

## Appearance

`NodesAppearance`: `HeightMode` (`tnhmFixed` default / `tnhmVariable`), `FixedHeight`, `LevelIndent`, `ExpandColumn`, `ShowLines`, `ShowFocus`, `Font`, `Fill`, `Stroke`, `SelectedFill`, `SelectedFontColor`, `SelectionArea` (`tsaDefault, tsaFromLevel, tsaFromText, tsaFull`), `ExtendedFill/ExtendedFont`, `ExpandNodeIcon`/`CollapseNodeIcon`. Icons come from `BitmapContainer` (no ImageList). Text supports FNC mini-HTML (`<b>`, `<font color=...>`, `<a href>` -> `OnNodeAnchorClick`). Load/save: `SaveToFile/LoadFromFile/SaveToStream/LoadFromStream` (not on WEB), `ViewJSON(AFileName)`, `ViewJSONFromText(AText)`, clipboard `CopyToClipboard/CutToClipboard/PasteFromClipboard`.

## TTMSFNCCheckedTreeView

`TTMSFNCTreeView` descendant whose node classes are `TTMSFNCCheckedTreeViewNode(s)`.
```delphi
property Checked[ANode: TTMSFNCTreeViewNode]: Boolean;   // column 0
function CheckedNodes(AColumn: Integer = 0; ARecurse: Boolean = True): TTMSFNCTreeViewCheckedNodes; // array of TTMSFNCTreeViewNode
```
The node value constructor sets `CheckType := tvntCheckBox` **only at design time**; nodes added in code still need `n.CheckTypes[0] := tvntCheckBox` (that is what its own `InitSample` does).

## TTMSFNCDirectoryTreeView (VCL/FMX/LCL only, `TMSPlatformsDesktop`)

```delphi
procedure LoadDirectory(ADirectory: String; AExpand: Boolean = False);
procedure LoadDrives(AExpand: Boolean = False);
procedure LoadDrive(ADrive: String; AExpand: Boolean = False);
function AddColumn(AKind: TTMSFNCDirectoryTreeViewColumnKind): TTMSFNCDirectoryTreeViewColumn; // tvckName, tvckDisplayName, tvckCreationDate, tvckModificationDate, tvckFreeSpace, tvckTotalSize, tvckFreeSpaceAndTotalSize, tvckCustom
function FindNodeByPath(AStartNode: TTMSFNCTreeViewNode; const APath: string): TTMSFNCTreeViewNode;
property Options: TTMSFNCDirectoryTreeViewOptions default [tvoFiles, tvoHidden, tvoDirectories];
property Filter: String;   // file mask; HIDES the inherited Filter collection
property SortOrder: TTMSFNCDirectoryTreeViewSortOrder;  // tvsoNone, tvsoFilesFirst, tvsoDirectoriesFirst
property OnGetCustomNodeText: procedure(Sender: TObject; ANode: TTMSFNCTreeViewNode; AColumn: Integer; AFile: String; var AText: String) of object;
```
Nodes are `TTMSFNCDirectoryTreeViewNode` with `FileName: String`; subfolders load lazily on expand.
```delphi
dtv := TTMSFNCDirectoryTreeView.Create(Self);
dtv.Parent := Self;
dtv.Align := alClient;
dtv.Options := [tvoDirectories];
dtv.LoadDirectory('C:\Projects');
// selected path: (dtv.SelectedNode as TTMSFNCDirectoryTreeViewNode).FileName
```

## Showing dataset data

Fill the nodes from the dataset in code. This works with every install:
```delphi
procedure TForm1.LoadTree(ADataSet: TDataSet);
var
  n: TTMSFNCTreeViewNode;
begin
  TMSFNCTreeView1.BeginUpdate;
  try
    TMSFNCTreeView1.ClearNodes;
    ADataSet.First;
    while not ADataSet.Eof do
    begin
      n := TMSFNCTreeView1.AddNode;                       // root node; AddNode(Parent) for a child
      n.Text[0] := ADataSet.FieldByName('Name').AsString;
      n.DataInteger := ADataSet.FieldByName('ID').AsInteger;  // keep the key for lookups
      ADataSet.Next;
    end;
  finally
    TMSFNCTreeView1.EndUpdate;
  end;
end;
```
For large datasets use virtual mode instead (`OnGetNumberOfNodes` / `OnGetNodeText`, above).

## TTMSFNCTreeViewDatabaseAdapter (not in the installed packages)

The class exists in the product (VCL/FMX/LCL, no WEB unit), but 7.3.1.2 doesn't compile it into any package. Only use it if the user confirms `uses VCL.TMSFNCTreeViewDatabaseAdapter` (or `FMX.`) compiles in their project. It gives a flat (single-level) DB view using virtual mode internally.
```delphi
property TreeView: TTMSFNCCustomTreeView;      // set this; it assigns TreeView.Adapter (Adapter is protected on the tree)
property Active: Boolean default False;
property DataSource: TDataSource;
property Columns: TTMSFNCTreeViewDatabaseAdapterColumns;  // FieldName, Header, CheckBoxField, PictureField, ProgressField, CheckTrue/CheckFalse, HTMLTemplate
property AutoCreateColumns: Boolean default True;
property PostMode: TTMSFNCTreeViewDatabaseAdapterPostMode default apmNode;  // apmNone, apmNode
procedure AddAllFields;  procedure RemoveAllColumns;  procedure LoadAllDataAndDisconnect;
```
```delphi
DBAdapter := TTMSFNCTreeViewDatabaseAdapter.Create(Self);
DBAdapter.TreeView := TMSFNCTreeView1;
DBAdapter.DataSource := DataSource1;
DBAdapter.Active := True;
```

## Platform notes

- Same API on VCL, FMX, WEB, LCL for `TTMSFNCTreeView`/`TTMSFNCCheckedTreeView`. `SaveToFile/LoadFromFile/SaveToStream/LoadFromStream` are `{$IFNDEF WEBLIB}`.
- `TTMSFNCDirectoryTreeView` and `TTMSFNCTreeViewDatabaseAdapter` have no `WEBLib.` unit.
- `Sort` is `reintroduce` on FMX (same call syntax).

## Does not exist / common mistakes

- `Items`, `Items.AddChild`, `Items.AddChildObject` (VCL TTreeView) — use `AddNode(Parent)` or `Parent.Nodes.Add`.
- `Node.Text := 'x'` / `Node.Caption` — `Text` is indexed per column: `Node.Text[0] := 'x'`.
- `Node.Parent`, `Node.Count`, `Node.HasChildren`, `Node.Item[i]` — use `Node.GetParent`, `Node.GetChildCount`, `Node.Nodes.Count`, `Node.Nodes[i]`. `Node.Level` does not exist on `TTMSFNCTreeViewNode` (it is on `Node.VirtualNode.Level`).
- `Node.Data` / `Node.ImageIndex` / `TreeView.Images` — use `DataObject`/`DataPointer`/`DataInteger`, and `CollapsedIconNames[col, False]` + `BitmapContainer`.
- `Node.Checked := True` / `TreeView.Checkboxes` / `OnCheckChanged` / `OnNodeCheck` — use `Checked[col]` + `CheckTypes[col] := tvntCheckBox`; events `OnAfterCheckNode` / `OnAfterUnCheckNode`.
- `TreeView.Selected` / `OnChange` / `OnSelectNode` — use `SelectedNode` (or `SelectedVirtualNode`) and `OnAfterSelectNode`.
- `FullExpand` / `FullCollapse` / `AlphaSort` — use `ExpandAll` / `CollapseAll` / `Sort(col)`.
- `TreeView.MultiSelect`, `TreeView.ReadOnly` — they live under `Interaction`.
- `ColumnCount`/`RowCount` — protected; use `Columns.Count` and `GetTotalNodeCount` / `GetVisibleNodeCount`.
- `Columns.Add('Name')` — `Add` takes no parameters; set `.Text`.
- Expecting cells to be editable by default — `EditorType` defaults to `tcetNone` (not editable).
- `TreeView.Clear` to empty data — it also deletes the columns; use `ClearNodes`.
- `TreeView.Adapter := DBAdapter` — `Adapter` is protected; set `DBAdapter.TreeView := TreeView`.
- In virtual mode, `ANode.Node.Text[...]` (nil access) or `ANode.ParentNode.Index` (ParentNode is an Integer row) — use `GetParentVirtualNode(ANode)`.
