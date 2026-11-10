# Rich editor (TTMSFNCRichEditor, toolbars, ruler, IO components, TTMSFNCHTMLEditor)
> Sections (line ranges): 6-23 Units, palette, platforms · 24-63 TTMSFNCRichEditor — content model · 64-136 Selection and formatting · 137-156 Find / replace, undo, clipboard, misc · 157-179 Merge fields · 180-227 Load / save · 228-252 Toolbars · 253-256 TTMSFNCRichEditorToolBarPopup · 257-265 TTMSFNCRichEditorHorizontalRuler · 266-274 TTMSFNCHTMLEditor · 275-280 Platform notes · 281-295 Does not exist / common mistakes

Verified against TMS FNC UI Pack 7.3.1.2 source: `*.TMSFNCRichEditorBase`, `*.TMSFNCRichEditor`, `*.TMSFNCRichEditorToolBar`, `*.TMSFNCRichEditorToolBarPopup`, `*.TMSFNCRichEditorRuler`, `*.TMSFNCRichEditorIO`, `*.TMSFNCRichEditorPDFIO`, `*.TMSFNCRichEditorPrintIO`, `*.TMSFNCRichEditorEMailIO`, `*.TMSFNCHTMLEditor` (+ FNC Core 4.5.0.0 `TMSFNCPDFIO` / `TMSFNCPrintIO`).

## Units, palette, platforms

All registered on palette page **`TMS FNC UI`**. Prefix: `VCL.` / `FMX.`; Lazarus uses `LCLTMSFNC...` (no dot, e.g. `LCLTMSFNCRichEditor`).

| Class | Unit |
|---|---|
| `TTMSFNCRichEditor` | `VCL.TMSFNCRichEditor` (+ `VCL.TMSFNCRichEditorBase` for `TBulletType`, `TTextElement`, `TCaretPos`, ...) |
| `TTMSFNCRichEditorFormatToolBar`, `TTMSFNCRichEditorEditToolBar` | `VCL.TMSFNCRichEditorToolBar` |
| `TTMSFNCRichEditorToolBarPopup` | `VCL.TMSFNCRichEditorToolBarPopup` |
| `TTMSFNCRichEditorHorizontalRuler` | `VCL.TMSFNCRichEditorRuler` |
| `TTMSFNCRichEditorHTMLIO`, `TTMSFNCRichEditorRTFIO` | `VCL.TMSFNCRichEditorIO` |
| `TTMSFNCRichEditorPDFIO` | `VCL.TMSFNCRichEditorPDFIO` (+ `VCL.TMSFNCPDFIO` for option types) |
| `TTMSFNCRichEditorPrintIO` | `VCL.TMSFNCRichEditorPrintIO` (+ `VCL.TMSFNCPrintIO` for `pnHeader` etc.) |
| `TTMSFNCRichEditorEmailIO` (not registered, VCL/Indy only) | `VCL.TMSFNCRichEditorEMailIO` |
| `TTMSFNCHTMLEditor` (mini-HTML dialog) | `VCL.TMSFNCHTMLEditor` |

**WEB (TMS WEB Core): the rich editor family is NOT available** — there is no `WEBLib.TMSFNCRichEditor.pas` and the WEB package does not contain it (only stray `*Reg` units exist). `TTMSFNCHTMLEditor` *is* in the WEB package. Available: VCL, FMX, LCL.

## TTMSFNCRichEditor — content model

Content is a list of elements (`TTextElement`, `TLineBreakElement`, `TPictureElement`, `TBulletElement`, `TTabElement`, ...). There is **no `Lines` property**. Character positions used by `SelectText`/`SelStart` count each line break as **2 characters** (`#13#10`).

