# Fitclip — design spec

**Direction:** a calm media utility built around one number. The video is the hero on the left (real frame, letterboxed in black), the result size is the hero on the right (giant figure, struck-through source above it, a meter against the limit). One font, one teal accent, flat dark surfaces, no decoration.

Approved reference: `_redesign/v2/fitclip.html` (+ `.png`), 1240×780. This repo adapts it 1:1 to a 1280×800 window; the other five screens reuse the same tokens and components.

## Palette

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#0a0c0c` | window and page background |
| `--panel` | `#121515` | link field, segmented controls, cards |
| `--raise` | `#1a1e1e` | selected segment, meter track, chips, ghost buttons |
| `--line` | `#222727` | hairlines, card borders |
| `--line-2` | `#2c3333` | toggle and keycap borders, dashed drop zone, inactive waveform bars |
| `--text` | `#eef3f2` | primary text, big numbers, limit tick |
| `--text-2` | `#93a09e` | secondary text |
| `--text-3` | `#596563` | labels, struck-through source size |
| `--acc` | `#2fd3bb` | **the only accent**: Compress button, trim handles, meter fill when it fits, active segment label, progress, "Fits" chip text |
| `--acc-ink` | `#02201b` | text and icons on the accent |
| `--acc-soft` | `#0f2a25` | "Fits Discord Free" chip background |
| `--over` | `#3a4241` | meter fill while a file is over the limit (neutral grey, deliberately not a second color) |

Rules: flat fills only (no color blends), no glow, no blurred shadows. Surfaces are separated by a step in lightness or a 1px hairline. Overlays on video use flat `rgba(10,12,12,.86)`. Discord's and Twitch's brand colors are never used.

## Type

**Space Grotesk** 400/500/600/700 only (Google Fonts). Numbers use `font-variant-numeric: tabular-nums` so counters don't jitter.

| Role | Size / weight | Notes |
|---|---|---|
| Result size | 116 / 700, −0.05em, line-height .9 | unit "MB" 34 / 700 in `--text-2` |
| Source size (struck) | 30 / 600, `--text-3`, 2px line-through | |
| Screen title | 26 / 700, −0.02em | |
| Body | 14 / 400 | 13.5 for row titles, 12–12.5 for meta |
| Labels | 12 / 500, uppercase, +0.06em, `--text-3` | |
| Button | 16 / 700 + 13.5 / 500 suffix at 70% | |

## Layout and radii

- Window 1280×800, frameless, Windows 11 controls on the right (46×40 hit areas). Top bar 60px: brand, link field (640px max), icon nav (Trim, Queue with count, Output, Settings), window controls.
- Content padding 8 / 26 / 26. Compress and Import: `740px | 1fr` with a 34px gap. Trim: `1fr | 380px`, the timeline card under the player. Queue and Output: `1fr | ~390px` side panel. Settings: `1fr | 470px` history card.
- Radii: player 20, buttons 16, cards 16–18, link field and segmented controls 12–14, segments 10, thumbs 6–8, pills 999.

## Screens (`design/app.html#screen=<id>`)

| id | Screen | Purpose |
|---|---|---|
| `compress` | Compress (main, approved) | Player with the real frame letterboxed, trim strip of real thumbnails with teal handles, "Fits Discord Free" chip, struck source size, giant result size, meter vs the limit, plan selector (20 MB Free / 50 MB Basic / 500 MB Nitro / Custom), output spec, recent list, Compress button |
| `trim` | Precise cut | Frame-accurate In/Out fields with ±1 frame, exact vs keyframe cut, scene snap, audio fade, keyboard keys; zoomed timeline with thumbnails, the clip's real audio waveform, labelled handles and playhead |
| `batch` | Queue | Table of clips (thumb, name, length, size before → after, status with progress), dashed drop zone; side panel with total before/after, one target for all, after-done action, skip-if-fits, output folder, Pause |
| `import` | Link import | Clip frame dimmed behind a big percentage and progress bar, four-step strip (read link, pick format, download, open), supported sources list, download quality, yt-dlp auto-update |
| `output` | Output settings | Codec cards (H.264 / H.265 / AV1), encoder, resolution cap, frame rate, audio, safety margin, container, extras; right card shows the bitrate plan for the current clip and the bits-per-pixel ladder |
| `settings` | Settings and history | Clipboard copy, output folder, file name pattern, keep original, default target, language, Explorer menu, update check, credits; history card grouped by day with copy/show actions |

