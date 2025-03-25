# File Renaming Tool

A modern, user-friendly tool for batch renaming files with customizable numbering, prefixes, and suffixes.

## Features

- **Batch Renaming**: Process multiple files at once
- **Smart Numbering**: Automatically detect and sort files by existing numbers
- **Customizable Format**: Set the number of digits for consistent file naming
- **Optional Prefixes/Suffixes**: Add text before or after the numbering
- **Folder Support**: Select entire folders for batch processing
- **Undo Functionality**: Easily revert changes if needed
- **Modern UI**: Clean, intuitive interface with dark mode
- **Progress Tracking**: Visual feedback during renaming operations

## Installation

1. Download the latest release from the [Releases](https://github.com/guptaaman777/rename-tool/releases) page
2. No installation required - simply run the `Rename Tool.exe` file

## Usage

1. **Select Files**: Choose individual files or an entire folder to rename
2. **Configure Format**: 
   - Set the number of digits (e.g., 3 for 001, 002, etc.)
   - Optionally enable and set a prefix (e.g., "Photo_")
   - Optionally enable and set a suffix (e.g., "_edited")
3. **Process**: Click "Process Rename" to start the operation
4. **Undo**: If needed, click "Undo" to revert all changes

## Examples

Input files:
- image1.jpg
- image2.jpg
- image10.jpg

With settings:
- Digits: 3
- Prefix: "Vacation_"
- Suffix: "_2023"

Result:
- Vacation_001_2023.jpg
- Vacation_002_2023.jpg
- Vacation_003_2023.jpg

## System Requirements

- Windows 10 or later
- No additional dependencies required

## Development

Built with:
- Python 3.9+
- PyQt6 for the modern UI
- Regular expressions for smart file numbering

## License

[MIT License](LICENSE)

## Support

If you encounter any issues or have suggestions for improvements, please [open an issue](https://github.com/guptaaman777/rename-tool/issues) on GitHub.