Building content (`TTMSFNCRichEditorBase`, public):
```delphi
function AddText(AValue: string): TTextElement; overload;
function AddText(AValue: string; AColor: TTMSFNCGraphicsColor): TTextElement; overload;
function AddText(AValue: string; AColor: TTMSFNCGraphicsColor; BkColor: TTMSFNCGraphicsColor): TTextElement; overload;
function AddText(AValue: string; AFont: TFont): TTextElement; overload;
function AddText(AValue: string; AFontSize: integer; AFontName: string; AFontStyle: TFontStyles): TTextElement; overload;
function AddText(AValue: string; AAlignment: TAlignment): TTextElement; overload;
function AddText(AValue: string; AFontSize: integer; AFontName: string; AFontStyle: TFontStyles; AAlignment: TAlignment): TTextElement; overload;
procedure AddHyperlink(AValue, AURL: string);
procedure AddMultiLineText(AValue: string);
function AddLineBreak: TREElement;
procedure AddLine(AColor: TTMSFNCGraphicsColor = clBlack; AWidth: integer = 1; APenStyle: TPenStyle = psSolid);
function AddTab: TTabElement;
procedure AddBullet(AType: TBulletType = btCircle);
function AddImage(Picture: TPicture): TPictureElement; overload;
function AddImage(Picture: TPicture; AWidth, AHeight: integer): TPictureElement; overload;
function AddImage(FileName: string): TPictureElement; overload;
function AddImage(FileName: string; AWidth, AHeight: integer): TPictureElement; overload;
// Insert* variants act at the caret:
function InsertText(AValue: string): TTextElement; overload;
function InsertMultiLineText(AValue: string): TTextElement;
function InsertLineBreak: TLineBreakElement; overload;
function InsertImage(FileName: string; AWidth: integer = 0; AHeight: integer = 0): TPictureElement; overload;
function InsertImage(AStream: TStream; AWidth: integer = 0; AHeight: integer = 0): TPictureElement; overload;
function InsertBullet(AType: TBulletType = btCircle): TBulletElement;
procedure Clear; virtual;
procedure BeginUpdate; override;
procedure EndUpdate; override;
property Text: string;                 // read/write plain text
property ContentAsPlainText: string;   // read/write
function PlainText: string;
function IsEmpty: boolean;
```
`TBulletType = (btCircle, btSquare, btArrow, btTick, btStar, btNumber, btChar, btCustom, btNone)`.

## Selection and formatting

```delphi
procedure SelectText(FromChar, ALength: integer);   // 2nd param is a LENGTH
procedure SelectAll; override;
procedure UnSelect;
procedure ClearSelection; override;
procedure ClearCaret;
procedure SetCaret(CaretPos: TCaretPos); overload;  // cpBeginDoc, cpEndDoc
procedure SetCaret(CharPos: integer); overload;
property SelStart: integer;  property SelLength: integer;
function SelectedText: string; override;
function HasSelection: boolean; override;

function SetSelectionBold(DoBold: boolean): boolean;
function SetSelectionItalic(DoItalic: boolean): boolean;
function SetSelectionUnderline(DoUnderline: boolean): boolean;
function SetSelectionStrikeOut(DoStrikeOut: boolean): boolean;
function SetSelectionSubscript(DoSubScript: boolean): boolean;
function SetSelectionSuperscript(DoSuperScript: boolean): boolean;
function SetSelectionColor(AColor: TTMSFNCGraphicsColor): boolean;
procedure SetSelectionBkColor(AColor: TTMSFNCGraphicsColor);
function SetSelectionFontName(AName: string): boolean;
function SetSelectionFontSize(ASize: integer): boolean;
procedure SetSelectionAttribute(AAlignment: TAlignment); overload;   // taLeftJustify/taCenter/taRightJustify
procedure SetSelectionAttribute(AFontName: string; AFontSize: integer; AFontStyle: TFontStyles; AColor: TTMSFNCGraphicsColor); overload;
procedure SetSelectionIndent(AIndent: integer);
procedure SetSelectionRightIndent(AIndent: integer);
procedure SetSelectionBullets(AType: TBulletType); overload;
procedure RemoveSelectionBullets;
procedure SetSelectionHyperlink(AURL: string);
procedure SetSelectionMergeField(AMergeName: string);
procedure SetSelectionHint(AHint: string);
// queries: IsSelectionBold/Italic/Underline/StrikeOut/Subscript/Superscript/Left/Center/Right,
// GetSelectionTextColor, GetSelectionBkColor, GetSelectionFontName, GetSelectionFontSize, GetSelectionIndent, GetSelectionBullet
```

