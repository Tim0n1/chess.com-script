from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
#import threading
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get('https://woochess.com/en/analysis')



def translate_move(move):
    capital_second_letter = move[7].upper()
    translated_move = move[6] + capital_second_letter
    return translated_move

def translate_move_coordinate(move):
    coordinates = move[16:18]
    y = 9 - int(coordinates[1])
    x = int(coordinates[0])
    return [y, x]

def make_coordinate_batch(coordinates):
    engine = EngineOperations(driver)
    if coordinates == '':
        return coordinates
    current_location = list(coordinates[1].values())[0]
    next_move = list(coordinates[0].values())[0]
    current_location = engine.find_element(current_location)
    next_move = engine.find_element(next_move)
    batch = [current_location, next_move]
    return batch

class EngineOperations:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, coordinates):
        source = BeautifulSoup(self.driver.page_source, 'html.parser')
        elements = source.find_all(class_="row-5277c")[
            int(coordinates[0]) - 1].children
        elements = list(elements)
        element = str(elements[int(coordinates[1]) - 1]).split(';')[0]
        element_current_location = element[44:46]
        return element_current_location

    def click_on_element(self, coordinates):
        current_location = ''
        next_move = ''
        batch = ''

        if len(coordinates) == 2:
            batch = make_coordinate_batch(coordinates)
        if len(coordinates) == 3:
            for j in range(1, 3):
                if list(coordinates[0].values()) == list(coordinates[j].values()):
                    coordinates.pop(j)
                    break
            batch = make_coordinate_batch(coordinates)

        if len(coordinates) == 4:
            king_abreviation = ['bK', 'wK']
            king_moves = []
            for i in coordinates:
                if list(i.keys())[0] in king_abreviation:
                    king_moves.append(i)
            batch = make_coordinate_batch(king_moves)
            print(king_moves)
        return batch

    def drag_piece(self, coordinates):
        previous_square = coordinates[0]
        next_square = coordinates[1]
        previous_piece_location = self.driver.find_element(By.CSS_SELECTOR, f'div[data-square="{previous_square}"]')
        next_piece_location = self.driver.find_element(By.CSS_SELECTOR, f'div[data-square="{next_square}"]')
        ActionChains(self.driver).drag_and_drop(previous_piece_location, next_piece_location).perform()

    def find_the_best_move(self):
        element = self.driver.find_element(By.CSS_SELECTOR, 'p[id="result-line"]')
        if element.text[0:5] == '+1000':
            return 'Mate in 1!'
        return element.text



class EngineConnector:
    def __init__(self, move_info):
        self.move_info = move_info

    def send_move(self):
        engine = EngineOperations(driver)
        result = ''
        full_translated_moves = []
        for i in self.move_info:
            piece_name = translate_move(i)
            piece_coordinate = translate_move_coordinate(i)
            full_translated_moves.append({piece_name: piece_coordinate})

        result = EngineOperations(driver).click_on_element(full_translated_moves)
        if result == '':
            return []
        print(result)
        engine.drag_piece(result)
        return result






#EngineConnector(['piece br square-68', 'piece br square-88', 'piece bk square-78', 'piece bk square-58']).send_move()
#['piece br square-68', 'piece br square-88', 'piece bk square-78', 'piece bk square-58'] - black
#['piece wr square-61', 'piece wk square-71', 'piece wr square-81', 'piece wk square-51'] white
