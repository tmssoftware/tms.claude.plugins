---
name: tms-fnc-core
description: >
  Accurate API knowledge for TMS FNC Core (product tms.fnc.core) in Delphi for VCL, FMX, TMS WEB Core and Lazarus, the
  foundation every TMS FNC product builds on. This skill should be used whenever code references TTMSFNCGraphics,
  TTMSFNCCustomControl, TTMSFNCGraphicsFill/Stroke/Font, gcXXX colors, TTMSFNCBitmap, TTMSFNCBitmapContainer,
  TTMSFNCURLBitmapContainer, TTMSFNCSVGImageCollection, TTMSFNCStylesManager, TTMSFNCPDFLib, TTMSFNCGraphicsPDFIO,
  TTMSFNCGraphicsPrintIO, TTMSFNCPrinter, TTMSFNCWebBrowser, TTMSFNCEdgeWebBrowser, TTMSFNCPopup, TTMSFNCPopupMenu,
  TTMSFNCHint, TTMSFNCResponsiveManager, TTMSFNCUndoManager, TTMSFNCUtils, TTMSFNCJSONReader/Writer, TTMSFNCPersistence,
  SaveSettingsToFile, TTMSFNCObjectResolver, TTMSFNCCloudBase, TTMSFNCHTTPServer, TTMSFNCDataBinder, TTMSFNCDataSet or
  TTMSFNCFilterRulesManager, or when the user asks how to draw custom graphics, generate a PDF, print, embed a web
  browser, parse JSON, persist settings or call a REST API with TMS FNC. Read it before writing or reviewing any TMS FNC
  Core code, because the real API differs from VCL TCanvas, FMX TCanvas and other component sets.
metadata:
  version: "0.2.0"
---

# TMS FNC Core API knowledge

TMS FNC Core (product id `tms.fnc.core`, version 4.5) is the framework-neutral base of all TMS FNC products: the graphics layer, base control classes, bitmaps and SVG, PDF and printing, web browser, popups, styles, JSON, persistence and REST helpers. The same API works in VCL, FMX, TMS WEB Core and Lazarus; only the unit prefix and a few classes differ. It's free and is installed automatically with TMS FNC UI Pack.

## Ground rules

- **Never guess member names.** Use only members in the reference files below. If something isn't covered, don't fall back on reading component source code: many users have trial or DCU-only installs without it, so the plugin must work from these references alone. Instead, in this order: (1) check the official API reference at https://doc.tmssoftware.com/fnc/core/ if web access is available, treating it as secondary (when it conflicts with these references, these win); (2) write the smallest use of the member and let the compiler confirm it ("Undeclared identifier" means it doesn't exist); (3) otherwise tell the user the member is unverified and suggest checking it with Code Insight in the IDE. Never invent a name.
- **Don't carry over names** from VCL/FMX `TCanvas`, `TWebBrowser`, `TPopupMenu`, `TJSONObject` helpers or older TMS components. Each reference file ends with a "Does not exist / common mistakes" list; check it.
- **Match the framework.** Use `VCL.`, `FMX.` or `WEBLib.` units consistently (Lazarus: `LCLTMSFNC...`, no dot). The framework-neutral `TMS.*` units are RTL-only copies, not the units for apps.
- Some classes don't exist on every framework. Check the reference before using one in a WEB or LCL project.

## The pitfalls that matter most

