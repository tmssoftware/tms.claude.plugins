# Code editor memo (TTMSFNCMemo, TTMSFNCMemoCustomLanguage, TTMSFNCMemoCustomTheme)

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCMemo`, `*.TMSFNCMemoCustomLanguage`, `*.TMSFNCMemoCustomTheme`, `*.TMSFNCMemoReg` (base class from FNC Core 4.5.0.0 `*.TMSFNCCustomWEBControl` / `*.TMSFNCWebBrowser`).

`TTMSFNCMemo` is **not** a native memo: it hosts the Monaco editor (VS Code's editor) inside the FNC web browser control (`TTMSFNCCustomMemo = class(TTMSFNCCustomWEBControl)`). Everything is asynchronous JavaScript underneath.

## Units, palette, platforms

```delphi
uses
  VCL.TMSFNCTypes, VCL.TMSFNCUtils, VCL.TMSFNCGraphics, VCL.TMSFNCGraphicsTypes,
  VCL.TMSFNCCustomControl, VCL.TMSFNCWebBrowser, VCL.TMSFNCCustomWEBControl,
  VCL.TMSFNCMemo,                     // TTMSFNCMemo, enums, TTMSFNCMemoSource...
  VCL.TMSFNCMemoCustomLanguage,       // TTMSFNCMemoCustomLanguage
  VCL.TMSFNCMemoCustomTheme;          // TTMSFNCMemoCustomTheme
```
Prefix `VCL.` / `FMX.` / `WEBLib.`; Lazarus `LCLTMSFNCMemo`, `LCLTMSFNCMemoCustomLanguage`, ... Palette page **`TMS FNC UI`**: `TTMSFNCMemo`, `TTMSFNCMemoCustomLanguage`, `TTMSFNCMemoCustomTheme`. Platforms: VCL, FMX, WEB, LCL (`ComponentPlatformsAttribute(TMSPlatformsWeb)`).

Runtime requirements:
- Windows (VCL/FMX): Microsoft Edge **WebView2 runtime** plus `WebView2Loader_x86.dll` / `WebView2Loader_x64.dll` next to the exe (FNC Core web browser requirement).
- `LibraryLocation: TTMSFNCMemoLibraryLocation` (`llOnline`, `llOffline`, default `llOffline`). Offline: Monaco is extracted from resources to `%TEMP%\ttmsfncmemo\` and loaded from `file://`. Online: loaded from `https://download.tmssoftware.com/fncwxpack/monaco/main.js`. WEB always uses the online URL.
- The editor is not ready until `OnInitialized` fires (`IsInitialized` exists but is **protected**; track readiness yourself in `OnInitialized`). Setting `Lines`/`Text`/`Language` before that is buffered and applied on load; calls that run JavaScript (Find, SelStart, ScrollToLine, ...) need the editor initialized.

## Key published properties (TTMSFNCMemo)

```delphi
property Lines: TTMSFNCMemoLines;                   // TStringList descendant, synced with the editor
property Text: string;                              // public; = Lines.Text
property Language: TTMSFNCMemoLanguage default mlPascal;
property Theme: TTMSFNCMemoTheme default mtVisualStudio;
property &Readonly: Boolean default false;
property Font: TTMSFNCMemoFont;                     // TTMSFNCGraphicsFont descendant
property Options: TTMSFNCMemoOptions;
property WantTab: Boolean default false;
property CompletionList: TTMSFNCMemoCodeCompletion;
property LibraryLocation: TTMSFNCMemoLibraryLocation default llOffline;
property CustomLanguages: TTMSFNCMemoLanguageReferences;  property CustomLanguageID: string;
property CustomThemes: TTMSFNCMemoThemeReferences;        property CustomThemeName: string;
property LanguageFileExtensionsMap: TTMSFNCMemoLanguageFileExtensionMap;
property Sources: TTMSFNCMemoSources;  property ActiveSource: Integer;
```
`TTMSFNCMemoTheme = (mtVisualStudio, mtVisualStudioDark, mtHighContrastDark, mtCustom)`.
`TTMSFNCMemoLanguage` = `mlAbap ... mlCpp, mlCsharp, mlCSS, ..., mlHtml, mlIni, mlJava, mlJavascript, mlJSON, ..., mlMarkdown, mlMySQL, mlPascal, mlPhp, mlPlainText, mlPowershell, mlPython, mlRuby, mlRust, mlSQL, mlSwift, mlTypeScript, mlVb, mlXml, mlYaml, mlCustom` (note casing: `mlJSON`, `mlSQL`, `mlCSS`, `mlHtml`, `mlXml`, `mlCsharp`).

