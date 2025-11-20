# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based tool for parsing and visualizing keyboard keymaps, primarily for ZMK (Zephyr-based Mechanical Keyboard) firmware. The project:
- Parses keymap files (ZMK `.keymap`, QMK JSON, Kanata `.cfg`) into a normalized YAML format
- Generates SVG visualizations of keyboard layouts with layers and combos
- Supports custom physical layouts and extensive visual customization

## Development Commands

### Environment Setup
```bash
# One-time setup: Create venv and install package
python3 -m venv venv
source venv/bin/activate
pip install -e .

# After setup, just activate the venv when needed
source venv/bin/activate
```

**Important**: The `generate-keymap.sh` script attempts to auto-install dependencies but may encounter issues:

**Known Issues**:
1. **Name Conflict**: If you see `ValueError: Both keymap_drawer and keymap_drawer.py exist`, the custom `keymap_drawer.py` script conflicts with the package directory. Rename it to `generate_keymap_internal.py` or similar.

2. **tree-sitter Compatibility**: If you encounter `AttributeError: 'tree_sitter.Query' object has no attribute 'captures'`, there's a version incompatibility. The development version may not work with the latest tree-sitter. In this case:
   ```bash
   # Install from PyPI instead of -e .
   pip install keymap-drawer
   ```

3. **Venv Path Issues**: If the venv was created in a different location or moved:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .  # or pip install keymap-drawer if tree-sitter issues occur
   ```

### Running the Tool
The main CLI is accessed via the `keymap` command:

```bash
# Parse a ZMK keymap to YAML
keymap parse -z <keymap.keymap> -o <output.yaml>

# Generate SVG from YAML
keymap draw <keymap.yaml> -o <output.svg>

# Dump default configuration
keymap dump-config -o config.yaml
```

### Testing and Linting
```bash
# Type checking
mypy keymap_drawer

# Linting
pylint keymap_drawer

# Code formatting
black keymap_drawer
isort keymap_drawer

# Check for unused dependencies
deptry .
```

### Project-Specific Scripts

The repository contains custom scripts for the maintainer's personal keyboard:

```bash
# Generate keymap visualization (copies from external ZMK config)
./generate-keymap.sh

# Standalone converter script
./convert_keymap.py

# Add shifted labels to keys in SVG
./add_shifted_labels.py

# Apply custom colorization
./colorize_keymap.py
```

## Code Architecture

### Core Modules

**`keymap_drawer/`** - Main package

**`parse/`** - Keymap parsing subsystem
- `parse.py` - Base parser class with common functionality
- `zmk.py` - ZMK-specific parser using tree-sitter for devicetree parsing
- `qmk.py` - QMK JSON keymap parser
- `kanata.py` - Kanata configuration parser (experimental)
- Each parser converts its native format → normalized `KeymapData` structure

**`draw/`** - SVG generation subsystem
- `draw.py` - Main `KeymapDrawer` class that orchestrates SVG generation
- `combo.py` - Combo visualization (draws connections from combo boxes to key positions)
- `glyph.py` - SVG glyph fetching and caching (Material Design icons, Tabler icons, etc.)
- `utils.py` - Drawing utilities for shapes, text, and positioning

**Core Components**
- `keymap.py` - `KeymapData` and `LayoutKey` Pydantic models representing the normalized keymap structure
- `physical_layout.py` - Physical layout specifications (QMK info.json, ZMK DTS, ortholinear layouts)
- `dts.py` - Devicetree (.dts) format parser for ZMK physical layouts
- `config.py` - `Config`, `ParseConfig`, and `DrawConfig` Pydantic models with defaults
- `__main__.py` - CLI argument parsing and command dispatching

### Data Flow

```
Input Format → Parser → KeymapData (YAML) → Drawer → SVG Output
     ↓                      ↓                    ↓
  .keymap              Normalized           Visual
  .json                 Structure          Rendering
  .cfg
