import sys
import csv

def main():
    # Read CSV data from stdin
    reader = csv.reader(sys.stdin)
    data = list(reader)

    # Check if data is empty
    if not data:
        print("No data provided.")
        sys.exit(1)

    # First line is headers
    headers = data[0]
    data = data[1:]  # Data without headers

    num_rows = len(data)
    num_cols = len(headers)

    # Ensure all rows have the correct number of columns
    for row_num, row in enumerate(data, start=2):  # Start from 2 because of headers
        if len(row) != num_cols:
            print(f"Inconsistent number of columns in row {row_num}.")
            sys.exit(1)

    # Convert data to columns
    columns = {}
    for col_idx, header in enumerate(headers):
        column = [row[col_idx] for row in data]
        columns[header] = column

    # Analysis
    always_true_columns = []
    always_false_columns = []
    # Using dictionaries to store matching and disagreeing columns
    always_match_columns = {}
    always_disagree_columns = {}

    # For each column, check if it's always the same value
    for header, col in columns.items():
        unique_values = set(col)
        if len(unique_values) == 1:
            value = unique_values.pop()
            # Depending on the value, classify as always true or always false
            if value in ['True', 'T', '1']:
                always_true_columns.append(header)
            elif value in ['False', 'F', '0']:
                always_false_columns.append(header)
            else:
                # If the value is neither standard True nor False, consider it always true
                always_true_columns.append(header)
            unique_values.add(value)  # Put the value back if needed later
        else:
            pass  # Column has varying values

    # For each pair of columns, check if they always match or always disagree
    header_list = list(headers)
    num_cols = len(header_list)
    for i in range(num_cols):
        for j in range(i + 1, num_cols):
            header_i = header_list[i]
            header_j = header_list[j]
            col_i = columns[header_i]
            col_j = columns[header_j]
            match = True
            disagree = True
            for val_i, val_j in zip(col_i, col_j):
                if val_i != val_j:
                    match = False
                if val_i == val_j:
                    disagree = False
                if not match and not disagree:
                    break  # No need to check further
            if match:
                if header_i not in always_match_columns:
                    always_match_columns[header_i] = set()
                always_match_columns[header_i].add(header_j)
                if header_j not in always_match_columns:
                    always_match_columns[header_j] = set()
                always_match_columns[header_j].add(header_i)
            elif disagree:
                if header_i not in always_disagree_columns:
                    always_disagree_columns[header_i] = set()
                always_disagree_columns[header_i].add(header_j)
                if header_j not in always_disagree_columns:
                    always_disagree_columns[header_j] = set()
                always_disagree_columns[header_j].add(header_i)

    # Output the results
    print("\nAlways True Columns:")
    if always_true_columns:
        print(", ".join(always_true_columns))
    else:
        print("None")

    print("\nAlways False Columns:")
    if always_false_columns:
        print(", ".join(always_false_columns))
    else:
        print("None")

    print("\nColumns That Always Match Another Column:")
    printed_pairs = set()
    for header, matching_headers in always_match_columns.items():
        for match_header in matching_headers:
            pair = tuple(sorted((header, match_header)))
            if pair not in printed_pairs:
                printed_pairs.add(pair)
                print(f"Columns '{pair[0]}' and '{pair[1]}' always match.")

    print("\nColumns That Always Disagree with Another Column:")
    printed_pairs = set()
    for header, disagree_headers in always_disagree_columns.items():
        for disagree_header in disagree_headers:
            pair = tuple(sorted((header, disagree_header)))
            if pair not in printed_pairs:
                printed_pairs.add(pair)
                print(f"Columns '{pair[0]}' and '{pair[1]}' always disagree.")

if __name__ == "__main__":
    main()
