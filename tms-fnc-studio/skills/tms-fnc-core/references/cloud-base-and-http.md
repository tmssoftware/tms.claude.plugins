# HTTP requests and HTTP server (TTMSFNCCloudBase, TTMSFNCHTTPServer)
> Sections (line ranges): 6-16 Units and palette · 17-64 Request model · 65-105 TTMSFNCCustomCloudBase / TTMSFNCCloudBase · 106-176 Examples · 177-216 TTMSFNCHTTPServer · 217-223 Platform notes · 224-236 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCCloudBase` (+ platform units `.Win`, `.Mac`, `.Android`, `.Unix`, `.WEB`), `TMS.TMSFNCHTTPServer` (+ `.Win`, `.General`), package `.dpk` files; demos `tms.fnc.core.demos\VCL\TMSFNCCloudBase`, `FMX\TMSFNCCloudBase`, `WEB\TMSFNCCloudBase`.

## Units and palette

| | VCL | FMX | WEB | Lazarus |
|---|---|---|---|---|
| `TTMSFNCCloudBase` | `VCL.TMSFNCCloudBase` | `FMX.TMSFNCCloudBase` | `WEBLib.TMSFNCCloudBase` | `LCLTMSFNCCloudBase` |

- Add only the main unit. The platform implementation (`*.TMSFNCCloudBase.Win` = WinInet, `.Mac` = NSURLSession (macOS/iOS), `.Android` = HttpURLConnection, `.Unix` = libcurl, `.WEB` = XMLHttpRequest) is pulled in by the main unit's `implementation uses`.
- `TTMSFNCCloudBase` is **not registered on the tool palette** (no `RegisterComponents` call). Create it in code: `TTMSFNCCloudBase.Create` (parameterless constructor exists) or `TTMSFNCCloudBase.Create(Self)`.
- It is the base class of the TMS FNC Cloud Pack services, Maps services etc.; descendants use the same `Request` / `ExecuteRequest` API.
- `TMS.TMSFNCCloudBase` is an RTL-only copy, not in a package; use the `VCL.`/`FMX.` unit in GUI apps.

## Request model (exact declarations)

```delphi
TTMSFNCCloudBaseRequestMethod = (rmGET, rmPOST, rmPOSTMULTIPART, rmPOSTMULTIPARTRELATED, rmPUT, rmPUTMULTIPART,
  rmPUTMULTIPARTRELATED, rmDELETE, rmPATCH, rmUPDATE);
TTMSFNCCloudBaseRequestResultType = (rrtString, rrtStream, rrtFile);
TTMSFNCCloudBaseRequestResultEvent = reference to procedure(const ARequestResult: TTMSFNCCloudBaseRequestResult);   // "of object" on Lazarus
TTMSFNCCloudBaseRequestResultProgressEvent = reference to procedure(const ARequestResult: TTMSFNCCloudBaseRequestResult; AProgress: Single);

TTMSFNCCloudBaseRequest = class
  procedure Clear; virtual;                 // resets everything incl. headers, Method := rmGET, ResultType := rrtString
  procedure ClearHeaders; virtual;
  function AddHeader(const AName: string; const AValue: string): TTMSFNCCloudBaseRequestHeader;
  function AddBasicAuthHeader(const AUserName: string; const APassword: string): TTMSFNCCloudBaseRequestHeader;
  function GetURL: string;                  // Host + ':' + Port (if > 0) + Path + '?' + Query
  property Host: string;                    // scheme + host, e.g. 'https://api.example.com' (may also be a full URL)
  property Port: Integer;
  property Path: string;                    // '/v1/items'
  property Query: string;                   // 'q=abc&page=2' (no leading '?'); URL-encode values yourself
  property Method: TTMSFNCCloudBaseRequestMethod default rmGET;
  property PostData: string;                // body for POST/PUT/PATCH
  property Headers: TTMSFNCCloudBaseRequestHeaders;
  property CustomHeaders: Boolean;          // True: do not add automatic Content-Type for uploads
  property ResultType: TTMSFNCCloudBaseRequestResultType default rrtString;
  property ResultFile: string;              // target path for rrtFile
  property UploadStream: TMemoryStream;     // created on demand
  property UploadFile: TTMSFNCUtilsFile;
  property Agent: string;                   // default 'Mozilla/5.001 (windows; ...)'
  property ReadTimeout: Integer;            // ms, default 60000
  property ConnectTimeout: Integer;         // ms, default 60000
  property Name: string;
  property DataString: String;  property DataObject: TObject;  property DataInteger: NativeInt;
  property DataBoolean: Boolean; property DataPointer: Pointer; property DataInt64: Int64;   // user tags
