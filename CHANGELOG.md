# Changelog

All notable changes to Fitclip are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-11-27

### Added
- Compress screen: source size, predicted result size and a meter against the upload limit.
- Discord presets: 20 MB Free, 50 MB Nitro Basic, 500 MB Nitro, plus Custom (any size, e.g. 10 MB, or 100 MB for Boost Level 3 servers).
- Two-pass bitrate planning from target size and clip length, with a 3% safety margin (1–8% configurable).
- Automatic resolution and frame rate: the largest of 1080p / 900p / 720p that keeps at least 0.07 bits per pixel, a 30 fps fallback, then 540p / 480p / 360p.
- Trim strip with real thumbnails and teal handles; Precise cut screen with frame stepping, exact or keyframe cut, audio fades and waveform.
- Link import through bundled yt-dlp: Twitch clips, highlights and VODs, Medal, YouTube and Shorts, and other public sites yt-dlp supports.
- Copy the finished file to the clipboard for pasting into Discord.
- Batch queue with drag and drop of files and folders, two jobs at a time, skips clips that already fit.
- Output settings: H.264 / H.265 / AV1; Auto / CPU x264 / NVENC / Quick Sync / AMF (VideoToolbox on macOS); resolution cap, frame rate, AAC bitrate, container, loudness normalization, fast start.
- Settings and history: output folder, file name pattern, "Fit for Discord" Explorer menu entry, update checks, English and Spanish UI.
- Windows installer and portable zip, macOS universal DMG, Linux AppImage and .deb.

[Unreleased]: https://github.com/DirectorEliminate/fitclip/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/DirectorEliminate/fitclip/releases/tag/v1.0.0
