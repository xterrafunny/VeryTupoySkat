from src.downloader import Downloader
from src.to_csv import to_csv
from src.moss_processor import moss_process
import sys

if __name__ == "__main__":
    idx = 1
    login_file = "login"
    contests_file = "contests"
    url = ["https://codeforces.com/", "/contest/{}?locale=en"]
    browser = "Safari"
    data = "data"
    moss_id = None
    csv_path = None
    while idx < len(sys.argv):
        if sys.argv[idx][0] == '-':
            if idx + 1 >= len(sys.argv):
                raise ValueError(
                    "{} passed without parameter".format(sys.argv[idx])
                )
            param = sys.argv[idx][1:]
            if param == "login":
                login_file = sys.argv[idx + 1]
                idx += 1
            elif param == "contests":
                contests_file = sys.argv[idx + 1]
                idx += 1
            elif param == "browser":
                browser = sys.argv[idx + 1]
                idx += 1
            elif param == "data":
                data = sys.argv[idx + 1]
                idx += 1
            elif param == "group":
                url = "group/{}".format(sys.argv[idx + 1]).join(url)
                idx += 1
            elif param == "mossId":
                moss_id = int(sys.argv[idx + 1])
                idx += 1
            elif param == "csvPath":
                csv_path = sys.argv[idx + 1]
                idx += 1
            else:
                raise ValueError("Bad argument parameter '{}'".format(param))
        idx += 1

    with open(login_file, 'r') as user_file:
        user = user_file.readline()[:-1]
        password = user_file.readline()[:-1]
    print(user, password, contests_file, url, browser, data)
    downloader = Downloader(user,
                            password,
                            contests_file,
                            url,
                            browser,
                            data)

    if moss_id is None:
        exit(0)

    moss_process(data, moss_id)

    if csv_path is not None:
        to_csv(data + "/report", csv_path)
