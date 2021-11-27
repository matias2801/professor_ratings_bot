from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import re
import string


class ProfessorReport:
    def __init__(self, professor_card_elements: WebElement):
        self.professor_card_elements = professor_card_elements
        self.teacher_cards = self.pull_teacher_cards()

    def pull_teacher_cards(self):
        return self.professor_card_elements.find_elements(
            By.CSS_SELECTOR,
            'a[class="TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"]'
        )

    def pull_prof_info(self):
        data_collection = []
        for card in self.teacher_cards:
            prof_name = card.find_element(
                By.CSS_SELECTOR,
                'div[class="CardName__StyledCardName-sc-1gyrgim-0 cJdVEK"]'
            ).get_attribute('innerHTML').strip()
            mod_prof_name = prof_name.translate(str.maketrans('','', string.punctuation))
            '''c = re.compile('[^<!->]')
            x = c.findall(prof_name)
             ''.join(x)'''

            rating = card.find_element(
                By.CSS_SELECTOR,
                'div[class="TeacherCard__NumRatingWrapper-syjs0d-2 joEEbw"]'
            ).get_attribute('innerHTML').strip()
            number_rating = re.findall('[0-9]\\.[0-9]', rating)

            subject = card.find_element(
                By.CSS_SELECTOR,
                'div[class="CardSchool__Department-sc-19lmz2k-0 haUIRO"]'
            ).get_attribute('innerHTML')

            data_collection.append(
                [mod_prof_name, number_rating[0], subject]
            )
        return data_collection

    # root > div > div > div.SearchResultsPage__StyledSearchResultsPage-sc-1srop1v-0.kdXwyM > div.SearchResultsPage__SearchResultsWrapper-sc-1srop1v-1.gsOeEv > div:nth-child(2) > a:nth-child(2) > div > div.TeacherCard__NumRatingWrapper-syjs0d-2.joEEbw > div > div.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2.kMhQxZ