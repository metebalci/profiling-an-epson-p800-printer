#!/usr/bin/env python3

import argparse
import os
import random
import shutil
import sys


def format_value(value):
    """Formats a float to max 7 digits (8 characters including the dot)."""
    formatted = f"{value:.7f}"
    # Trim from the right to keep at most 8 characters total (incl. dot)
    return formatted[:8]


def randomize_ti1_patches(input_file, output_file):
    """Randomizes patch locations within sets in a .ti1 file."""
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Locate data section
    try:
        start_idx = lines.index("BEGIN_DATA\n") + 1
        end_idx = lines.index("END_DATA\n")
    except ValueError:
        raise ValueError("BEGIN_DATA or END_DATA not found in file.")

    header = lines[:start_idx]
    footer = lines[end_idx:]

    # Extract data lines
    data_lines = lines[start_idx:end_idx]

    # Get number of sets
    num_sets = 1
    for line in lines:
        if line.startswith("NUMBER_OF_SETS_OF_PATCHES"):
            num_sets = int(line.strip().split()[1])
            break

    # Split into sets
    patches_per_set = len(data_lines) // num_sets
    sets = [data_lines[i * patches_per_set:(i + 1) * patches_per_set] for i in range(num_sets)]

    # Shuffle within each set (deterministic with seed based on number of patches)
    random.seed(len(data_lines))
    for s in sets:
        random.shuffle(s)

    # Flatten
    shuffled_data = [line for s in sets for line in s]

    # Write output
    with open(output_file, "w") as f:
        f.writelines(header + shuffled_data + footer)


def rescale_ti1_rgb(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out_lines.append(line)

        if line.strip() == "BEGIN_DATA_FORMAT":
            # Capture format block
            format_lines = []
            i += 1
            while not lines[i].strip().startswith("END_DATA_FORMAT"):
                format_lines.append(lines[i].strip())
                out_lines.append(lines[i])
                i += 1
            out_lines.append(lines[i])  # END_DATA_FORMAT
            i += 1

            # Determine RGB column indexes
            fields = " ".join(format_lines).split()
            rgb_indices = [j for j, f in enumerate(fields) if f in ("RGB_R", "RGB_G", "RGB_B")]

            # Look ahead to BEGIN_DATA
            while i < len(lines) and not lines[i].strip().startswith("BEGIN_DATA"):
                out_lines.append(lines[i])
                i += 1

            if i < len(lines) and lines[i].strip() == "BEGIN_DATA":
                out_lines.append(lines[i])  # BEGIN_DATA
                i += 1

                # Process data rows
                while i < len(lines) and not lines[i].strip().startswith("END_DATA"):
                    parts = lines[i].strip().split()
                    if rgb_indices:
                        for idx in rgb_indices:
                            scaled = float(parts[idx]) * 2.55
                            parts[idx] = format_value(scaled)
                        out_lines.append(" ".join(parts) + "\n")
                    else:
                        out_lines.append(lines[i])
                    i += 1

                if i < len(lines):
                    out_lines.append(lines[i])  # END_DATA
        i += 1

    with open(output_file, "w") as f:
        f.writelines(out_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rescale RGB values and optionally randomize patch locations in targen's .ti1 file for i1Profiler.")
    parser.add_argument("input", help="Input .ti1 file")
    parser.add_argument("-r", "--randomize", action="store_true", help="Randomize patch locations (creates a backup with .bak extension)")

    args = parser.parse_args()
    input_file = args.input
    output_file = os.path.splitext(input_file)[0] + ".txt"

    try:
        if args.randomize:
            # Create backup
            backup_file = input_file + ".bak"
            shutil.copy2(input_file, backup_file)
            
            # Randomize patches in the original file
            randomize_ti1_patches(input_file, input_file)

        rescale_ti1_rgb(input_file, output_file)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)