Example (from demo `VCL\RichEditor`, `SampleFormat` / `SampleBullet`):
```delphi
procedure TForm1.FillEditor;
begin
  TMSFNCRichEditor1.BeginUpdate;
  try
    TMSFNCRichEditor1.Clear;
    TMSFNCRichEditor1.AddText('This is sample formatted text with bold, italic, underline, strikethrough');
    TMSFNCRichEditor1.SelectText(35, 4);
    TMSFNCRichEditor1.SetSelectionBold(True);
    TMSFNCRichEditor1.SelectText(41, 6);
    TMSFNCRichEditor1.SetSelectionItalic(True);
    TMSFNCRichEditor1.SelectText(15, 9);
    TMSFNCRichEditor1.SetSelectionColor(gcGreen);
    TMSFNCRichEditor1.AddLineBreak;

    TMSFNCRichEditor1.AddText('Item 1');
    TMSFNCRichEditor1.AddLineBreak;
    TMSFNCRichEditor1.AddText('Item 2');
    TMSFNCRichEditor1.AddLineBreak;
    TMSFNCRichEditor1.SelectText(75, 16);            // "Item 1"#13#10"Item 2"#13#10
    TMSFNCRichEditor1.SetSelectionBullets(btCircle);

    TMSFNCRichEditor1.AddHyperlink('TMS software', 'https://www.tmssoftware.com');
    TMSFNCRichEditor1.AddLineBreak;
    TMSFNCRichEditor1.AddImage('.\car.png');

    TMSFNCRichEditor1.ClearSelection;
    TMSFNCRichEditor1.ClearCaret;
  finally
    TMSFNCRichEditor1.EndUpdate;
  end;
end;
```
Use `gc*` colors (`gcRed`, `gcYellow`) — they are valid in both VCL (`TColor`) and FMX (`TAlphaColor`); `clRed` is wrong on FMX.

## Find / replace, undo, clipboard, misc

```delphi
function Find(AText: string; MatchCase: boolean = false): boolean;
function FindFirst(AText: string; MatchCase: boolean = false): boolean;
function FindNext: boolean;
function Replace(AText, AReplacement: string; MatchCase: boolean = false): boolean;
function ReplaceAll(AText, AReplacement: string; MatchCase: boolean = false): boolean;
function Highlight(AText: string; MatchCase: boolean = false): boolean;  procedure UnHighlight;
procedure Undo;  procedure Redo;  function CanUndo: boolean;  function CanRedo: boolean;
procedure CutToClipboard; procedure CopyToClipboard; function PasteFromClipboard: string;
procedure CopyRTFToClipboard; procedure CopyHTMLToClipboard;
procedure ScrollToCaret; procedure ScrollToBegin; procedure ScrollToEnd;
property Modified: boolean;  property ZoomFactor: double;  property PageMargin: TPageMargin;
procedure SetPageSize(APageSize: TPageSize);   // psA4, psA5, psA6, psLetter, psLegal
```
Published: `ReadOnly`, `WantTab` (default False), `WantReturn`, `AllowSelect`, `URLAuto: TURLAuto` (`uAuto`, `uOff`), `URLOpen: TURLOpen` (`uoCtrl` default, `uoAlt`, `uoClick`, `uoNone`), `URLColor`, `URLUnderline`, `HighlightColor`, `SelectionColor`, `LineSpacing`, `AutoCorrect`, `AutoCompletion`, `GraphicSelection`, `ToolBarPopup`, `Author`, `Comments`, `Tags`, `LastModifiedBy`.

Events: `OnChange`, `OnSelectionChanged`, `OnCaretChanged`, `OnClickHyperlink: THyperlinkClickEvent = procedure(Sender: TObject; URL: string)`, `OnClickGraphic`, `OnPasteText(Sender; var AText: string; var Allow: boolean)`, `OnPasteBitmap`, `OnDropFile`, `OnDropImage`, `OnGetElementHint`, `OnContextForWord`, `OnBeforePopupMenu`, `OnDrawGraphic`, `OnDrawBackground`, `OnAutoComplete`, `OnMergeField`, `OnEnterWord`, `OnCorrectWord`.

## Merge fields

```delphi
procedure SetSelectionMergeField(AMergeName: string);  // mark selected text as field
procedure GetMergeFields(AList: TStringList);
procedure Merge(NamesAndValues: TStringList); overload; virtual;  // Name=Value pairs; Objects[] may hold a TPicture
procedure UnMerge;                                                   // restore the template
property IsMerged: boolean;
OnMergeField: procedure(Sender: TObject; MergeName: string; var MergeValue: string; var DoMerge: boolean) of object;
```
```delphi
var sl: TStringList;
begin
  sl := TStringList.Create;
  try
    sl.Values['NAME'] := 'Bill Gates';
    TMSFNCRichEditor1.Merge(sl);
  finally
    sl.Free;
  end;
end;
```

