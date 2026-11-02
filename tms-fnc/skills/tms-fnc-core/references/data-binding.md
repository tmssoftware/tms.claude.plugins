# Data binding, FNC dataset and filters (TTMSFNCDataBinder, TTMSFNCDataSet, TTMSFNCDataLinkCSV/JSON, TTMSFNCFilterBuilder, TTMSFNCFilterRulesManager)

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCDataBinding`, `TMS.TMSFNCDataSet`, `TMS.TMSFNCCustomDataLink`, `TMS.TMSFNCDataLinkCSV`, `TMS.TMSFNCDataLinkJSON`, `TMS.TMSFNCFilterBuilder`, `TMS.TMSFNCFilterStructure`, `TMS.TMSFNCFilterRulesManager`, the `*Reg.pas` units and `Packages\d13\*.dpk`; demos `tms.fnc.core.demos\VCL\DataBinding`, `WEB\TMSFNCDataBinding`, `VCL\TTMSFNCDataSet\CustomDataLink`, `VCL\TMSFNCFilterRulesManager\Grid Example` and `Panel Control Example`.

## Units and palette

| Class | Unit(s) | Palette page | Frameworks |
|---|---|---|---|
| `TTMSFNCDataBinder` | `VCL.TMSFNCDataBinding`, `FMX.TMSFNCDataBinding`, `WEBLib.TMSFNCDataBinding`, `LCLTMSFNCDataBinding` | TMS FNC DB | VCL, FMX, WEB, LCL |
| `TTMSFNCDataSet` | `TMS.TMSFNCDataSet` | TMS FNC DB | VCL, FMX (package `TMSFNCCorePkg`) |
| `TTMSFNCDataLinkCSV` | `TMS.TMSFNCDataLinkCSV` | TMS FNC DB | VCL, FMX |
| `TTMSFNCDataLinkJSON` | `TMS.TMSFNCDataLinkJSON` | TMS FNC DB | VCL, FMX |
| `TTMSFNCFilterRulesManager` | `TMS.TMSFNCFilterRulesManager` | TMS FNC UI | VCL, FMX, WEB (in `TMSFNCCoreWEB`) |
| `TTMSFNCFilterBuilder` (not a component) | `TMS.TMSFNCFilterBuilder` | none | all |
| `TTMSFNCFilterStructure` (not a component) | `TMS.TMSFNCFilterStructure` | none | all |

Also add `Data.DB` (`DB` on WEB) for `TDataSource`/`TDataSet`, and `TMS.TMSFNCValue` when you build `TTMSFNCValue` arguments.

There is also an older unit `VCL.TMSFNCFilterRulesManager` (v0.9 beta, different API, not registered on the palette). Always use **`TMS.TMSFNCFilterRulesManager`**, which is what the palette component and the demos use; never put both in one `uses` clause.

## TTMSFNCDataBinder: bind any control property to a dataset

Non-visual component that binds published properties of any object (FNC controls, VCL/FMX controls, your own classes) to fields of a `TDataSource`, using RTTI. Bindings are items of `Items: TTMSFNCDataBinderItems`; the `Connect*` methods add items for you.

```delphi
TTMSFNCDataBinderBindType = (dbbtSingleValue, dbbtList, dbbtColumnList, dbbtGrid);

