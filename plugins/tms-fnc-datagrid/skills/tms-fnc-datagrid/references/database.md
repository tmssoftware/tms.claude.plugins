# TMS FNC DataGrid: database binding

Units: `VCL.TMSFNCDataGridDatabaseAdapter` / `FMX.TMSFNCDataGridDatabaseAdapter` / `WEBLib.TMSFNCDataGridDatabaseAdapter`, plus `Data.DB` (`DB` on WEB).
Verified against `VCL.TMSFNCDataGridDatabaseAdapter.pas` (adapter v1.1.1.1) and the UI Pack demos in `{VCL,FMX}\DataGrid\Database\`.

## How it is wired

```
TDataSet --> TDataSource --> TTMSFNCDataGridDatabaseAdapter.DataSource
                                 ^
TTMSFNCDataGrid.Adapter ---------+
```

The direction matters. The **grid** points at the adapter (`TTMSFNCDataGrid.Adapter`), and the adapter points at a `TDataSource` (not directly at a dataset). The adapter has no `DataGrid` or `Grid` property.

```delphi
property Adapter: TTMSFNCDataGridDataAdapter read GetAdapter write SetAdapter;  // on TTMSFNCCustomDataGrid, published on TTMSFNCDataGrid
```

Class hierarchy: `TTMSFNCDataGridDatabaseAdapter = class(TTMSFNCCustomDataGridDatabaseAdapter)`, which descends from `TTMSFNCDataGridRendererDataAdapter`. Use the published `TTMSFNCDataGridDatabaseAdapter`.

### Code setup

```delphi
uses Data.DB, FireDAC.Comp.Client, VCL.TMSFNCDataGrid, VCL.TMSFNCDataGridDatabaseAdapter;

Adapter := TTMSFNCDataGridDatabaseAdapter.Create(Self);
Adapter.DataSource := DataSource1;      // DataSource1.DataSet := FDQuery1;
TMSFNCDataGrid1.Adapter := Adapter;     // REQUIRED at run time
FDQuery1.Open;                          // grid fills when the dataset opens
```

Constructors:

```delphi
constructor Create(AOwner: TComponent); overload; override;
constructor Create(AOwner: TComponent; ASkipAssign: Boolean); reintroduce; overload; virtual;
```

Only at **design time** does `Create` assign itself to the first grid on the form that has no adapter. In run-time code you must set `Grid.Adapter` yourself.

The demo DFM wiring (Biolife_ClientDataSet) looks like this. The adapter is a non-visual component with a design-time box, which is why `Width`/`Height`/`Visible` show up in the DFM:

```
object TMSFNCDataGrid1: TTMSFNCDataGrid
  Adapter = TMSFNCDataGridDatabaseAdapter1
end
object TMSFNCDataGridDatabaseAdapter1: TTMSFNCDataGridDatabaseAdapter
  DataSource = DataSource1
end
object DataSource1: TDataSource
  DataSet = ClientDataSet1