## Load / save

| Format | How |
|---|---|
| Native `.rte` | `LoadFromFile(const FileName: string)`, `SaveToFile`, `LoadFromStream(const AStream: TStream)`, `SaveToStream`, `property ContentAsRTE: string` |
| Plain text | `LoadFromTextFile(const FileName: string)`, `SaveToText(AFileName: string)`, `Text`, `ContentAsPlainText` |
| RTF | `TTMSFNCRichEditorRTFIO.Load(const FileName: string)` / `Load(AStream)` / `Save(const FileName: string)` / `Save(AStream)`; editor: `function ContentAsRTF: string`, `SelectionAsRTF`, `InsertAsRTF(rtfstring: string)` |
| HTML | `TTMSFNCRichEditorHTMLIO.Save(const FileName: string)` / `Save(FileName, ImgPath)` / `Load(const FileName: string; Encoding: TEncoding = nil)` / `LoadHTML(HtmlValue: string)` / `InsertHTML(HtmlValue: string)`; editor: `ContentAsHTML(ImgPath: string = ''): string`, `ContentAsPlainHTML`, `SelectionAsHTML` |
| PDF | `TTMSFNCRichEditorPDFIO.Save(const AFileName: String)` / `Save(const AStream: TStream)` |
| Print | `TTMSFNCRichEditorPrintIO.Print` |

`LoadFromFile` is the native RTE format, **not** RTF/HTML/TXT (the edit toolbar picks the loader by extension). HTMLIO published: `RichEditor`, `Head: TStrings`, `BodyClass`, `HyperlinkTarget`, `InlineImages` (base64 images), `PlainHTML`, `SpaceAsNbSp` (default True), `OnImageNotFound`.

```delphi
// RTF round trip
TMSFNCRichEditorRTFIO1.RichEditor := TMSFNCRichEditor1;
TMSFNCRichEditor1.Clear;
TMSFNCRichEditorRTFIO1.Load('letter.rtf');
TMSFNCRichEditorRTFIO1.Save('letter_copy.rtf');

// HTML with images embedded
TMSFNCRichEditorHTMLIO1.RichEditor := TMSFNCRichEditor1;
TMSFNCRichEditorHTMLIO1.InlineImages := True;
TMSFNCRichEditorHTMLIO1.Save('page.html');
```

PDF and print (demo `VCL\RichEditor`):
```delphi
TMSFNCRichEditorPDFIO1.RichEditor := TMSFNCRichEditor1;
TMSFNCRichEditorPDFIO1.Options.OpenInPDFReader := True;
TMSFNCRichEditorPDFIO1.Options.Header := 'TMS FNC RichEditor PDF Export';
TMSFNCRichEditorPDFIO1.Save('richeditorexport.pdf');

procedure TForm1.TMSFNCRichEditorPDFIO1GetFooter(Sender, AExportObject: TObject;
  APageIndex: Integer; var AFooter: UnicodeString);
begin
  AFooter := 'Page ' + IntToStr(APageIndex);
end;

TMSFNCRichEditorPrintIO1.RichEditor := TMSFNCRichEditor1;
TMSFNCRichEditorPrintIO1.Options.Header := 'TMS FNC RichEditor Print Export';
TMSFNCRichEditorPrintIO1.Options.PageNumber := pnHeader;   // pnNone, pnHeader, pnFooter
TMSFNCRichEditorPrintIO1.Print;
```
PDFIO/PrintIO auto-assign the first rich editor on the owner form when dropped/created with a form owner. `Options.ExportImages` (default True) exists on both.

`TTMSFNCRichEditorEmailIO` (VCL, Indy): `RichEditor` is **public** (not published) and it is not on the palette; `procedure GenerateEmail(idMessage: TIdMessage; ImgPath: string = '')` fills a `TIdMessage` with HTML body + embedded images.

## Toolbars (TTMSFNCRichEditorFormatToolBar / TTMSFNCRichEditorEditToolBar)

