#!/bin/bash
#
# Keymap Generator for Kinesis Advantage 360
#
# This script:
# 1. Sets up virtual environment and dependencies (if needed)
# 2. Copies the latest keymap from your ZMK config directory
# 3. Generates YAML and SVG visualization
# 4. Adds shifted labels and custom styling
#
# Output: adv360.svg (open in browser to view)
#

set -e  # Exit on error

echo "🎹 Generating Kinesis Advantage 360 Keymap Visualization"
echo "========================================================="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if package is installed by trying to import it
if ! python3 -c "import keymap_drawer" 2>/dev/null; then
    echo "📦 Installing keymap-drawer package and dependencies..."
    python3 -m pip install --quiet -e .
    echo "✅ Package installed"
fi

# Run the keymap generator
./generate_keymap_internal.py

echo ""
echo "✅ Done! Open adv360.svg to view your keymap"
