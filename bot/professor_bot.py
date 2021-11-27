import bot.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
import re, time
from bot.prof_report import ProfessorReport
from prettytable import PrettyTable
from selenium.webdriver.common.keys import Keys



class ProfessorBot(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        super(ProfessorBot, self).__init__()
        self.implicitly_wait(30)
        '''In an inherited subclass, a parent class can be referred to with the use of the super() function.
         The super function returns a temporary object of the superclass that allows access to all of its methods to its
          child class.'''

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def close_pop_up(self):
        close_button = self.find_element(
            By.CSS_SELECTOR,
            'div[tabindex="-1"]'
        ).find_element(
            By.CSS_SELECTOR,
            'button'
        )
        close_button.click()

    def select_school(self):
        searh_bar = self.find_element(
            By.CSS_SELECTOR,
            'input[placeholder="Your school"]'
        )
        school_name_keys = input("Enter the full name of your school.\n"
                            "E.g., georgia state university: ")
        searh_bar.send_keys(f'{school_name_keys}')

        dropdown = self.find_element(
            By.CLASS_NAME,
            "SearchTypeahead__StyledSearchTypeaheadDropdown-sc-1i57108-0"
        )

        go_to_school = dropdown.find_element(
            By.CSS_SELECTOR,
            f'a[aria-label="School page for {school_name_keys}"]'
        )
        go_to_school.click()

    def view_top_professors(self):
        element = self.find_element(
            By.CSS_SELECTOR,
            'span[class="hidden-sm"]'
            )
        element.click()

    def get_all_professor_info(self):
        number_element = self.find_element(
            By.CSS_SELECTOR,
            'div[class="SearchResultsPage__SearchResultsPageHeader-sc-1srop1v-3 flHcYr"]'
        )
        innerHTML = number_element.find_element(
            By.CSS_SELECTOR,
            'h1'
        ).get_attribute('innerHTML')

        # fix this later to allow for 3-digit numbers
        match = re.findall("[0-9][0-9][0-9][0-9]", innerHTML)
        num = match[0]
        print(num)
        see_more = self.find_element(
            By.CSS_SELECTOR,
            'button[class="Buttons__Button-sc-19xdot-1 PaginationButton__StyledPaginationButton-txi1dr-1 gjQZal"]'
        )

        # for testing purposes we will only do the first 48 results
        for i in range(5):
            see_more.click()
            time.sleep(.8)

        '''iter_num = int(round(num/8, 0))
        for i in range(iter_num):
            try:
                see_more.click()
                time.sleep(.8)
            except:
                pass'''

    def report_results(self):
        professor_list = self.find_element(
            By.CSS_SELECTOR,
            'div[class="SearchResultsPage__SearchResultsWrapper-sc-1srop1v-1 gsOeEv"]'
        )
        report = ProfessorReport(professor_list)
        table = PrettyTable(
            field_names=['Professor Name', 'Rating', 'Subject']
        )
        table.add_rows(report.pull_prof_info())
        print(table)

        #print(school_name_selection)
        #print(dropdown.get_attribute("innerHTML"))





