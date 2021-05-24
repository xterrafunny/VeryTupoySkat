import re
from argparse import ArgumentParser
from os import listdir, path


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
            with open(path.join(
                    path_to_data,
                    "{}/{}".format(problem_dir, file)), 'r') as current:
                content = ''.join(current.readlines())
                # if problem_dir == "314449-A" and file == "match39-top.html":
                #     print(content)
                contestants = re.findall(r"\d{6}-\w-.{1,50}\.cpp \(\d+%\)",
                                         content)
                if problem_dir == "314449-A" and file == "match39-top.html":
                    print(contestants)
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
                    file.write(contest + ',' + problem + ','
                               + ','.join(arr) + '\n')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data", help="Path to data/report/",
                        default="data/report")
    parser.add_argument("--output_csv", help="Output csv file path",
                        default="result.csv")
    args = parser.parse_args()
    to_csv(args.data, args.output_csv)