`Options` (TTMSFNCMemoOptions, published): `LineNumbers` (True), `Folding` (True), `MiniMap: TTMSFNCMemoMinimapOptions` (`Enabled`, `Side: soRight/soLeft`, `Size`, `Scale`, `ShowSlider`, `Autohide`, `MaxColumn`, `RenderCharacters`), `WordWrap: TTMSFNCMemoWordWrapType` (`wwtOn, wwtOff, wwtWordWrapColumn, wwtBounded`), `WordWrapColumn`, `TabSize` (2), `ContextMenu`, `DragAndDrop`, `GlyphMargin`, `AutoGlyphMargin`, `Links`, `AutoOpenLink` (True), `RenderLineHighlight: TTMSFNCMemoLineHighLight` (`hlNone, hlAll, hlLine, hlGutter`), `RenderWhiteSpace: TTMSFNCMemoWhitepace` (`mwNone, mwAll, mwBoundary, mwSelection, mwTrailing`), `RenderIndentGuides`, `Scrollbar: TTMSFNCMemoScrollOptions` (`Horizontal/Vertical: soAuto/soVisible/soHidden`), `QuickSuggestion` (`Strings/Comments/Other: smOn/smOff/smInline`), `BlockSelection`, `MouseWheelZoom`, `FormatOnPaste`, `FormatOnType`, `CommandPalette`, `UseCustomCodeCompletion` (True), `BracketPairColorization`, `SelectionHighlight`, `RoundedSelection`, `CodeLens`.

## Public methods

```delphi
procedure Clear;
procedure BeginUpdate; override;  procedure EndUpdate; override;
procedure LoadFromFile(AFileName: string);          // not WEB; also picks Language via LanguageFileExtensionsMap
procedure LoadFromURL(AURL: string);
procedure CopyToClipBoard; procedure PasteFromClipBoard; procedure CutToClipBoard;
procedure SelectAll; procedure Unselect; procedure Undo; procedure Redo;
procedure FoldAll; procedure UnfoldAll;
procedure FormatDocument; procedure FormatSelection;
procedure DeleteSelection;
procedure Find(ASearchString: string; ABehaviour: TTMSFNCMemoFindBehaviour = fbDown); overload;   // fbDown, fbUp, fbAll
procedure Find(ASearchString: string; AOptions: TTMSFNCMemoFindOptions; ABehaviour: TTMSFNCMemoFindBehaviour = fbDown); overload;
procedure FindAll(ASearchString: string); overload;
procedure FindNext(ASearchString: string); reintroduce; overload;
procedure FindPrevious(ASearchString: string); reintroduce; overload;
procedure Replace(AStartPos, ALength: Integer; AReplaceString: string); overload;
procedure Replace(ASearchString, AReplaceString: string; ABehaviour: TTMSFNCMemoFindBehaviour = fbDown); overload;
procedure ReplaceNext(ASearchString, AReplaceString: string); overload;
procedure ReplaceAll(ASearchString, AReplaceString: string); overload;
procedure ShowFindDialog;
procedure ScrollToLine(ALineNumber: Integer);  procedure ScrollToLineCenter(ALineNumber: Integer);
procedure GoToBookmark(AIndex: Integer); procedure GoToBreakPoint(AIndex: Integer); procedure GoToLineHighlight(AIndex: Integer);
function GetWordAtPosition: string; overload;
function TextPosToPos(const APos: Integer): TTMSFNCMemoCaretPosition;
function PosToTextPos(const APosition: TTMSFNCMemoCaretPosition): Integer;
property CaretPosition: TTMSFNCMemoCaretPosition;    // record Line, Pos: Integer
property SelStart: Integer; property SelLength: Integer; property SelText: String;  // SelText write = Replace(SelStart, SelLength, Value)
property BreakPoints[Line: Integer]: Boolean;  property BreakPointCount: Integer;
property Bookmarks[Line: Integer]: Boolean;    property BookmarksCount: Integer;
property LineHighlight[Line: Integer]: Boolean; property LineHighlightCount: Integer;
function DefaultMemoFindOptions: TTMSFNCMemoFindOptions;   // unit-level function
```
`TTMSFNCMemoFindOptions` record: `SearchOnlyEditableRange, SetSelect, IsRegex, MatchCase: Boolean; WordSeparators: String; CaptureMatches: Boolean; LimitResultCount: Integer`. Start from `DefaultMemoFindOptions` and change fields.

## Events

