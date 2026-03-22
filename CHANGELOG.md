# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## \[0.1.0\] - 2026-03-22

### Added

- New Light theme version of the `patinhooh-theme`.
- Added scripts to patch the dark theme into the light theme with a palette file, allowing for easier updates and maintenance of the theme colors.
- Set unnecessary code border color, so unreachable code is more visible on light themes.
- TOML syntax highlighting.
- Added languages that look good to the language list in the README.

### Changed

- Changed cursor color to the main theme color
- Changed bracket highlight colors to be the same as the default foreground color.
- Adjust terminal white color.

### Removed

- "editorWatermark.foreground" color as it is not used in the current version of VS Code.

## \[0.0.2\] - 2025-07-05

### Changed

- Updated Markdown: reduced text color variation for improved consistency.
- Updated Markdown: adjusted symbol colors to better match the theme used in other languages.

### Fixed

- Python: Corrected color of decorator symbol
- Markdown: Fixed bold syntax rendering both bold and italic instead of just bold

## \[0.0.1\] - 2025-07-04

### Added

- Initial creation of the `patinhooh-theme`.
