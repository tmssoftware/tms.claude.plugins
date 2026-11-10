# Web browser controls (TTMSFNCWebBrowser, TTMSFNCEdgeWebBrowser, TTMSFNCWebCoreClientBrowser)
> Sections (line ranges): 6-17 Units and palette · 18-146 TTMSFNCWebBrowser: core API · 147-195 TTMSFNCEdgeWebBrowser: WebView2-only extras · 196-203 WebView2 runtime and loader DLL · 204-226 TTMSFNCWebCoreClientBrowser · 227-233 Platform notes · 234-246 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCWebBrowser`, `*.TMSFNCWebBrowser.Win`, `WEBLib.TMSFNCWebBrowser.WEB`, `*.TMSFNCEdgeWebBrowser`, `*.TMSFNCWebCoreClientBrowser`.

## Units and palette

| Class | Unit | Frameworks | Palette |
|---|---|---|---|
| `TTMSFNCWebBrowser` | `*.TMSFNCWebBrowser` | VCL, FMX, LCL, WEB | TMS FNC UI |
| `TTMSFNCEdgeWebBrowser` | `*.TMSFNCEdgeWebBrowser` (+ `*.TMSFNCWebBrowser` for the types) | VCL, FMX (Windows only: `pidWin32 or pidWin64`) | TMS FNC UI |
| `TTMSFNCWebCoreClientBrowser` | `*.TMSFNCWebCoreClientBrowser` | VCL, FMX (registered `{$IFNDEF LCLLIB}`), no WEB | TMS FNC UI |

Prefix rule: `VCL.` / `FMX.` / `WEBLib.`, LCL is `LCLTMSFNC...`. Event param types (`TTMSFNCCustomWebBrowserNavigateCompleteParams` etc.), `TTMSFNCWebBrowserPrintSettings`, `TTMSFNCWebBrowserCookie` and `ITMSFNCCustomWebBrowserBridge` are declared in `*.TMSFNCWebBrowser`.

Native engine per platform: Windows = Edge Chromium **WebView2** (both `TTMSFNCWebBrowser` and `TTMSFNCEdgeWebBrowser`), macOS/iOS = WKWebView, Android = WebView, Linux = WebKitGTK, WEB = a host element in the page (limited, see platform notes).

## TTMSFNCWebBrowser: core API

All members below are public on `TTMSFNCWebBrowser` and `TTMSFNCEdgeWebBrowser`.
```delphi
procedure Navigate; overload;                        // navigates to URL
procedure Navigate(const AURL: string); overload;
procedure LoadHTML(AHTML: String);
procedure LoadFile(AFile: String);
procedure ExecuteJavaScript(AScript: String; ACompleteEvent: TTMSFNCWebBrowserJavaScriptCompleteEvent = nil; AImmediate: Boolean = False);
function ExecuteJavaScriptSync(AScript: string): string;   // pumps messages up to ~60 s; not on WEB/Android
procedure GoBack;  procedure GoForward;  procedure Reload;  procedure StopLoading;
function CanGoBack: Boolean;  function CanGoForward: Boolean;
procedure AddBridge(ABridgeName: string; ABridgeObject: TObject);
procedure RemoveBridge(ABridgeName: string);
function GetBridgeCommunicationLayer(ABridgeName: string): string;
procedure CaptureScreenShot(ACompleteEvent: TTMSFNCWebBrowserCaptureScreenShotCompleteEvent = nil);
procedure ShowDebugConsole;
procedure ClearCache;
procedure Initialize;  procedure DeInitialize;
function NativeBrowser: Pointer;  function NativeEnvironment: Pointer;
property URL: string;                                // published
property UserAgent: string;  property CacheFolder: string;  property CacheFolderName: string;  property AutoClearCache: Boolean;
property EnableContextMenu, EnableShowDebugConsole, EnableAcceleratorKeys: Boolean;  // public on TTMSFNCWebBrowser
property DesigntimeEnabled: Boolean;  property DeferInitialization: Boolean;          // published
// published events
property OnInitialized: TNotifyEvent;
property OnBeforeNavigate: TTMSFNCCustomWebBrowserBeforeNavigate;
property OnNavigateComplete: TTMSFNCCustomWebBrowserNavigateComplete;
property OnDocumentComplete: TNotifyEvent;
property OnCaptureScreenShot: TTMSFNCCustomWebBrowserCaptureScreenShot;
property OnHardwareButtonClicked: TNotifyEvent;   // Android back button
property OnError: TTMSFNCWebBrowserErrorEvent;    // AError.Message, AError.&Type ('DLL_ERROR', ...)
```

Types:
```delphi
TTMSFNCWebBrowserJavaScriptCompleteEvent = reference to procedure(const AValue: string);   // LCL: procedure ... of object
TTMSFNCWebBrowserCaptureScreenShotCompleteEvent = reference to procedure(const AScreenShot: TTMSFNCBitmap);
TTMSFNCCustomWebBrowserNavigateCompleteParams = record URL: String; Success: Boolean; ErrorCode: Integer; end;
TTMSFNCCustomWebBrowserBeforeNavigateParams = record URL: String; Cancel: Boolean; end;
TTMSFNCCustomWebBrowserNavigateComplete = procedure(Sender: TObject; var Params: TTMSFNCCustomWebBrowserNavigateCompleteParams) of object;
TTMSFNCCustomWebBrowserBeforeNavigate = procedure(Sender: TObject; var Params: TTMSFNCCustomWebBrowserBeforeNavigateParams) of object;
```

### Initialization is asynchronous

The native browser is created after the control gets a handle. Until then (Windows: until the WebView2 controller exists) `Navigate(AURL)`, `LoadHTML`, `ExecuteJavaScript` and `AddBridge` are **silently ignored**. When initialization completes the control navigates to `URL` and fires `OnInitialized`. So either set `URL` before initialization, or do the first `LoadHTML` / `AddBridge` / script in `OnInitialized`.

### Example: navigation (demo `VCL\TMSFNCWebBrowser`)

```delphi
uses VCL.TMSFNCWebBrowser, VCL.TMSFNCTypes;

