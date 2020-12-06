import sys

groups = sys.stdin.read().split('\n\n')
n = 0
for group in groups:
    all_questions = set()

    answers = list(map(set, group.split()))
    for answer in answers:
        all_questions.update(answer)
    
    for q in all_questions:
        if all(q in answer for answer in answers):
            n += 1

print(n)
