# Responsive layouts, state management, undo, scroll bar, toggle button (TTMSFNCResponsiveManager, TTMSFNCUndoManager, TTMSFNCScrollBar, TTMSFNCToggleButton)
> Sections (line ranges): 6-17 Units and palette · 18-98 TTMSFNCResponsiveManager · 99-102 TTMSFNCCustomStateManager · 103-143 TTMSFNCUndoManager · 144-168 TTMSFNCScrollBar · 169-172 TTMSFNCToggleButton · 173-177 Platform notes · 178-189 Does not exist / common mistakes

Verified against TMS FNC Core 4.5.0.0 source: `*.TMSFNCResponsiveManager`, `*.TMSFNCStateManager`, `*.TMSFNCUndo`, `*.TMSFNCCustomControl`, `*.TMSFNCScrollBar`, `*.TMSFNCToggleButton`.

## Units and palette

| Class | Unit | Frameworks | Palette |
|---|---|---|---|
| `TTMSFNCResponsiveManager` | `*.TMSFNCResponsiveManager` | VCL, FMX, LCL, WEB | TMS FNC UI |
| `TTMSFNCStateManagerItem`, `TTMSFNCCustomStateManager` (base only) | `*.TMSFNCStateManager` | VCL, FMX, LCL, WEB | - |
| `TTMSFNCUndoManager` | `*.TMSFNCUndo` | VCL, FMX, LCL, WEB | not a component |
| `TTMSFNCScrollBar` | `*.TMSFNCScrollBar` | VCL, FMX, LCL, WEB | TMS FNC UI |
| `TTMSFNCToggleButton` | `*.TMSFNCToggleButton` | VCL, FMX, LCL, WEB | not registered |

Prefix rule: `VCL.` / `FMX.` / `WEBLib.`, LCL is `LCLTMSFNC...`. Event handlers of the responsive manager use `TTMSFNCStateManagerItem`, so add `*.TMSFNCStateManager` to the uses clause too.

## TTMSFNCResponsiveManager

Stores complete layouts ("states") of a container and switches between them. A state's `Content` is JSON produced by serializing every **named** child control of `Control` (its published properties plus parent name). With `AutoLoadOnResize` the manager hooks `Control.OnResize` and loads the state whose constraint best matches the current size.

```delphi
// TTMSFNCResponsiveManager, published
property Control: TTMSFNCStateManagerControl;   // TControl (VCL/LCL/WEB) or TFmxObject (FMX); usually the form
property States: TTMSFNCResponsiveManagerItems;  // collection of TTMSFNCResponsiveManagerItem
property ActiveState: Integer;                   // default -1; setting it loads that state
property Mode: TTMSFNCResponsiveManagerResizeMode;  // mrmWidthOnly (default), mrmHeightOnly, mrmWidthFirst, mrmHeightFirst
property AutoLoadOnResize: Boolean;              // default True
property AutoSave: Boolean;                      // default True; design-time only: saves the active state before switching
property OnBeforeLoadState: TTMSFNCStateManagerBeforeLoadStateEvent;   // (Sender; AState: TTMSFNCStateManagerItem; var ACanLoad: Boolean)
property OnAfterLoadState: TTMSFNCStateManagerAfterLoadStateEvent;     // (Sender; AState: TTMSFNCStateManagerItem)
property OnBeforeLoadControlState: TTMSFNCStateManagerBeforeLoadControlStateEvent;
  // (Sender; AState; AControl: TTMSFNCStateManagerControl; var AValue: string; var ACanLoad: Boolean)
property OnAfterLoadControlState: TTMSFNCStateManagerAfterLoadControlStateEvent;
property OnLoadStateCustom: TTMSFNCStateManagerLoadStateCustomEvent;   // (Sender; AState; var ALoad: Boolean)

// public
procedure LoadState; overload;                          // pick by current Control size
procedure LoadState(AStringValue: string); overload;    // pick by Constraint.StringValue
procedure LoadState(ABooleanValue: Boolean); overload;
procedure LoadState(ANumberValue: Extended); overload;
function SaveToNewState: TTMSFNCResponsiveManagerItem; overload;   // snapshot + Constraint := current size
function SaveToNewState(AStringValue: string): TTMSFNCResponsiveManagerItem; overload;
function SaveToNewState(ABooleanValue: Boolean): TTMSFNCResponsiveManagerItem; overload;
function SaveToNewState(ANumberValue: Extended): TTMSFNCResponsiveManagerItem; overload;
function FindState: TTMSFNCResponsiveManagerItem; overload;        // also FindState(string/Boolean/Extended)
procedure Preview;                                      // opens a resizable preview form (design aid)
// inherited from TTMSFNCCustomStateManager
procedure SaveToState(AState: TTMSFNCStateManagerItem); overload;   // also SaveToState(AIndex: Integer), SaveToState(AName: string)
procedure LoadStateByName(AName: string);  procedure LoadStateByIndex(AIndex: Integer);
procedure LoadStateCustom(ACallBack: TTMSFNCStateManagerLoadStateCustomCallback = nil);  // reference to procedure(AState; var ALoad: Boolean)
function FindStateByName(AName: string): TTMSFNCStateManagerItem;
function FindConflicts(AConflictedControlNames: TStrings): Boolean;
procedure Optimize;
procedure BeginUpdate; procedure EndUpdate;
```