end
```

Behaviour: the grid follows Open, Close, scrolling and editing through the adapter's `DataLink`. **Unidirectional datasets are rejected** with `EDatabaseError` ("Operation not allowed on a unidirectional dataset"). For FireDAC this means `FetchOptions.Unidirectional` must be False, and `TSQLQuery` must go through a `TClientDataSet`.

## Published properties (exact declarations)

```delphi
property AutoCreateColumns: Boolean default True;     // adds a mapping per field not yet in Columns when the dataset opens
property AutoRemoveColumns: Boolean default True;     // clears mappings/grid columns when the dataset closes (only if none explicitly defined)
property Columns: TTMSFNCDataGridDatabaseAdapterColumns;
property DataSource: TDataSource;
property DetailControl: TTMSFNCDataGridCellControl;   // master-detail: control shown in an expandable child row
property DynamicRecordCount: Boolean default False;   // for fetch-on-demand datasets where RecordCount grows
property HeaderRow: Integer default 0;                // grid row that receives field headers
property KeepData: Boolean default False;             // keep cell data after the dataset closes
property LoadMode: TTMSFNCDataGridDatabaseAdapterLoadMode default almBuffered;
property ShowBooleanFields: Boolean default True;     // ftBoolean as check boxes
property ShowDateTimeFields: Boolean default True;
property ShowMemoFields: Boolean default False;       // False shows '(MEMO)'
property ShowPictureFields: Boolean default True;     // ftGraphic as images
property Version: string;                             // read-only
// events
property OnAfterApplyFilter: TTMSFNCDataGridDatabaseAdapterAfterApplyFilterEvent;
property OnBeforeApplyFilter: TTMSFNCDataGridDatabaseAdapterBeforeApplyFilterEvent;
property OnDataToField: TTMSFNCDataGridDatabaseAdapterDataToFieldEvent;
property OnFieldToData: TTMSFNCDataGridDatabaseAdapterFieldToDataEvent;
property OnFilterData: TNotifyEvent;
property OnGetFilterValues: TTMSFNCDataGridDatabaseAdapterGetFilterValuesEvent;
property OnGetHTMLTemplate: TTMSFNCDataGridDatabaseAdapterGetHTMLTemplateEvent;
property OnGetHTMLTemplateData: TTMSFNCDataGridDatabaseAdapterGetHTMLTemplateDataEvent;
property OnGetRecordCount: TTMSFNCDataGridDatabaseAdapterGetRecordCountEvent;
property OnSortData: TNotifyEvent;
```

`DataSetType` (`adsSequenced`/`adsNonSequenced`) and `DataSetTypeAuto` are **protected** on `TTMSFNCDataGridDatabaseAdapter`, and the type is detected from `TDataSet.IsSequenced`. `LookupKeys` is public on the custom class only.

Event signatures:

```delphi
TTMSFNCDataGridDatabaseAdapterDataToFieldEvent = procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; AMasterField, AField: TField; AInplaceEditor: TTMSFNCDataGridInplaceEditor; ACellValue: TTMSFNCDataGridCellValue; var Handled: Boolean) of object;
TTMSFNCDataGridDatabaseAdapterFieldToDataEvent = procedure(Sender: TObject; ACell: TTMSFNCDataGridCellCoord; AMasterField, AField: TField; var ACellValue: TTMSFNCDataGridCellValue; var Handled: Boolean) of object;
TTMSFNCDataGridDatabaseAdapterGetFilterValuesEvent = procedure(Sender: TObject; AColumn: Integer; AValues: TStrings) of object;
TTMSFNCDataGridDatabaseAdapterBeforeApplyFilterEvent = procedure(Sender: TObject; var AFilter: string) of object;
TTMSFNCDataGridDatabaseAdapterAfterApplyFilterEvent = procedure(Sender: TObject; AFilter: string) of object;
TTMSFNCDataGridDatabaseAdapterGetRecordCountEvent = procedure(Sender: TObject; var ARecordCount: Integer) of object;
TTMSFNCDataGridDatabaseAdapterGetHTMLTemplateEvent = procedure(Sender: TObject; ACol, ARow: integer; var AHTMLTemplate: string; AFields: TFields) of object;
TTMSFNCDataGridDatabaseAdapterGetHTMLTemplateDataEvent = procedure(Sender: TObject; ACol, ARow: integer; AFieldname: string; var AData: string) of object;
```

`AMasterField` is the lookup field for a lookup column, otherwise nil. Set `Handled := True` after you assign the value yourself.

## Column mapping

`Columns: TTMSFNCDataGridDatabaseAdapterColumns` holds items of type `TTMSFNCDataGridDatabaseAdapterColumn`. **Item N drives grid column N + FixedColumnCount.**

Published item properties:

```delphi
property FieldName: string;
property Header: string;              // empty = Field.DisplayLabel
property HTMLTemplate: string;        // e.g. '<b><#LastName></b>, <#FirstName>' (templated column is read-only, FieldAtColumn = nil)
property CheckBoxField: Boolean default false;   // text/number booleans ('Y'/'N') compared to GridColumn.Binding.BooleanTrueValue
property PictureField: Boolean default false;    // image in a non-ftGraphic blob
property ProgressField: Boolean default false;
property UseColumnEditor: Boolean default False; // True = use grid column's editor instead of field-type editor
property UseLookupEditor: Boolean default True;  // combo box for lookup fields
```

Public item members: `Field: TField`, `GridColumn: TTMSFNCDataGridColumn` (read-only), `AutoCreated: Boolean`, `Adapter`, and `DataBoolean`/`DataInteger`/`DataObject`/`DataPointer`/`DataString` tags. Setting more than one of `CheckBoxField`/`PictureField`/`ProgressField` to True raises an exception.

Collection methods: `Add`, `Insert(index)`, `HasFieldsDefined: boolean`, `Items[Index]` (default).

To show only selected fields in a fixed order:

```delphi
Adapter.AutoCreateColumns := False;
Adapter.Columns.Clear;
with Adapter.Columns.Add do begin FieldName := 'CustNo';  Header := 'No.'; end;
with Adapter.Columns.Add do begin FieldName := 'Company'; end;
with Adapter.Columns.Add do begin FieldName := 'Active';  CheckBoxField := True; end;
```

Adapter methods for columns:

```delphi
procedure AddAllFields;       // bind Columns to all dataset fields (dataset need not be open)
procedure CreateColumns;      // clear and recreate one auto mapping per visible field (discards custom mappings)
procedure RemoveAllColumns;   // remove mappings, grid Row/ColumnCount := 0
procedure RemoveAllFields;    // keep items, clear field binding
property ColumnAtField[AFieldName: string]: TTMSFNCDataGridDatabaseAdapterColumn;
property FieldAtColumn[AColumn: Integer]: TField;          // AColumn is data column index (excluding fixed)
property FieldIndexAtColumn[AColumn: Integer]: Integer;
property FieldNames[AIndex: Integer]: string;
function GetGridColumnIndex(AColumn: Integer): Integer;
```

Grid formatting still goes through grid events. For example, from the Biolife demo:

```delphi
procedure TForm130.TMSFNCDataGrid1GetCellFormatting(Sender: TObject; ACell: TTMSFNCDataGridCellCoord;
  AData: TTMSFNCDataGridCellValue; var AFormatting: TTMSFNCDataGridDataFormatting;
  var AConvertSettings: TFormatSettings; var ACanFormat: Boolean);
