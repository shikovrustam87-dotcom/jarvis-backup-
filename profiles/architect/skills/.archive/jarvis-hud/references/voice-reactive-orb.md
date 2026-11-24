# Voice-reactive orb (Web Audio API)

How to make the Jarvis orb's size follow live speech instead of a CSS timer.
This is the technique that made him say "тембр работает, всё идеально" after
several failed attempts where the orb only emitted a fixed pulse.

## Why the naive version fails

A CSS `@keyframes` animation on `.core` (e.g. `coreListen { 50% { transform:
scale(1.10) } }`) sets the transform every frame. Setting
`core.style.transform` from JS does **nothing** — the animation wins, the orb
pulses at a fixed period, and the voice has no effect. The user describes this
as "он просто волны пускает" / "под темпер не реагирует".

**First step is always: remove every `animation` on `.core` and its state
classes.** Leave `.core { transform-origin:250px 250px; will-change:transform }`
and drive it purely from JS.

## Mic capture

`getUserMedia` works under `file://` once the browser permission is granted.
Browsers need a user gesture, so attach a one-shot click listener *and* try
immediately (the permission may already be stored).

```js
var micActive=false, audioCtx, analyser, micData, smooth=0;

function startMic(){
  if (micActive) return;
  var st = document.getElementById('micState');      // on-screen badge
  if (st) st.textContent = 'запрос...';
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
    if (st) st.textContent = 'НЕТ API'; return;
  }
  navigator.mediaDevices.getUserMedia({ audio:true })
    .then(function(stream){
      audioCtx = new (window.AudioContext||window.webkitAudioContext)();
      var src = audioCtx.createMediaStreamSource(stream);
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 512;
      analyser.smoothingTimeConstant = 0.72;
      src.connect(analyser);
      micData = new Uint8Array(analyser.frequencyBinCount);
      micActive = true;
      if (st) st.textContent = 'МИК ЕСТЬ';
      requestAnimationFrame(micLoop);
    })
    .catch(function(e){ if (st) st.textContent = 'ОТКАЗ: ' + (e.name||'?'); });
}
document.addEventListener('click', function once(){ startMic();
  document.removeEventListener('click', once); });
startMic();
```

## Per-frame loop: loudness → scale

Average the frequency bins, normalise, then smooth with a fast attack and slow
release — that is what reads as "breathing in the rhythm of speech" rather than
jitter.

```js
function micLoop(){
  if (!micActive) return;
  analyser.getByteFrequencyData(micData);
  var sum=0; for (var i=0;i<micData.length;i++) sum+=micData[i];
  var norm = Math.min((sum/micData.length)/45, 1);   // /45 = sensitive

  if (norm > smooth) smooth += (norm-smooth)*0.55;   // fast up
  else               smooth += (norm-smooth)*0.12;   // slow down

  var core = document.querySelector('.core');
  var jarvisTalking = Date.now() < speakUntil;       // see below
  var k = jarvisTalking ? 1 - smooth*0.20            // Jarvis → INWARD
                        : 1 + smooth*0.28;           // Rustam → OUTWARD
  if (core) core.style.transform = 'scale(' + k.toFixed(4) + ')';
  requestAnimationFrame(micLoop);
}
```

Tuning knobs: the `/45` divisor sets sensitivity (lower = reacts to quieter
speech); the `0.28` / `0.20` amplitudes set how far it grows/shrinks; the
`0.55` / `0.12` weights set attack/release speed.

## Making Jarvis's own voice drive the inward pulse

The HUD cannot hear the agent's TTS directly. Expose a hook and call it when
the agent speaks:

```js
var speakUntil = 0;
window.jarvisSpeak = function(ms){ speakUntil = Date.now() + (ms||2500); };
```

From the console (or a driving script): `jarvisSpeak(3000)` makes the orb
contract inward for 3 seconds.

## Wave / spike / ripple generators (the visual layer)

He wanted, in order of iteration, and each is a small function:

- **Spikes** — a radial picket fence: `N=64` `<line>` elements from radius
  `baseR` outward, `x2/y2` recomputed each frame from `smooth`, each spike given
  a per-index `jitter` so the fence looks alive, not mechanical.
- **Ripples** — 3 `<ellipse>` rings (squashed, `ry ≈ rx*0.28`) with a `go` class
  that runs a `scale(.55 → 1.9)` + fade-out keyframe; fire one on a *burst*
  (`norm - prevNorm > 0.16`, rate-limited to ~260ms).
- **Pulse line** — a closed `<path>` built by walking `steps` points around a
  circle and perturbing the radius on a `i % 12` pattern (sharp peak, small
  rebound) to fake an ECG trace. Keep amplitude small (≈4px) — he asked for
  "маленькие красивые", and rejected the large white expanding rings outright.

**Do not** ship big bright expanding rings — he explicitly rejected them
("убери этот белый круг"). Waves must be dark-navy, in the orb's palette,
small, and tied to speech bursts.