Both descend from `TTMSFNCRichEditorToolBar` (a `TTMSFNCToolBar`, not registered) and are linked with the published `property RichEditor: TTMSFNCRichEditor`. The toolbar registers itself with the editor and refreshes its button states on selection changes.

- Format toolbar: `Options: TTMSFNCRichEditorFormatToolBarOptions` = set of `ftoFontName, ftoFontSize, ftoBold, ftoItalic, ftoUnderline, ftoStrikeout, ftoAlignLeft, ftoAlignCenter, ftoAlignRight, ftoTextColor, ftoBackgroundColor, ftoImage, ftoHyperlink, ftoBullets, ftoNumbering, ftoUnindent, ftoIndent` (default all). Accessors: `FontNamePicker`, `FontSizePicker`, `TextColorPicker`, `BackgroundColorPicker`, `BulletsPicker`, `BoldButton`, `ItalicButton`, `UnderlineButton`, `StrikeoutButton`, `AlignLeftButton`, `AlignCenterButton`, `AlignRightButton`, `IndentButton`, `UnindentButton`, `NumberingButton`, `ImageButton`, `HyperlinkButton`. Events: `OnApplyBold`, `OnApplyItalic`, `OnApplyFontName(Sender; AFontName: String)`, `OnApplyFontSize(Sender; AFontSize: Integer)`, `OnApplyTextColor/OnApplyBackgroundColor(Sender; AColor: TTMSFNCGraphicsColor)`, `OnApplyBullets(Sender; AIndex: Integer)`, `OnInsertHyperlink`, `OnInsertBitmap`, ...
- Edit toolbar: `Options` = set of `etoOpenFile, etoSaveFile, etoCut, etoCopy, etoPaste, etoUndo, etoRedo`. Accessors `OpenFileButton`, `SaveFileButton`, `CutButton`, `CopyButton`, `PasteButton`, `UndoButton`, `RedoButton`. Events `OnOpenFile`, `OnSaveFile`, `OnCut`, `OnCopy`, `OnPaste`, `OnUndo`, `OnRedo` (TNotifyEvent). **Assigning `OnOpenFile`/`OnSaveFile` replaces the built-in dialog** (handler is called, then Exit). Built-in open: `.txt` → `LoadFromTextFile`, `.rtf` → RTFIO, anything else → `LoadFromFile` (RTE).

```delphi
procedure TForm1.FormCreate(Sender: TObject);
var
  re: TTMSFNCRichEditor;
  tb: TTMSFNCRichEditorFormatToolBar;
begin
  re := TTMSFNCRichEditor.Create(Self);
  re.Parent := Self;
  re.Align := alClient;

  tb := TTMSFNCRichEditorFormatToolBar.Create(Self);
  tb.Parent := Self;
  tb.Align := alTop;
  tb.Options := tb.Options - [ftoImage, ftoHyperlink];
  tb.RichEditor := re;
end;
```

## TTMSFNCRichEditorToolBarPopup

