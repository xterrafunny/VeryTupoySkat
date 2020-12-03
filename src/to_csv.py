from os import listdir
import re


def to_csv(path_to_data: str,
           result_path: str):
    plagiarism = dict()
    for problem_dir in listdir(path_to_data):
        if not re.fullmatch(r"\d+-\w", problem_dir):
            continue
        contest, problem = problem_dir.split('-')
        if plagiarism.get(contest) is None:
            plagiarism[contest] = dict()
        if plagiarism[contest].get(problem) is None:
            plagiarism[contest][problem] = list()
        for file in listdir(path_to_data + "/{}".format(problem_dir)):
            if file.find("top") == -1:
                continue
            with open(path_to_data + "/{}/{}".format(problem_dir, file), 'r') as current:
                content = ''.join(current.readlines())
                contestants = re.findall(r"\d{6}-\w-.{1,20}\.txt \(\d+%\)", content)
                plagiarism[contest][problem].append([])
                for contestant in contestants:
                    submission, percent = contestant.split()
                    percent = percent[1:-2]
                    submission = submission[9:-4]
                    plagiarism[contest][problem][-1].append(submission)
                    plagiarism[contest][problem][-1].append(percent)

    with open(result_path, "w") as file:
        for contest in plagiarism:
            for problem in plagiarism[contest]:
                for arr in plagiarism[contest][problem]:
                    file.write(contest + ',' + problem + ',' + ','.join(arr) + '\n')
