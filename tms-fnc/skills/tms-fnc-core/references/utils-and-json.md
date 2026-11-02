# Utilities and JSON (TTMSFNCUtils, TTMSFNCJSONReader, TTMSFNCJSONWriter, TMS.TMSFNCValue)

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCUtils`, `*.TMSFNCTypes` (JSON class helpers), `*.TMSFNCJSONReader`, `*.TMSFNCJSONWriter`, `TMS.TMSFNCValue`, `Next.Core.Promises`, `Next.Core.TTry`; demos `tms.fnc.core.demos\VCL\TMSFNCCloudBase`, `WEB\TMSFNCCloudBase`.

## Units

| Purpose | VCL | FMX | WEB | Lazarus |
|---|---|---|---|---|
| `TTMSFNCUtils` | `VCL.TMSFNCUtils` | `FMX.TMSFNCUtils` | `WEBLib.TMSFNCUtils` | `LCLTMSFNCUtils` |
| JSON class helpers (`TObject.ToJSON`, `TJSONValue.AsString` ...) | `VCL.TMSFNCTypes` | `FMX.TMSFNCTypes` | `WEBLib.TMSFNCTypes` | `LCLTMSFNCTypes` |
| Stream JSON reader / writer | `VCL.TMSFNCJSONReader` / `VCL.TMSFNCJSONWriter` | `FMX.` ... | `WEBLib.` ... | `LCLTMSFNC` ... |
| `TTMSFNCValue` helpers | `TMS.TMSFNCValue` (framework neutral, all frameworks) |||

- `TJSONValue`, `TJSONObject`, `TJSONArray` used by the helpers are the RTL classes: unit `System.JSON` (written `JSON` in the demos) on VCL/FMX, `WEBLib.JSON` on WEB, `fpjson` on Lazarus. Add that unit to `uses` yourself.
- `TMS.TMSFNCUtils` is an RTL-only copy (no Graphics/Controls/Forms; `OpenFile`, `Message`, `SelectFile`, bitmap helpers are compiled out). It is not in any package; it exists for non-visual/console code. In a VCL or FMX app use the `VCL.`/`FMX.` unit. Never put both prefixes of the same unit in one `uses` clause (same class names, ambiguous).
- Nothing here is a component; there is no palette entry. All `TTMSFNCUtils` members are `class` methods, call them on the class.

## TTMSFNCUtils: most used class methods (exact declarations)

```delphi
// shell / environment
class procedure OpenURL(AURL: string);
class procedure OpenFile(AFile: string; AControlReference: TControl = nil);   // not in TMS.TMSFNCUtils
class function GetDocumentsPath: string;
class function GetAppPath: string;
class function GetTempPath: string;
class function AddBackslash(const AValue: string): string;
class function AddForwardslash(const AValue: string): string;
class function GetResourceStream(AResourceName: string): TResourceStream; overload;
class function GetResourceStream(AResourceName: string; AInstance: NativeUInt): TResourceStream; overload;
class function GetDPIScale(AOwner: TComponent = nil; ADefaultDPI: Integer = -1): Single;
class procedure Log(const AMessage: string); overload;
class procedure Log(const AObject: TObject); overload;            // logs AObject.JSON (console.log on WEB)
class function &Message(const AMessage: string): Integer; overload;
class function SelectFile(var AFileName: string; const ADefaultFolder: string = ''; const AFilter: string = ''; const ACallBack: TTMSFNCUtilsFileCallBackEvent = nil): Boolean;
class function SaveFile(var AFileName: string; const AFilter: string = ''; const ACallBack: TTMSFNCUtilsFileCallBackEvent = nil): Boolean;
class function IfElse<T>(ACondition: Boolean; AResultTRUE, AResultFALSE: T): T;

