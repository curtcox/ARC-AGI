import os
import json

def load_problems(directory) -> dict:
    problems = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                problems[filename] = json.load(file)
    return problems

def guess_output(problem) -> list:
    # for pair in problem['train']:
    #     consider pair['input'] produces pair['output']:
    for pair in problem['test']:
        return pair['input']

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
