# Pladria v2.5 - Build Guide

## How to Build

### 🚀 **Quick Build (Recommended)**
Double-click: `BUILD_FROM_EXPLORER.bat`

### 🔧 **Alternative Methods**
- Double-click: `BUILD_QUICK.bat`
- Command line: `cd Package && python build_pladria_improved.py`

## Output

The built application will be in:
```
dist/Pladria_v2.5_Portable/
├── Pladria.exe              # Main executable
├── _internal/               # Dependencies
├── README.txt              # User guide
└── Launch_Pladria.bat      # Launcher
```

## Requirements
- Python 3.8+
- All dependencies installed automatically

## Build Modes
- **Unpacked** (default): Fast startup
- **Onefile**: Single executable (change `BUILD_MODE` in script)
