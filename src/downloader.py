from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import clipboard


class Downloader:
    def _select_driver(self, browser):
        self.driver = None
        if browser == "Chrome":
            self.driver = webdriver.Chrome()
        elif browser == "Firefox":
            self.driver = webdriver.Firefox()
        elif browser == "Opera":
            self.driver = webdriver.Opera()
        elif browser == "Safari":
            self.driver = webdriver.Safari()
        elif browser == "IE":
            self.driver = webdriver.Ie()
        else:
            raise Exception("Browser {} is not supported".format(browser))

    def _get_current_cf_login(self):
        lang_chooser = self.driver.find_element_by_class_name("lang-chooser")
        login = lang_chooser.find_elements_by_tag_name("div")[1]. \
            find_elements_by_tag_name("a")[0].text
        if login == "Enter":
            return None
        else:
            return login

    def _logout(self):
        lang_chooser = self.driver.find_element_by_class_name("lang-chooser")
        logout_button = lang_chooser.find_elements_by_tag_name("div")[1]. \
            find_elements_by_tag_name("a")[1]
        if logout_button.text == "Register":
            return
        else:
            logout_button.click()

    def _login(self, user, password):
        self.driver.get("http://codeforces.com/enter?locale=en")

        def load_correct(driver: webdriver.Chrome):
            current_page = driver.current_url.split('/')[3]
            current_page = current_page.split('?')[0]
            return current_page in ("profile", "enter")

        WebDriverWait(self.driver, self.timeout).until(load_correct)
        page = self.driver.current_url.split('/')[3].split('?')[0]
        if page == "profile":
            current_user = self.driver.title.split()[0]
            if current_user == user:
                return
            else:
                self._logout()
                self._login(user, password)
        if page == "enter":
            login_field = self.driver.find_element_by_id("handleOrEmail")
            login_field.send_keys(user)
            password_field = self.driver.find_element_by_id("password")
            password_field.send_keys(password)
            self.driver.find_element_by_class_name("submit").click()

            def login_correct(driver: webdriver.Chrome):
                try:
                    driver.find_element_by_id("sidebar")
                except:
                    return False
                return True

            WebDriverWait(self.driver, self.timeout).until(login_correct)

    def _parse_contests(self,
                        contest_list_path: str):
        self.contests = []
        with open(contest_list_path, "r") as contests:
            for line in contests.readlines():
                self.contests.append(line.strip())

    def _process_page(self,
                      page_index: int,
                      participants: dict,
                      contest: str):
        url = self.template.format(
            contest + "/status/page/{}?order=BY_JUDGED_DESC".format(page_index)
        )
        self.driver.get(url)

        def check_current_page(driver: webdriver.Chrome):
            nonlocal page_index
            active_page = driver.find_element_by_class_name("active")
            return int(active_page.get_attribute("pageindex")) == page_index

        WebDriverWait(self.driver, self.timeout).until(check_current_page)
        table = self.driver.find_element_by_class_name(
            "status-frame-datatable"
        )
        rows = table.find_elements_by_tag_name("tr")
        for row in rows:
            if row.get_attribute("class") == "first-row":
                continue
            try:
                row.find_element_by_class_name("verdict-accepted")
            except:
                continue

            submission_id = row.get_attribute("data-submission-id")
            columns = row.find_elements_by_tag_name("td")
            name = str(columns[2].find_element_by_tag_name("a").text).strip()
            problem = str(
                columns[3].find_element_by_tag_name("a").text
            ).strip()
            problem = problem.split()[0]
            if participants.get((name, problem)) is None:
                participants[(name, problem)] = submission_id

    def _download_submission(self,
                             contest: str,
                             name: str,
                             problem: str,
                             submission_id: str):
        self.driver.get(self.template.format(
            contest + "/submission/{}".format(submission_id)
        ))

        def load_correct(driver: webdriver.Chrome):
            nonlocal submission_id
            return submission_id == driver.title.split()[1][1:]

        WebDriverWait(self.driver, self.timeout).until(load_correct)
        while clipboard.paste() == "":
            copy_elem = self.driver.find_element_by_class_name("caption")
            copy_elem.find_elements_by_tag_name("div")[1].click()
        with open("{}/{}-{}-{}.txt".format(self.store_path,
                                           contest,
                                           problem, name), "w") as sol:
            sol.write(clipboard.paste())
            clipboard.copy("")

    def _process_contest(self,
                         contest: str):
        def get_manager_button(driver: webdriver.Chrome):
            try:
                return driver.find_element_by_class_name("toggleMashupManager")
            except:
                return None

        self.driver.get(self.template.format(contest))

        def dashboard_load_correct(driver: webdriver.Chrome):
            nonlocal get_manager_button
            return get_manager_button(driver) is not None

        WebDriverWait(self.driver, self.timeout).until(dashboard_load_correct)
        button = get_manager_button(self.driver)
        if button.text == "Enable manager mode":
            button.click()
            self._process_contest(contest)
        self.driver.get(self.template.format(contest + "/status"))

        def status_load_correct(driver: webdriver.Chrome):
            return driver.title.split()[0] == "Status"

        WebDriverWait(self.driver, self.timeout).until(status_load_correct)
        page_index = self.driver.find_elements_by_class_name("page-index")
        pages_cnt = int(page_index[-1].get_attribute("pageindex"))
        participants = dict()
        for page_idx in range(1, pages_cnt + 1):
            self._process_page(page_idx, participants, contest)

        for (name, problem) in participants:
            self._download_submission(contest, name, problem,
                                      participants[(name, problem)])

    def __init__(self,
                 user: str,
                 password: str,
                 contest_list_path: str,
                 contest_url_template: str = "http://codeforces.com",
                 browser: str = "Chrome",
                 store_path: str = "data"):

        self.timeout = 100
        self.store_path = store_path
        self._parse_contests(contest_list_path)
        self._select_driver(browser)
        self._login(user, password)
        self.template = contest_url_template
        clipboard.copy("")
        for contest in self.contests:
            self._process_contest(contest)
        self.driver.close()
