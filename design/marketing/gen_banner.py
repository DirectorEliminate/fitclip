"""Generates assets/banner.svg (animated, system font stack, real clip frames embedded as small JPEGs)
and design/marketing/banner.html (same SVG inlined, rendered to assets/banner.png with Space Grotesk).
Run from the repo root:  python design/marketing/gen_banner.py

Animation (8 s loop, CSS keyframes only, no scripts): the trim handles close in on 00:12-00:37,
the size counter steps down 57.2 -> 23.8 MB, then the compress step takes it to 19.2 MB and the
meter turns teal under the 20 MB Discord Free limit. At 96-100 % everything returns to the start state.
"""
import base64, io
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[2]
img = root / 'design/img'

SANS = "'Space Grotesk',Inter,'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
BG, PANEL, RAISE, LINE = '#0a0c0c', '#121515', '#1a1e1e', '#222727'
TEXT, TEXT2, TEXT3, ACC, INK, SOFT, OVER = '#eef3f2', '#93a09e', '#596563', '#2fd3bb', '#02201b', '#0f2a25', '#3a4241'


def b64jpeg(im, q=72):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


# --- embedded media: one frame (1000 px) + a 10-thumb strip (2x) ---
frame = Image.open(img / 'tw-frame.jpg').resize((1000, 562), Image.LANCZOS)
FRAME = b64jpeg(frame, 70)
VX, VY, VW, VH = 716, 16, 500, 320            # black player box
IH = VW * 9 / 16                               # letterboxed image height
IY = VY + (VH - IH) / 2
SX, SY, SW, SH = 716, 346, 500, 38             # trim strip
gap = 2
tw = (SW - gap * 9) / 10
strip = Image.new('RGB', (SW * 2, SH * 2), BG)
for i in range(10):
    t = Image.open(img / f'tw-t{i}.jpg')
    w, h = round(tw * 2), SH * 2
    t = t.resize((w, round(t.height * w / t.width)), Image.LANCZOS)
    top = (t.height - h) // 2
    strip.paste(t.crop((0, top, w, top + h)), (round(i * (tw + gap) * 2), 0))
STRIP = b64jpeg(strip, 68)

L, R = SX + SW * 0.20, SX + SW * 0.6167       # final selection 00:12-00:37 of 1:00
HW = 8                                         # handle width

# --- number states (value, start %, end %) ---
STATES = [('57.2', 0, 12), ('46.1', 12, 18), ('35.0', 18, 24), ('23.8', 24, 40), ('21.4', 40, 46), ('19.2', 46, 96)]


def win(a, b):
    """opacity keyframes: visible in [a, b) and, for the first state, again in [96, 100]"""
    if a == 0:
        return f'0%,{b - .1:.1f}%{{opacity:1}}{b}%,95.9%{{opacity:0}}96%,100%{{opacity:1}}'
    return f'0%,{a - .1:.1f}%{{opacity:0}}{a}%,{b - .1:.1f}%{{opacity:1}}{b}%,100%{{opacity:0}}'


css = [
    '.a{animation-duration:8s;animation-iteration-count:infinite;animation-timing-function:ease-in-out}',
    '.o{transform-box:view-box}',
    f'.hl{{animation-name:hl}}@keyframes hl{{0%,8%{{transform:translateX(0)}}28%,90%{{transform:translateX({L - SX:.1f}px)}}97%,100%{{transform:translateX(0)}}}}',
    f'.hr{{animation-name:hr}}@keyframes hr{{0%,8%{{transform:translateX(0)}}28%,90%{{transform:translateX({R - (SX + SW):.1f}px)}}97%,100%{{transform:translateX(0)}}}}',
    f'.ln{{transform-origin:{SX}px 0;animation-name:ln}}@keyframes ln{{0%,8%{{transform:translateX(0) scaleX(1)}}28%,90%{{transform:translateX({L - SX:.1f}px) scaleX({(R - L) / SW:.4f})}}97%,100%{{transform:translateX(0) scaleX(1)}}}}',
    f'.dl{{transform-origin:{SX}px 0;animation-name:dm}}.dr{{transform-origin:{SX + SW}px 0;animation-name:dm}}@keyframes dm{{0%,8%{{transform:scaleX(0)}}28%,90%{{transform:scaleX(1)}}97%,100%{{transform:scaleX(0)}}}}',
    f'.fill{{transform-origin:64px 0;animation-name:fl}}@keyframes fl{{0%,40%{{transform:scaleX(0)}}52%,90%{{transform:scaleX(1)}}97%,100%{{transform:scaleX(0)}}}}',
    '.over{animation-name:ov}@keyframes ov{0%,40%{opacity:1}46%,94%{opacity:0}97%,100%{opacity:1}}',
    '.fits{animation-name:fi;animation-timing-function:step-end}@keyframes fi{0%{opacity:0}46%{opacity:1}96%,100%{opacity:0}}',
    '.nofit{animation-name:nf;animation-timing-function:step-end}@keyframes nf{0%{opacity:1}46%{opacity:0}96%,100%{opacity:1}}',
    '.was{animation-name:wa}@keyframes wa{0%,10%{opacity:0}14%,92%{opacity:1}96%,100%{opacity:0}}',
]
nums = []
for i, (v, a, b) in enumerate(STATES):
    css.append(f'.n{i}{{animation-name:n{i};animation-timing-function:step-end}}@keyframes n{i}{{{win(a, b)}}}')
    nums.append(f'<text class="a n{i}" x="60" y="250" font-family="{SANS}" font-size="132" font-weight="700" letter-spacing="-6" fill="{TEXT}">{v}<tspan font-size="40" letter-spacing="-1" fill="{TEXT2}" dx="10">MB</tspan></text>')
