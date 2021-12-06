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
        self.implicitly_wait(45)
        '''In an inherited subclass, a parent class can be referred to with the use of the super() function.
         The super function returns a temporary object of the superclass that allows access to all of its methods to its
          child class. In this instance, it makes webdriver accessible to all of our methods.'''

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

    def get_school(self):
        school_name = input("Enter the name of your school as it shows up on ratemyprofessors.com.\n"
                            "Examples: 'Harvard University' or 'Georgia State University'\n"
                            "Your school: ")
        return school_name

    def select_school(self):
        searh_bar = self.find_element(
            By.CSS_SELECTOR,
            'input[placeholder="Your school"]'
        )
        school = self.get_school()
        searh_bar.send_keys(f'{school}')

        dropdown = self.find_element(
            By.CLASS_NAME,
            "SearchTypeahead__StyledSearchTypeaheadDropdown-sc-1i57108-0"
        )

        go_to_school = dropdown.find_element(
            By.CSS_SELECTOR,
            f'a[aria-label="School page for {school}"]'
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

        match = re.findall('[^\\D\\s]', innerHTML)  # pull the number of professors for the school page we're on
        num = int(''.join(match))
        print(num)

        see_more = self.find_element(
            By.CSS_SELECTOR,
            'button[class="Buttons__Button-sc-19xdot-1 PaginationButton__StyledPaginationButton-txi1dr-1 gjQZal"]'
        )

        iter_num = num//8
        print(iter_num)
        for i in range(iter_num):  # press "Show More" until all professors are showing
            see_more.click()
            time.sleep(0.65)

    def make_file(self):  # user input for filename to be used for our .py and .txt files
        file_name = input('Enter the name of your export file: ')
        return file_name

    def report_results(self):
        professor_list = self.find_element(
            By.CSS_SELECTOR,
            'div[class="SearchResultsPage__SearchResultsWrapper-sc-1srop1v-1 gsOeEv"]'
        )
        report = ProfessorReport(professor_list)
        table = PrettyTable(
            field_names=['Professor Name', 'Rating', 'Subject']
        )

        all_data = report.pull_prof_info()
        table.add_rows(all_data)

        file_name = self.make_file()

        with open(f'{file_name}.txt', 'w') as export:
            export.write(f'{table}')
        with open(f'{file_name}.py', 'w') as list_data:
            list_data.write(f'{all_data}')

        #print(school_name_selection)
        #print(dropdown.get_attribute("innerHTML"))