```delphi
OnChange, OnChangeTracking, OnInitialized: TNotifyEvent;
OnGutterClick / OnGutterRightClick / OnGutterMiddleClick,
OnLineNumberClick / ..., OnGlyphMarginClick / ...:  procedure(Sender: TObject; LineNumber: Integer) of object;
OnGetCodeCompletion: procedure(Sender: TObject; Token: String; CustomCompletionList: TTMSFNCMemoCodeCompletion; Position: TTMSFNCMemoCaretPosition) of object;
OnLinkClick: procedure(Sender: TObject; AURL: string) of object;
OnPaste: procedure(Sender: TObject; var APasteValue: string; var AAllow: Boolean) of object;
OnFindNext / OnFindPrevious: procedure(Sender: TObject; Match: TTMSFNCMemoMatch) of object;   // Match, Position, Range
OnFindAll: procedure(Sender: TObject; Matches: TTMSFNCMemoMatches) of object;
OnReplaceNext / OnReplacePrevious, OnReplaceAll
```

## Example: basic setup, completion, breakpoints (demo `VCL\Memo\Default`)

```delphi
procedure TForm1.FormCreate(Sender: TObject);
begin
  Memo := TTMSFNCMemo.Create(Self);
  Memo.Parent := Self;
  Memo.Align := alClient;
  Memo.Language := mlPascal;
  Memo.Theme := mtVisualStudioDark;
  Memo.Options.MiniMap.Enabled := False;
  Memo.Options.WordWrap := wwtOff;
  Memo.Lines.Text := 'begin' + sLineBreak + '  ShowMessage(''Hello'');' + sLineBreak + 'end.';
  Memo.OnGetCodeCompletion := MemoGetCodeCompletion;
  Memo.OnGutterClick := MemoGutterClick;
end;

procedure TForm1.MemoGetCodeCompletion(Sender: TObject; Token: string;
  CustomCompletionList: TTMSFNCMemoCodeCompletion; Position: TTMSFNCMemoCaretPosition);
begin
  CustomCompletionList.Add('IntToStr(');
  CustomCompletionList.Add('ShowMessage', skFunction, 'ShowMessage(''$1'')', itrInsertAsSnippet, 'Shows a message');
end;

procedure TForm1.MemoGutterClick(Sender: TObject; LineNumber: Integer);
begin
  Memo.BreakPoints[LineNumber] := not Memo.BreakPoints[LineNumber];
end;

// file I/O goes through Lines (or LoadFromFile to also auto-detect the language)
Memo.LoadFromFile(OpenDialog1.FileName);
Memo.Lines.SaveToFile(SaveDialog1.FileName);
```
`TTMSFNCMemoCodeCompletion.Add(AName: string; AKind: TTMSFNCMemoSuggestionKind = skText; AInsertText: string = ''; AInsertTextRules: TTMSFNCMemoSuggestionInsertTextRule = itrNone; ADocumentation: string = '')`. Static list: fill the published `CompletionList` instead of handling the event.

## Multiple sources (tabs) — demo `VCL\Memo\Sources`

`TTMSFNCMemoSource` (collection item): published `Name`, `ReadOnly`, `Language`, `Lines: TStringList`; public `BreakPoints`, `Bookmarks`, `LineHighlights`, `CaretPosition`, `SaveToFile`, `SaveToStream`. The memo shows `Sources[ActiveSource]`. There is no built-in tab bar — pair with `TTMSFNCTabSet`.
```delphi
procedure TForm1.TMSFNCTabSet1ChangeTab(Sender: TObject; APreviousTabIndex, ACurrentTabIndex: Integer);
begin
  TMSFNCMemo1.ActiveSource := ACurrentTabIndex;
end;

var s: TTMSFNCMemoSource;
s := TMSFNCMemo1.AddSourceFromFile(OpenDialog1.FileName);   // not WEB; AddSourceFromStream for WEB
TMSFNCTabSet1.AddTab(s.Name);
s := TMSFNCMemo1.Sources.AddSource('select * from t', mlSQL, 'query.sql');
TMSFNCMemo1.Sources.Delete(ATabIndex);
```
Memo-level helpers: `AddSourceFromFile(AFileName: string; AName: string = '')`, `AddSourcesFromFolder(AFolder: string)`, `AddSourceFromStream`, `FindSource(AName: string)`, `RemoveSource(AName: string)`.

## Custom language and theme (demo `VCL\Memo\Language and Theme`)

`TTMSFNCMemoCustomLanguage` (Monaco Monarch tokenizer): `LanguageID`, `Tokenizer` (items with `Name` + `Rules`), `ExtraKeys` (`Add(AName; AValueList: array of string)` / `Add(AName, AValueRegex: string)`), `Brackets`, `IgnoreCase`, `DefaultToken`. Rule: `Regex`, `Action` (`Token`, `Next`, `Bracket: lbkNone/lbkOpen/lbkClose`, `Cases.Add(AGuard, AActionToken)`, `Group`), `Include`. `Rules.Add(ARegex, AActionToken)` / `Add(ARegex, AActionToken, AActionNext)`.

