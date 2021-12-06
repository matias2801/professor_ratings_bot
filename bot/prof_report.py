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
        # ^ This targets the outermost DOM element that contains all of the elements that hold our relevant data
        # The object that is returned by pull_teacher_cards() is iterable

    def pull_prof_info(self):
        data_collection = []
        for card in self.teacher_cards:
            prof_name = card.find_element(
                By.CSS_SELECTOR,
                'div[class="CardName__StyledCardName-sc-1gyrgim-0 cJdVEK"]'
            ).get_attribute('innerHTML').strip()
            mod_prof_name = prof_name.translate(str.maketrans('','', string.punctuation))
            # ^ this gets rid of the extra characters that are included in the innerHTML around the professor names

            rating = card.find_element(
                By.CSS_SELECTOR,
                'div[class="TeacherCard__NumRatingWrapper-syjs0d-2 joEEbw"]'
            ).get_attribute('innerHTML').strip()
            number_rating = re.findall('[0-9]\\.[0-9]', rating)
            # ^ this creates a list of matches in the rating object in the form of '1.0', '3.5', etc.
            # the list should have a length of one. Even it it does not, we only need to reference the first item in the
            # list to get our rating.

            subject = card.find_element(
                By.CSS_SELECTOR,
                'div[class="CardSchool__Department-sc-19lmz2k-0 haUIRO"]'
            ).get_attribute('innerHTML')

            # using this condition will exclude professors who have not received any ratings from the dataset
            # (or professors who have an overall ratting of 0.0, if they exist):
            if number_rating[0] == '0.0':
                pass
            else:
                data_collection.append(
                    [mod_prof_name, number_rating[0], subject]
                )

            # we can make this more specific and meaningful later by pulling the number of ratings each professor has
            # received

        return data_collection

    # root > div > div > div.SearchResultsPage__StyledSearchResultsPage-sc-1srop1v-0.kdXwyM > div.SearchResultsPage__SearchResultsWrapper-sc-1srop1v-1.gsOeEv > div:nth-child(2) > a:nth-child(2) > div > div.TeacherCard__NumRatingWrapper-syjs0d-2.joEEbw > div > div.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2.kMhQxZ