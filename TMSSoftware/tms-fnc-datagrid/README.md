# TMS FNC DataGrid plugin

Helps Delphi developers get productive with **TMS FNC DataGrid** (`TTMSFNCDataGrid`, part of the TMS FNC UI Pack) in VCL, FMX and TMS WEB Core projects.

## Install

```
/plugin install tms-fnc-datagrid --marketplace tmssoftware/tms.claude.plugins
```

## What it does

| Skill | How to use | What happens |
|---|---|---|
| **Get started** | `/get-started`, or "add a TMS data grid to my form" | Detects your framework, checks the UI Pack is installed (and explains how to install it with TMS Smart Setup if not), then adds a working grid with sample data or your own dataset. |
| **Unlock a feature** | `/unlock-feature [feature]`, or "add grouping to my grid" | Shows a menu of advanced features, asks one or two questions about your data, and writes the feature into your project. Features: filtering and filter row, multi-column/custom sorting, grouping, conditional formatting, cell controls, grid in grid, merged cells, editing and AutoFill, database binding and master-detail, Excel/PDF export and printing, non-visual data processing. |
| **Review** | `/review [unit or folder]`, or "check my grid code" | Checks your grid code for members that don't exist, wrong event signatures, framework unit mix-ups, database binding mistakes and missing `BeginUpdate`/`EndUpdate`, and proposes fixes. |
| **DataGrid knowledge** | Automatic | Loads whenever you work with TTMSFNCDataGrid code, so Claude uses the real API instead of guessing from TStringGrid or TAdvStringGrid. |

## Requirements

- Delphi / RAD Studio with **TMS FNC UI Pack** and **TMS FNC Core** installed (VCL, FMX or TMS WEB Core). To install:
  ```
  tms credentials
  tms install tms.fnc.uipack
  ```
  using TMS Smart Setup, or use the installer from tmssoftware.com.
- No connectors or accounts are needed. The plugin works on your local project files.

## Notes

- Excel export (`TTMSFNCDataGridExcelIO`) is available for VCL and FMX only and writes `.xls`. By default it leaves out the header row and first column; the plugin sets `DataGridStartRow`/`DataGridStartCol` to 0 to export everything.
- The StellarDS dataset shown in some demos comes from TMS FNC Cloud Pack.

## Links

- Product page: [TMS FNC UI Pack](https://www.tmssoftware.com/site/tmsfncuipack.asp)
- Documentation: [TMS FNC DataGrid](https://doc.tmssoftware.com/fnc/uipack/datagrid/index.html) · [Getting started](https://doc.tmssoftware.com/fnc/uipack/datagrid/getting-started.html) · [API reference](https://doc.tmssoftware.com/fnc/uipack/api/ttmsfncdatagrid/index.html)
- Support: [TMS Support Center – FNC](https://support.tmssoftware.com/c/fnc)
- Source of this plugin: [tmssoftware/tms.claude.plugins](https://github.com/tmssoftware/tms.claude.plugins)
