#!/usr/bin/env python3

import sys
import re
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

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
    print("Running command: keymap -c keymap_config.yaml draw adv360.yaml -o adv360.svg")
    subprocess.run(["keymap", "-c", "keymap_config.yaml", "draw", "adv360.yaml", "-o", "adv360.svg"], check=True)
    print("SVG file created: adv360.svg")
    print("Conversion complete!")

def read_custom_css():
    """Read the custom CSS file."""
    css_file = Path("additional_styles.css")
    if css_file.exists():
        return css_file.read_text()
    return None

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
    
    # Apply custom styling to the SVG
    svg_file = "adv360.svg"
    add_css_to_svg(svg_file)

if __name__ == "__main__":
    main() 