// TTMSFNCDataBinder
function ConnectSingle(AObject: TObject; ADataSource: TDataSource; APropertyName: string; AFieldName: string): TTMSFNCDataBinderItem;
function ConnectSingleHTMLTemplate(AObject: TObject; ADataSource: TDataSource; APropertyName: string; AHTMLTemplate: string): TTMSFNCDataBinderItem;
function ConnectList(AObject: TObject; ADataSource: TDataSource; APropertyName: string; AFieldName: string): TTMSFNCDataBinderItem; overload;
function ConnectList(AObject: TObject; ADataSource: TDataSource; APropertyName: string; ASubPropertyNames: TTMSFNCDataBinderStringArray; ASubFieldNames: TTMSFNCDataBinderStringArray): TTMSFNCDataBinderItem; overload;
function ConnectListHTMLTemplate(AObject: TObject; ADataSource: TDataSource; APropertyName: string; AHTMLTemplate: string): TTMSFNCDataBinderItem; overload;
function ConnectColumnList(AObject: TObject; ADataSource: TDataSource; AListPropertyName: string; AColumnsPropertyName: string; AColumnsSubPropertyName: string; AListSubPropertyName: string): TTMSFNCDataBinderItem;
function ConnectGrid(AObject: TObject; ADatasource: TDataSource): TTMSFNCDataBinderItem;   // AObject must implement ITMSFNCDataBinderGrid
function Connect(AObject: TObject; ADataSource: TDataSource; APropertyName: string; AFieldName: string = ''; AHTMLTemplate: string = ''; ASubPropertyNames: TTMSFNCDataBinderStringArray = nil; ASubFieldNames: TTMSFNCDataBinderStringArray = nil; ASubHTMLTemplates: TTMSFNCDataBinderStringArray = nil; ABindType: TTMSFNCDataBinderBindType = dbbtSingleValue): TTMSFNCDataBinderItem;
function IsConnected(AObject: TObject): Boolean;
property ItemByName[AName: string]: TTMSFNCDataBinderItem;
property ItemByObject[AObject: TObject; APropertyName: string]: TTMSFNCDataBinderItem;
procedure BeginUpdate; override;  procedure EndUpdate; override;
procedure StartEditor(const AObject: TObject = nil);          // runtime binding editor dialog
class function GetPropertyNames(AObject: TObject; IncludePublic: Boolean = True): TTMSFNCDataBinderStringArray; overload;
class procedure BlobFieldToBitmap(AField: TField; ABitmap: TTMSFNCBitmap);
class procedure BitmapToBlobField(AField: TField; ABitmap: TTMSFNCBitmap);
// published
property Active: Boolean default False;      // nothing happens until True
property DataSource: TDataSource;            // default source for items without their own
property Items: TTMSFNCDataBinderItems;
property OnBeforeWriteFieldToProperty / OnAfterWriteFieldToProperty;
property OnBeforeWritePropertyToField / OnAfterWritePropertyToField;
property OnBeforeWriteHTMLTemplateToProperty / OnAfterWriteHTMLTemplateToProperty;

// TTMSFNCDataBinderItem (published)
property BindComponent: TComponent;  property PropertyName: string;  property FieldName: string;
property DataSource: TDataSource;    property BindType: TTMSFNCDataBinderBindType default dbbtSingleValue;
property Active: Boolean default True;  property HTMLTemplate: string;  property BooleanStringValue: string;
property SubPropertyNames: TTMSFNCDataBinderPropertyNames;  property SubFieldNames: TTMSFNCDataBinderFieldNames;
property ColumnsPropertyName: string;  property ColumnsSubPropertyName: string;  property Name: string;
// public: NotifySetActiveRecord, NotifyValueChanged, NotifyEdit, NotifyPost, NotifyUpdate, WriteValueToField,
//         DataSetEdit, DataSetPost, DataSetInsert, DataSetDelete, DataSetCancel, DataSetLocate(AKeyFieldNames, AKeyValues: string): Boolean
```

HTML templates use `<#FIELDNAME>` placeholders. Example (VCL `DataBinding` demo, ClientDataSet on biolife data):

```delphi
uses Data.DB, VCL.TMSFNCDataBinding;

procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCDataBinder1.ConnectSingleHTMLTemplate(HTMLPaintBox1, DataSource1, 'HTML',
    '<b>Name: <#COMMON_NAME></b><br/><font size="10"><#NOTES></font>');
  TMSFNCDataBinder1.ConnectSingle(Image1, DataSource1, 'Picture', 'Graphic');   // blob -> picture
  TMSFNCDataBinder1.ConnectList(ListBox1, DataSource1, 'Items', 'Species Name');  // TStrings or TCollection property
  TMSFNCDataBinder1.ConnectGrid(StringGridEx1, DataSource1);                      // implements ITMSFNCDataBinderGrid
  TMSFNCDataBinder1.Active := True;
end;

// a list-type control reports its selection back so the dataset follows
procedure TForm1.DoSelectCell(Sender: TObject; ACol, ARow: Longint; var CanSelect: Boolean);
begin
  TMSFNCDataBinder1.ItemByObject[Sender, ''].NotifySetActiveRecord;
end;
```