`TTMSFNCResponsiveManagerItem` (published): `Name`, `Content: string`, `Default: Boolean`, `Constraint: TTMSFNCResponsiveManagerConstraint` (`Width`, `Height`, `StringValue`, `NumberValue`, `BooleanValue`); public `Load`, `DataInteger`, `DataString`, `DataObject`, `DataPointer`, `DataBoolean`.

**Matching rule** (`InternalFindState`, `mrmWidthOnly`): a state qualifies when `Control width >= Constraint.Width`; among the qualifying states the one with the largest constraint wins; if none qualifies the smallest state is used. So each state's `Constraint.Width` is the **minimum** width from which that layout applies. On VCL the constraint is DPI-scaled against `DesigntimeFormPixelsPerInch`.

### Typical workflow (demo `VCL\Responsive`)

States are normally built at design time: drop the manager on the form (it sets `Control` to the owner form at design time only), lay out the form, use the component editor to add a state, resize, rearrange, add the next state. At runtime the form's resizes switch layouts automatically; react in `OnAfterLoadState`:
```delphi
uses VCL.TMSFNCResponsiveManager, VCL.TMSFNCStateManager;

procedure TForm20.TMSFNCResponsiveManager1AfterLoadState(Sender: TObject;
  AState: TTMSFNCStateManagerItem);
begin
  if AState.Index = 0 then
    Button1.Images := VirtualImageList2     // compact layout: small icons
  else
    Button1.Images := VirtualImageList1;
end;
```

### Runtime creation

```delphi
procedure TForm1.FormCreate(Sender: TObject);
begin
  FRM := TTMSFNCResponsiveManager.Create(Self);
  FRM.Control := Self;                 // runtime: must be set explicitly; hooks Self.OnResize
  FRM.AutoLoadOnResize := False;       // build states first
  ArrangeWide;                         // your code: position named controls for wide screens
  FRM.SaveToNewState.Constraint.Width := 800;   // wide layout from 800 px
  ArrangeNarrow;
  FRM.SaveToNewState.Constraint.Width := 0;     // narrow layout below 800 px
  FRM.AutoLoadOnResize := True;
  FRM.LoadState;                       // apply the state for the current size
end;

// non-size states, e.g. a theme
FRM.SaveToNewState('dark');
FRM.LoadState('dark');
```

## TTMSFNCCustomStateManager

The base class (unit `*.TMSFNCStateManager`) implements the snapshot/restore engine. There is **no** concrete `TTMSFNCStateManager` component in FNC Core; the only registered descendant is `TTMSFNCResponsiveManager`, which you can also use as a plain state manager with string/number/Boolean constraints and `LoadStateByName`.

## TTMSFNCUndoManager

A snapshot-based undo stack (a `TCollection`, not a component). Every `TTMSFNCCustomControl` exposes one lazily created instance:
```delphi
property UndoManager: TTMSFNCUndoManager;   // public on TTMSFNCCustomControl
```
```delphi
// TTMSFNCUndoManager
constructor Create(AObject: TObject);            // for non-control objects; you free it
procedure PushState(const AActionName: string);  // snapshot AObject's published properties (TTMSFNCPersistence)
procedure Undo;  procedure Redo;
function CanUndo: Boolean;  function CanRedo: Boolean;
function NextUndoAction: string;  function NextRedoAction: string;
procedure ClearUndoStack;                        // clears and pushes a baseline state ('')
property MaxStackCount: Integer;                 // default 20; oldest snapshot dropped
property Stack[Index: Integer]: TTMSFNCUndoStackItem; default;   // ActionName, Obj, State: TStream
```
Semantics from source: each `PushState` stores the **state after** a change; `Undo` reloads the previous snapshot. You therefore need a baseline first (`ClearUndoStack` pushes one). `CanUndo` is `FCurrent > 0`. Pushing after an undo discards the redo branch. Snapshots go through `ITMSFNCPersistence.SaveSettingsToStream` when the object implements it, otherwise `TTMSFNCPersistence.SaveSettingsToStream` (published properties only, not runtime data such as grid cells unless the control persists them).

