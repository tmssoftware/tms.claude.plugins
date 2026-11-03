---
name: get-started
description: >
  This skill should be used when the user says "get started with TMS FNC", "add a TTMSFNCDataGrid / TTMSFNCTreeView /
  TTMSFNCPlanner / TTMSFNCRichEditor / TTMSFNCKanbanBoard (or any other TMS FNC control) to my form",
  "add a data grid / tree view / planner / rich text editor / kanban board to my Delphi project", "set up TMS FNC UI Pack",
  "use TMS FNC Core in my project", or invokes /get-started in a VCL, FMX or TMS WEB Core project.
  It adds a working FNC component with sample data to the user's project and explains what was done.
argument-hint: "[component]"
metadata:
  version: "0.2.0"
---

# Get started with TMS FNC UI Pack and TMS FNC Core

Add a working TMS FNC component to the user's Delphi project, show something useful in it, and point to the next features worth trying. Keep the conversation short and practical: the goal is a working control on screen within a few minutes.

## Knowledge to load

Before writing any FNC code, load the skill that covers the component and read its setup reference plus the component's own reference:

| Component | Skill | Read first |
|---|---|---|
| `TTMSFNCDataGrid` (+ database adapter, PDF/Excel/print IO) | `tms-fnc-datagrid` | `setup-and-install.md`, `core-api.md` |
| Any other UI Pack control (TreeView, Planner, RichEditor, Memo, Kanban, lists, edits, pickers, buttons, page control, ribbon, dialogs, SpreadGrid, ...) | `tms-fnc-uipack` | `setup-and-components.md`, then the component's file |
| FNC Core features (graphics, bitmaps/SVG, PDF, printing, web browser, popups, JSON, persistence, REST/cloud base, styles, responsive manager) | `tms-fnc-core` | `setup-and-install.md`, then the topic file |

Use only members documented there. Work from the references, not from component source code: users may have trial or DCU-only installs, and the knowledge skills explain what to do when a member isn't covered. Never guess API names from VCL/FMX standard controls, TMS VCL UI Pack (`TAdv*`) or other component sets.

## Step 1: Inspect the project

1. Find the project file (`*.dpr` / `*.dproj`) and the main form unit (`*.pas` + `*.dfm` or `*.fmx`). For TMS WEB Core, the form has a `*.dfm` with `WEBLib.*` units in its uses clause and the project usually uses `WEBLib.Forms`.
2. Determine the framework from the uses clauses:
   - `Vcl.Forms` / `Vcl.Controls` → VCL
   - `FMX.Forms` / `FMX.Types` → FMX
   - `WEBLib.Forms` → TMS WEB Core
   If it's ambiguous or there are several projects, ask the user which project and form to use.
3. Check whether the products are available: look for existing `*.TMSFNC*` units in the project, or ask the user whether TMS FNC UI Pack (and therefore TMS FNC Core) is installed in their IDE. If they don't know, tell them to look for the **TMS FNC UI** palette page in the IDE. For Core-only features (graphics, PDF lib, web browser, JSON) only TMS FNC Core is needed.

## Step 2: If the products are not installed

Do not try to install them on the user's behalf, and never ask for or handle their TMS account details. Explain the two options from the setup reference (TMS Smart Setup command line, or the regular installer from the TMS website) with the exact commands documented there: `tms install tms.fnc.uipack` installs the UI Pack and its TMS FNC Core dependency, `tms install tms.fnc.core` installs Core alone. Ask the user to confirm when it's installed, then continue.

## Step 3: Pick the component and ask one question

If the user named a component (argument or message), use it. Otherwise ask what they want to build and suggest the fitting control (for example: tabular data → DataGrid, hierarchy → TreeView, appointments → Planner, formatted text → RichEditor, code editing → Memo, task board → KanbanBoard, a settings form → edits, pickers and switches).

Then ask what it should show at first:
- **Sample data**: a small in-memory data set that fits the component (products in a grid, folders in a tree, a few appointments this week in a planner, three columns of cards on a kanban board).
- **Their own data**: a dataset they already have (TFDQuery, TClientDataSet, etc.). Use the component's database adapter when it has one (DataGrid, Planner, Timeline, KanbanBoard; for a TreeView fill the nodes from the dataset in code, see `treeview.md`), following its reference exactly.

## Step 4: Add the component

Prefer creating the component at runtime in code (in the form's `OnCreate`, or `WebFormCreate` for WEB Core). It works without touching the form designer file and is easy to review. Only edit the `.dfm`/`.fmx` if the user asks for a design-time component.

1. Add the correct framework-prefixed units to the form's `uses` clause (`VCL.`, `FMX.` or `WEBLib.`, as listed in the reference).
2. Add a private field for the component on the form class.
3. In the create handler: create it with the form as owner, set `Parent` and `Align` (or position), wrap data loading in `BeginUpdate`/`EndUpdate` where the class has them, and fill the sample data with the documented API.
4. Turn on the friendly defaults the reference confirms (for a grid: header sorting, column resizing, a sensible selection mode; for a tree: columns and expand state; for a planner: a sensible mode and day range).
5. Keep the code idiomatic Delphi: match the user's existing naming and formatting.

## Step 5: Verify

- Re-read the changed unit and check every FNC member used against the references.
- If the user has Delphi command-line tools on PATH (`msbuild` with the RAD Studio environment, or `dcc32`/`dcc64`), offer to compile. Otherwise ask them to compile and run (F9) and report any error messages back.
- When you create a new project from scratch, start from the minimal `.dproj` and `build.cmd` in the datagrid skill's `references/setup-and-install.md` ("Building from the command line"). It applies to every FNC control and avoids the usual first-build failures (missing unit scope names, the IDE library path not visible to msbuild, PowerShell quoting).
- If a compile error mentions an unknown identifier on an FNC member, look it up in the references (and, if needed, the official docs at doc.tmssoftware.com) and fix it. Never "fix" it by guessing a different name; if the right member can't be found, tell the user.
- If the user asked for a particular look, check it from an image the app saves of itself (see "Checking the look" in the datagrid skill's `references/styling.md`), not from a screenshot of the user's desktop. Close the instance you started before rebuilding.

## Step 6: Wrap up

Summarize in plain language what the component now does, then suggest 3 features to try next with a one-line benefit each. Tell the user they can run `/unlock-feature` to add any of them.