procedure TForm1.FormCreate(Sender: TObject);
begin
  FBrowser := TTMSFNCWebBrowser.Create(Self);
  FBrowser.Parent := Self;
  FBrowser.Align := alClient;
  FBrowser.URL := 'https://www.tmssoftware.com';   // loaded once the engine is ready
  FBrowser.OnNavigateComplete := BrowserNavigateComplete;
  FBrowser.OnInitialized := BrowserInitialized;
end;

procedure TForm1.BrowserNavigateComplete(Sender: TObject;
  var Params: TTMSFNCCustomWebBrowserNavigateCompleteParams);
begin
  Edit1.Text := Params.URL;
  btnBack.Enabled := FBrowser.CanGoBack;
  btnForward.Enabled := FBrowser.CanGoForward;
end;

procedure TForm1.GoClick(Sender: TObject);
begin
  FBrowser.Navigate('https://' + Edit1.Text);
end;
```

### ExecuteJavaScript with a result

The callback is an anonymous method, invoked asynchronously. On Windows (WebView2) `AValue` is the **JSON-encoded** result: a string comes back with quotes (`"abc"`), `undefined` / `null` as `null`.
```delphi
FBrowser.ExecuteJavaScript('document.title',
  procedure(const AValue: string)
  begin
    Caption := AValue.DeQuotedString('"');
  end);

FBrowser.ExecuteJavaScript('document.getElementById("ratioP").innerHTML = "Done";');
```

### JS -> Delphi bridge (AddBridge)

The bridge object must implement `ITMSFNCCustomWebBrowserBridge` and expose a **published** `ObjectMessage` property; JavaScript sets it, the setter runs in Delphi.
```delphi
ITMSFNCCustomWebBrowserBridge = interface(IInterface)
  function GetObjectMessage: string;
  procedure SetObjectMessage(const AValue: string);
  property ObjectMessage: string read GetObjectMessage write SetObjectMessage;