FNC list control with item collection (each item gets `Text` from field `Name`):

```delphi
TMSFNCDataBinder1.ConnectList(TMSFNCListBox1, DataSource1, 'Items', ['Text'], ['Name']);
TMSFNCDataBinder1.ConnectSingle(Edit1, DataSource1, 'Text', 'Name');
TMSFNCDataBinder1.Active := True;
```

- `ConnectGrid` needs `ITMSFNCDataBinderGrid` (`SetDataColumnCount`, `SetDataRowCount`, `ClearData`, `GetDataRowCount`, `SetDataValue`, `SetDataHeader`, `DataInsertRow`, plus `DataBeginUpdate`/`DataEndUpdate`); UI Pack `TTMSFNCGrid` and `TTMSFNCDataGrid` implement it. For `TTMSFNCDataGrid`, its own database adapter is the richer option (see the DataGrid skill).
- Selection sync uses `ITMSFNCDataBinderSelection` (`DataGetItemIndex`, `DataSetItemIndex`), implemented by `TTMSFNCCustomControl`.
- Write-back from edited standard controls to the dataset is done through the RTL observers (`IControlValueObserver`, `IEditLinkObserver`), compiled in for Delphi 10.4+ VCL/FMX only (`SUPPORTSBINDING`). Where no observer fires, push a value yourself with `Item.DataSetEdit; Item.WriteValueToField; Item.DataSetPost;`.

## TTMSFNCDataSet + TTMSFNCDataLinkCSV / TTMSFNCDataLinkJSON

`TTMSFNCDataSet` is a `TDataSet` over any object implementing `ITMSFNCDataObject`. The CSV/JSON data links are ready-made data objects that read a file.

```delphi
// TTMSFNCDataSet (published unless noted)
property DataLink: TComponent;            // a TTMSFNCDataLinkCSV / TTMSFNCDataLinkJSON
property DataObject: TObject;             // public: any object implementing ITMSFNCDataObject
property Active; property FieldDefs;      // + all standard TDataSet events, OnFilterRecord
property OnCreateValue, OnObjectInsert, OnObjectUpdate, OnObjectRemove, OnObjectRefresh;
property ReadOnly: Boolean default False;                 // public
procedure SortBy(AField: string; ADirection: TTMSFNCDataSetSortDirection = dsdAscending);   // dsdAscending, dsdDescending
procedure UnSort;
// Filter + Filtered work; Filter is parsed by TTMSFNCFilterBuilder (Delphi dataset syntax: [Field] LIKE 'A%', =, <>, AND, OR, NOT)

// TTMSFNCDataLinkCSV (published)
property FileName: string;  property FileEncoding: TTMSFNCCustomDataLinkFileEncoding default feDefault;  // feANSI, feASCII, feUnicode, feUTF7, feUTF8
property HasFieldNames: Boolean default True;  property AutoSeparator: Boolean default True;
property Separator: string;  property QuoteEmptyValues: Boolean default False;  property AutoSaveChanges: Boolean default False;
// TTMSFNCDataLinkJSON (published)
property FileName; property FileEncoding; property AutoSaveChanges;
property DataRootElement: string;   // path to the record array when the root is an object, e.g. 'data.items'
property MetaDataElement: string;   // optional array of {"id":..,"name":..} field descriptors
property DateTimeFormat: string;
// both (public)
procedure LoadFromFile(AFileName: string; AEncoding: TEncoding);
procedure SaveToFile(AFileName: string; AEncoding: TEncoding);
procedure LoadFromStream(AStream: TStream; AEncoding: TEncoding); virtual; abstract;
procedure SaveToStream(AStream: TStream; AEncoding: TEncoding); virtual; abstract;
```

