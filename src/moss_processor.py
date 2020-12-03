import mosspy
from os import listdir, system


def moss_process(submission_path: str,
                 moss_id):
    def process_problem(contest: str,
                        problem: str):
        nonlocal submission_path
        moss = mosspy.Moss(moss_id, "python")
        moss.addFilesByWildcard("{}/{}-{}-*".format(submission_path, contest, problem))
        url = moss.send()
        moss.saveWebPage(url, "{}/{}-{}.html".format(submission_path, contest, problem))
        mosspy.download_report(url, "{}/report/{}-{}/".format(submission_path, contest, problem),
                               connections=20, log_level=10)
        system("rm {}/{}-{}.html".format(submission_path, contest, problem))

    submissions = listdir("{}/".format(submission_path))
    processed = set()
    idx = 0
    for file in submissions:
        temp = file.split("-")
        current_contest = temp[0]
        current_problem = temp[1]
        if (current_contest, current_problem) in processed:
            continue
        process_problem(current_contest, current_problem)
        processed.add((current_contest, current_problem))