begin
  if ACell.Column = 5 then
  begin
    AFormatting.Format := '%.2f';
    AFormatting.&Type := gdftNumber;
  end;
end;
```

## Editing and write-back

- Editing in the grid writes through `EditSetData`. The adapter moves the dataset to the record, calls `Edit`, assigns the field via `ConvertDataToField` (or `OnDataToField`), and refreshes. **It does not post.** The record is posted when the dataset moves to another record or when you call `Adapter.DataSetPost`.
- Default in-place editors are picked by field type: integer gives a signed numeric edit, float/currency a float edit, date a date picker, time a time picker, and a lookup field a combo box. Override this per column with `UseColumnEditor := True`, or tweak it in the grid's `OnGetInplaceEditorProperties` (demo: `(AInplaceEditor as TTMSFNCDataGridEdit).Precision := 2` when `AInplaceEditorType = getFloatEdit`).
- Boolean check boxes and `ftGraphic` images cannot be edited as text.
- Dataset helpers on the adapter (public):

```delphi
procedure DataSetEdit;  procedure DataSetPost;  procedure DataSetInsert;
procedure DataSetDelete; procedure DataSetCancel;
function DataSetCanModify: Boolean; function DataSetIsEditing: Boolean; function DataSetIsInserting: Boolean;
function DataSetLocate(AKeyFieldNames: string; AKeyValues: string): Boolean;  // exact, case-sensitive Locate
procedure DataSetEnableControls; procedure DataSetDisableControls;
procedure InsertRow(ARow: Integer); override;   procedure DeleteRow(ARow: Integer); override;
procedure ReloadFromDataSet;  procedure LoadAllData;  procedure Update; reintroduce;
procedure BeginUpdate; override; procedure EndUpdate; override;
function CheckDataSet: Boolean;  function GetActiveRow: Integer; virtual;
function SetActiveRecord(ARow: Integer): Boolean; virtual;  procedure ResetActiveRecord;
function IsValidDataRow(ARow: Integer): Boolean;  function IsValidDataCell(ACell: TTMSFNCDataGridCellCoord): Boolean;
procedure LoadValuesFromField(AField: TField; AValues: TStrings);
class procedure BlobFieldToPicture(AField: TBlobField; ABitmap: TTMSFNCBitmap);
property DataLink: TTMSFNCDataGridDatabaseAdapterDataLink;   // read-only
```

`DeleteRow` does nothing while the dataset is in edit or insert mode. To read field values of an arbitrary visible row, call `SetActiveRecord(ARow)`, read `Adapter.DataLink.DataSet.FieldByName(...)`, then call `ResetActiveRecord`.

The demos also put a `TBindNavigator` (LiveBindings, `TBindSourceDB` on the same dataset) next to the grid for navigation and posting. It is optional.

## LoadMode: who sorts, filters, groups

```delphi
TTMSFNCDataGridDatabaseAdapterLoadMode = (almBuffered, almAllRecords);
```

- `almBuffered` (default) buffers only visible rows (or the current page), which suits big datasets.
  - **Sorting is passed to the dataset.** An index on the **first** sorted column only is created automatically for `TCustomClientDataSet` (`IndexDefs`/`IndexName`), FireDAC `TFDDataSet` (`Indexes`, VCL/FMX), and `TTMSFNCCustomDataSet` (VCL/FMX). Any other dataset needs `OnSortData`, for example to rewrite ORDER BY.
  - **Filtering becomes `TDataSet.Filter`** with bracketed names like `[Country] LIKE '%land%' AND [Price] > '10'`, and `Filtered := True`. Adjust the expression in `OnBeforeApplyFilter`, or take over completely with `OnFilterData`, which suppresses both Before/After events.
  - **Grouping is not available.**
- `almAllRecords` buffers everything, and the grid sorts, filters and groups in memory. The StellarDS demo uses it: `TMSFNCDataGridDatabaseAdapter1.LoadMode := almAllRecords;`. With a `DetailControl`, filtering still goes to the dataset.

`OnGetFilterValues` supplies the filter drop-down values. By default every record is iterated, using a clone where supported, so a large dataset can be slow there.

## Filtering and sorting from code (demo Biolife_ClientDataSet_Filtering_Sorting)

```delphi
procedure TForm130.FormCreate(Sender: TObject);
begin
  TMSFNCDataGrid1.Options.Sorting.Enabled := True;
  TMSFNCDataGrid1.Options.Filtering.Enabled := True;
  TMSFNCDataGrid1.ScrollMode := gsmCellScrolling;
