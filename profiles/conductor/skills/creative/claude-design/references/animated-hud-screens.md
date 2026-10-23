# Animated HUD / sci-fi screens (single-file HTML)

Recipe for Jarvis/Iron-Man-style boot screens, "system initializing" visuals,
and sci-fi status dashboards: one self-contained HTML file, SVG + CSS animation,
no JS dependency. Load when the user asks for a HUD look, a startup screen, or an
animated system visual.

## Deliverable

- One self-contained `.html` on the Desktop (inline `<style>`, inline `<svg>`).
- Show it to the user inline with `::preview{file="<abs path>"}` on its own line.
  This user reviews by eye and cannot read code, so the preview IS the feedback
  loop — render it every pass, do not describe it in prose.
- No external assets or CDN; gradients and shapes only, so it opens offline.

## Skeleton

- Centered square stage: `.stage{width:min(96vmin,1100px);aspect-ratio:1}` so the
  composition scales to any window.
- One `<svg viewBox="0 0 400 400">` absolutely positioned over the stage for the
  rings; an HTML `<div>` above it (higher z-index) for the centre text and the
  corner status readouts.
- Background as separate fixed layers: a radial-gradient "space" wash, a star
  field, and a faint grid with a radial mask so it fades at the edges.

## Animation primitives (CSS only)

- Spin: `@keyframes spin{to{transform:rotate(360deg)}}`; the class sets
  `transform-origin:50% 50%; animation:spin 30s linear infinite`. Add `reverse`
  to the shorthand for counter-rotating rings; vary the duration per ring for depth.
- Dashed rings: a `<circle fill="none">` with `stroke-dasharray` (e.g. `3 12`,
  `2 25`) and `stroke-linecap="round"` — cheap detail that reads as instrument ticks.
- Breathe/pulse: opacity keyframes (`0%,100%{opacity:.26}50%{opacity:.82}`).
- Scanning line: a `<line>` from the centre outward, inside a spinning group.
- **Orbiting bodies**: put the orbit `<ellipse>` AND the planet inside one
  `<g transform="rotate(theta 200 200)">`, then animate that group with the spin
  class. `transform-origin` must be the SVG centre in user units (`200px 200px`).
- Tilt an orbit by rotating the group; nest a second `rotate` around the planet if
  it must stay upright.

## Making planets look real

- Sphere shading = `radialGradient` with the highlight offset to ~34%/30%
  (`cx="34%" cy="30%"`): light at `0%`, mid tone at ~45%, dark limb at `100%`.
- Natural palette (do not hand-pick "pretty" colors): Mars burnt red, Jupiter
  banded beige/orange, Saturn pale gold **with a ring**, Earth blue + green
  continents, Neptune deep blue, Venus pale yellow.
- Saturn's ring: a rotated `<ellipse fill="none">` with a wide stroke, drawn in
  two passes (one behind the disc, a thinner one in front) so the ring passes in
  front and behind the planet.
- Jupiter's bands: a few low-opacity `stroke` arcs across the disc.
- Galaxy: concentric dashed arcs for the spiral arms + a radial-gradient core +
  scattered small circles for dust, all inside one slowly spinning group.

## Iterating (this user dictates by voice)

- Change **one thing per pass** and re-preview. Use `patch` for targeted edits on
  the existing file: a full `write_file` rewrite of the same artifact is refused
  when the task has not read the current file, and a rewrite also risks dropping
  earlier tweaks.
- A fragmented or ambiguous request (a word dropped mid-sentence, a scene change
  described in one breath) must be confirmed with a single `clarify` before a
  large rework — guessing wrong means rebuilding the whole scene.
- Save a *major* revision under a new filename instead of overwriting, so the user
  can compare; keep the older file until they say the new one is better.
- Palette preference for this user's personal screens: deep blue, not gold/yellow.
- Fullscreen: the user wants a boot screen to fill the monitor — size with `vmin`
  and add a click-to-fullscreen affordance
  (`document.documentElement.requestFullscreen()`). **The button does nothing in
  the Hermes chat preview** — that pane is a sandboxed iframe and the Fullscreen
  API is blocked there, so the user clicks and sees no change. Do not re-patch the
  button when they report this; instead open the file in a real browser so they can
  test it: `powershell -NoProfile -Command "Start-Process '<abs path>'"`. Plain
  `start "" "<path>"` from the MSYS bash terminal silently fails to launch it —
  use `Start-Process`.

## Pitfalls

- Keep hex colors `#rrggbb`; shorthand and named colors are not guaranteed to
  parse on every surface.
- Set `transform-origin` explicitly in the SVG's coordinate units for orbit
  groups — the `50% 50%` default is wrong once a `viewBox` is in play.
- Animate only `transform` and `opacity`, never layout properties.
- A syntax error in the SVG silently blanks the whole scene — preview before
  telling the user it is done.
- Fullscreen and other Fullscreen-API / clipboard features are blocked in the chat
  preview iframe. When the deliverable depends on one, verify it in a real browser
  window (`Start-Process`), not in `::preview`, or you will report a broken feature
  as working.