end;

TTMSFNCCloudBaseRequestResult = class(TTMSFNCCloudBaseRequest)   // copy of Request + response
  property ResultString: string;
  property ResultStream: TMemoryStream;
  property ResponseCode: Integer;
  property Success: Boolean;                // ResponseCode in ValidHTTPCodes = [200, 201, 202, 204]
  property ResponseHeaders: TTMSFNCCloudBaseRequestHeaders;
  function GetResponseHeader(AName: string): string;
  property ResultBytesReceived: Int64;  property ResultTotalBytes: Int64;
  property Async: Boolean;  property Running: Boolean;
  procedure Cancel; virtual;
end;
```

## TTMSFNCCustomCloudBase / TTMSFNCCloudBase

```delphi
constructor Create; reintroduce; overload; virtual;
constructor Create(AOwner: TComponent); overload; override;
function ExecuteRequest(const ARequestResultEvent: TTMSFNCCloudBaseRequestResultEvent = nil;
  const ARequestResultProgressEvent: TTMSFNCCloudBaseRequestResultProgressEvent = nil;
  const AAsync: Boolean = True): TTMSFNCCloudBaseRequestResult; virtual;     // WEB: returns TJSPromise
function AddRequest(...same params...): TTMSFNCCloudBaseRequestResult; virtual; // queue without starting
procedure ExecuteAllRequests;
procedure CancelRequests; virtual;
procedure CancelRequest(const ARequest: TTMSFNCCloudBaseRequestResult); virtual;
function GetRequestCount(const IsRunning: Boolean = False; const ARequestName: string = ''): Integer; virtual;
property Request: TTMSFNCCloudBaseRequest;              // the request you fill in
property RequestResult: TTMSFNCCloudBaseRequestResult;  // last completed
property RunningRequests: TTMSFNCCloudBaseRequests;
property PostDataBuilder: TTMSFNCCloudBaseRequestPostDataBuilder;   // multipart body helper
class procedure SimpleGETAsyncAsString(const AURL: string; const ARequestResultEvent: TTMSFNCCloudBaseRequestResultEvent);
class procedure SimpleGETAsyncAsStream(const AURL: string; const ARequestResultEvent: TTMSFNCCloudBaseRequestResultEvent);
class procedure DownloadFileFromURL(const AURL: string; const ARequestResultEvent: TTMSFNCCloudBaseRequestResultEvent);
class function SimpleGETSyncAsString(const AURL: string): string;          // not on WEB / Lazarus
class function SimpleGETSyncAsStream(const AURL: string): TMemoryStream;   // not on WEB / Lazarus
class procedure Curl(const ACurl: string; ACallback: TTMSFNCCloudBaseRequestResultEvent); overload;  // parses a curl command line; not WEB/Lazarus
// published on TTMSFNCCloudBase:
property Logging: Boolean default False;  property LogFileName: string;
property OnRequestStarted, OnRequestComplete, OnRequestCancelled: ...(Sender: TObject; const ARequestResult: TTMSFNCCloudBaseRequestResult);
property OnRequestProgress: TTMSFNCCloudBaseProgressEvent;   // (Sender; const ARequestResult; AProgress: Single; AUpload: Boolean)
property OnRequestLog: TTMSFNCCloudBaseLogEvent;             // (Sender; const ARequestResult; AMessage: string)
property OnRequestsComplete: TNotifyEvent;
```

Global shortcuts in the same unit: `HTTPCloudRequest(const AURL: string; AResultType = rrtString; AMethod = rmGET; const ARequestResultEvent = nil)`, `HTTPCloudRequest(const AHost, APath, AQuery, APostData: string; AResultType = rrtString; AMethod = rmPOST; const ARequestResultEvent = nil)`, `HTTPAddHeader`, `HTTPClearHeaders`, `HTTPPostDataBuilder`. They use one hidden global instance.

### Execution model (from source)

- `ExecuteRequest` copies `Request` into a new `TTMSFNCCloudBaseRequestResult`, so you can `Request.Clear` and prepare the next call immediately.
- Async (default, desktop/mobile): runs in a `TTask`; the **`ExecuteRequest` callback is marshalled to the main thread** with `TThread.Queue`. The result object is owned by `RunningRequests` and removed (freed) after your callback: never free it, copy `ResultString`/`ResultStream` if you need them later.
- The component events `OnRequestComplete` / `OnRequestStarted` are raised by the platform code from the **worker thread** for async requests (e.g. WinInet code calls `OnComplete` directly). Update UI from the per-request callback, not from these events (or wrap in `TThread.Queue`).
- `AAsync = False` executes in the calling thread and returns the filled result (desktop only).
- No `Content-Type` is added for `PostData`; add it yourself. For `UploadStream`/`UploadFile` an `application/octet-stream` or multipart content type is added unless `CustomHeaders := True`.

## Examples

GET JSON (TMSFNCCloudBase demo, VCL; WEB demo is identical except `@DoGetMovies`):

```delphi
uses VCL.TMSFNCCloudBase, VCL.TMSFNCUtils, JSON;

