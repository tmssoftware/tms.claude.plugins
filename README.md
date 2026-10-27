# TMS Software plugins for Claude

Claude plugins that help Delphi developers work with TMS Software products.

## Install

In Claude Code:

```
/plugin marketplace add tmssoftware/tms.claude.plugins
/plugin install tms-fnc-datagrid@tms-software
```

## Plugins

Plugins are grouped by vendor folder: everything from TMS Software lives under [`TMSSoftware/`](TMSSoftware).

| Plugin | Install id | What it does |
|---|---|---|
| [TMS FNC DataGrid](TMSSoftware/tms-fnc-datagrid) ([docs](https://doc.tmssoftware.com/fnc/uipack/datagrid/index.html)) | `tms-fnc-datagrid@tms-software` | Get started with TMS FNC DataGrid (VCL, FMX, TMS WEB Core), add advanced features such as grouping, filter row, conditional formatting, cell controls, database binding and Excel/PDF export, and review grid code against the real API. |

Each plugin needs the matching TMS product installed in your IDE (for example via TMS Smart Setup: `tms install tms.fnc.uipack`).

## License

Proprietary, © TMS Software. See [LICENSE](LICENSE).
