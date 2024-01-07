# 1. get file path from sys.argv[1]
# 2. read log file
# 3. parse log file:
#    line with score is in format:
#       2024-01-07 13:21:45,102 | INFO | runner.run_game:73 | Controller <bot_name> scored <score> points.
# 4. get scores of each bot_name and sum them
# 5. print scores

import sys
import re

def get_scores(log_file_path):
    scores = {}
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = re.search(r'Controller (?P<bot_name>.+) scored (?P<score>\d+) points.', line)
            if match:
                bot_name = match.group('bot_name')
                score = int(match.group('score'))
                if bot_name not in scores:
                    scores[bot_name] = 0
                scores[bot_name] += score
    return scores

def print_scores(scores):
    for i, (name, score) in enumerate(sorted(scores.items(), key=lambda x: x[1], reverse=True)):
        print(f"{int(i) + 1}.   {name}: {score}.")
    print(f"Total: {sum(scores.values())}.")
    print(f"Average: {sum(scores.values()) / len(scores)}.")
    print(f"Min: {min(scores.values())}.")
    print(f"Max: {max(scores.values())}.")
    print(f"Median: {sorted(scores.values())[len(scores) // 2]}.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <log_file_path>")
        sys.exit(1)
    log_file_path = sys.argv[1]
    scores = get_scores(log_file_path)
    print_scores(scores)