```delphi
uses Data.DB, TMS.TMSFNCDataSet, TMS.TMSFNCDataLinkCSV, TMS.TMSFNCDataLinkJSON;

procedure TForm1.OpenCSV;
begin
  FCsv := TTMSFNCDataLinkCSV.Create(Self);
  FCsv.FileName := 'customers.csv';        // first line = field names (HasFieldNames)
  FCsv.FileEncoding := feUTF8;
  FDataSet := TTMSFNCDataSet.Create(Self);
  FDataSet.DataLink := FCsv;
  FDataSet.Active := True;                 // loads FileName now
  DataSource1.DataSet := FDataSet;
  FDataSet.SortBy('Name');
  FDataSet.Filter := '[Country] = ''Belgium''';
  FDataSet.Filtered := True;
end;

procedure TForm1.OpenJSON;
begin
  FJson := TTMSFNCDataLinkJSON.Create(Self);
  FJson.FileName := 'orders.json';         // setting FileName clears DataRootElement/MetaDataElement
  FJson.DataRootElement := 'result.orders';  // not needed when the file root is an array
  FDataSet.DataLink := FJson;
  FDataSet.Active := True;
end;
```

- CSV fields are all `ftString`. JSON field types are inferred from the **first record** (Integer, Largeint, Float, DateTime/Date/Time, Boolean, String).
- `Active := True` calls the link's `Activate`, which loads `FileName`; an empty `FileName` raises `Missing file path.`. Changing `FileName`/`DataRootElement` closes the dataset.
- Edits are written back to the file only when `AutoSaveChanges = True`.

Custom data object (VCL `TTMSFNCDataSet\CustomDataLink` demo): implement `ITMSFNCDataObject` on your list and assign it to `DataObject`:

