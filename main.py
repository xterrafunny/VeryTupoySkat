from src.downloader import Downloader
from src.to_csv import to_csv
from src.moss_processor import moss_process
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", help="Path to file with login and password", default="login")
    parser.add_argument("--contests", help="Path to file with contest id's", default="contests")
    parser.add_argument("--browser", help="Browser to use", default="Safari")
    parser.add_argument("--submissions", help="Folder to store submissions", default="data")
    parser.add_argument("--url", help="URL to codeforces contest with '{}' where id should be", required=True)
    parser.add_argument("--moss_id", help="Moss ID to use", required=True)
    parser.add_argument("--output_csv", help="Output csv file path", default="result.csv")
    parser.add_argument("--resource_path", help="Path to Chromedriver", default="/usr/local/bin/chromedriver")
    args = parser.parse_args()

    with open(args.login) as login_file:
        lines = login_file.readlines()
        login = lines[0].strip()
        password = lines[1].strip()

    with open(args.contests) as contest_file:
        contests = []
        for line in contest_file.readlines():
            stripped = line.strip()
            if len(stripped) > 0:
                contests.append(stripped)

    print(login, password, contests, args.browser, args.submissions, args.url, args.moss_id, args.output_csv, sep='\n')

    downloader = Downloader(login, password, contests, args.url, args.browser, args.submissions)

    moss_process(args.submissions, args.moss_id)