procedure TForm1.Button1Click(Sender: TObject);
begin
  if not Assigned(FCloud) then
    FCloud := TTMSFNCCloudBase.Create(Self)
  else
    FCloud.Request.Clear;
  FCloud.Request.Host := 'https://api.tvmaze.com';
  FCloud.Request.Path := '/search/shows';
  FCloud.Request.Query := 'q=' + TTMSFNCUtils.URLEncode(Edit1.Text);
  FCloud.Request.Method := rmGET;
  FCloud.ExecuteRequest(DoGetShows);
end;

procedure TForm1.DoGetShows(const ARequestResult: TTMSFNCCloudBaseRequestResult);
begin
  if not ARequestResult.Success then
  begin
    ShowMessage(Format('HTTP %d: %s', [ARequestResult.ResponseCode, ARequestResult.ResultString]));
    Exit;
  end;
  ParseShows(ARequestResult.ResultString);   // see utils-and-json.md
end;
```

POST JSON with an anonymous callback and bearer token:

```delphi
FCloud.Request.Clear;
FCloud.Request.Host := 'https://api.example.com';
FCloud.Request.Path := '/v1/orders';
FCloud.Request.Method := rmPOST;
FCloud.Request.AddHeader('Content-Type', 'application/json');
FCloud.Request.AddHeader('Authorization', 'Bearer ' + FToken);
FCloud.Request.PostData := '{"item":"A12","qty":3}';
FCloud.ExecuteRequest(
  procedure(const ARequestResult: TTMSFNCCloudBaseRequestResult)
  begin
    Memo1.Lines.Text := ARequestResult.ResultString;   // main thread
  end);
```

Download binary (stream) with progress:

```delphi
FCloud.Request.Clear;
FCloud.Request.Host := ImageURL;          // a full URL in Host works: GetURL = Host + Path + Query
FCloud.Request.ResultType := rrtStream;
FCloud.ExecuteRequest(
  procedure(const ARequestResult: TTMSFNCCloudBaseRequestResult)
  begin
    if ARequestResult.Success then
    begin
      ARequestResult.ResultStream.Position := 0;
      Image1.Picture.LoadFromStream(ARequestResult.ResultStream);   // copy/load now; the result is freed afterwards
    end;
  end,
  procedure(const ARequestResult: TTMSFNCCloudBaseRequestResult; AProgress: Single)
  begin
    ProgressBar1.Position := Round(AProgress);
  end);
```

One-liners: `TTMSFNCCloudBase.SimpleGETAsyncAsString(URL, procedure(const R: TTMSFNCCloudBaseRequestResult) begin ... R.ResultString ... end);` and (desktop) `s := TTMSFNCCloudBase.SimpleGETSyncAsString(URL);`.

## TTMSFNCHTTPServer (TMS.TMSFNCHTTPServer)

A small embedded HTTP server. The unit is framework neutral but is **not compiled into any FNC Core package** and the component is not registered: add `TMS.TMSFNCHTTPServer` (and its `.Win`/`.General` units, found automatically on the library path) to the project and create it in code. Windows uses the http.sys HTTP Server API; other platforms use Indy (`IdHTTPServer`, `IdSSLOpenSSL`). Not available on WEB.

```delphi
TTMSFNCHTTPServer = class(TTMSFNCCustomHTTPServer)
public
  property BindingIP: string;
  property OnCommandGet: TTMSFNCHTTPServerCommandEvent;     // Windows: GET, POST and HEAD
  property OnCommandOther: TTMSFNCHTTPServerCommandEvent;   // other verbs
