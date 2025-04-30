#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Define paths
    keymap_file = Path("adv360.keymap")
    yaml_output = Path("adv360.yaml")
    svg_output = Path("adv360.svg")
    config_file = Path("keymap_config.yaml")
    
    # Check if files exist
    if not keymap_file.exists():
        print(f"Error: Keymap file '{keymap_file}' not found.")
        sys.exit(1)
    
    if not config_file.exists():
        print(f"Warning: Config file '{config_file}' not found. Using default settings.")
        config_arg = []
    else:
        config_arg = ["-c", str(config_file)]
        print(f"Using config file: {config_file}")
    
    # Step 1: Convert keymap to YAML
    print(f"Converting {keymap_file} to YAML with human-readable keys...")
    
    # First dump the original file to see what we're working with
    subprocess.run(["cat", str(keymap_file)], check=True)
    
    try:
        cmd = ["keymap"] + config_arg + ["parse", "-z", str(keymap_file), "-o", str(yaml_output)]
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print(f"YAML file created: {yaml_output}")
        
        # Display the first few lines of the generated YAML
        subprocess.run(["head", "-n", "20", str(yaml_output)], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error converting to YAML: {e}")
        sys.exit(1)
    
    # Step 2: Generate SVG from YAML
    print(f"Generating SVG from {yaml_output}...")
    try:
        cmd = ["keymap"] + config_arg + ["draw", str(yaml_output), "-o", str(svg_output)]
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print(f"SVG file created: {svg_output}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating SVG: {e}")
        sys.exit(1)
    
    print("Conversion complete!")

if __name__ == "__main__":
    main() 