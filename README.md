# TMS Software plugins for Claude

Claude plugins that help Delphi developers work with TMS Software products.

## Install

In Claude Code:

```
/plugin marketplace add tmssoftware/tms.claude.plugins
/plugin install tms-fnc-studio@tms-software
```

## Plugins

| Plugin | Install id | What it does |
|---|---|---|
| [TMS FNC Studio](tms-fnc-studio) ([UI Pack docs](https://doc.tmssoftware.com/fnc/uipack/index.html), [Core docs](https://doc.tmssoftware.com/fnc/core/index.html)) | `tms-fnc-studio@tms-software` | Build VCL, FMX and TMS WEB Core apps with TMS FNC UI Pack and TMS FNC Core: add DataGrid, TreeView, Planner, RichEditor, Kanban Board, inputs, pickers and navigation controls, use Core graphics, PDF, web browser, JSON and persistence, and review FNC code against the real API. Replaces the former `tms-fnc-datagrid` and `tms-fnc` plugins. |

Each plugin needs the matching TMS product installed in your IDE (for example via TMS Smart Setup: `tms install tms.fnc.uipack`).

## Maintaining

Line 2 of every skill reference file is a generated section map (`> Sections (line ranges): ...`) that lets agents read only the lines they need. After editing a reference, regenerate the maps:

```
python scripts/update-section-maps.py           # rewrite
python scripts/update-section-maps.py --check   # exit 1 if a map is stale
```

## License

Proprietary, © TMS Software. See [LICENSE](LICENSE).
