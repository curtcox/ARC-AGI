import os
import json

# The examples are structured as follows:
# {"train": [{"input": [[0, 0, 0, 0, 0,
# Each example maps a list[list[integer]] to a list[list[integer]].

def load_problems(directory) -> dict:
    problems = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                problems[filename] = json.load(file)
    return problems

def construct_output(input, invariants):
    return input

def color_count(a: list) -> int:
    """Count the number of unique colors in the grid."""
    colors = set()
    for row in a:
        for color in row:
            colors.add(color)
    return len(colors)

def zero_count(a: list) -> int:
    """Count the number of zeros in the grid."""
    count = 0
    for row in a:
        for color in row:
            if color == 0:
                count += 1
    return count

def dimensions(a: list) -> tuple:
    """Get the dimensions (height, width) of the grid."""
    height = len(a)
    width = len(a[0]) if a else 0
    return (height, width)

def non_zero_count(a: list) -> int:
    """Count the number of non-zero cells in the grid."""
    count = 0
    for row in a:
        for color in row:
            if color != 0:
                count += 1
    return count

def colors_set(a: list) -> set:
    """Get the set of colors used in the grid."""
    colors = set()
    for row in a:
        for color in row:
            colors.add(color)
    return colors

def sum_of_colors(a: list) -> int:
    """Calculate the sum of all cell values in the grid."""
    total = 0
    for row in a:
        total += sum(row)
    return total

def height(a: list) -> int:
    """Get the height of the grid."""
    return len(a)

def width(a: list) -> int:
    """Get the width of the grid."""
    return len(a[0]) if a else 0

def color_transitions(input_grid: list, output_grid: list) -> set:
    """Compute the set of color transitions between input and output grids."""
    transitions = set()
    input_height = len(input_grid)
    input_width = len(input_grid[0]) if input_grid else 0
    output_height = len(output_grid)
    output_width = len(output_grid[0]) if output_grid else 0

    min_height = min(input_height, output_height)
    min_width = min(input_width, output_width)

    for i in range(min_height):
        for j in range(min_width):
            c_in = input_grid[i][j]
            c_out = output_grid[i][j]
            transitions.add((c_in, c_out))
    return transitions

def check_color_transitions_equal(train):
    """Check if the set of color transitions is the same across all training examples."""
    transitions_list = [color_transitions(example['input'], example['output']) for example in train]
    first_transitions = transitions_list[0]
    return all(transitions == first_transitions for transitions in transitions_list)

def check_transition_cardinality_equal(train):
    """Check if the cardinality of color transitions is the same across all training examples."""
    counts = [len(color_transitions(example['input'], example['output'])) for example in train]
    first_count = counts[0]
    return all(count == first_count for count in counts)

def check_that(train, comparison_func):
    """Check if a condition holds for all examples in the training data."""
    return all(comparison_func(example['input'], example['output']) for example in train)

def find_invariants(problem) -> dict:
    """Find and return invariants across the training examples."""
    invariants = {}
    train = problem['train']

    # Size
    invariants['len(in)==len(out)']                 = check_that(train, lambda x, y: len(x) == len(y))
    invariants['len(in)>len(out)']                  = check_that(train, lambda x, y: len(x) > len(y))
    invariants['len(in)<len(out)']                  = check_that(train, lambda x, y: len(x) < len(y))
    invariants['height(in)==height(out)']           = check_that(train, lambda x, y: height(x) == height(y))
    invariants['height(in)>height(out)']            = check_that(train, lambda x, y: height(x)  > height(y))
    invariants['width(in)==width(out)']             = check_that(train, lambda x, y:  width(x) == width(y))
    invariants['width(in)<width(out)']              = check_that(train, lambda x, y:  width(x)  < width(y))
    invariants['dimensions(in)==dimensions(out)']   = check_that(train, lambda x, y: dimensions(x) == dimensions(y))

    # Colors
    invariants['len(colors(in))==len(colors(out))'] = check_that(train, lambda x, y: color_count(x) == color_count(y))
    invariants['len(colors(in))>len(colors(out))']  = check_that(train, lambda x, y: color_count(x)  > color_count(y))
    invariants['len(colors(in))<len(colors(out))']  = check_that(train, lambda x, y: color_count(x)  < color_count(y))
    invariants['colors(in)==colors(out)']           = check_that(train, lambda x, y:  colors_set(x) == colors_set(y))
    invariants['colors(in)>colors(out)']            = check_that(train, lambda x, y:  colors_set(x)  > colors_set(y))
    invariants['colors(in)<colors(out)']            = check_that(train, lambda x, y:  colors_set(x)  < colors_set(y))
    invariants['sum(colors(in))==sum(colors(out))'] = check_that(train, lambda x, y: sum_of_colors(x) == sum_of_colors(y))

    # Color Transitions
    invariants['transitions(in,out)']      = check_color_transitions_equal(train)
    invariants['len(transitions(in,out))'] = check_transition_cardinality_equal(train)

    # Non-zero Cell Count Equality
    invariants['count(nonzero(in))==count(nonzero(out))'] = check_that(train, lambda x, y: non_zero_count(x) == non_zero_count(y))
    invariants['zeros(in)==zeros(out)']                   = check_that(train, lambda x, y: zero_count(x) == zero_count(y))
    invariants['zeros(in)>zeros(out)']                    = check_that(train, lambda x, y: zero_count(x) > zero_count(y))
    invariants['zeros(in)<zeros(out)']                    = check_that(train, lambda x, y: zero_count(x) < zero_count(y))

    # Print or return the invariants dictionary
    print(invariants)
    return invariants

def guess_output(problem) -> list:
    for pair in problem['test']:
        return construct_output(pair['input'], find_invariants(problem))
    raise ValueError("No test")

def attempt_problem(name, problem) -> bool:
    print(f"Attempting : {name}")
    for pair in problem['test']:
        return guess_output(problem) == pair['output']
    raise ValueError("No test")

def main():

    successes = 0

    for name, problem in load_problems('data/training').items():
        if attempt_problem(name, problem):
          successes += 1

    print(f"Training successes: {successes}")

    for name, problem in load_problems('data/evaluation').items():
        if attempt_problem(name, problem):
           successes += 1

    print(f"Total successes: {successes}")

if __name__ == "__main__":
    main()
