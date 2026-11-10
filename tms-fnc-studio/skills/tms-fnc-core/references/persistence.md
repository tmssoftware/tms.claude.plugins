# Persistence to JSON (TTMSFNCPersistence, ITMSFNCPersistence, TTMSFNCObjectResolver)
> Sections (line ranges): 6-15 Units · 16-24 How it works · 25-55 TTMSFNCPersistence · 56-100 Controls and components: SaveSettingsToFile · 101-145 Plain objects: TObject helper · 146-179 Interfaces for custom classes · 180-190 JSON to Delphi classes: TTMSFNCJSONToClass · 191-228 TTMSFNCObjectResolver · 229-234 Platform notes · 235-247 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCPersistence`, `*.TMSFNCTypes` (`TTMSFNCObjectHelper`), `*.TMSFNCCustomControl`, `*.TMSFNCCustomComponent`, `TMS.TMSFNCObjectResolver`. No dedicated demo; the FilterRulesManager demos use the resolver path syntax.

## Units

| Purpose | VCL | FMX | WEB | Lazarus |
|---|---|---|---|---|
| `TTMSFNCPersistence`, interfaces, `TTMSFNCJSONToClass` | `VCL.TMSFNCPersistence` | `FMX.TMSFNCPersistence` | `WEBLib.TMSFNCPersistence` | `LCLTMSFNCPersistence` |
| `obj.ToJSON` / `FromJSON` helper | `VCL.TMSFNCTypes` | `FMX.TMSFNCTypes` | `WEBLib.TMSFNCTypes` | `LCLTMSFNCTypes` |
| `TTMSFNCObjectResolver` (path get/set via RTTI) | `TMS.TMSFNCObjectResolver` (framework neutral; in `TMSFNCCorePkg`) ||||

`TMS.TMSFNCPersistence` is an RTL-only copy that is not in any package; do not mix it with the `VCL.`/`FMX.` unit. Nothing here is on the tool palette.

## How it works (from the source)

- The writer serializes **published** properties only (`GetPropList(ClassInfo, tkAny)`), recursively: nested objects, `TCollection`, `TList`, `TStrings`, `TTMSFNCBitmap` (as Base64), `TObjectList<T>`, `TList<string|Integer|Double>`, `TDictionary<string|Integer, ...>`.
- Each object is written as `{"$type":"TClassName", ...props}`. The key name is the class var `TTMSFNCPersistence.ClassTypeVariable` (initialized to `'$type'`). When non-empty, the reader **requires `$type` as the first key** of every object and raises `ETMSFNCReaderException` otherwise.
- New objects (collection items, list items) are created by class name with `GetClass(AClassName)`: custom classes must be registered with `RegisterClass` (RTL) or the read fails with `Type "X" not found` (unless `TTMSFNCPersistence.IgnoreExceptions := True`, then the item is skipped).
- A published object property whose current value is a `TComponent` **or nil** is "assignable": it is written as the component `Name` string (`""` for nil) and, on load, looked up with `FindComponent` on `TTMSFNCPersistence.RootObject` (only when that is set). All other object properties are read **into the existing instance** (`GetObjectProp`), so sub-objects must be created in the constructor; a nil sub-object is never created by the reader.
- Unknown JSON keys are skipped (`SkipValue`); property names are matched case-insensitively.
- Before writing a property the writer asks the object itself: if it implements `ITMSFNCPersistence`, `CanSaveProperty` decides (and fully replaces the `ExcludeProperties` check); then `OnCustomWriteProperty` / `ITMSFNCCustomReadWriteIO` can take over.

## TTMSFNCPersistence (class methods)

```delphi
TTMSFNCPersistence = class
public class var
  ClassTypeVariable: string;      // '$type'
  IgnoreExceptions: Boolean;      // False
public
  class procedure SaveSettingsToFile(AObject: TObject; AFileName: string);
  class procedure LoadSettingsFromFile(AObject: TObject; AFileName: string);
  class procedure SaveSettingsToStream(AObject: TObject; AStream: TStream);
  class procedure LoadSettingsFromStream(AObject: TObject; AStream: TStream);   // sets AStream.Position := 0 first
  class function CreateObject(const AClassName: string; BaseClass: TClass): TObject;
  class property ExcludeProperties: TTMSFNCExcludePropertyListArray;          // array of string
  class property OnCustomWriteProperty: TTMSFNCWriterCustomWritePropertyEvent;
  class property OnCustomReadProperty: TTMSFNCReaderCustomReadPropertyEvent;
  class property RootObject: TObject;
  class property IOReference: TObject;      // object implementing ITMSFNCPersistenceIO / ITMSFNCBasePersistenceIO
end;

TTMSFNCObjectPersistence = class
  class function SaveObjectToString(AObject: TObject): string;
  class procedure LoadObjectFromString(AObject: TObject; AString: string);