// encoding, URL, streams
class function URLEncode(const AURL: string): string;
class function URLDecode(const AURL: string; const ATrim: Boolean = True): string;
class procedure SplitURL(AURL: string; var AHost: string; var APath: string; var AQuery: string; var APort: Integer);
class function Encode64(const AValue: string; const AURL: Boolean = False): string; overload;
class function Encode64(const AValue: TBytes; const AURL: Boolean = False): string; overload;
class function Decode64(const AValue: string; const AURL: Boolean = False): string; overload;
class function Decode64ToBytes(const AValue: string; const AURL: Boolean = False): TBytes; overload;
class function SaveStreamToBase64(const AStream: TStream; const AURL: Boolean = False): string;
class procedure LoadStreamFromBase64(const ABase64: string; const AStream: TStream; const AURL: Boolean = False);
class function SaveStreamToHexStr(const AStream: TStream): string;
class procedure LoadStreamFromHexStr(const AHexStr: string; const AStream: TStream);
class function FileToBase64(const AFile: TTMSFNCUtilsFile): string;
class function SaveBitmapToBase64(const ABitmap: TTMSFNCBitmapHelperClass; const AURL: Boolean = False): string;
class function CreateBitmapFromBase64(const ABase64: string; const AURL: Boolean = False): TTMSFNCBitmap;   // caller frees
class procedure LoadBitmapFromBase64(const ABase64: string; const ABitmap: TTMSFNCBitmapHelperClass; const AURL: Boolean = False);
class function GetMimeType(AFile: string): string; overload;
class function GetMimeType(AData: TStream; AResetPosition: Boolean = True): string; overload;
class function GetFileExtension(AMime: string): string;
class function DownloadImage(AURL: string): TMemoryStream;        // synchronous, caller frees
class function EscapeString(const AValue: string): string;
class function UnescapeString(const AValue: string): string;
class function HTMLStrip(AHTML: string): string;
class function FormatBytesAsString(ASize: Extended): String;
class procedure Split(const ADelimiter: Char; AInput: string; const AStrings: TStrings; const AClearEmptyStrings: Boolean = False); overload;
class function Split(const ADelimiter: Char; const AInput: string; const AClearEmptyStrings: Boolean = False): TTMSFNCUtilsStringArray; overload;

// numbers and dates (culture independent)
class function StrToFloatDot(AValue: string): Double;
class function FloatToStrDot(AValue: Double): string;
class function TryStrToFloatDot(AValue: string; var AResult: Double): Boolean;
class function DateTimeToISO(const ADateTime: TDateTime; AAddDelimiters: Boolean = False; AAddMilliSeconds: Boolean = False): string;
class function DateToISO(const ADate: TDate; AAddDelimiters: Boolean = False): string;
class function ISOToDateTime(const AISOString: string; AIsUTC: Boolean = False): TDateTime;
class function ISOToDate(const AISOString: string): TDate;
class function DateTimeToUTC(const ADateTime: TDateTime): string;     // local time + '+hh:00' offset
class function DateTimeToMilliSeconds(const ADateTime: TDateTime): Int64;   // Unix ms
class function EpochToDateTime(const AEpoch: string): TDateTime;       // string of Unix seconds
```

Notes from the implementation:
- `DateTimeToISO(d)` gives `yyyymmddThhnnss`; pass `AAddDelimiters = True` for `yyyy-mm-ddThh:nn:ss`. `AAddMilliSeconds` appends `.zzzZ`. It does no time-zone conversion.
- `SelectFile`/`SaveFile` are synchronous on desktop; on WEB the result arrives in the callback (`TTMSFNCUtilsFileCallBackEvent = reference to procedure(const AFile: string; const AResult: Boolean)`, `of object` on WEB/LCL).
- `SplitURL` treats a URL without scheme as https.

## TTMSFNCUtils JSON helpers

All take/return RTL JSON classes. `ParseJSON` returns a new object: **the caller frees it**. Values returned by the getters are owned by the parent, never free them.

```delphi
class function ParseJSON(AJSON: string): TJSONValue;
class function IsJSON(AJSON: string): Boolean;
class function GetJSONValue(AJSONValue: TJSONValue; APropertyName: string): TJSONValue;   // direct child, nil if missing
class function FindJSONValue(AJSONValue: TJSONValue; APath: string): TJSONValue;          // path, e.g. 'show.image.medium'
class function GetJSONProp(AJSONValue: TJSONValue; APropertyName: string): string;       // '' if missing or null
class function GetJSONIntegerValue(AJSONValue: TJSONValue; APropertyName: string): Integer;
class function GetJSONDoubleValue(AJSONValue: TJSONValue; APropertyName: string): Double;
class function GetJSONValueAsString(AJSONValue: TJSONValue): string;
class function GetJSONValueAsInteger(AJSONValue: TJSONValue): Integer;
class function GetJSONValueAsDouble(AJSONValue: TJSONValue): Double;
class function GetJSONValueAsBoolean(AJSONValue: TJSONValue): Boolean;
class function IsJSONTrue(AJSONValue: TJSONValue): Boolean;
class function IsJSONFalse(AJSONValue: TJSONValue): Boolean;
class function GetJSONArraySize(AJSONArray: TJSONArray): Integer;
class function GetJSONArrayItem(AJSONArray: TJSONArray; AIndex: Integer): TJSONValue;
class function GetJSONObjectSize(AJSONObject: TJSONObject): Integer;
class function GetJSONObjectItem(AJSONObject: TJSONObject; AIndex: Integer): TJSONValue;
class function GetJSONObjectName(AJSONObject: TJSONObject; AIndex: Integer): string;
```

They exist so the same code compiles against `System.JSON`, `WEBLib.JSON` and `fpjson`. Example from the TMSFNCCloudBase demo (VCL and WEB identical):

```delphi
uses VCL.TMSFNCUtils, JSON;