published
  property Active: Boolean;  property Port: Word;  property UseSSL: Boolean;
end;
TTMSFNCHTTPServerCommandEvent = procedure(AConnection: TTMSFNCHTTPServerConnection; ARequest: TTMSFNCHTTPServerRequest; AResponse: TTMSFNCHTTPServerResponse) of object;
// ARequest: Command, CommandType (hsmGET, hsmPOST, ...), URI, QueryParams, PostStream, Headers, RemoteIP, RemotePort
// AResponse: ResponseCode, ResponseText, ContentText, Headers (SetHeader/AddValue/Get/Exists/Remove), CloseConnection, Redirect(AURL)
```

```delphi
uses TMS.TMSFNCHTTPServer;

procedure TForm1.FormCreate(Sender: TObject);
begin
  FServer := TTMSFNCHTTPServer.Create(Self);
  FServer.Port := 8080;
  FServer.OnCommandGet := DoCommandGet;
  FServer.Active := True;
end;

procedure TForm1.DoCommandGet(AConnection: TTMSFNCHTTPServerConnection;
  ARequest: TTMSFNCHTTPServerRequest; AResponse: TTMSFNCHTTPServerResponse);
begin
  // runs on a server worker thread: no direct UI access
  AResponse.ResponseCode := 200;
  AResponse.Headers.SetHeader('Content-Type', 'application/json');
  AResponse.ContentText := '{"path":"' + ARequest.URI + '"}';
  // content is written automatically after the handler unless you called WriteHeader/WriteContent
end;
```

## Platform notes

- WEB: `ExecuteRequest` returns a `TJSPromise` (resolved after completion when `AAsync = False`, so it can be awaited in an `async` method); callbacks need `@Method` in pas2js; `SimpleGETSync*` and `Curl` do not exist; CORS rules of the browser apply; `UploadFile` is a `TTMSFNCUtilsFile` record.
- Lazarus: callback types are `of object` (no anonymous methods); `SimpleGETSync*` and `Curl` are not available.
- Linux (FMXLinux) uses libcurl; it must be installed on the target.
- Android needs the INTERNET permission in the project options.

## Does not exist / common mistakes

- `TTMSFNCCloudBase.Get(URL)` / `Post(URL, Body)` / `ExecuteRequestAsync` / `RequestAsync`: fill `Request` and call `ExecuteRequest`; for quick GETs use `SimpleGETAsyncAsString` / `SimpleGETSyncAsString`.
- `Request.URL` / `Request.Url := 'https://...'`: there is no URL property; set `Host` (+ `Path`, `Query`), `GetURL` only reads.
- `Request.Body` / `Request.Content` / `Request.ContentType` / `Request.Timeout`: use `PostData`, `AddHeader('Content-Type', ...)`, `ReadTimeout` / `ConnectTimeout`.
- `ARequestResult.StatusCode` / `ResultJSON` / `ResponseText` / `IsSuccess`: use `ResponseCode`, parse `ResultString` with `TTMSFNCUtils.ParseJSON`, `Success`.
- `OnRequestResult` / `OnRequestError` / `OnResponse` events: there are none; check `Success` in the callback or use `OnRequestComplete` (worker thread).
- Freeing `ARequestResult` or keeping a reference to `ResultStream` after the callback: the component frees async results.
- Putting `'?'` in `Query` or a query string in `Path`: `GetURL` already inserts `?`.
- Expecting Delphi `TNetHTTPClient`/Indy behaviour (exceptions on 4xx/5xx): CloudBase does not raise; it sets `ResponseCode` and `Success = False`.
- Dropping `TTMSFNCCloudBase` from the palette: it is not on the palette; create in code.
- `TTMSFNCHTTPServer.OnRequest` / `OnGet` / `Response.ContentStream`: use `OnCommandGet` / `OnCommandOther` and `AResponse.ContentText` (`ContentStream` is commented out in source).