end;

procedure TForm130.Edit1ChangeTracking(Sender: TObject);
var
  fltr: TTMSFNCDataGridDataFilterData;
begin
  TMSFNCDataGrid1.ClearFilter;
  if Edit1.Text <> '' then
  begin
    fltr := TMSFNCDataGrid1.Filter.Add;
    fltr.Column := 1;               // grid column index (includes fixed column)
    fltr.CaseSensitive := False;
    fltr.Condition := Edit1.Text;   // e.g. 'S*'
    TMSFNCDataGrid1.ApplyFilter;
  end;
end;

TMSFNCDataGrid1.Sort(3, gsdAscending);   // Sort(AColumn: Integer; ADirection: TTMSFNCDataGridSortDirection)

procedure TForm130.TMSFNCDataGrid1BeforeSortColumn(Sender: TObject; AColumn: Integer; var ACanSort: Boolean);
begin
  ACanSort := not (AColumn in [6, 7]);  // block memo/picture columns
end;
```

Paging (Biolife demo): `Grid.Paging := True; Grid.Footer.Visible := True; Grid.Footer.Paging.Visible := True;`. Paging disables `DetailControl`.

## FireDAC (demo Customers_FireDac_SQLite)

```
object FDConnection1: TFDConnection
  Params.Strings = ('Database=fddemo.sdb' 'DriverID=SQLite')
  LoginPrompt = False
end
object FDTable1: TFDTable
  Connection = FDConnection1
  TableName = 'Customers'
end
object DataSource1: TDataSource  DataSet = FDTable1  end
object TMSFNCDataGridDatabaseAdapter1: TTMSFNCDataGridDatabaseAdapter
  DataSource = DataSource1
  Columns = <>            // empty: AutoCreateColumns builds them on open
end
```

```delphi
procedure TForm130.FormCreate(Sender: TObject);
begin
  TMSFNCDataGrid1.ScrollMode := gsmCellScrolling;
  FDConnection1.Connected := True;
end;
procedure TForm130.Button1Click(Sender: TObject);
begin
  FDTable1.Active := not FDTable1.Active;
end;
```

## ClientDataSet (demo Biolife_ClientDataSet)

Same wiring with `TClientDataSet` (`Datasnap.DBClient`). The demo predefines `Columns` items with `FieldName`s ('Species No', 'Category', 'Common_Name', ..., 'Notes', 'Graphic') and toggles `ShowPictureFields` / `ShowMemoFields` at run time. Changing either reloads the grid.

## Master-detail (demo Master_Detail_FireDac_SQLite)

There are two grids and two adapters. The master adapter's `DetailControl` is the detail grid, and the dataset-level master-detail link is ordinary FireDAC:

```
object TMSFNCDataGridDatabaseAdapter1: TTMSFNCDataGridDatabaseAdapter
  DataSource = DataSource1            // FDTable1 'Customers'
  DetailControl = TMSFNCDataGrid2
