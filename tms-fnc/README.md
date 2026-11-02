# TMS FNC plugin

Helps Delphi developers get productive with **TMS FNC UI Pack** and **TMS FNC Core** in VCL, FMX and TMS WEB Core projects: TTMSFNCDataGrid, TreeView, Planner, RichEditor, Memo, Kanban Board, lists, edits, pickers, navigation controls, dialogs and more, plus the Core graphics, bitmap/SVG, PDF, printing, web browser, popup, JSON, persistence and REST building blocks they share.

This plugin replaces the former `tms-fnc-datagrid` plugin. Everything that plugin did is still here.

## Install

```
/plugin marketplace add tmssoftware/tms.claude.plugins
/plugin install tms-fnc@tms-software
```

If you had the old plugin installed, remove it first: `/plugin uninstall tms-fnc-datagrid@tms-software`.

## What it does

| Skill | How to use | What happens |
|---|---|---|
| **Get started** | `/get-started [component]`, or "add a TMS tree view to my form" | Detects your framework, checks the UI Pack / Core is installed (and explains how to install it with TMS Smart Setup if not), then adds a working FNC control with sample data or your own dataset. |
| **Unlock a feature** | `/unlock-feature [feature]`, or "add grouping to my grid" | Shows a menu of advanced features for the control you have, asks one or two questions about your data, and writes the feature into your project. For the DataGrid: filtering and filter row, sorting, grouping, conditional formatting, cell controls, grid in grid, merged cells, editing, database binding, Excel/PDF export. For other controls: TreeView virtual mode and database adapter, Planner resources and recurrency, RichEditor toolbars and IO, PDF export, persistence, styles and more. |
| **Review** | `/review [unit or folder]`, or "check my FNC code" | Checks your FNC code for members that don't exist, wrong event signatures, framework unit mix-ups, database binding mistakes and missing `BeginUpdate`/`EndUpdate`, and proposes fixes. |
| **DataGrid knowledge** | Automatic | Loads whenever you work with TTMSFNCDataGrid code. |
| **UI Pack knowledge** | Automatic | Loads whenever you work with the other UI Pack controls (TreeView, Planner, RichEditor, Memo, Kanban Board, lists, edits, pickers, buttons, page control, ribbon, toolbars, dialogs, SpreadGrid, the older TTMSFNCGrid). |
| **Core knowledge** | Automatic | Loads whenever you work with FNC Core (TTMSFNCGraphics, bitmap container, SVG, TTMSFNCPDFLib, PDF/print IO, web browser, popups, hints, styles, responsive manager, JSON, persistence, cloud base). |

The knowledge skills keep Claude on the real API instead of guessing from VCL/FMX standard controls or TMS VCL UI Pack (`TAdv*`) components.

## Requirements

- Delphi / RAD Studio with **TMS FNC UI Pack** and **TMS FNC Core** installed (VCL, FMX or TMS WEB Core). Core-only features need just TMS FNC Core. To install:
  ```
  tms credentials
  tms install tms.fnc.uipack
  ```
  using TMS Smart Setup (this also installs `tms.fnc.core`), or use the installers from tmssoftware.com.
- No connectors or accounts are needed. The plugin works on your local project files.

## Notes

- Excel export (`TTMSFNCDataGridExcelIO`) is available for VCL and FMX only and writes `.xls`. By default it leaves out the header row and first column; the plugin sets `DataGridStartRow`/`DataGridStartCol` to 0 to export everything.
- TTMSFNCWebBrowser, TTMSFNCEdgeWebBrowser and TTMSFNCMemo use the Microsoft Edge WebView2 runtime on Windows.
- The StellarDS dataset shown in some demos comes from TMS FNC Cloud Pack.

## Links

- Product pages: [TMS FNC UI Pack](https://www.tmssoftware.com/site/tmsfncuipack.asp) · [TMS FNC Core](https://www.tmssoftware.com/site/tmsfnccore.asp)
- Documentation: [TMS FNC UI Pack](https://doc.tmssoftware.com/fnc/uipack/index.html) · [TMS FNC Core](https://doc.tmssoftware.com/fnc/core/index.html) · [DataGrid](https://doc.tmssoftware.com/fnc/uipack/datagrid/index.html)
- Support: [TMS Support Center – FNC](https://support.tmssoftware.com/c/fnc)
- Source of this plugin: [tmssoftware/tms.claude.plugins](https://github.com/tmssoftware/tms.claude.plugins)
- Privacy: [plugin privacy policy](PRIVACY.md). The plugin collects no data.