1. Custom FNC controls override `Draw(AGraphics: TTMSFNCGraphics; ARect: TRectF)`, not `Paint`. `Fill`/`Stroke` are protected on `TTMSFNCCustomControl`. `TTMSFNCGraphics` has no `FillRect`, `TextOut`, `TextWidth`, `DrawImage` or `DrawCircle`; see `graphics.md`. Enum prefixes are `gfk*`, `gsk*`, `gta*`. `DrawText` renders mini-HTML by default.
2. An off-screen bitmap canvas needs `BeginScene`/`EndScene`. Copy `g.Bitmap` before freeing `g`. `RestoreState` frees the saved state.
3. `gcNull` is -1 on VCL/WEB and 0 (`TAlphaColors.Null`) on FMX. On FMX use `gc*` colours, not `cl*`.
4. Images are referenced by name through a `BitmapContainer` + `BitmapName`. Lookup is `FindBitmap(name)` (case-insensitive). `TTMSFNCBitmapContainer.AddFromURL` does nothing on VCL/FMX/LCL, so use `TTMSFNCURLBitmapContainer`. On VCL `TTMSFNCBitmap` is a `TPicture` (no Canvas). WEB has no SVG engine and loads images asynchronously. `TTMSFNCSVGImageCollection` is VCL-only.
5. Styles: the component is `TTMSFNCStylesManager`. `Style` is a file name; built-in styles go through `StyleResource := 'FNC_DARK'` and need `TMSFNCStylesResources.res` linked. There is no `Apply` or `LoadFromFile`, and no `.tss` files. Some TMS docs pages say otherwise; trust `styles.md`.
6. PDF: export a control with `TTMSFNCGraphicsPDFIO` (unit `*.TMSFNCGraphicsPDFEngine`) and print with `TTMSFNCGraphicsPrintIO`. `TTMSFNCPDFIO` / `TTMSFNCPrintIO` don't exist. In `TTMSFNCPDFLib`, set Header/Footer before `NewPage`, use `Font.SizeNoScale` (`Font.Size` is rescaled), and free the stream `EndDocument` returns when no file name was given.
7. Printing with `TMSFNCPrinter`: `BeginDoc` calls `OnDrawContent`, and you must call `EndDoc` inside that handler.
8. Web browser: on Windows it needs the WebView2 runtime and `WebView2Loader_x86/x64.dll`. `Navigate`/`LoadHTML`/`AddBridge` are silently ignored until it is initialized, so set `URL` or work in `OnInitialized`. Print, PrintToPDF, cookies, settings and downloads exist only on `TTMSFNCEdgeWebBrowser`. On Windows `ExecuteJavaScript` results come back JSON-encoded. On WEB `Navigate` does nothing.
9. `TTMSFNCPopup` has no Show/Close: use `Popup`/`PopupModal` and close with `IsOpen := False`. Popup menu items use `Text`. `TTMSFNCPopupMenu` and `TTMSFNCHint` don't exist for WEB.
10. JSON: free the object `ParseJSON` returns; don't free values from `GetJSONValue`/`GetJSONArrayItem`. `TTMSFNCJSONWriter` writes to the target stream only when it is freed. Base64 is `Encode64`/`Decode64`.
11. Persistence saves only published properties, with a `"$type"` key first. Load plain external JSON with `obj.FromJSON`. Custom item classes need `RegisterClass`. On controls, `SaveSettingsToFile`/`LoadSettingsFromFile` skip layout/identity properties.
12. `TTMSFNCCloudBase` is created in code (not on the palette). It has no URL property: set `Request.Host`/`Path`/`Query`. It doesn't raise on 4xx/5xx (check `Success`/`ResponseCode`) and frees the result after the callback. `OnRequestComplete` fires on the worker thread; the `ExecuteRequest` callback runs on the main thread.
13. Data binding: the component is `TTMSFNCDataBinder` (`Active` defaults to False). Use the `TMS.TMSFNCFilterRulesManager` unit, not the old `VCL.TMSFNCFilterRulesManager` beta.
14. There is no `TTMSFNCStateManager` component and no `LoadState(Integer)`; use `TTMSFNCResponsiveManager` and `LoadStateByIndex`. The undo manager stores snapshots: call `ClearUndoStack` for a baseline, then `PushState` after each change.

## Reference files

Read the file(s) for the task at hand. Don't load all of them.

| File | Covers |
|---|---|
| `references/setup-and-install.md` | Product, packages, Smart Setup, palette pages, unit prefixes per framework, which units exist where, base classes, common types and colours |
| `references/graphics.md` | `TTMSFNCGraphics` drawing, text and measuring, fill/stroke/font, gradients, paths, clipping, bitmap canvas, custom control `Draw` |
| `references/bitmaps-and-svg.md` | `TTMSFNCBitmap`, SVG, bitmap container, URL bitmap container, SVG image collection, images by name |
| `references/styles.md` | `TTMSFNCStylesManager`, built-in and custom styles, `AdaptToStyle` |
| `references/pdf-and-print.md` | `TTMSFNCPDFLib`, PDF/print export of controls, `TTMSFNCPrinter` |
| `references/webbrowser.md` | Web browser, Edge browser, JavaScript and bridges, WebView2 deployment |
| `references/popups-and-hints.md` | `TTMSFNCPopup`, `TTMSFNCPopupMenu`, `TTMSFNCHint` |
| `references/responsive-state-undo.md` | Responsive manager, state manager, undo manager, scroll bar, toggle button |
| `references/utils-and-json.md` | `TTMSFNCUtils`, JSON helpers, JSON reader/writer, `TMS.TMSFNCValue`, promises |
| `references/persistence.md` | Saving/loading objects and control settings as JSON, object resolver |
| `references/cloud-base-and-http.md` | `TTMSFNCCloudBase` REST requests, `TTMSFNCHTTPServer` |
| `references/data-binding.md` | Data binder, FNC dataset with CSV/JSON links, filter builder and rules manager |

## Related skills

- `tms-fnc-uipack`: the UI Pack controls built on Core.
- `tms-fnc-datagrid`: TTMSFNCDataGrid.
- `/get-started`, `/unlock-feature`, `/review`.