end
object TMSFNCDataGridDatabaseAdapter2: TTMSFNCDataGridDatabaseAdapter
  DataSource = DataSource2            // FDTable2 'Orders'
end
object TMSFNCDataGrid2: TTMSFNCDataGrid
  Adapter = TMSFNCDataGridDatabaseAdapter2
end
object FDTable2: TFDTable
  IndexFieldNames = 'CustomerID'
  MasterSource = DataSource1
  MasterFields = 'CustomerID'
  TableName = 'Orders'
end
```

```delphi
procedure TForm130.Button1Click(Sender: TObject);
begin
  FDTable1.Active := not FDTable1.Active;
  FDTable2.Active := not FDTable2.Active;
end;
procedure TForm130.FDTable1AfterOpen(DataSet: TDataSet);
begin
  TMSFNCDataGrid1.ColumnWidths[0] := 30;   // expand/collapse node column
  TMSFNCDataGrid1.AutoSizeColumns();
end;
```

How it works: each data row gets a collapsed child row. Expanding a row moves the master dataset to that record (so `MasterSource` refreshes the detail), then places the control in the child row. Only one row is expanded at a time. The control is hidden when not in use. `DetailControl` is `TTMSFNCDataGridCellControl` (`TWinControl` on VCL/WEB, `TControl` on FMX), so any control works, not only a grid. Disabled while `Paging` is on. `IsValidDataRow` is False for detail rows.

## StellarDS (cloud)

Demo `StellarDS` binds the adapter to `TTMSFNCCloudStellarDataStoreDataSetVCL` (unit `VCL.TMSFNCCloudStellarDataStoreDataSet`; FMX: `TTMSFNCCloudStellarDataStoreDataSetFMX`). That dataset is part of **TMS FNC Cloud Pack** (`tms.fnc.cloudpack`), not the UI Pack. From the grid's side it is a normal `TDataSet`: `DataSource1.DataSet := TMSFNCCloudStellarDataStoreDataSetVCL1`, and the demo sets `LoadMode := almAllRecords`. Dataset configuration (from the demo): `.Authentication.ClientID`, `.Adapter.Authentication.Secret`, `.Adapter.Authentication.CallBackURL`, `.ProjectID`, `.Table := 'DataGridDemo'`, `.Adapter.OnConnected`, then `.Active := True`.

## Does not exist / common mistakes

| Wrong | Right |
|---|---|
| `TTMSFNCDataGridDBAdapter`, `TTMSFNCDBDataGrid`, `TTMSFNCDataGridDataBinder` | `TTMSFNCDataGridDatabaseAdapter` |
| `Adapter.DataGrid := Grid` / `Adapter.Grid` | `Grid.Adapter := Adapter` |
| `Adapter.DataSet := FDQuery1` | `Adapter.DataSource := DataSource1` (a `TDataSource`) |
| `Grid.DataSource := ...` | No such property. Go through the adapter |
| `Adapter.Active := True` / `Adapter.Open` | Open the dataset |
| `Adapter.Columns[i].Width` / `.Visible` / `.ReadOnly` | Those live on the grid column: `Adapter.Columns[i].GridColumn` (`TTMSFNCDataGridColumn`) or `Grid.Columns[...]`. Hide a field via `TField.Visible := False` |
| `Adapter.Columns[i].Title` / `.Caption` | `.Header` |
| Expect edits to be posted on cell exit | Not posted until the record changes or `Adapter.DataSetPost` |
| Grouping in default mode | Needs `LoadMode := almAllRecords` |
| Multi-column sort with `almBuffered` on CDS/FireDAC | Only the first sort column becomes an index. Use `almAllRecords` or `OnSortData` |
| `Adapter.MasterSource` / `Adapter.DetailAdapter` | `Adapter.DetailControl := DetailGrid`, plus the dataset's own `MasterSource`/`MasterFields` |
| Unidirectional query (`TSQLQuery`, FireDAC `Unidirectional`) | Rejected with `EDatabaseError`. Use a bidirectional dataset |
| Setting `DataSetType` on the published adapter | Protected. Detection is automatic from `IsSequenced` |