end;
```
`GetBridgeCommunicationLayer('MyBridge')` returns JS defining `sendMyBridgeObjectMessage(value)` (Windows: `window.chrome.webview.hostObjects.sync.MyBridge.ObjectMessage = v`; macOS/iOS/Linux: `webkit.messageHandlers`; WEB: a `CustomEvent`). Demo `VCL\TMSFNCWebBrowser`:
```delphi
type
  TMyBridgeObject = class(TInterfacedPersistent, ITMSFNCCustomWebBrowserBridge)
  private
    function GetObjectMessage: string;
    procedure SetObjectMessage(const Value: string);
  published
    property ObjectMessage: string read GetObjectMessage write SetObjectMessage;
  end;

procedure TMyBridgeObject.SetObjectMessage(const Value: string);
begin
  Form1.Memo1.Lines.Add('From JS: ' + Value);
end;

procedure TForm1.BrowserInitialized(Sender: TObject);
const
  BridgeName = 'MyBridge';
begin
  FBridge := TMyBridgeObject.Create;               // keep a reference, free it yourself
  FBrowser.AddBridge(BridgeName, FBridge);
  FBrowser.LoadHTML('<html><head><script>' + FBrowser.GetBridgeCommunicationLayer(BridgeName) +
    '</script></head><body><button onclick="send' + BridgeName +
    'ObjectMessage(''Yes'');">Yes</button></body></html>');
end;
```
Call `RemoveBridge(BridgeName)` before freeing the bridge object.

## TTMSFNCEdgeWebBrowser: WebView2-only extras (Windows)

`TTMSFNCWebBrowser` on VCL/FMX is compiled with `FNCLIB` defined, so everything below is **hidden** on it (`{$IFNDEF FNCLIB}`). Use `TTMSFNCEdgeWebBrowser` for:
```delphi
property Settings: TTMSFNCWebBrowserSettings;   // EnableContextMenu, EnableShowDebugConsole, EnableAcceleratorKeys,
                                                // UsePopupMenuAsContextMenu, AllowExternalDrop, Language, AdditionalBrowserArguments
procedure GetCookies(AURI: string = '');        // result in OnGetCookies(Sender; ACookies: array of TTMSFNCWebBrowserCookie)
procedure AddCookie(ACookie: TTMSFNCWebBrowserCookie);   // record: Name, Value, Domain, Path, Expires, Secure, HTTPOnly, SameSite
procedure DeleteCookie(AName: string; ADomain: string; APath: string);
procedure DeleteAllCookies;
function InitialPrintSettings: TTMSFNCWebBrowserPrintSettings;  // record: Orientation (poPortrait/poLandscape), ScaleFactor, Margin*, PrintBackgrounds, PrintHeaderAndFooter, HeaderTitle, FooterURI ...
procedure Print; overload;  procedure Print(APrintSettings: TTMSFNCWebBrowserPrintSettings); overload;
procedure ShowPrintUI;
procedure PrintToPDF(AFileName: string); overload;   // OnPrintedToPDF(Sender; ASuccessful: Boolean)
procedure PrintToPDFStream; overload;                // result in OnGetPrintPDFStream(Sender; AStream: TMemoryStream)
procedure NavigateWithData(AURI: string; AMethod: string; ABody: string; AHeaders: TStrings = nil); overload;
procedure SetVirtualHostNameToFolderMapping(AHostName, AFolderPath: string; AAccessKind: TTMSFNCWebBrowserHostResourceAccessKind);
procedure ClearVirtualHostNameToFolderMapping(AHostName: string);
function FindOnPage(const ASearchTerm: string; ACaseSensitive: Boolean = False; AMatchWholeWord: Boolean = False; AHighlightAllMatches: Boolean = True; ASuppressDefaultDialog: Boolean = False): Boolean;
function FindNext: Boolean;  function FindPrevious: Boolean;  procedure StopFindOnPage;
procedure SubscribeDevtools(AEventName: string);  procedure CallDevToolsProtocolMethod(AMethodName: string; AParametersAsJSON: string);
procedure OpenTaskManager;
property Downloads: TTMSFNCWebBrowserDownloads;   // + CancelDownload/PauseDownload/ResumeDownload
function GetBrowserVersion: string;  function GetDocumentTitle: string;  function GetUserDataFolder: string;
// extra published events: OnWebMessageReceived (Params.WebMessageAsJSON, Params.Source), OnNewWindowRequested,
// OnPermissionRequested, OnScriptDialogOpening, OnSourceChanged, OnDocumentTitleChanged, OnDOMContentLoaded,
// OnGetConsoleMessage, OnDownloadStarted, OnDownloadStateChanged, OnProcessFailed, OnZoomFactorChanged, OnWebResourceRequested ...
```
Demo `VCL\TMSFNCEdgeWebBrowser\BrowserPrintAndPDF`:
```delphi
uses VCL.TMSFNCWebBrowser, VCL.TMSFNCEdgeWebBrowser;

