#!/usr/bin/env python3

import argparse
import os


def format_value(value):
    """Formats a float to max 7 digits (8 characters including the dot)."""
    formatted = f"{value:.7f}"
    # Trim from the right to keep at most 8 characters total (incl. dot)
    return formatted[:8]


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

    print(f"✅ Rescaled RGB values and saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rescale RGB values in a .ti1 file from 0–100 to 0–255 for i1Profiler.")
    parser.add_argument("input", help="Input .ti1 file")
    parser.add_argument("-o", "--output", help="Output file (default: input_basename.txt)")

    args = parser.parse_args()
    default_output = os.path.splitext(args.input)[0] + ".txt"
    output_file = args.output or default_output

    rescale_ti1_rgb(args.input, output_file)
