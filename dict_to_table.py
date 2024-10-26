#!/usr/bin/env python3
import sys
import csv
import ast
from typing import List, Dict

def parse_line(line: str) -> Dict[str, bool]:
    """Parse a line containing a dictionary string into a Python dictionary."""
    try:
        # Use ast.literal_eval to safely evaluate the string as a Python literal
        return ast.literal_eval(line.strip())
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing line: {line}", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)
        return {}

def process_input() -> List[Dict[str, bool]]:
    """Read and parse input lines from stdin."""
    data = []
    for line in sys.stdin:
        if line.strip():  # Skip empty lines
            parsed = parse_line(line)
            if parsed:  # Only add if parsing was successful
                data.append(parsed)
    return data

def write_csv(data: List[Dict[str, bool]]):
    """Write the data as CSV to stdout."""
    if not data:
        print("No valid data to process", file=sys.stderr)
        return

    # Get headers from the first dictionary
    headers = list(data[0].keys())
    
    # Create CSV writer
    writer = csv.DictWriter(sys.stdout, fieldnames=headers)
    
    # Write headers and data
    writer.writeheader()
    writer.writerows(data)

def main():
    """Main program execution."""
    try:
        data = process_input()
        write_csv(data)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()