end;

TTMSFNCWriterCustomWritePropertyEvent = procedure(AObject: TObject; APropertyName: string; APropertyKind: TTypeKind; AWriter: TTMSFNCJSONWriter; var ACanWrite: Boolean) of object;
TTMSFNCReaderCustomReadPropertyEvent = procedure(AObject: TObject; APropertyName: string; APropertyKind: TTypeKind; AReader: TTMSFNCJSONReader; var ACanRead: Boolean) of object;
```

The class-level save methods have **no** `AAppearanceOnly` parameter; that exists only on the control methods below. Lower-level `TTMSFNCWriter.Create(AStream)` / `TTMSFNCReader.Create(AStream)` with `Write(AObject)`, `Read(AObject)`, `Read(AClass): TObject`, `WriteArray`, `ReadArray` are public too, but the class methods above cover normal use.

## Controls and components: SaveSettingsToFile / LoadSettingsFromFile

`TTMSFNCCustomControl` (base of every FNC visual control, including all UI Pack controls) and `TTMSFNCCustomComponent` implement `ITMSFNCPersistence`:

```delphi
procedure SaveSettingsToFile(AFileName: string; AAppearanceOnly: Boolean = False); virtual;
procedure LoadSettingsFromFile(AFileName: string); virtual;
procedure SaveSettingsToStream(AStream: TStream; AAppearanceOnly: Boolean = False); virtual;
procedure LoadSettingsFromStream(AStream: TStream); virtual;
function CanSaveProperty(AObject: TObject; APropertyName: string; APropertyType: TTypeKind): Boolean; virtual;
function CanLoadProperty(AObject: TObject; APropertyName: string; APropertyType: TTypeKind): Boolean; virtual;
// published events on TTMSFNCCustomControl:
property OnCanSaveProperty: TTMSFNCCustomControlCanSavePropertyEvent;
property OnCanLoadProperty: TTMSFNCCustomControlCanLoadPropertyEvent;
// TTMSFNCCustomControlCanSavePropertyEvent = procedure(Sender: TObject; AObject: TObject; APropertyName: string; APropertyType: TTypeKind; var ACanSave: Boolean) of object;
```

- On the control itself, the names in the global `ExcludePropertyList` are skipped: `Align`, `Anchors`, `Left`, `Top`, `Width`, `Height`, `Position`, `Size`, `Margins`, `Padding`, `Name`, `Visible`, `Enabled`, `Hint`, `ShowHint`, `PopupMenu`, `Tag`, `TabOrder`, `TabStop`, `Opacity`, `StyleElements`, `BitmapContainer`, ... (59 names). Layout and identity are therefore not restored; content and appearance are.
- `AAppearanceOnly = True` keeps only properties of type `TAlphaColor`/`TColor`/`TTMSFNCGraphicsFill`/`TTMSFNCGraphicsStroke`, names containing `Appearance`, and `Fill`, `Stroke`, `Font`.
- `LoadSettingsFromFile`/`Stream` on a control wrap the read in `BeginUpdate; ... EndUpdate; Invalidate`.

```delphi
uses System.IOUtils, System.TypInfo, VCL.TMSFNCTypes, VCL.TMSFNCPersistence;

procedure TForm1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  TMSFNCTreeView1.SaveSettingsToFile(TPath.Combine(TPath.GetDocumentsPath, 'tree.json'));
  TMSFNCPanel1.SaveSettingsToFile('panel-theme.json', True);   // colors / fills / fonts only
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
  if FileExists('tree.json') then
    TMSFNCTreeView1.LoadSettingsFromFile('tree.json');
end;

// skip a property while saving
procedure TForm1.TMSFNCTreeView1CanSaveProperty(Sender, AObject: TObject;
  APropertyName: string; APropertyType: TTypeKind; var ACanSave: Boolean);
begin
  if APropertyName = 'Columns' then     // AObject is the object that owns the property (control or sub-object)
    ACanSave := False;
end;
```

## Plain objects: TObject helper

`TTMSFNCObjectHelper` (unit `*.TMSFNCTypes`) works on any `TObject` with published properties:

```delphi
function ToJSON: string; overload;
function ToJSON(AExcludedProperties: TTMSFNCObjectExcludePropertyListArray): string; overload;
procedure FromJSON(const Value: string);
property JSON: string read ToJSON write FromJSON;
procedure SaveToJSONFile(const AFileName: string);
procedure LoadFromJSONFile(const AFileName: string);
procedure SaveToJSONStream(const AStream: TStream);
procedure LoadFromJSONStream(const AStream: TStream);
procedure Log;
```

`FromJSON` temporarily sets `ClassTypeVariable := ''` and so accepts JSON **without** `$type` keys (e.g. a REST response). `LoadFromJSONFile`/`LoadFromJSONStream` do not: they need the `$type` format that `SaveToJSONFile` writes.

```delphi
type
  TPerson = class(TPersistent)
  private
    FName: string; FAge: Integer; FTags: TStringList;
  public
    constructor Create;
    destructor Destroy; override;
  published
    property Name: string read FName write FName;
    property Age: Integer read FAge write FAge;
    property Tags: TStringList read FTags;          // created in Create, filled in place on load
  end;
