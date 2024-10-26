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

def is_length_equal(train) -> bool:
    for example in train:
        if len(example['input']) != len(example['output']):
            return False
    return True

def is_length_less_than(train) -> bool:
    for example in train:
        if len(example['input']) >= len(example['output']):
            return False
    return True

def is_length_greater_than(train) -> bool:
    for example in train:
        if len(example['input']) <= len(example['output']):
            return False
    return True

def find_invariants(problem) -> list:
    invariants = {}
    train = problem['train']
    invariants['length_equal']        = is_length_equal(train)
    invariants['length_greater_than'] = is_length_greater_than(train)
    invariants['length_less_than']    = is_length_less_than(train)
    print(invariants)
    return invariants

def guess_output(problem) -> list:
    for pair in problem['test']:
        return construct_output(pair['input'], find_invariants(problem))

def attempt_problem(name, problem) -> bool:
    print(f"Attempting : {name}")
    for pair in problem['test']:
        return guess_output(problem) == pair['output']

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
