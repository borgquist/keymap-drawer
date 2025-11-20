#!/bin/bash
#
# Keymap Generator for Kinesis Advantage 360
#
# This script:
# 1. Copies the latest keymap from your ZMK config directory
# 2. Generates YAML and SVG visualization
# 3. Adds shifted labels and custom styling
#
# Output: adv360.svg (open in browser to view)
#

set -e  # Exit on error

echo "🎹 Generating Kinesis Advantage 360 Keymap Visualization"
echo "========================================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Run the keymap generator
./keymap_drawer.py

echo ""
echo "✅ Done! Open adv360.svg to view your keymap"
