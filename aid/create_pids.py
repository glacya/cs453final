#!/usr/bin/env python3
"""
List all project IDs (folder names) under datasets/TrickyBugs and write them to pids.txt.
"""
from pathlib import Path

# Base directory containing all project folders
datasets_dir = Path("datasets/TrickyBugs")
# Output file for PIDs
output_file = Path("pids.txt")

# Collect all directory names
pids = [p.name for p in datasets_dir.iterdir() if p.is_dir()]

# Sort the list for consistency
pids.sort()

# Write to pids.txt, one per line
output_file.write_text("\n".join(pids), encoding="utf-8")

print(f"Written {len(pids)} PIDs to {output_file}")