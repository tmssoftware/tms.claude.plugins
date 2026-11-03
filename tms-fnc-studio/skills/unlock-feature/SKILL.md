---
name: unlock-feature
description: >
  This skill should be used when the user asks to "unlock an advanced feature" of a TMS FNC control, "what else can the
  grid / tree view / planner / rich editor do", "add grouping / filtering / a filter row / conditional formatting /
  merged cells / cell controls / master-detail / Excel or PDF export / printing" to a TTMSFNCDataGrid, "add a database
  adapter / checkboxes / virtual nodes to my TTMSFNCTreeView", "add recurring appointments / resources to my
  TTMSFNCPlanner", "add a toolbar to my TTMSFNCRichEditor", "export a TMS FNC control to PDF", or invokes
  /unlock-feature, optionally with a feature name as argument.
  It shows a short feature menu, asks about the user's data, and writes the feature into their project.
argument-hint: "[feature name]"
metadata:
  version: "0.2.0"
---

# Unlock an advanced TMS FNC feature

Help the user add an advanced feature to a TMS FNC control that already exists in their project, quickly and correctly. Show a menu, ask about their data, build the feature, and explain it briefly.

Before writing code, load the skill for the control: `tms-fnc-datagrid` for `TTMSFNCDataGrid`, `tms-fnc-uipack` for every other UI Pack control, `tms-fnc-core` for Core features (PDF, printing, graphics, persistence, styles, web browser). Use only members documented in their references; don't rely on component source code, which many users don't have. Never guess API names from TAdvStringGrid, TTMSFNCGrid, TStringGrid, TTreeView or other component sets.

## Step 1: Find the control

Search the project for `TTMSFNC*` declarations (form fields or runtime `Create` calls). Note the framework (VCL / FMX / WEB, from unit prefixes), how data gets in (filled in code vs. a database adapter), and the shape of the data.
- No FNC control found → tell the user and offer `/get-started` first.
- Several candidates → ask which one.

## Step 2: Pick a feature

If the user named a feature (argument or message), skip the menu. Otherwise present the menu for that control in plain language, grouped and short. Use AskUserQuestion when available, or a numbered list.

### TTMSFNCDataGrid (skill `tms-fnc-datagrid`)

| Feature | What it gives the user | Reference |
|---|---|---|
| Filtering & filter row | Let users filter rows from header dropdowns or a filter row | `sorting-filtering.md`, `filter-row.md` |
| Sorting (multi-column, custom) | Sort by several columns or with custom compare logic | `sorting-filtering.md` |
| Grouping | Group rows by one or more columns, with expand/collapse and summaries; drag-to-group panel | `grouping.md` |
| Conditional formatting | Colour, icons or bars based on cell values | `conditional-formatting.md` |
| Styling & number formats | A polished dashboard look: header colours, zebra rows, selection colour, fonts, currency/date formats | `styling.md` |
| Cell controls | Checkboxes, buttons, progress bars, images inside cells | `cell-controls.md` |
| Grid in grid | Nested detail grids inside rows | `cell-controls.md` |
| Merged cells | Span cells across rows/columns | `merging.md` |
| Editing & AutoFill | In-place editors per column, validation, Excel-style fill | `editing.md` |
| Database binding & master-detail | Show and edit dataset data; linked master/detail grids | `database.md` |
| Export & print | Excel, PDF or printer output | `export.md` |
| Non-visual data processing | Use the grid's data engine without UI, e.g. for export | `renderer.md` |

### Other UI Pack controls (skill `tms-fnc-uipack`)

Read the control's reference file and offer the features it documents. Typical menus:

| Control | Features worth offering | Reference |
|---|---|---|
| TreeView | Multiple columns, checkboxes, virtual mode for large data, editing, sorting/filtering, database adapter | `treeview.md` |
| Planner | Modes (day/week/month/timeline), resources, item editor, recurrency, database adapter, toolbar popup | `planner.md` |
| RichEditor | Format toolbar and ruler, images and hyperlinks, merge fields, HTML/RTF load and save, PDF export, printing | `rich-editor.md` |
| KanbanBoard | Columns and cards, drag and drop, database adapter | `kanban.md` |
| Lists (ListBox, TableView, TileList, SearchList, ResponsiveList) | Checkboxes, search/filtering, categories, custom item drawing | `lists.md` |
| Memo | Language and theme, custom languages, custom themes | `memo.md` |
| Navigation (PageControl, TabSet, NavigationPanel, Ribbon, ToolBar) | Pages and tabs in code, close buttons, toolbars with pickers | `containers-and-navigation.md` |

### Cross-cutting Core features (skill `tms-fnc-core`)

| Feature | Reference |
|---|---|
| Export a control or custom drawing to PDF, print it | `pdf-and-print.md` |
| Save and restore control settings / objects as JSON | `persistence.md` |
| Images from a bitmap container or SVG collection | `bitmaps-and-svg.md` |
| Application-wide styles | `styles.md` |
| Popups, popup menus and hints | `popups-and-hints.md` |
| Layout that adapts to the form size | `responsive-state-undo.md` |

Mention that features can be combined; do one at a time.

## Step 3: Ask 1–2 questions

Read the feature's reference file first, then ask only what the code depends on, framed in terms of the user's own data. Examples:
- Grid grouping: "Which column should rows be grouped by? Should groups show a count or a sum of a column?"
- Grid conditional formatting: "Which column, and what rule (e.g. Stock below 10 shows red)?"
- TreeView database adapter: "Which dataset and which fields hold the parent/child relation and the text?"
- Planner resources: "Which resources (people, rooms) should appear as columns?"
- Export: "PDF, Excel, printer, or several? Triggered from a button?"

Use sensible defaults for everything else and say what you chose.

## Step 4: Build it

1. Add any extra units to the uses clause (framework prefix must match the control's: `VCL.`, `FMX.`, or `WEBLib.`).
2. Add the code where it fits the existing structure: setup in the form create handler next to the control's existing setup, event handlers as form methods with the exact signatures from the reference, and assign them in code if the control was created at runtime.
3. Wrap bulk changes in `BeginUpdate`/`EndUpdate`.
4. If the feature needs an extra component (an IO, adapter, toolbar or container component), create it in code next to the control unless the user prefers the designer.
5. Follow the demo-derived patterns in the reference file. If the reference says something doesn't exist, don't use it.

## Step 5: Verify and explain

- Re-read the changes and check every FNC member against the references.
- Offer to compile if Delphi command-line tools are available; otherwise ask the user to compile and run, and fix reported errors from the references (or the official docs at doc.tmssoftware.com); if a member can't be confirmed, say so instead of guessing. For command-line builds use the `build.cmd` approach in the datagrid skill's `setup-and-install.md`.
- For visual features, check the result from an image the app saves of itself (datagrid `styling.md`, "Checking the look"). Never take a screenshot of the user's whole desktop. Close the app instance you started before rebuilding.
- Explain in 2–4 plain sentences what the user will now see and how to tweak it (which property or event to change).
- Suggest one or two related features to unlock next.