procedure TForm1.ParseShows(const AText: string);
var
  o, item, show, img: TJSONValue;
  ja: TJSONArray;
  I: Integer;
begin
  o := TTMSFNCUtils.ParseJSON(AText);
  if not Assigned(o) then
    Exit;
  try
    ja := o as TJSONArray;
    for I := 0 to TTMSFNCUtils.GetJSONArraySize(ja) - 1 do
    begin
      item := TTMSFNCUtils.GetJSONArrayItem(ja, I);
      show := TTMSFNCUtils.GetJSONValue(item, 'show');
      if Assigned(show) then
      begin
        ListBox1.Items.Add(TTMSFNCUtils.GetJSONProp(show, 'name'));
        img := TTMSFNCUtils.GetJSONValue(show, 'image');
        if Assigned(img) then
          FURLs.Add(TTMSFNCUtils.GetJSONProp(img, 'medium'));
      end;
    end;
  finally
    o.Free;   // frees all child values too
  end;
end;
```

## JSON class helpers (unit *.TMSFNCTypes)

```delphi
TTMSFNCObjectHelper = class helper for TObject
  function ToJSON: string; overload;
  function ToJSON(AExcludedProperties: TTMSFNCObjectExcludePropertyListArray): string; overload;
  procedure FromJSON(const Value: string);
  property JSON: string read ToJSON write FromJSON;
  property JSONValue: TJSONValue read ToJSONValue;       // new parsed tree, caller frees
  procedure Log;
  procedure SaveToJSONFile(const AFileName: string);
  procedure LoadFromJSONFile(const AFileName: string);
  procedure SaveToJSONStream(const AStream: TStream);
  procedure LoadFromJSONStream(const AStream: TStream);
end;

TTMSFNCJSONValueHelper = class helper for TJSONValue
  property Properties[AName: string]: TJSONValue; default;   // v['name']
  property AsArray: TJSONArray;
  property AsString: string;
  property AsDouble: Double;
  property AsInteger: Integer;
  property AsBoolean: Boolean;
  function Find(const APath: string): TJSONValue;
end;

TTMSFNCJSONArrayHelper = class helper for TJSONArray
  property Values[AIndex: Integer]: TJSONValue; default;
  property Length: Integer;
end;
```

These are thin wrappers over `TTMSFNCPersistence` and the `TTMSFNCUtils.GetJSON*` methods; see persistence.md for what gets serialized. The getters return nil / '' / 0 for a missing key instead of raising, so `Properties['a'].Properties['b']` on a missing `a` passes nil on. Prefer the explicit `Properties[...]` / `Values[...]` names over the `default` shorthand (`v['x']`): members of the RTL JSON class itself always win over a helper, so the shorthand is fragile across Delphi versions.

```delphi
var v: TJSONValue;
v := TTMSFNCUtils.ParseJSON('{"user":{"name":"Ann","age":31},"tags":["a","b"]}');
try
  ShowMessage(v.Properties['user'].Properties['name'].AsString + ' ' + IntToStr(v.Find('user.age').AsInteger));
  ShowMessage(v.Properties['tags'].AsArray.Values[1].AsString + ' of ' + IntToStr(v.Properties['tags'].AsArray.Length));
