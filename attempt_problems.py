import os
import json

def load_problems(directory) -> dict:
    problems = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                problems[filename] = json.load(file)
    return problems

def construct_output(input, invariants):
    return input

def color_count(a:list) -> int:
    colors = set()
    for row in a:
        for color in row:
            colors.add(color)
    return len(colors)

# The examples are structured as follows:
# {"train": [{"input": [[0, 0, 0, 0, 0,
# Each example maps a list[list[integer]] to a list[list[integer]].

def check_that(train, comparison_func):
    return all(comparison_func(example['input'], example['output']) for example in train)

def find_invariants(problem) -> dict:
    invariants = {}
    train = problem['train']
    invariants['len(in)==len(out)']                 = check_that(train, lambda x, y: len(x) == len(y))
    invariants['len(in)>len(out)']                  = check_that(train, lambda x, y: len(x) > len(y))
    invariants['len(in)<len(out)']                  = check_that(train, lambda x, y: len(x) < len(y))
    invariants['len(colors(in))==len(colors(out))'] = check_that(train, lambda x, y: color_count(x) == color_count(y))
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
