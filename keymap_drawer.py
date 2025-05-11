#!/usr/bin/env python3

import sys
import re
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
import html
import shutil
import os

# Copy the most recent keymap file from the other directory
def copy_most_recent_keymap(force=True):
    source_dir = Path("/Users/fredrik/Projects/other/Adv360-Pro-ZMK/config")
    target_dir = Path.cwd()
    
    # Check if source directory exists
    if not source_dir.exists():
        print(f"Source directory {source_dir} does not exist.")
        return
    
    # Look for keymap files in the source directory
    keymap_files = list(source_dir.glob("*.keymap"))
    
    if not keymap_files:
        print(f"No keymap files found in {source_dir}")
        return
    
    # Find the most recent keymap file
    most_recent_file = max(keymap_files, key=lambda f: f.stat().st_mtime)
    
    # Destination filename (keeping the same basename)
    dest_file = target_dir / most_recent_file.name
    
    # Check if destination file exists and is newer (only if force=False)
    if not force and dest_file.exists() and dest_file.stat().st_mtime > most_recent_file.stat().st_mtime:
        print(f"File {dest_file.name} in target directory is newer than source. Not overwriting.")
        return
    
    # Copy the file
    shutil.copy2(most_recent_file, dest_file)
    source_str = str(source_dir)
    target_str = str(target_dir)
    print(f"Copied most recent keymap file: {most_recent_file.name}")
    print(f"  From: {source_str}")
    print(f"  To:   {target_str}")

# Execute the function to copy the most recent keymap file
copy_most_recent_keymap(force=True)

def convert_keymap():
    """Run the keymap conversion process."""
    print("Using config file: keymap_config.yaml")
    print("Converting adv360.keymap to YAML with human-readable keys...")
    
    # Read and display the keymap file
    with open("adv360.keymap", "r") as f:
        keymap_content = f.read()
        print(keymap_content)
    
    # Run the keymap command to parse the keymap
    print("Running command: keymap -c keymap_config.yaml parse -z adv360.keymap -o adv360.yaml")
    subprocess.run(["keymap", "-c", "keymap_config.yaml", "parse", "-z", "adv360.keymap", "-o", "adv360.yaml"], check=True)
    print("YAML file created: adv360.yaml")
    
    # Parse and display the YAML file
    with open("adv360.yaml", "r") as f:
        yaml_content = f.read()
        print(yaml_content)
    
    # Run the keymap command to draw the keymap
    print("Generating SVG from adv360.yaml...")
    print("Running command: keymap -c keymap_config.yaml draw adv360.yaml --select-layers Base L2 -o adv360.svg")
    subprocess.run([
        "keymap", "-c", "keymap_config.yaml", "draw", "adv360.yaml",
        "--select-layers", "Base", "L2",
        "-o", "adv360.svg"
    ], check=True)
    print("SVG file created: adv360.svg")
    print("Conversion complete!")

def read_custom_css():
    """Read the custom CSS file."""
    css_file = Path("additional_styles.css")
    if css_file.exists():
        return css_file.read_text()
    return None

def add_shifted_labels(svg_file):
    """Add shifted labels to the SVG file, skipping numpad keys."""
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

    # Indices of numpad keys in your layout (adjust if your layout changes)
    NUMPAD_INDICES = {10, 12, 22, 23, 24, 25, 26, 39, 40, 41, 42, 43, 55, 56, 57, 58, 59, 71, 72, 73, 74, 75}
    # Set of numpad key labels
    NUMPAD_LABELS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/', '-', '+', '.', '↵'}

    with open(svg_file, 'r') as f:
        content = f.read()

    # Use regex to find all key groups and their indices
    def add_shifted(match):
        g_tag = match.group(1)
        rect = match.group(2)
        text = match.group(3)
        key = match.group(4)
        endtext = match.group(5)
        # Extract key index from class (e.g., keypos-22)
        m = re.search(r'keypos-(\d+)', g_tag)
        if m and int(m.group(1)) in NUMPAD_INDICES and key in NUMPAD_LABELS:
            return match.group(0)  # Don't modify numpad keys
        if key in SHIFTED_KEYS:
            return f'{g_tag}{rect}{text}<tspan class="primary-label" y="5">{key}</tspan><tspan class="shifted-label" x="0" y="-15">{SHIFTED_KEYS[key]}</tspan>{endtext}'
        return match.group(0)

    # Pattern to match key groups with a single character key
    pattern = r'(<g[^>]*keypos-\d+[^>]*>)(\s*<rect[^>]*>)(\s*<text[^>]*>)([^<])(<\/text>)'
    content = re.sub(pattern, add_shifted, content)

    with open(svg_file, 'w') as f:
        f.write(content)

    print(f"Added shifted labels to {svg_file}")

