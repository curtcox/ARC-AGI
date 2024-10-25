import os
import json

def load_problems(directory):
    problems = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                problems.append(json.load(file))
    return problems

def attempt_problem(problem):
    successes = 0
    for pair in problem['train']:
        if pair['input'] == pair['output']:
            successes += 1
        print(f"Training problem: {'Success' if pair['input'] == pair['output'] else 'Failure'}")
    for pair in problem['test']:
        if pair['input'] == pair['output']:
            successes += 1
        print(f"Evaluation problem: {'Success' if pair['input'] == pair['output'] else 'Failure'}")
    return successes

def main():
    training_problems = load_problems('data/training')
    evaluation_problems = load_problems('data/evaluation')

    total_successes = 0

    for problem in training_problems:
        total_successes += attempt_problem(problem)

    for problem in evaluation_problems:
        total_successes += attempt_problem(problem)

    print(f"Total number of successes: {total_successes}")

if __name__ == "__main__":
    main()