// constructor TPerson.Create: FTags := TStringList.Create;  destructor: FTags.Free

var p: TPerson; s: string;
p := TPerson.Create;
try
  p.Name := 'Ann'; p.Age := 31; p.Tags.Add('admin');
  s := p.JSON;              // {"$type":"TPerson","Name":"Ann","Age":31,"Tags":["admin"]}
  p.FromJSON('{"Name":"Bob","Age":40}');   // no $type needed here
  p.SaveToJSONFile('person.json');
finally
  p.Free;
end;
```

## Interfaces for custom classes

```delphi
ITMSFNCPersistence = interface        // filter which properties are saved/loaded
  procedure SaveSettingsToFile(AFileName: string; AAppearanceOnly: Boolean = False);
  procedure LoadSettingsFromFile(AFileName: string);
  procedure SaveSettingsToStream(AStream: TStream; AAppearanceOnly: Boolean = False);
  procedure LoadSettingsFromStream(AStream: TStream);
  function CanSaveProperty(AObject: TObject; APropertyName: string; APropertyType: TTypeKind): Boolean;
  function CanLoadProperty(AObject: TObject; APropertyName: string; APropertyType: TTypeKind): Boolean;
end;
ITMSFNCCustomReadWriteIO = interface  // write/read one property yourself; set ACanWrite/ACanRead := False when handled
  procedure CustomWriteProperty(AObject: TObject; APropertyName: string; APropertyKind: TTypeKind; AWriter: TTMSFNCJSONWriter; var ACanWrite: Boolean);
  procedure CustomReadProperty(AObject: TObject; APropertyName: string; APropertyKind: TTypeKind; AReader: TTMSFNCJSONReader; var ACanRead: Boolean);
end;
ITMSFNCBaseListIO = interface         // on a TList/TObjectList/dictionary: which class to create for items
  function GetItemClass: TClass;
end;
ITMSFNCBaseCollectionIO = interface   // on a TCollection: add an item for a read object
  function AddItem(const AObject: TObject): TCollectionItem;
end;
ITMSFNCBasePersistenceIO = interface  // on IOReference: create objects by class name
  function CreateObject(const AClassName: string; const ABaseClass: TClass): TObject;
end;
ITMSFNCPersistenceIO = interface(ITMSFNCBasePersistenceIO)   // on IOReference: write references instead of objects
  function NeedsObjectReference(const AClass: TClass): Boolean;
  function GetObjectReference(const AObject: TObject): string;
  function FindObject(const AReference: string): TObject;
  procedure FixOwners(const AObject: TObject; const AObjectList: TObject);
end;
```

A class implementing these on a plain `TPersistent` needs working `QueryInterface`/`_AddRef`/`_Release` (derive from `TInterfacedPersistent`, or return -1 from `_AddRef`/`_Release` as FNC classes do).

## JSON to Delphi classes: TTMSFNCJSONToClass

Generates Delphi source (class declarations with published properties) from a JSON sample:

```delphi
class function ExportToDelphi(AJSONString: string; ACallBack: TTMSFNCJSONToClassExportEvent = nil): string; overload;
class function ExportToDelphi(AJSONString: string; AOptions: TTMSFNCJSONToClassOptions; ACallBack: TTMSFNCJSONToClassExportEvent = nil): string; overload;
class function ExportToDelphiFromFile(AFileName: string; ACallBack: TTMSFNCJSONToClassExportEvent = nil): string; overload;
function DefaultJSONToClassOptions: TTMSFNCJSONToClassOptions;   // record: SortProperties, DelphiCasing, AddConstructor, AddDestructor, AddAssign, AddUnit, BaseClass (cbcNone/cbcPersistent), AddImplementation, RemoveSpecialCharacters
```

## TTMSFNCObjectResolver (TMS.TMSFNCObjectResolver)

Reads or writes values through a dot/bracket path using extended RTTI (used by `TTMSFNCFilterRulesManager`).

```delphi
class function Resolve(ARoot: TObject; const APath: string): TTMSObjectPathResolverResult; static;
class function SetValue(ARoot: TObject; const APath: string; const AValue: TValue): TTMSObjectPathResolverResult; static;
class function GetCollectionPaths(AComponent: TComponent): TArray<string>; static;               // not on WEB
class function GetItemProperties(ASource: TComponent; const AItemsPath: string): TArray<TTMSFNCObjectPropertyInfo>; static;  // not on WEB
function RTTIValueToString(const AValue: TValue): string;    // global