finally
  v.Free;
end;
```

## TTMSFNCJSONWriter / TTMSFNCJSONReader (streaming, no DOM)

Used internally by persistence; useful for writing large JSON without building a tree.

```delphi
TTMSFNCJSONWriter = class
  constructor Create(const AStream: TStream);
  function WriteBeginObject: TTMSFNCJSONWriter;   function WriteEndObject: TTMSFNCJSONWriter;
  function WriteBeginArray: TTMSFNCJSONWriter;    function WriteEndArray: TTMSFNCJSONWriter;
  function WriteName(const Name: string): TTMSFNCJSONWriter;
  function WriteString(const Value: string): TTMSFNCJSONWriter;
  function WriteRawString(const Value: string): TTMSFNCJSONWriter;
  function WriteBoolean(const Value: boolean): TTMSFNCJSONWriter;
  function WriteInteger(const Value: Int64): TTMSFNCJSONWriter;
  function WriteDouble(const Value: double): TTMSFNCJSONWriter;
  function WriteNull: TTMSFNCJSONWriter;
  procedure Close;                                  // only validates nesting
  property IndentLength: integer;                   // 0 = compact
end;

TTMSFNCJSONReader = class
  constructor Create(const AStream: TStream);
  procedure ReadBeginObject;  procedure ReadEndObject;
  procedure ReadBeginArray;   procedure ReadEndArray;
  function HasNext: boolean;  function Peek: TTMSFNCJSONToken;   // jstoBeginObject, jstoName, jstoText, jstoNumber, jstoBoolean, jstoNull, ...
  function ReadName: string;  function PeekName: string;
  function ReadString: string; function ReadInteger: integer; function ReadInt64: Int64;
  function ReadDouble: double; function ReadBoolean: boolean;  procedure ReadNull;
  procedure SkipValue;        function IsNull: boolean;        function Eof: boolean;
end;
```

```delphi
var
  ss: TStringStream;
  w: TTMSFNCJSONWriter;
  r: TTMSFNCJSONReader;
begin
  ss := TStringStream.Create('', TEncoding.UTF8);
  try
    w := TTMSFNCJSONWriter.Create(ss);
    try
      w.IndentLength := 2;
      w.WriteBeginObject;
      w.WriteName('name').WriteString('Ann');
      w.WriteName('scores').WriteBeginArray.WriteInteger(7).WriteInteger(9).WriteEndArray;
      w.WriteEndObject;
      w.Close;
    finally
      w.Free;          // text is copied into ss only here
    end;

    ss.Position := 0;
    r := TTMSFNCJSONReader.Create(ss);
    try
      r.ReadBeginObject;
      while r.HasNext do
        if r.ReadName = 'name' then
          Caption := r.ReadString
        else
          r.SkipValue;
      r.ReadEndObject;
    finally
      r.Free;
    end;
  finally
    ss.Free;
  end;
