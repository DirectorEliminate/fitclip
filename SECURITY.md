# Security policy

## Supported versions
Only the latest release of Fitclip receives security fixes. The app checks for updates once a day (you can turn this off in Settings).

## Reporting a vulnerability
Please **do not** open a public issue. Report privately through
[GitHub Security Advisories](https://github.com/DirectorEliminate/fitclip/security/advisories/new).
Include the version, OS, steps to reproduce and, if possible, a sample file or link that triggers the problem.
We aim to reply within 72 hours and to ship a fix for confirmed issues within 14 days.

## Scope
Fitclip opens untrusted media files and downloads from links you paste, so these areas matter most:
- Crafted video files that crash or exploit the bundled FFmpeg build.
- Links or site responses that make the bundled yt-dlp write outside the downloads folder or run commands.
- The updater: anything that could install an unsigned or tampered build.
- The Explorer "Fit for Discord" menu entry and file associations.

Vulnerabilities in FFmpeg or yt-dlp themselves should also be reported upstream; we update the bundled versions as soon as fixes are released.

## What Fitclip does not do
It does not upload your videos, has no account system and sends no telemetry. The only automatic network request is the update check for the app and yt-dlp.