`TTMSFNCMemoCustomTheme`: `ThemeName`, `Base` (Monaco base theme), `Inherit` (default True), `Colors: TTMSFNCMemoThemeColors` (`EditorBackground`, `EditorForeground`, `EditorSelectionBackground`, `EditorLineNumberForeground`, `EditorLineHighlightBackground`, `EditorCursorForeground`, ... all `TTMSFNCGraphicsColor`, default `gcNull`), `Rules.Add(AToken: string; AForeground: TTMSFNCGraphicsColor)` (+ overloads with `AFontStyle: TFontStyles`).

```delphi
procedure TForm1.ApplyCustom;
var
  root: TTMSFNCMemoCustomLanguageTokenizerItem;
begin
  TMSFNCMemoCustomLanguage1.LanguageID := 'mylang';
  TMSFNCMemoCustomLanguage1.ExtraKeys.Add('keywords', ['if', 'else', 'while', 'return']);
  root := TMSFNCMemoCustomLanguage1.Tokenizer.Add;
  root.Name := 'root';
  root.Rules.Add('\/\/.*$', 'comment');
  root.Rules.Add('\d+', 'number');

  TMSFNCMemo1.CustomLanguages.Add.Language := TMSFNCMemoCustomLanguage1;
  TMSFNCMemo1.Language := mlCustom;                 // uses CustomLanguageID, or the first custom language

  TMSFNCMemoCustomTheme1.ThemeName := 'mytheme';
  TMSFNCMemoCustomTheme1.Inherit := False;
  TMSFNCMemoCustomTheme1.Colors.EditorBackground := $1C212A;
  TMSFNCMemoCustomTheme1.Rules.Add('comment', $E09A22);
  TMSFNCMemo1.CustomThemes.Add.Theme := TMSFNCMemoCustomTheme1;
  TMSFNCMemo1.Theme := mtCustom;                    // uses CustomThemeName, or the first custom theme
end;
```
Register the custom language/theme in `CustomLanguages` / `CustomThemes` **before** switching to `mlCustom` / `mtCustom`; with `mlCustom` and no custom language and empty `CustomLanguageID`, `SetLanguage` silently exits.

## Platform notes

- WEB: no `LoadFromFile`, `AddSourceFromFile`, `AddSourcesFromFolder`, `CompletionList.LoadFromFile` (all `{$IFNDEF WEBLIB}`); use `LoadFromURL`, `AddSourceFromStream`, `Lines.Text`.
- FMX on macOS/iOS/Android uses the platform web view (no WebView2).

## Does not exist / common mistakes

- `Memo.SyntaxHighlighter`, `Highlighter`, `TTMSFNCMemoPascalStyler`, `TAdvMemo`-style stylers — use `Language := mlPascal` (or `mlCustom` + `TTMSFNCMemoCustomLanguage`).
- `ShowLineNumbers`, `Gutter.ShowLineNumbers`, `WordWrap := True`, `TabWidth`, `ReadOnly` — use `Options.LineNumbers`, `Options.WordWrap := wwtOn`, `Options.TabSize`, `&Readonly` (spelled `Readonly`).
- `Memo.SaveToFile` — not on the memo; use `Memo.Lines.SaveToFile` (or `Sources[i].SaveToFile`).
- `Modified` property, `OnCursorPositionChanged`, `OnSelectionChange`, `OnCaretMove` — do not exist on TTMSFNCMemo (the event types `TTMSFNCMemoCursorPositionEvent`/`TTMSFNCMemoSelectionEvent` are declared but not used as properties); use `OnChange` / `OnChangeTracking` and read `CaretPosition`.
- `CaretX/CaretY`, `GotoLine` — use `CaretPosition` (record `Line`, `Pos`) and `ScrollToLine`/`ScrollToLineCenter`.
- `Memo.Highlight(...)`/`HighlightLine` — use `LineHighlight[Line] := True`.
- Custom completion (`OnGetCodeCompletion` / `CompletionList`) is switched by `Options.UseCustomCodeCompletion` (default True) — don't turn it off when you expect your items.
- Calling `Find`/`SelStart`/`ScrollToLine` in `FormCreate` — the Monaco instance isn't loaded yet; do it in `OnInitialized`.
- Deploying without `WebView2Loader_x64.dll`/`_x86.dll` or the WebView2 runtime on Windows — the memo stays blank.
- `TTMSFNCMemo` as a lightweight plain-text memo — it's a browser control; use a standard `TMemo` for simple text.