Demos for GIFs: `#screen=compress&demo=compress`, `#screen=import&demo=import`, `#screen=batch&demo=batch` (`window.__seek(t, dur)`, 6 s loops).

## Components

- **Link field** — states: empty placeholder + "Open file"; typing (teal caret) + "Fetch" on accent; downloading (2px teal progress line along the bottom) + "Downloading"; done + "Downloaded".
- **Player** — black box, `object-fit: contain`; chips top-left/top-right; play pill bottom-left; credit line bottom-right.
- **Trim strip** — 10 thumbnails, 3px gaps, 74% dark veil outside the selection, selection border 2.5px teal with 11px side handles, 3px white playhead.
- **Meter** — 12px track, fill teal when it fits and `--over` grey when it doesn't, 2px white tick at the limit, scale = limit × 1.1.
- **Segmented control** — panel with 5px padding; selected segment = `--raise` + teal label.
- **Pills** — "Fits Discord Free" (`--acc-soft` + teal), neutral (`--raise` + grey) for "x MB over".
- **Toggle** — 38×22; on = teal track with dark knob.
- **Rows** — 1px hairline separators; thumb + name + meta + teal size on the right.
- **Primary button** — 58px, teal; while compressing, a dark 28% shade covers the remaining part and the label shows "pass n of 2 · %".

## Motion

- Size counter: values interpolate with tabular numerals; the struck source appears once trimming starts.
- Trim: handles ease (cubic in-out) 1.6 s; dims and readout follow.
- Compress: shade recedes left to right over 1.4 s, chip flips from "x MB over" to "Fits Discord Free" when the number crosses the limit, button ends on "Copied to clipboard".
- GIF loops are seamless: compress rewinds the handles at the end, batch and import fade their changing parts to the t=0 state.
- The video in the compress GIF plays at 6 fps (real frames from the clip) to keep the GIF under 4 MB; UI animates at 12 fps.

## Assets and rendering

- `python design/render.py .` renders everything in `design/render.json` (6 screenshots at 2x, 3 GIFs at 960px/12 fps, banner PNG, social preview). This copy of `render.py` adds a `dither` option for GIF jobs (`bayer:bayer_scale=5`).
- `python design/marketing/gen_banner.py` writes `assets/banner.svg` (CSS keyframes only, system font stack, clip frame and thumbnail strip embedded as small JPEG data URIs) and `design/marketing/banner.html` (same SVG with Space Grotesk, used for `assets/banner.png`).
- Real media in `design/img/`: `tw-frame.jpg` (1920×1080 frame at 0:21), `tw-t0…t9.jpg` (strip thumbs every 6 s from 0:03), `tw-z00…z19.jpg` (zoomed timeline thumbs every 1.5 s from 0:10), `seq/f01…f72.jpg` (0:19.5–0:25.5 at 12 fps, 800px, for the compress GIF). The trim waveform is the clip's real audio RMS (180 bins over 0:10–0:40), inlined as `WAVE` in `app.html`.

ffmpeg commands used (source: `_redesign/media/twitch/ropz-ace.mp4`):
```bash
ffmpeg -ss 21 -i ropz-ace.mp4 -frames:v 1 -q:v 3 design/img/tw-frame.jpg
ffmpeg -ss $t -i ropz-ace.mp4 -frames:v 1 -vf scale=320:-1 -q:v 4 design/img/tw-t$i.jpg     # t = 3 + 6i
ffmpeg -ss $t -i ropz-ace.mp4 -frames:v 1 -vf scale=192:-1 -q:v 5 design/img/tw-z$n.jpg     # t = 10 + 1.5n
ffmpeg -ss 19.5 -t 6 -i ropz-ace.mp4 -vf "fps=12,scale=800:-1" -q:v 5 design/img/seq/f%02d.jpg
ffmpeg -i ropz-ace.mp4 -ac 1 -ar 8000 -f s16le -   # → RMS per bin for the waveform
```