```delphi
procedure TForm1.FormCreate(Sender: TObject);
begin
  TMSFNCScrollBar1.UndoManager.ClearUndoStack;      // baseline
end;

procedure TForm1.ChangeClick(Sender: TObject);
begin
  TMSFNCScrollBar1.Fill.Color := gcRed;
  TMSFNCScrollBar1.Value := 50;
  TMSFNCScrollBar1.UndoManager.PushState('Change color and value');
  UndoButton.Caption := 'Undo ' + TMSFNCScrollBar1.UndoManager.NextUndoAction;
end;

procedure TForm1.UndoClick(Sender: TObject);
begin
  if TMSFNCScrollBar1.UndoManager.CanUndo then
    TMSFNCScrollBar1.UndoManager.Undo;
end;
```
Works the same on any FNC control. UI Pack's `TTMSFNCDataGrid` uses this class internally for its own undo.

## TTMSFNCScrollBar (brief)

FNC-drawn scroll bar control (`TTMSFNCCustomControl` descendant).
```delphi
TTMSFNCScrollBarKind = (sbkHorizontal, sbkVertical);
property Kind: TTMSFNCScrollBarKind;   // default sbkVertical (default size 18 x 121)
property Min: Double;  property Max: Double;   // 0 / 100
property Value: Double;                        // clamped to [Min, Max - PageSize]
property PageSize: Double;  property SmallChange: Double (1);  property LargeChange: Double (20);
property Tracking: Boolean;                    // default True: OnValueChanged while dragging
property Appearance: TTMSFNCScrollBarAppearance;   // ThumbFill, ThumbStroke, ScrollButtonSize, ThumbButtonSize, ...Hover/Down fills
property Fill; property Stroke;
property OnValueChanged: TTMSFNCScrollBarValueChanged;       // procedure(Sender: TObject; Value: Double) of object
property OnPageSizeChanged: TTMSFNCScrollBarPageSizeChanged; // procedure(Sender: TObject; PageSize: Double) of object
```
```delphi
sb := TTMSFNCScrollBar.Create(Self);
sb.Parent := Self;
sb.Kind := sbkHorizontal;
sb.Align := alBottom;
sb.Max := 1000;
sb.PageSize := 100;
sb.OnValueChanged := ScrollValueChanged;
```

## TTMSFNCToggleButton (brief)

A thin wrapper used internally, not on the palette. VCL: descends from `Vcl.StdCtrls.TButton`, adds published `isPressed: Boolean`, `GroupIndex: Integer` (buttons with the same non-zero `GroupIndex` on the same parent act as a radio group) and its own `OnClick`. FMX: descends from `FMX.StdCtrls.TButton` with `StaysPressed := True` (use FMX's `IsPressed`). WEB/LCL: `isPressed` toggles on click and colors the button `clSkyBlue`.

## Platform notes

- `TTMSFNCResponsiveManager` on WEB: same API (`[ComponentPlatformsAttribute(TMSPlatformsWeb)]`). On FMX `Control` is a `TFmxObject` and the resize hook is installed on `TControl` controls.
- The responsive manager stores state JSON in the form file; large forms make large DFM/FMX files. `Optimize` compacts the stored content by comparing property values across states.

## Does not exist / common mistakes

- `TTMSFNCStateManager` component: does not exist; use `TTMSFNCResponsiveManager`.
- `Breakpoints`, `AddBreakpoint`, `OnBreakpointChanged`, `Layouts`: the API is `States` + `Constraint.Width/Height` + `SaveToNewState` / `LoadState`.
- `LoadState(AIndex: Integer)`: the integer overload does not exist; `LoadState(5)` resolves to the `Extended` (NumberValue) overload. Use `LoadStateByIndex(AIndex)` or `ActiveState := AIndex`.
- Setting `Control.OnResize` (e.g. the form's `OnResize`) in code **after** assigning `Control`: replaces the manager's hook and auto-switching stops. Assign your handler first; the manager chains to it.
- Expecting runtime-created, unnamed controls to be saved: only controls with a non-empty `Name` are serialized. `TTMSFNCCustomComponent` descendants are never persisted.
- Expecting `Control` to default to the form at runtime: only the design-time constructor does that.
- `UndoManager.BeginUpdate`, `.Add`, `.Execute`, `TTMSFNCUndo`: the class is `TTMSFNCUndoManager`; API is `PushState` / `Undo` / `Redo`. Calling `PushState` before the change (command-pattern style) shifts every undo by one step.
- `TTMSFNCScrollBar.Position` / `OnChange` / `OnScroll` (VCL `TScrollBar`): use `Value` and `OnValueChanged`. `Kind := sbHorizontal` (VCL enum): the values are `sbkHorizontal` / `sbkVertical`.
- `TTMSFNCToggleButton.Checked` / `Down`: VCL/WEB/LCL use `isPressed`; FMX uses the inherited `IsPressed`.