end;
```

## TMS.TMSFNCValue (TTMSFNCValue)

`TTMSFNCValue = TValue` (RTL `System.Rtti`) on VCL/FMX/LCL, `JSValue` on WEB. Used by the filter builder, filter rules and the DataGrid cell values. Global functions (no class prefix):

```delphi
function TextToFNCValue(AValueText: string): TTMSFNCValue; overload;        // detects number/date/bool/text
function FNCValueToString(AValue: TTMSFNCValue): string; overload;
function FNCValueFromString(const AValue: string): TTMSFNCValue;
function FNCValueFromInteger(AValue: Integer): TTMSFNCValue;
function FNCValueFromDouble(AValue: Double): TTMSFNCValue;
function FNCValueFromBoolean(AValue: Boolean): TTMSFNCValue;
function TValueToFNCValue(AValue: TValue): TTMSFNCValue;
function ValueToString(AValue: TTMSFNCValue): string; overload;
function ValueToInteger(AValue: TTMSFNCValue): Integer; overload;
function ValueToFloat(AValue: TTMSFNCValue): Double; overload;
function ValueToDateTime(AValue: TTMSFNCValue): TDateTime; overload;
function ValueToBoolean(AValue: TTMSFNCValue): Boolean; overload;
function ValueIsEmpty(AValue: TTMSFNCValue): Boolean;
function CompareFNCValue(AValue1: TTMSFNCValue; AValue2: TTMSFNCValue; ATypeKind: TTypeKind = tkUnknown): Integer; overload;
function IsFNCValueEqual(AValue1: TTMSFNCValue; AValue2: TTMSFNCValue; ATypeKind: TTypeKind = tkUnknown): Boolean; overload;
function GetEmptyFNCValue: TTMSFNCValue;
```
Most have a second overload taking `AFormatSettings: TFormatSettings`.

## Next.Core.Promises / Next.Core.TTry

MIT-licensed third-party units (Laurens van Run) compiled into `TMSFNCCorePkg` (VCL/FMX only, not WEB). No FNC Core or UI Pack component exposes them; other TMS products build on them. Entry points: `Promise.New<T>`, `Promise.Resolve<T>(AFunc)`, `Promise.All<T>`, `IPromise<T>.ThenBy / Catch / &Finally / Await / Main`; `TTry.&Of<T>(AFunc): ITry<T>` with `Map`, `Recover`, `Fail`, `Accept`, `Resolve`. Use them only if the user asks; do not use them for FNC callbacks.

## Platform notes

- WEB: `TJSONValue` comes from `WEBLib.JSON`; the getters behave the same. `Log(AObject)` writes the object to `console.log`. Method pointers passed as callbacks need `@` in pas2js (`@DoDone`).
- `TTMSFNCUtilsFile` is a `string` path on desktop and a record `(Data: TJSUint8Array; Name: string)` on WEB.
- `GetFonts` on WEB returns a fixed list of common web fonts.
- `DownloadImage` is synchronous (WinInet/NSURL/curl); on WEB prefer `TTMSFNCCloudBase` (cloud-base-and-http.md).

## Does not exist / common mistakes

- `TTMSFNCUtils.EncodeBase64` / `DecodeBase64` / `Base64ToFile` / `StreamToBase64`: use `Encode64`, `Decode64`, `Decode64ToBytes`, `SaveStreamToBase64`, `LoadStreamFromBase64`, `FileToBase64`.
- `TTMSFNCUtils.HTTPEncode` / `URLEncodeParam`: use `URLEncode` / `URLDecode`.
- `TTMSFNCUtils.ShellExecute`, `OpenDocument`, `OpenBrowser`: use `OpenURL` (URLs) or `OpenFile` (local files).
- `TTMSFNCUtils.DownloadFile` / `HTTPGet`: not here; use `TTMSFNCCloudBase.DownloadFileFromURL` or `SimpleGETSyncAsString` (cloud-base-and-http.md), or `DownloadImage` for an image stream.
- `TTMSFNCUtils.GetJSONString` / `GetJSONInteger` / `GetJSONBoolean`: the names are `GetJSONProp` (string), `GetJSONIntegerValue`, `GetJSONDoubleValue`, `GetJSONValueAsBoolean`.
- `TTMSFNCUtils.ObjectToJSON` / `JSONToObject`: use the `TObject` helper `obj.ToJSON` / `obj.FromJSON(s)` (unit `*.TMSFNCTypes`) or `TTMSFNCObjectPersistence.SaveObjectToString` / `LoadObjectFromString`.
- `TTMSFNCUtils.DateTimeToEpoch` / `UnixToDateTime`: use `DateTimeToMilliSeconds` (ms) and `EpochToDateTime(const AEpoch: string)` (seconds, as string); the RTL `DateUtils.DateTimeToUnix` is fine too.
- `TTMSFNCUtils.ISOToDateTime` already exists; do not confuse with `DateTimeToISO` output, which has no delimiters unless `AAddDelimiters = True`.
- Freeing the result of `GetJSONValue` / `GetJSONArrayItem` / `v['x']`: they are children of the parsed root; free only the `ParseJSON` (or `JSONValue`) result.
- Reading the stream right after `TTMSFNCJSONWriter.Close`: it is still empty. Free the writer first.
- `feoNotContains`, `NotContainsOperator`: commented out in source; see data-binding.md (use `IsInverted`).
- Another `class helper for TObject` / `TJSONValue` in scope (e.g. from another library) hides the FNC one: only the last helper in `uses` is active.
