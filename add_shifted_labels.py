#!/usr/bin/env python3

import re
import xml.etree.ElementTree as ET
from pathlib import Path
import html

# Define the shifted values for each key
SHIFTED_KEYS = {
    "1": "!",
    "2": "@",
    "3": "#",
    "4": "$",
    "5": "%",
    "6": "^",
    "7": "&amp;",  # Properly escaped ampersand
    "8": "*",
    "9": "(",
    "0": ")",
    "-": "_",
    "=": "+",
    "`": "~",
    "[": "{",
    "]": "}",
    "\\": "|",
    ";": ":",
    "'": "&quot;",  # Properly escaped quotation mark
    ",": "&lt;",    # Properly escaped less-than
    ".": "&gt;",    # Properly escaped greater-than
    "/": "?"
}

def add_shifted_labels(svg_file):
    """Add shifted labels to the SVG file"""
    with open(svg_file, 'r') as f:
        content = f.read()
    
    # For each key in our mapping
    for key, shifted in SHIFTED_KEYS.items():
        # Use regex to find text elements containing exactly our key character
        pattern = rf'(<g[^>]*key[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)({re.escape(key)})(</text>)'
        
        # Replace with our dual-labeled structure
        replacement = rf'\1<tspan class="primary-label" y="5">\2</tspan><tspan class="shifted-label" x="0" y="-15">{shifted}</tspan>\3'
        
        # Apply the replacement
        content = re.sub(pattern, replacement, content)
    
    # Write the modified content back to the file
    with open(svg_file, 'w') as f:
        f.write(content)
    
    print(f"Added shifted labels to {svg_file}")

if __name__ == "__main__":
    # Start with a fresh copy of the original SVG
    original_svg = "adv360_original.svg"
    svg_file = "adv360.svg"
    
    # Copy the original SVG to the target file
    with open(original_svg, 'r') as src, open(svg_file, 'w') as dst:
        dst.write(src.read())
    
    # Add the shifted labels
    add_shifted_labels(svg_file) 