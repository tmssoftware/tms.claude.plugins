---
name: unlock-feature
description: >
  This skill should be used when the user asks to "unlock an advanced feature" of the TMS FNC DataGrid,
  "what else can the grid do", "add grouping / filtering / a filter row / conditional formatting / merged cells /
  cell controls / checkboxes / a grid in a grid / master-detail / Excel export / PDF export / printing" to a
  TTMSFNCDataGrid, or invokes /unlock-feature, optionally with a feature name as argument.
  It shows a short feature menu, asks about the user's data, and writes the feature into their project.
argument-hint: "[feature name]"
metadata:
  version: "0.1.0"
---

# Unlock an advanced TMS FNC DataGrid feature

Help the user add an advanced feature to a TTMSFNCDataGrid that already exists in their project, quickly and correctly. Show a menu, ask about their data, build the feature, and explain it briefly.

Before writing code, load the `tms-fnc-datagrid` skill. Use only members documented in its references or verified in the user's installed source. Never guess API names from TAdvStringGrid, TTMSFNCGrid or TStringGrid.

## Step 1: Find the grid

Search the project for `TTMSFNCDataGrid` declarations (form fields or runtime `Create` calls). Note the framework (VCL / FMX / WEB, from unit prefixes), how data gets in (cells filled in code vs. a database adapter), and the columns.
- No grid found → tell the user and offer `/get-started` first.
- Several grids → ask which one.

## Step 2: Pick a feature

If the user named a feature (argument or message), skip the menu. Otherwise present this menu in plain language, grouped and short. Use AskUserQuestion when available, or a numbered list:

| Feature | What it gives the user | Reference |
|---|---|---|
| Filtering & filter row | Let users filter rows from header dropdowns or a filter row | `sorting-filtering.md`, `filter-row.md` |
| Sorting (multi-column, custom) | Sort by several columns or with custom compare logic | `sorting-filtering.md` |
| Grouping | Group rows by one or more columns, with expand/collapse and summaries; drag-to-group panel | `grouping.md` |
| Conditional formatting | Colour, icons or bars based on cell values | `conditional-formatting.md` |
| Cell controls | Checkboxes, buttons, progress bars, images inside cells | `cell-controls.md` |
| Grid in grid | Nested detail grids inside rows | `cell-controls.md` |
| Merged cells | Span cells across rows/columns | `merging.md` |
| Editing & AutoFill | In-place editors per column, validation, Excel-style fill | `editing.md` |
| Database binding & master-detail | Show and edit dataset data; linked master/detail grids | `database.md` |
| Export & print | Excel, PDF or printer output | `export.md` |
| Non-visual data processing | Use the grid's data engine without UI, e.g. for export | `renderer.md` |

Mention that features can be combined; do one at a time.

## Step 3: Ask 1–2 questions

Read the feature's reference file first, then ask only what the code depends on, framed in terms of the user's own columns. Examples:
- Grouping: "Which column should rows be grouped by? Should groups show a count or a sum of a column?"
- Conditional formatting: "Which column, and what rule (e.g. Stock below 10 shows red)?"
- Cell controls: "Which column gets the checkbox/button, and what should happen when it's clicked?"
- Export: "Excel, PDF, or both? Triggered from a button?"

Use sensible defaults for everything else and say what you chose.

## Step 4: Build it

1. Add any extra units to the uses clause (framework prefix must match the grid's: `VCL.`, `FMX.`, or `WEBLib.`).
2. Add the code where it fits the existing structure: setup in the form create handler next to the grid's existing setup, event handlers as form methods with the exact signatures from the reference, and assign them in code if the grid was created at runtime.
3. Wrap bulk changes in `BeginUpdate`/`EndUpdate`.
4. If the feature needs an extra component (e.g. an export or database adapter component), create it in code next to the grid unless the user prefers the designer.
5. Follow the demo-derived patterns in the reference file. If the reference says something doesn't exist, don't use it.

## Step 5: Verify and explain

- Re-read the changes and check every grid member against the references.
- Offer to compile if Delphi command-line tools are available; otherwise ask the user to compile and run, and fix reported errors from the references or the installed `*.TMSFNCDataGrid*.pas` source.
- Explain in 2–4 plain sentences what the user will now see and how to tweak it (which property or rule to change).
- Suggest one or two related features to unlock next (e.g. after grouping → group summaries or conditional formatting; after database binding → filter row or export).