## Image sources

| Asset | Source | Rights | Action |
|---|---|---|---|
| Every video frame, thumbnail, waveform and GIF frame in `design/img/`, `assets/screenshots/`, `assets/gifs/`, `assets/banner.svg`, `assets/banner.png`, `assets/social-preview.png` | Twitch clip "ropz - ACE (with 1vs4 clutch)", channel **PGL_CS2**, https://clips.twitch.tv/ToughBigHabaneroHeyGuys-rPoOnphVkaMCW8lp (1080p60, 60 s, 57.2 MB), local copy `_redesign/media/twitch/ropz-ace.mp4` | The footage is a PGL CS2 Major broadcast. It belongs to **PGL** (broadcast and overlay), shows the **players and teams** (ropz, FaZe Clan, FURIA and others, including their likeness and the in-broadcast player cams), sponsor marks visible in the overlay (e.g. ZOWIE), and **Valve**'s Counter-Strike 2. No license was obtained; it is used only to mock up the UI. | **Replace before publishing** with your own clip or one used with written permission from the rights holders, then re-run the ffmpeg commands above, `gen_banner.py` and `render.py`. Keep the file names so nothing else changes. |
| `assets/logo.svg`, UI icons | Drawn for this repo | MIT, part of the repo | — |
| Space Grotesk | Google Fonts (Florian Karsten) | SIL Open Font License 1.1 | — |

Also replace the clip-specific text (file names such as `ropz-ace.mp4`, "PGL_CS2 · ropz — ACE with 1vs4 clutch", the clip URL in the link field, the README "Before/After" table and the disclaimer sentence about the PGL clip) when you swap the footage.

## Verify before publishing

1. **Discord limits.** Free 20 MB (raised from 10 MB on 13 Aug 2026 per Discord's announcement as reported by press; some Discord help pages still showed 10 MB), Nitro Basic 50 MB, Nitro 500 MB (one third-party source mentioned 1 GB for Nitro — not confirmed), Boost Level 2 = 50 MB and Level 3 = 100 MB per Discord's Server Boosting page. Re-check https://support.discord.com the week you launch.
2. **MB definition.** Fitclip treats Discord's "20 MB" as 20 × 1,048,576 bytes with a 3% margin. Confirm whether Discord counts MB as MiB or 10⁶ bytes; if it is 10⁶, 20,342,374 bytes would be over 20,000,000 and the default margin must be raised to about 5%, or the base changed.
3. **Limit history** in the FAQ: 8 MB → 25 MB (2023) → 10 MB (Sept 2024) → 20 MB (Aug 2026).
4. **Inline playback** of H.265 and AV1 in Discord varies by client; the copy only says "varies", keep it that way unless tested.
5. **yt-dlp extractors**: Twitch clips/VODs/highlights, Medal, YouTube/Shorts, Streamable, Reddit, X, Kick — confirm each in yt-dlp's `supportedsites.md` for the bundled version.
6. **Steam game recording export** as a source (README/README.es "Game recordings" row) — confirm the export format is a normal MP4.
7. **0.07 bits-per-pixel threshold** and the "about 5 minutes at 360p fits 20 MB" estimate are design heuristics; tune them with real encodes before quoting them as results.
8. **Example result 19.2 MB** for the 25 s trim is a planned value (target 19.4 MB, two-pass usually lands 0.5–2% under). Run the real encode on your replacement clip and update the numbers everywhere.
9. **FFmpeg licensing**: shipping x264/x265 makes the bundled FFmpeg GPL; publish its source and build config with each release.
10. **Package IDs** (`Fitclip.Fitclip` on winget, `fitclip` on Scoop/Homebrew, `io.github.DirectorEliminate.Fitclip` on Flathub) do not exist until you submit them.
11. **Comparison table**: online compressor watermarks and size caps vary by service and change often; the table is generic on purpose. HandBrake "average bitrate only" (no target-size field) — confirm for the current HandBrake version.