```delphi
ITMSFNCDataObject = interface
  procedure Activate(AValue: Boolean);
  procedure AddRecord(ARecord: TValue);
  procedure DeleteRecord(AIndex: Integer);
  procedure InsertRecord(AIndex: Integer; ARecord: TValue);
  function CreateDefaultRecord: TValue;
  procedure InitializeFieldDefs(AFieldDefs: TFieldDefs);      // AFieldDefs.Add('Name', ftString, 255) ...
  function GetRecordCount: Integer;
  function GetRecordIndex(ARecord: TValue): Integer;
  function GetRecord(AIndex: Integer): TValue;
  function GetRecordValue(ARecord: TValue; AField: string; APropTye: TFieldType): ValueType;   // ValueType = Variant
  procedure SetRecordValue(ARecordIndex: Integer; AField: string; AValue: ValueType);
  function CompareRecords(AField: string; ARecord1, ARecord2: TValue): Integer;   // used by SortBy
  procedure SetNotification(ANotifyObject: ITMSFNCDataObjectNotification);      // keep it to call DataRefresh / Deactivate
  function Clone: TObject;
end;
```
`TMSFNCDataSet1.DataObject := FMyList; TMSFNCDataSet1.Active := True;` (the demo's list returns -1 from `_AddRef`/`_Release`, so the dataset does not own it). Note: the demo's `GetRecordValue` lacks the third parameter and does not match the current interface; use the 3-parameter signature above.

## TTMSFNCFilterBuilder: filter expressions in code

Non-visual `TPersistent` (create/free yourself; also a shared instance via the global function `TMSFNCFilterBuilder`). Builds, parses and evaluates filter trees; used by `TTMSFNCDataSet`, the filter rules and UI Pack filter controls.

```delphi
TTMSFNCFilterBuilderDataType = (fdtAutomatic, fdtText, fdtBoolean, fdtDateTime, fdtDate, fdtTime, fdtFloat, fdtNumber, fdtOther);
TTMSFNCFilterBuilderGroupOperator = (fgoAND, fgoOR);
TTMSFNCFilterBuilderExpressionOperator = (feoStartsWith, feoEndsWith, feoContains, feoEqual, feoNotEqual, feoEmpty,
  feoNotEmpty, feoLargerThan, feoSmallerThan, feoLargerThanOrEqual, feoSmallerThanOrEqual);
TTMSFNCFilterBuilderFormatType = (fftDelphiDataSet, fftUniversalFilterExpressions, fftOData, fftCustom);

// TTMSFNCFilterBuilder
constructor Create;
function AddDataColumn(AName: string; ADataType: TTMSFNCFilterBuilderDataType = fdtAutomatic; ADisplayName: string = ''): TTMSFNCFilterBuilderColumn; overload;
procedure AddDataColumnsFromFilter;
function ParseExpression(AFilterText: string): Boolean;
function isExpressionValid(AExpression: string): Boolean;
function ValidateFilterRow(AInputData: TArray<TTMSFNCValue>): Boolean;    // values in DataColumns order
function ValidateFilterArray(AInputArray: TTMSFNCFilterValidateInputArray; AByRow: Boolean = False): TTMSFNCFilterValidateOutputArray;
procedure ClearFilter;  procedure BeginUpdate;  procedure EndUpdate;
property Filter: TTMSFNCFilterBuilderGroup;          // root group
property FilterText: string;                         // read = generate, write = parse
property DisplayFilterText: string;
property DataColumns: TTMSFNCFilterBuilderColumns;
property FormatType: TTMSFNCFilterBuilderFormatType default fftDelphiDataSet;
property ParseFormat: TTMSFNCFilterBuilderParseFormat;   // operator tokens for fftCustom
property OnChanged: TNotifyEvent;  property OnParseError: TTMSFNCFilterBuilderFilterEvent;

// TTMSFNCFilterBuilderGroup
function AddExpression(AColumnName: string; AExpressionOperator: TTMSFNCFilterBuilderExpressionOperator; AValue: TTMSFNCValue; AInverted: Boolean = False; ACaseSensitive: Boolean = False): TTMSFNCFilterBuilderExpression; overload;
function AddExpression(AColumnName: string; AValue: TTMSFNCValue): TTMSFNCFilterBuilderExpression; overload;
function AddGroup(AGroupOperator: TTMSFNCFilterBuilderGroupOperator = fgoAND): TTMSFNCFilterBuilderGroup;
function AddANDGroup: TTMSFNCFilterBuilderGroup;  function AddORGroup: TTMSFNCFilterBuilderGroup;
procedure Clear;
property GroupOperator: TTMSFNCFilterBuilderGroupOperator default fgoAND;
property IsInverted: Boolean default False;
property Groups: TTMSFNCFilterBuilderGroups;  property Expressions: TTMSFNCFilterBuilderExpressions;
property FilterText: string;   // read-only
```

```delphi
uses TMS.TMSFNCFilterBuilder, TMS.TMSFNCValue;

var
  fb: TTMSFNCFilterBuilder;
  g: TTMSFNCFilterBuilderGroup;
begin
  fb := TTMSFNCFilterBuilder.Create;
  try
    fb.AddDataColumn('Name', fdtText);
    fb.AddDataColumn('Age', fdtNumber);
    fb.Filter.GroupOperator := fgoAND;
    fb.Filter.AddExpression('Name', feoStartsWith, FNCValueFromString('A'));
    g := fb.Filter.AddORGroup;
    g.AddExpression('Age', feoLargerThan, FNCValueFromInteger(30));
    g.AddExpression('Age', feoEmpty, GetEmptyFNCValue);
    Memo1.Lines.Add(fb.FilterText);      // Delphi TDataSet.Filter syntax by default
    if fb.ValidateFilterRow([FNCValueFromString('Ann'), FNCValueFromInteger(31)]) then
      Memo1.Lines.Add('Ann matches');

    fb.FormatType := fftOData;           // same tree, OData text ("eq", "contains(...)")
    Memo1.Lines.Add(fb.FilterText);

    fb.FormatType := fftDelphiDataSet;
    if not fb.ParseExpression('([Age] > 40) OR ([Name] LIKE ''%son'')') then
      ShowMessage('invalid filter');
  finally
    fb.Free;
  end;
end;
```

`TTMSFNCFilterStructure` (unit `TMS.TMSFNCFilterStructure`) is a simpler flat model used by UI Pack `TTMSFNCFilterView`: `Items.AddSingleItem(AFieldName, AFieldType, AExpressionOperator, AValue, AEnabled = False)`, `Items.AddGroup(...)`, read-only `FilterText`, `FilterFormatType`. Items are created **disabled** by default and disabled items are left out of `FilterText`.

## TTMSFNCFilterRulesManager: filter + act on live objects

Non-visual `TComponent`. Each rule resolves items on `Source` through an `ItemsPath` (TTMSFNCObjectResolver syntax, see persistence.md), evaluates a filter per item and writes action values (e.g. `Visible`) to matching / non-matching items.

```delphi
// TTMSFNCFilterRulesManager
procedure Apply;                                     // all rules
procedure ApplyRule(ARule: TTMSFNCFilterRule);
procedure ApplyActiveRules(const APattern: string);  // by name pattern, leading '!' inverts
function GetRuleByName(const AName: string): TTMSFNCFilterRule;
function AddPlaceholder(const APlaceholderName: string; ASource: TObject; const APropertyName: string): TTMSFNCCustomFilterRulesManager;  // {Name} in FilterText/ItemsPath
function AddRule(const AName: string; ASource: TComponent; const AItemsPath: string; const AFieldName: string;
  AExpressionOperator: TTMSFNCFilterBuilderExpressionOperator; const AValue: TTMSFNCValue; AActive: Boolean = True;
  ACallBackAction: TTMSFNCFilterRuleApplyCallBackEvent = nil; AInactiveCallBackAction: TTMSFNCFilterRuleInactiveCallBackEvent = nil): TTMSFNCFilterRule; overload;
function AddRule(const AName: string; ASource: TComponent; const AItemsPath: string; AFilterText: string; AActive: Boolean = True; ...): TTMSFNCFilterRule; overload;
function AddRuleEquals / AddRuleContains / AddRuleStartsWith / AddRuleEndsWith(const AName: string; ASource: TComponent;
  const AItemsPath: string; const AFieldName: string; const AValue: string; AActive: Boolean = True; AApply: Boolean = False; ...): TTMSFNCFilterRule;  // AddRuleEquals takes AValue: TTMSFNCValue
function ShowWhere / HideWhere / EnableWhere / DisableWhere(ASource: TComponent; const AItemsPath: string; const AFieldName: string;
  AExpressionOperator: TTMSFNCFilterBuilderExpressionOperator; const AValue: TTMSFNCValue; const AApply: Boolean = True; ...): TTMSFNCFilterRule;
property Rules: TTMSFNCFilterRules;  property Placeholders: TTMSFNCFilterRulePlaceholders;
property OnBeforeApply, OnAfterApply, OnBeforeApplyRule, OnAfterApplyRule, OnBeforeApplyItem, OnAfterApplyItem, OnMatchItem;

// TTMSFNCFilterRule
procedure Apply;  procedure ApplyInactive;  function CountMatchingItems: Integer;
function AddAction(const ATargetPath: string; const AMatchValue: TTMSFNCValue; const ANoMatchValue: TTMSFNCValue): TTMSFNCFilterRule; overload;
function AddVisibilityAction(AMatchVisible: Boolean = True): TTMSFNCFilterRule;   // 'Visible': match=True, no match=False, inactive=True
function AddEnableAction(AMatchEnabled: Boolean = True): TTMSFNCFilterRule;
function AddFieldType(const AFieldName: string; ADataType: TTMSFNCFilterBuilderDataType): TTMSFNCFilterRule;
property Name: string; property Active: Boolean default True; property Source: TComponent;
property ItemsPath: string; property FilterText: string; property Actions: TTMSFNCFilterRuleActions;
property FilterBuilder: TTMSFNCFilterBuilder;   // public, rebuilt on every Apply
```

From the Grid Example demo (items are `TEmployee` objects with a published `Visible` property):

```delphi
uses TMS.TMSFNCFilterRulesManager;

FManager := TTMSFNCFilterRulesManager.Create(Self);
FManager.AddPlaceholder('SearchFieldComboIndex', SearchFieldCombo, 'ItemIndex');
FManager.AddPlaceholder('FilterField', SearchFieldCombo, 'Items[{SearchFieldComboIndex}]');
FManager.AddPlaceholder('SearchText', EditSearch, 'Text');
FManager.AddRuleStartsWith('NameFilter', FEmployees, 'Items[0..*]', '{FilterField}', '{SearchText}').AddVisibilityAction;

procedure TFormMain.ApplyFilter;
begin
  FManager.Rules[0].Active := True;
  FManager.Apply;          // placeholders are read now
  RefreshGrid;
end;
```

Panel Control Example: `mgr.AddRuleStartsWith('ShowActionButtons', pnlControls, 'Controls[*]', 'Name', 'btn', False).AddVisibilityAction;` then toggle `mgr.Rules[0].Active` and call `mgr.Rules[0].Apply`.

## Platform notes

- `TTMSFNCDataBinder` exists for VCL, FMX, WEB and LCL. In the WEB demo field names come from a `TWebClientDataSet` (`<#_COMMON_NAME>`); callbacks/events as usual.
- `TTMSFNCDataSet` and the CSV/JSON links live in the framework-neutral package `TMSFNCCorePkg` (VCL and FMX); they are not in the WEB package `TMSFNCCoreWEB`.
- `TTMSFNCFilterBuilder`, `TTMSFNCValue` and `TTMSFNCFilterRulesManager` are in both `TMSFNCCorePkg` and `TMSFNCCoreWEB` (`TTMSFNCValue = JSValue` on WEB; `TTMSFNCObjectResolver.GetCollectionPaths`/`GetItemProperties` are not available there).

## Does not exist / common mistakes

- `TTMSFNCDataBinding` component: the component class is **`TTMSFNCDataBinder`** (unit `*.TMSFNCDataBinding`).
- `Binder.Bind(...)`, `AddBinding`, `Binder.Links`, `DataField` property on controls: use `ConnectSingle` / `ConnectList` / `ConnectGrid` / `Connect`, or `Items.Add` with `BindComponent`, `PropertyName`, `FieldName`.
- Forgetting `TMSFNCDataBinder1.Active := True`: the binder's `Active` defaults to **False** (items default to True).
- `ConnectGrid` on a control that does not implement `ITMSFNCDataBinderGrid` (e.g. a plain `TStringGrid`): nothing is shown; the VCL demo subclasses `TStringGrid` to implement it.
- `TTMSFNCDataSet.FileName` / `LoadFromFile` / `LoadFromJSON` / `Sort`: the file belongs to the link (`TTMSFNCDataLinkCSV.FileName`, `LoadFromFile(AFileName, AEncoding)`); sorting is `SortBy(AField, ADirection)` / `UnSort`.
- `TTMSFNCDataLinkCSV.Delimiter` / `FirstRowHeaders`: the names are `Separator` (+ `AutoSeparator`) and `HasFieldNames`.
- Setting `DataRootElement` before `FileName` on the JSON link: assigning `FileName` at runtime resets `DataRootElement` and `MetaDataElement` to ''.
- Opening the dataset after `Link.LoadFromStream(...)` without a `FileName`: `Active := True` reloads from `FileName` and raises `Missing file path.`.
- `feoNotContains`, `feoNotStartsWith`, `feoBetween`, `feoIn`, `fgoXOR`, `fgoNOT`: not in the enums (XOR/NotContains are commented out). Use `AInverted = True` on `AddExpression` (or `IsInverted` on a group) and combine two expressions for a range.
- `TTMSFNCFilterBuilder.Create(Self)` / dropping it on a form: it is a `TPersistent` with a parameterless `Create`; free it yourself.
- `Filter.Expressions.Add('Name LIKE ''A%''')`: the string overload is protected; use `AddExpression(...)` or `ParseExpression` / `FilterText :=` on the builder.
- `ValidateFilterRow` with values in arbitrary order: the array index must match `DataColumns` order.
- `TTMSFNCFilterRulesManager` from `VCL.TMSFNCFilterRulesManager`: that is the old beta API (`FilterRules`, `GetRuleByName(ARuleName)`, `ApplyActiveRules(ARuleName = '')`). Use `TMS.TMSFNCFilterRulesManager` (`Rules`, `Apply`, `AddRule...`).
- Rule actions need a writable property with that name on every item (`AddVisibilityAction` writes `Visible`); for plain data objects declare it yourself, as the demo's `TEmployee.Visible`, and refresh your display after `Apply`.
- `AddRuleStartsWith(..., AValue: string)` converts with `TextToFNCValue`, so `'123'` becomes an Integer value; use the `AddRule(..., feoStartsWith, FNCValueFromString('123'))` overload to force text.