procedure TForm2.PrintBtnClick(Sender: TObject);
var
  ps: TTMSFNCWebBrowserPrintSettings;
begin
  ps := TMSFNCEdgeWebBrowser1.InitialPrintSettings;
  ps.PrintHeaderAndFooter := False;
  ps.Orientation := poLandscape;     // TTMSFNCWebBrowserPrintOrientation; qualify it if VCL.TMSFNCPDFLib is also used
  TMSFNCEdgeWebBrowser1.Print(ps);
end;

procedure TForm2.PrintToPDFBtnClick(Sender: TObject);
begin
  TMSFNCEdgeWebBrowser1.PrintToPDF(GetCurrentDir + '\test.pdf');
end;
```
Other Edge demos: `Cookies`, `ContextMenu`, `DevTools`, `DownloadManager`, `NavigateWithData` (VCL and FMX).

## WebView2 runtime and loader DLL (Windows)

- Requires the **Microsoft Edge WebView2 Runtime** (Evergreen, preinstalled on Windows 11; installable on Windows 10).
- Requires the loader DLL next to the EXE (or on the DLL search path): **`WebView2Loader_x86.dll`** for Win32, **`WebView2Loader_x64.dll`** for Win64 (constant `CoreWebView2DLL` in `*.TMSFNCWebBrowser.Win`). It is loaded with `LoadLibrary` during unit initialization; deploy it with the application.
- Missing DLL → `OnError` / message "Could not initialize Edge Chromium! Please check if WebView2Loader_x64.dll is correctly distributed and accessible." Missing runtime → "...Please check Edge Chromium installation and verify correct version number."
- WebView2 needs a writable user-data/cache folder: `CacheFolder` / `CacheFolderName` (an uncreatable folder raises the cache-folder error). `AutoClearCache` clears it at start.
- `FindOnPage` needs WebView2 Runtime >= 1.0.3405.78.

## TTMSFNCWebCoreClientBrowser

A desktop/mobile host for a TMS WEB Core application (two-way messaging with the web app). It intercepts `webclientevent://` navigations and, on document complete, performs a handshake and fires `OnConnected`.
```delphi
procedure SendMessage(const AMessage: string);   // calls Application.ReceiveMessageFromClient in the web app
procedure Send(const AJSON: TJSONValue);
procedure Connect;
property OnReceiveMessage: TTMSFNCWebCoreClientBrowserReceiveMessageEvent; // procedure(Sender: TObject; AMessage: TJSONValue) of object
property OnConnected: TNotifyEvent;
```
```delphi
procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCWebCoreClientBrowser1.URL := 'http://localhost:8000/MyWebApp/index.html';
  TMSFNCWebCoreClientBrowser1.OnReceiveMessage := ClientReceiveMessage;
end;

procedure TForm1.ClientReceiveMessage(Sender: TObject; AMessage: TJSONValue);
begin
  Memo1.Lines.Add(AMessage.ToJSON);
end;
```

