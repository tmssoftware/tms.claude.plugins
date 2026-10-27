---
name: get-started
description: >
  This skill should be used when the user says "get started with the TMS FNC DataGrid",
  "add a TTMSFNCDataGrid to my form", "add a data grid to my Delphi project", "show data in a TMS grid",
  "set up TMS FNC DataGrid", or invokes /get-started in a VCL, FMX or TMS WEB Core project.
  It adds a working grid with sample data to the user's project and explains what was done.
metadata:
  version: "0.1.0"
---

# Get started with TMS FNC DataGrid

Add a working TTMSFNCDataGrid to the user's Delphi project, show data in it, and point to the next features worth unlocking. Keep the conversation short and practical: the goal is a grid on screen within a few minutes.

Before writing any grid code, load the `tms-fnc-datagrid` skill and read `references/setup-and-install.md` and `references/core-api.md`. Use only members documented there or verified in the user's installed source. Never guess API names from TAdvStringGrid, TTMSFNCGrid or TStringGrid.

## Step 1: Inspect the project

1. Find the project file (`*.dpr` / `*.dproj`) and the main form unit (`*.pas` + `*.dfm` or `*.fmx`). For TMS WEB Core, the form has a `*.dfm` with `WEBLib.*` units in its uses clause and the project usually uses `WEBLib.Forms`.
2. Determine the framework from the uses clauses:
   - `Vcl.Forms` / `Vcl.Controls` → VCL
   - `FMX.Forms` / `FMX.Types` → FMX
   - `WEBLib.Forms` → TMS WEB Core
   If it's ambiguous or there are several projects, ask the user which project and form to use.
3. Check whether TMS FNC UI Pack is available: look for existing `*.TMSFNCDataGrid` or other `*.TMSFNC*` units in the project, or ask the user whether the TMS FNC UI Pack is installed in their IDE. If they don't know, tell them to look for the TMS FNC UI Pack palette page in the IDE.

## Step 2: If the UI Pack is not installed

Do not try to install it on the user's behalf. Explain the two options from `references/setup-and-install.md` (TMS Smart Setup command line, or the regular installer from the TMS website) with the exact commands documented there, and mention it requires TMS FNC Core. Ask the user to confirm when it's installed, then continue.

## Step 3: Ask one question

Ask what the grid should show at first:
- **Sample data**: a small in-memory table (e.g. a few products with name, category, price, stock), so they see sorting/filtering/editing work right away.
- **Their own data**: a dataset they already have (TFDQuery, TClientDataSet, etc.). If so, read `references/database.md` and use the database adapter instead of filling cells.

## Step 4: Add the grid

Prefer adding the grid at runtime in code (in the form's `OnCreate`, or `WebFormCreate` for WEB Core). It works without touching the form designer file and is easy to review. Only edit the `.dfm`/`.fmx` if the user asks for a design-time component.

1. Add the correct framework-prefixed units to the form's `uses` clause (from `references/setup-and-install.md`).
2. Add a private field for the grid on the form class.
3. In the create handler: create the grid, set `Parent` and `Align` so it fills the form (or a panel the user names), wrap data loading in `BeginUpdate`/`EndUpdate`, set up the column headers, and fill the sample rows using the documented data-access API.
4. Turn on the friendly defaults that make the grid feel alive, only if `core-api.md` and `sorting-filtering.md` confirm them: sorting by clicking a header, column resizing, and a sensible selection mode.
5. Keep the code idiomatic Delphi: match the user's existing naming and formatting.

For database data: drop a database adapter in code, connect it to the user's `TDataSource`, link it to the grid, and open the dataset, following `references/database.md` exactly.

## Step 5: Verify

- Re-read the changed unit and check every grid member used against the references.
- If the user has Delphi command-line tools on PATH (`msbuild` with the RAD Studio environment, or `dcc32`/`dcc64`), offer to compile. Otherwise ask them to compile and run (F9) and report any error messages back.
- If a compile error mentions an unknown identifier on a grid member, look it up in the references or the installed source (`*.TMSFNCDataGrid*.pas`) and fix it. Never "fix" it by guessing a different name.

## Step 6: Wrap up

Summarize in plain language what the grid now does, then suggest 3 features to try next with a one-line benefit each (for example, filtering, grouping, conditional formatting, Excel/PDF export). Tell the user they can run `/unlock-feature` to add any of them.
