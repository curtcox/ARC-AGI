import os
import json

def load_problems(directory):
    problems = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                problems.append(json.load(file))
    return problems

def guess_output(problem):
    # for pair in problem['train']:
    #     consider pair['input'] produces pair['output']:
    for pair in problem['test']:
        return pair['input']

def attempt_problem(problem):
    for pair in problem['test']:
        return guess_output(problem) == pair['output']

def main():

    successes = 0

    training_problems = load_problems('data/training')
    for problem in training_problems:
        if attempt_problem(problem):
          successes += 1

    print(f"Training successes: {successes}")

    evaluation_problems = load_problems('data/evaluation')
    for problem in evaluation_problems:
        if attempt_problem(problem):
           successes += 1

    print(f"Total successes: {successes}")

if __name__ == "__main__":
    main()