CSS = '\n    '.join(css)
NUMS = '\n  '.join(nums)

MW = 520                                           # meter width
lim = 64 + MW * 20 / 22

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="400" viewBox="0 0 1280 400" role="img" aria-labelledby="t d">
  <title id="t">Fitclip — free Discord video compressor: 57.2 MB Twitch clip to 19.2 MB</title>
  <desc id="d">A 57.2 MB Twitch clip is trimmed to 25 seconds and compressed to 19.2 MB so it fits Discord's 20 MB free upload limit.</desc>
  <style>
    {CSS}
  </style>
  <rect width="1280" height="400" fill="{BG}"/>
  <g transform="translate(64 40)">
    <rect width="28" height="28" rx="8" fill="{ACC}"/>
    <path d="M10.5 8H8v2.5M17.5 8H20v2.5M10.5 20H8v-2.5M17.5 20H20v-2.5" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="104" y="61" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">Fitclip</text>
  <text x="196" y="61" font-family="{SANS}" font-size="16" fill="{TEXT3}">free Discord video compressor</text>

  <g class="a was"><text x="64" y="128" font-family="{SANS}" font-size="30" font-weight="600" fill="{TEXT3}">57.2 MB</text><rect x="64" y="117" width="118" height="2.5" fill="{TEXT3}"/></g>
  {NUMS}

  <rect x="64" y="282" width="{MW}" height="12" rx="6" fill="{RAISE}"/>
  <rect class="a over" x="64" y="282" width="{MW}" height="12" rx="6" fill="{OVER}"/>
  <rect class="a fill" x="64" y="282" width="{MW * 19.2 / 22:.1f}" height="12" rx="6" fill="{ACC}"/>
  <rect x="{lim - 1:.1f}" y="276" width="2" height="24" fill="{TEXT}"/>
  <g class="a fits">
    <rect x="64" y="318" width="182" height="30" rx="15" fill="{SOFT}"/>
    <path d="m80 333.5 4 4 7.5-8" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="100" y="338.5" font-family="{SANS}" font-size="14" font-weight="600" fill="{ACC}">Fits Discord Free</text>
  </g>
  <g class="a nofit">
    <rect x="64" y="318" width="206" height="30" rx="15" fill="{RAISE}"/>
    <text x="80" y="338.5" font-family="{SANS}" font-size="14" font-weight="600" fill="{TEXT2}">Over the 20 MB free limit</text>
  </g>
  <text x="{64 + MW}" y="338.5" text-anchor="end" font-family="{SANS}" font-size="14" fill="{TEXT2}"><tspan font-weight="600" fill="{TEXT}">20 MB</tspan> limit</text>

  <rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" rx="18" fill="#000"/>
  <image x="{VX}" y="{IY:.1f}" width="{VW}" height="{IH:.1f}" href="{FRAME}" preserveAspectRatio="xMidYMid meet"/>
  <rect x="{VX + 12}" y="{VY + 10}" width="246" height="26" rx="8" fill="{BG}" fill-opacity=".86"/>
  <text x="{VX + 22}" y="{VY + 27.5}" font-family="{SANS}" font-size="12" fill="{TEXT2}"><tspan font-weight="600" fill="{TEXT}">ropz-ace.mp4</tspan> · Twitch clip · 1080p60</text>

  <clipPath id="sc"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="9"/></clipPath>
  <g clip-path="url(#sc)">
    <image x="{SX}" y="{SY}" width="{SW}" height="{SH}" href="{STRIP}"/>
    <rect class="a dl" x="{SX}" y="{SY}" width="{L - SX:.1f}" height="{SH}" fill="{BG}" fill-opacity=".74"/>
    <rect class="a dr" x="{R:.1f}" y="{SY}" width="{SX + SW - R:.1f}" height="{SH}" fill="{BG}" fill-opacity=".74"/>
  </g>
  <rect class="a ln" x="{SX}" y="{SY}" width="{SW}" height="2.5" fill="{ACC}"/>
  <rect class="a ln" x="{SX}" y="{SY + SH - 2.5}" width="{SW}" height="2.5" fill="{ACC}"/>
  <rect class="a hl" x="{SX}" y="{SY}" width="{HW}" height="{SH}" rx="3" fill="{ACC}"/>
  <rect class="a hr" x="{SX + SW - HW}" y="{SY}" width="{HW}" height="{SH}" rx="3" fill="{ACC}"/>
</svg>
'''
(root / 'assets/banner.svg').write_text(svg, encoding='utf-8')
html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Fitclip — banner (PNG source, generated by gen_banner.py)</title>
<link rel="stylesheet" href="../fitclip.css">
<style>html,body{{width:1280px;height:400px;background:{BG}}} svg{{display:block}}</style>
</head>
<body>
{svg}</body>
</html>
'''
(root / 'design/marketing/banner.html').write_text(html, encoding='utf-8')
print(f'wrote assets/banner.svg ({len(svg) / 1024:.0f} KB) and design/marketing/banner.html')