```

### Key Abstractions

**Physical Layout** - Describes key positions and dimensions
- Can be specified via QMK keyboard name, QMK info.json, ZMK DTS file, or parametrized ortholinear layout
- The `physical_layout.py` module handles all variants and normalizes them

**KeymapData** - Normalized representation
- Layers: `dict[str, list[LayoutKey]]` - each layer has a list of keys
- Combos: `list[ComboSpec]` - key combinations that trigger additional functionality
- Layout: Physical layout specification
- Config: Optional embedded draw configuration

**LayoutKey** - Individual key representation (Pydantic model)
- `t` (tap): Primary legend shown in center
- `h` (hold): Hold function shown at bottom
- `s` (shifted): Shifted character shown at top
- `type`: Visual styling (e.g., "held", "ghost", "trans")
- Position determined by layer index

### Configuration System

Configuration is hierarchical with multiple sources:
1. Default values in `config.py`
2. User config file (`-c/--config`)
3. Embedded `draw_config` in YAML keymap
4. CLI arguments (highest priority)

**Parse Config** (`parse_config`) - Controls keymap parsing
- `raw_binding_map`: Direct string mappings for custom key labels
- `zmk_keycode_map`, `qmk_keycode_map`: Keycode transformations
- `modifier_fn_map`: How modifier combinations are displayed
- `trans_legend`: How transparent keys are shown

**Draw Config** (`draw_config`) - Controls SVG generation
- Dimensions: `key_w`, `key_h`, `split_gap`, `combo_w`, `combo_h`
- Styling: `svg_style`, `svg_style_dark`, `svg_extra_style`
- Layout: `n_columns`, `separate_combo_diagrams`
- Visual effects: `draw_key_sides`, `glyph_*_size`, `shrink_wide_legends`

## Important Patterns

### Parser Implementation
When adding support for new keymap formats:
1. Subclass `KeymapParser` from `parse/parse.py`
2. Implement `_parse_keymap()` to extract layer structure
3. Use `_maybe_translate()` to apply keycode mappings
4. Call `_postprocess_layers()` for layer activator detection
5. Return `KeymapData` object

### Drawing Customization
The SVG styling is controlled by CSS in `DrawConfig`:
- `svg_style` - Base styles (not recommended to modify)
- `svg_extra_style` - User overrides (preferred method)
- Classes: `.key`, `.combo`, `.held`, `.ghost`, `.trans`, `.layer-activator`

### Glyph System
SVG glyphs are referenced in key legends with `$$source:name$$` syntax:
- Example: `$$material:settings$$` fetches from Material Design Icons
- Glyphs are cached locally (controlled by `use_local_cache`)
- Custom glyphs can be defined in `glyphs` config field

### Physical Layout Resolution
The tool tries multiple strategies to find physical layout:
1. ZMK keyboard name lookup in bundled resources
2. QMK keyboard name → fetch info.json from QMK API
3. Local QMK info.json file path
4. ZMK DTS layout file (devicetree format)
5. Parametrized ortholinear layout (rows × columns)
6. Cols+thumbs notation (e.g., `23332+2 2+33331`)

## Configuration Files

**`keymap_config.yaml`** - Personal configuration for the maintainer's keyboard
- Extensive `raw_binding_map` for custom key labels
- Custom draw configuration (colors, styling)
- This file is specific to the maintainer's workflow and serves as a comprehensive example

**`pyproject.toml`** - Project metadata and tool configuration
- Poetry build system (though package also works with pip)
- Pylint, mypy, black, isort settings
- Line length: 120 characters
- Python ≥3.12 required

**`resources/`** - Bundled layout definitions and mappings
- QMK keyboard mappings
- Extra physical layouts for popular keyboards
- Not typically modified during development

## Notes

- The codebase uses Pydantic v2 for data validation and serialization
- Tree-sitter is used for robust parsing of ZMK devicetree files
- The tool can be used both as a library and CLI
- SVG output can be styled with dark mode support (`dark_mode: "auto"`)
- The web UI mentioned in docs is separate from this codebase