## Platform notes

- **WEB (`WEBLib.TMSFNCWebBrowser`)**: `LoadHTML` sets the control element's `innerHTML`; `ExecuteJavaScript` runs the script in the page; bridges work through DOM `CustomEvent`s. `Navigate`, `GoBack`, `GoForward`, `Reload`, `LoadFile` are **empty** (no-ops). `ExecuteJavaScriptSync` does not wait. No `TTMSFNCEdgeWebBrowser` and no `TTMSFNCWebCoreClientBrowser` on WEB.
- **VCL/FMX Windows**: both browser classes use WebView2. `TTMSFNCEdgeWebBrowser` just republishes the Edge-only API; it is not a different engine.
- **FMX**: native browser is a native window on top of the form; FMX controls cannot overlap it.
- **Android**: `ExecuteJavaScriptSync` does not block; use the callback form.

## Does not exist / common mistakes

- `ExecuteScript`, `EvaluateJavaScript`, `RunJavaScript`, `ExecJS`: the method is `ExecuteJavaScript(AScript, ACompleteEvent, AImmediate)`; the callback is an anonymous method `procedure(const AValue: string)`, not an event property. There is no `OnJavaScriptResult` / `OnExecuteScriptCompleted` event.
- `NavigateToString`, `LoadFromString`, `HTML := ...`, `Document`, `DocumentText`, `GetHTML`: use `LoadHTML(AHTML)`; read the DOM with `ExecuteJavaScript('document.documentElement.outerHTML', ...)`.
- `OnNavigationCompleted`, `OnLoadEnd`, `OnLoadStart`, `OnDocumentLoaded`: use `OnNavigateComplete` (`var Params: TTMSFNCCustomWebBrowserNavigateCompleteParams`), `OnBeforeNavigate` (set `Params.Cancel := True` to block), `OnDocumentComplete`.
- `TTMSFNCWebBrowserBridge` class, `RegisterBridge`, `AddJavaScriptBridge`, `window.external`: use `AddBridge(Name, Obj)` with a `TInterfacedPersistent` that implements `ITMSFNCCustomWebBrowserBridge` and publishes `ObjectMessage`, plus the JS from `GetBridgeCommunicationLayer`.
- `TMSFNCWebBrowser1.Settings`, `.GetCookies`, `.Print`, `.PrintToPDF`, `.NavigateWithData`, `.FindOnPage`, `.Downloads`, `OnWebMessageReceived` on `TTMSFNCWebBrowser`: compiled out (`{$IFNDEF FNCLIB}`). Use `TTMSFNCEdgeWebBrowser` (Windows only).
- `TTMSFNCEdgeWebBrowser.EnableContextMenu` etc. directly: on the Edge class use `Settings.EnableContextMenu`.
- Calling `Navigate` / `LoadHTML` / `AddBridge` in `FormCreate` on Windows: ignored because WebView2 is not ready. Set `URL`, or wait for `OnInitialized`.
- Comparing `ExecuteJavaScript` results without unquoting: WebView2 returns JSON (`"text"`).
- `TWebBrowser` / `TEdgeBrowser` members (`Navigate2`, `OleObject`, `DefaultInterface`, `OnNavigateComplete2`, `ExecuteScript` on `TEdgeBrowser`): not present; the FNC control wraps WebView2 itself (`NativeBrowser` returns the `ICoreWebView2Controller` pointer on Windows).
- Shipping only the EXE: without `WebView2Loader_x86/x64.dll` the browser stays blank.