def add_css_to_svg(svg_file):
    """Add custom CSS to the SVG file."""
    custom_css = read_custom_css()
    if not custom_css:
        print("No custom CSS file found")
        return
    
    with open(svg_file, 'r') as f:
        content = f.read()
    
    # Find the style tag
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not style_match:
        print("No style tag found in SVG")
        return
    
    # Add our custom CSS to the style section
    original_style = style_match.group(1)
    new_style = original_style + "\n" + custom_css
    content = content.replace(style_match.group(0), f'<style>{new_style}</style>')
    
    # Apply classes to specific keycaps
    
    # App shortcuts - adjust class names to match the CSS names
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(WApp)(</text>)', 
                     r'\1<tspan class="WhatsApp-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(Spot)(</text>)', 
                     r'\1<tspan class="Spotify-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(Chrm)(</text>)', 
                     r'\1<tspan class="Chrome-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(Curs)(</text>)', 
                     r'\1<tspan class="Cursor-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(GitH)(</text>)', 
                     r'\1<tspan class="GitHub-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(TpLt)(</text>)', 
                     r'\1<tspan class="topLeft-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(L←)(</text>)', 
                     r'\1<tspan class="LeftScr-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(R→)(</text>)', 
                     r'\1<tspan class="RightScr-key">\2</tspan>\3', content)
    
    # Currency
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(€)(</text>)', 
                     r'\1<tspan class="euro-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(£)(</text>)', 
                     r'\1<tspan class="pound-key">\2</tspan>\3', content)
    
    # System
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(Boot)(</text>)', 
                     r'\1<tspan class="BOOT-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(L1)(</text>)', 
                     r'\1<tspan class="Fn1-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(Fn2)(</text>)', 
                     r'\1<tspan class="Fn2-key">\2</tspan>\3', content)
    
    # Special chars
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(@)(</text>)', 
                     r'\1<tspan class="Email-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(ö)(</text>)', 
                     r'\1<tspan class="o-umlaut-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(å)(</text>)', 
                     r'\1<tspan class="a-ring-key">\2</tspan>\3', content)
    
    # Navigation
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)([↑↓←→])(</text>)', 
                     r'\1<tspan class="arrow-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(⌘[↑↓←→])(</text>)', 
                     r'\1<tspan class="arrow-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(⌥[↑↓←→])(</text>)', 
                     r'\1<tspan class="arrow-key">\2</tspan>\3', content)
    
    # Screenshot
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(ScrS)(</text>)', 
                     r'\1<tspan class="Screenshot-key">\2</tspan>\3', content)
    
    # Modifiers
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(Shft|Ctrl|Alt|Cmd)(</text>)', 
                     r'\1<tspan class="mod-key">\2</tspan>\3', content)
    content = re.sub(r'(<g[^>]*>\s*<rect[^>]*>\s*<text[^>]*>)(Spce|↵|⌫|Tab|Esc)(</text>)', 
                     r'\1<tspan class="mod-key">\2</tspan>\3', content)
    
    # Apply directly to the <rect> elements for key backgrounds
    key_mapping = {
        "WApp": "WhatsApp-key",
        "Spot": "Spotify-key",
        "Chrm": "Chrome-key",
        "Curs": "Cursor-key",
        "GitH": "GitHub-key",
        "TpLt": "topLeft-key",
        "L←": "LeftScr-key",
        "R→": "RightScr-key",
        "€": "euro-key",
        "£": "pound-key",
        "Boot": "BOOT-key",
        "L1": "Fn1-key",
        "Fn2": "Fn2-key",
        "@": "Email-key",
        "ö": "o-umlaut-key",
        "å": "a-ring-key",
        "ScrS": "Screenshot-key"
    }
    
    # Apply directly to the <rect> elements using the mapping
    for label, class_name in key_mapping.items():
        content = re.sub(
            rf'(<g[^>]*>\s*)(<rect[^>]*>)(\s*<text[^>]*>){label}(</text>)',
            rf'\1<rect class="{class_name}" x="-26" y="-26" width="52" height="52" rx="6" ry="6"/>\3{label}\4',
            content
        )
        content = re.sub(
            rf'(<g[^>]*>\s*)(<rect[^>]*>)(\s*<text[^>]*><tspan class="{class_name}">){label}(</tspan>)',
            rf'\1<rect class="{class_name}" x="-26" y="-26" width="52" height="52" rx="6" ry="6"/>\3{label}\4',
            content
        )
    
    # Apply to arrow keys
    content = re.sub(
        r'(<g[^>]*>\s*)(<rect[^>]*>)(\s*<text[^>]*>)[↑↓←→](</text>)',
        r'\1<rect class="arrow-key" x="-26" y="-26" width="52" height="52" rx="6" ry="6"/>\3\4',
        content
    )
    content = re.sub(
        r'(<g[^>]*>\s*)(<rect[^>]*>)(\s*<text[^>]*>)[⌘⌥][↑↓←→](</text>)',
        r'\1<rect class="arrow-key" x="-26" y="-26" width="52" height="52" rx="6" ry="6"/>\3\4',
        content
    )
    
    # Apply to modifier keys
    content = re.sub(
        r'(<g[^>]*>\s*)(<rect[^>]*>)(\s*<text[^>]*>)(Shft|Ctrl|Alt|Cmd|Spce|↵|⌫|Tab|Esc)(</text>)',
        r'\1<rect class="mod-key" x="-26" y="-26" width="52" height="52" rx="6" ry="6"/>\3\4\5',
        content
    )
    
    with open(svg_file, 'w') as f:
        f.write(content)
    
    print(f"Added custom styling to {svg_file}")

def main():
    # Convert the keymap to YAML and then to SVG
    convert_keymap()
    
    # Add shifted labels to the SVG
    svg_file = "adv360.svg"
    add_shifted_labels(svg_file)
    
    # Apply custom styling to the SVG
    add_css_to_svg(svg_file)

if __name__ == "__main__":
    main() 