# Lifting a logo out of a photo into the HUD

He supplies a product-label photo (e.g. a «М&Ф» monogram + crown) and wants it
centred in the orb. Do NOT retype it in a font — crop the pixels.

## 1. Find the photo and measure it

```powershell
Add-Type -AssemblyName System.Drawing
$img=[System.Drawing.Image]::FromFile('C:\Users\Пользователь\Desktop\photo_....jpg')
"$($img.Width) x $($img.Height)"; $img.Dispose()
```

## 2. Crop the logo region and knock out the background (PIL)

The label sits on a light parchment/white field. Threshold on brightness AND
saturation so only the light, near-neutral background becomes transparent
(gold and reds survive):

```python
from PIL import Image
src = Image.open('photo_....jpg').convert('RGBA')
crop = src.crop((x1, y1, x2, y2))          # tighten by inspecting the crop
px = crop.load(); w, h = crop.size
out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); opx = out.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        brightness = (r + g + b) / 3
        sat = max(r, g, b) - min(r, g, b)
        if brightness > 205 and sat < 45:   # light + neutral -> transparent
            opx[x, y] = (0, 0, 0, 0)
        else:
            opx[x, y] = (r, g, b, 255)
out.save('logo_mif.png')
```

Always re-inspect the cropped/knocked-out PNG with `vision_analyze` before
using it — confirm the logo is whole and the field is gone.

## 3. Place it in the orb (SVG)

```html
<image class="core-logo" x="160" y="150" width="180" height="174"
       href="logo_mif.png" xlink:href="logo_mif.png"
       preserveAspectRatio="xMidYMid meet"/>
```

Put the `<image>` inside the `.core` group so it scales/pulses with the orb.
Give it a soft gold glow (`filter:drop-shadow(...)`) to seat it in the navy.
Keep the PNG beside the HTML in the `Для Джарвиса` folder — a `file://` page
loads a relative `href` fine, but not one behind a path the browser can't reach.
