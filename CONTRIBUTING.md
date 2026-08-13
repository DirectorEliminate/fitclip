# Contributing to Fitclip

Thanks for helping make Fitclip, the free Discord video compressor, better. Bug reports, presets, translations, docs and code are all welcome.

## Before you start
- Search [issues](https://github.com/DirectorEliminate/fitclip/issues) and [Discussions](https://github.com/DirectorEliminate/fitclip/discussions) first.
- For anything bigger than a small fix, open an issue so we can agree on the approach before you write code.

## Reporting a bug
Use the **Bug report** template. The most useful things to include:
- Fitclip version and OS.
- The source file's details. *Settings → Copy diagnostics* includes resolution, fps, codec, length and size, but no file names or paths unless you add them.
- The target you picked and the size you got. "Aimed at 20 MB, got 20.4 MB" is a real bug and we want those.
- For link imports: the site (Twitch, Medal, YouTube…) and whether the same link works with plain `yt-dlp` on your machine.

## Development setup
```bash
git clone https://github.com/DirectorEliminate/fitclip
cd fitclip
# app source lives in /app (Tauri 2 + Rust + TypeScript)
npm install
npm run fetch-tools   # downloads FFmpeg and yt-dlp into app/src-tauri/bin/ (not committed)
npm run tauri dev
```

## What a good pull request looks like
- One topic per PR, with a short description and a linked issue.
- Size planning changes come with numbers: source details, target, result size, and the plan Fitclip printed. Never ship a change that makes files overshoot the target.
- No new network requests without discussion. Fitclip is offline-first: the only automatic request is the update check.
- UI changes follow `design notes` (Space Grotesk, one flat accent `#2fd3bb`, flat fills only, no blurred shadows, no emoji in the UI). Re-render the screenshots with `python design/render.py .`
- Update `CHANGELOG.md` under **Unreleased**.

## Translations
UI strings are in `app/src/i18n/<lang>.json`. Copy `en.json`, translate it and open a PR. Keep Discord, Nitro, Twitch and other names as they are.

## Code of conduct
Be kind, assume good intent, keep discussions about the work. Harassment of any kind is not tolerated.

By contributing you agree that your contribution is licensed under the MIT License.