Floating mini format toolbar shown when the mouse hovers over a selection. Link both ways at design time or in code: `TMSFNCRichEditor1.ToolBarPopup := TMSFNCRichEditorToolBarPopup1;` (published `ToolBarPopup: TTMSFNCRichEditorCustomToolBarPopup` on the editor; the editor sets the popup's `RichEditor` itself when showing it). Published: `RichEditor`. Public: `Options: TTMSFNCRichEditorFormatToolBarOptions` (default font name/size, B/I/U/S, text+background color only), `Placement`, `PlacementControl`, `DragGrip`.

## TTMSFNCRichEditorHorizontalRuler

The registered ruler class (no `TTMSFNCRichEditorRuler`). Published `RichEditor: TTMSFNCRichEditor`, `LeftIndent`, `RightIndent`, `HangingIndent` (Integer), `Tabs: TTMSFNCRichEditorRulerTabCollection` (`AddTab(AIndent: Integer = 0): integer`), `Layout` (`LeftMargin` 50, `RightMargin` 46, `RulerPosition: rpTop/rpBottom`, `ShowLeftIndent`, `ShowRightIndent`, `ShowHangingIndent`, `TabMove: tmTickMark/tmStep/tmLabel/tmAll/tmPixel`, `AutoWidth`, `AutoPosition`, `TickMarks`), `Appearance` (`RulerFill`, `RulerStroke`, `MarginFill`, `IndentFill`, `TickMarkColor`, `TabColor`, `Font`, ...). Events `OnLeftIndentChanged`, `OnRightIndentChanged`, `OnLeftMarginChanged`, ... `(Sender: TObject; Indent: Integer)`; `OnTabAdded/OnTabChanged/OnTabRemove (Sender: TObject; Index: Integer; Indent: Integer)`.
```delphi
TMSFNCRichEditorHorizontalRuler1.Parent := Panel3;
TMSFNCRichEditorHorizontalRuler1.Align := alTop;
TMSFNCRichEditorHorizontalRuler1.RichEditor := TMSFNCRichEditor1;
```

## TTMSFNCHTMLEditor (mini-HTML text dialog)

Non-visual `TTMSFNCCustomComponent` that opens a dialog (toolbar + memo + preview) to edit **FNC mini-HTML** (the `TTMSFNCHTMLText` syntax), not a rich document. Published `Text: String`, `BitmapContainer`. VCL/FMX/LCL: `function Execute: TModalResult;` WEB: `procedure Execute(AProc: TModalResultProc = nil);`.
```delphi
TMSFNCHTMLEditor1.Text := TMSFNCHTMLText1.Text;
if TMSFNCHTMLEditor1.Execute = mrOk then
  TMSFNCHTMLText1.Text := TMSFNCHTMLEditor1.Text;
```

## Platform notes

- VCL/FMX/LCL only for the rich editor family; WEB has none of it (use `TTMSFNCHTMLEditor`/`TTMSFNCHTMLText` or a web control).
- FMX: `TTMSFNCGraphicsColor = TAlphaColor`; `TPicture` is `TTMSFNCBitmap`; `AddBitmap(TBitmap)` exists only on non-FMX.
- `TTMSFNCRichEditor.Print` is an empty method in the FNC build (body is `{$IFNDEF FNCLIB}`) — use `TTMSFNCRichEditorPrintIO`.

## Does not exist / common mistakes

- `RichEditor.Lines`, `Lines.Add`, `Paragraph`, `SelAttributes` (TRichEdit API) — use `AddText`/`AddLineBreak`, `SelectText` + `SetSelection*`.
- `LoadFromRTF`, `SaveToRTF`, `LoadFromHTML`, `SaveToHTML`, `SaveToPDF` on the editor — use `TTMSFNCRichEditorRTFIO`, `TTMSFNCRichEditorHTMLIO`, `TTMSFNCRichEditorPDFIO` (`Save`/`Load`). `ContentAsHTML`/`ContentAsRTF` are read-only functions.
- `LoadFromFile('x.rtf')` / `LoadFromFile('x.txt')` — `LoadFromFile` reads native RTE only; use RTFIO / `LoadFromTextFile`.
- `SelectText(FromChar, ToChar)` — the second parameter is a length; line breaks count as 2 chars.
- `RichEditor1.Print` — no-op in FNC; use `TTMSFNCRichEditorPrintIO.Print`.
- `TTMSFNCRichEditorRuler`, `TTMSFNCRichEditorToolBar` on the palette, `TAdvRichEditorFormatToolBar`, `TAdvRichEditorEditButtonBar`, `TAdvRichEditorPopupToolBar` — use `TTMSFNCRichEditorHorizontalRuler`, `TTMSFNCRichEditorFormatToolBar`, `TTMSFNCRichEditorEditToolBar`, `TTMSFNCRichEditorToolBarPopup`.
- Setting only `ToolBar.RichEditor` for the popup — the popup is assigned via `RichEditor.ToolBarPopup`.
- `PopupToolBar` property — that is the non-FNC (TMS VCL) name; FNC uses `ToolBarPopup`.
- `InsertHyperlink(...)` on the editor — use `AddHyperlink(AValue, AURL)` or `SetSelectionHyperlink(AURL)`; click event is `OnClickHyperlink` (not `OnHyperlinkClick`/`OnLinkClick`).
- `TTMSFNCRichEditorEmailIO` on the palette / FMX — VCL-only, unregistered, requires Indy.
- `TTMSFNCRichEditor` in TMS WEB Core — not available.
- `TTMSFNCHTMLEditor` as a WYSIWYG HTML document editor — it edits FNC mini-HTML strings in a modal dialog.
