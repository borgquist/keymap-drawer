# Keymap Converter

This tool converts a ZMK keymap file to YAML and SVG formats using the `keymap-drawer` package.

## Setup

1. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the required packages:
```bash
pip install keymap-drawer
```

## Usage

Run the conversion script:
```bash
./convert_keymap.py
```

This will:
1. Parse the `adv360.keymap` file to create `adv360.yaml`
2. Generate `adv360.svg` from the YAML file

## Key Renaming

The tool uses `keymap_config.yaml` to map ZMK key codes to human-readable labels. For example:
- `&kp LCTRL` becomes `Ctrl`
- `&kp LEFT_COMMAND` becomes `Cmd`
- Modifier combinations are converted to symbols like `⌃⌥⌘1`

You can customize these mappings by editing the `raw_binding_map` section in `keymap_config.yaml`.

## Requirements

- Python 3.8+
- Virtual environment
- keymap-drawer package

## Customization

You can customize the script in several ways:

- **Different keymap file**: Edit the `keymap_file` variable in `convert_keymap.py`
- **Key labels**: Modify the `raw_binding_map` section in `keymap_config.yaml`
- **SVG appearance**: Change colors, sizes, and styles in the `draw_config` section of `keymap_config.yaml`