TTMSObjectPathResolverResult = record
  Kind: TTMSObjectPathResolverResultKind;   // rrkError, rrkObject, rrkScalar, rrkArray, rrkArray2D
  Value: TValue;                            // rrkObject / rrkScalar; SetValue: number of writes (Integer)
  ArrayValues: TArray<TTMSObjectPathResolverElement>;            // Value, Index, Index2, SubArray
  Array2DValues: TArray<TArray<TTMSObjectPathResolverElement>>;  // [row][col]
  TypeName: string;
  ErrorMessage: string;
  function IsError: Boolean;
  function ToDisplayString: string;
end;
```

Path syntax: `Prop`, `Prop.Sub`, `Prop[n]` (TCollection/TList/array/indexed property), `Cells[col,row]`; index expressions `n`, `*`, `a..b`, `a..*`, `a..b:step`, `*:step`, `a|b|c`, `{PropName}` (value of a property on the current object). If `ARoot` is a `TComponent`, the first segment may be a child component name (`Form1` + `'Grid1.Cells[0,1]'`).

```delphi
uses TMS.TMSFNCObjectResolver, System.Rtti;
var r: TTMSObjectPathResolverResult; e: TTMSObjectPathResolverElement;
r := TTMSFNCObjectResolver.Resolve(Self, 'ListBox1.Items.Count');
if not r.IsError then Caption := RTTIValueToString(r.Value);

r := TTMSFNCObjectResolver.Resolve(TMSFNCTreeView1, 'Nodes[*].Values[0].Text');   // node text lives in Values[col].Text
for e in r.ArrayValues do Memo1.Lines.Add(RTTIValueToString(e.Value));

r := TTMSFNCObjectResolver.SetValue(TMSFNCTreeView1, 'Nodes[0..2].Expanded', TValue.From<Boolean>(True));
if r.IsError then ShowMessage(r.ErrorMessage);
```

## Platform notes

- WEB: `LoadSettingsFromFile` loads asynchronously (`TMemoryStream.LoadFromFile` with a callback); the object is not filled when the call returns. In WEB apps prefer `LoadSettingsFromStream` or `FromJSON` with a string you already have. `TTMSFNCPropertyInfo` is `TTypeMemberProperty` on WEB, `PPropInfo` elsewhere.
- `TTMSFNCJSONToClass` exists on all FNC builds (`{$IFDEF FNCLIB}`).
- Object resolver indexed properties on WEB are emulated (`TRttiIndexedProperty` helper in the unit).

## Does not exist / common mistakes

- `SaveToJSON` / `LoadFromJSON` / `SaveLayout` / `SaveToIni` / `SaveToRegistry` on FNC controls: use `SaveSettingsToFile` / `LoadSettingsFromFile` / `...ToStream` (or the helper `ToJSON` / `FromJSON` / `SaveToJSONFile`).
- `TTMSFNCPersistence.SaveSettingsToFile(Obj, FileName, True)`: the class method has no appearance-only flag; call `Control.SaveSettingsToFile(FileName, True)`.
- `TTMSFNCPersistence.ObjectToJSON` / `JSONToObject` / `SaveObjectToJSON`: use `obj.ToJSON`, `obj.FromJSON(s)`, `TTMSFNCObjectPersistence.SaveObjectToString` / `LoadObjectFromString`.
- Loading external JSON with `LoadSettingsFromFile` / `LoadFromJSONFile` / `LoadObjectFromString`: fails with `"$type" property not found in Object descriptor`. Use `obj.FromJSON(text)` or set `TTMSFNCPersistence.ClassTypeVariable := ''` around the call (restore `'$type'` afterwards; it is global).
- Expecting public (non-published) properties or fields in the JSON: only published properties are written.
- Expecting `Width`, `Height`, `Align`, `Visible`, `Enabled`, `Name`, `Tag` of a control to be saved: they are in `ExcludePropertyList`.
- Forgetting `RegisterClass(TMyItem)` for objects that must be created while reading (collection items of custom classes, `TObjectList<TMyItem>` items): `Type "TMyItem" not found`.
- `ITMSFNCPersistence.CanSaveProperty` together with `TTMSFNCPersistence.ExcludeProperties`: when the object implements the interface, its answer replaces the `ExcludeProperties` check.
- `TTMSFNCObjectResolver.SetValue(Root, Path, 'text')` with a string: the string overload is commented out in source; use `TValue.From<string>('text')`.
- `TTMSFNCObjectResolver.GetValue` / `Evaluate` / `Find`: the read method is `Resolve`; check `IsError` and `Kind` before reading `Value`.
