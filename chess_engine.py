from selenium import webdriver
from bs4 import BeautifulSoup
import threading
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
    current_location = list(coordinates[1].values())[0]
    next_move = list(coordinates[0].values())[0]
    current_location = EngineOperations(driver).find_element(current_location)
    next_move = EngineOperations(driver).find_element(next_move)
    batch = [current_location, next_move]
    return batch

class EngineOperations:
    def __init__(self, driver):
        self.driver = driver
        self.page_source = BeautifulSoup(driver.page_source, 'html.parser')

    def find_element(self, coordinates):
        elements = self.page_source.find_all(class_="row-5277c")[
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
            print(coordinates)
            for j in range(1, 3):
                if list(coordinates[0].values()) == list(coordinates[j].values()):
                    coordinates.pop(j)
                    break
            batch = make_coordinate_batch(coordinates)

        if len(coordinates) == 4:
            current_moves = coordinates[2:5]
            print(current_moves)
            next_move = coordinates[0:2]
            print(next_move)
            coordinates = [next_move[1], current_moves[1]]
            batch = make_coordinate_batch(coordinates)
            #print(coordinates)
        #driver_element = self.driver.find_element(By.)
        # for i in elements:
        #     print(i)
        #driver.find_element(By.)
        return batch




class EngineConnector:
    def __init__(self, move_info):
        self.move_info = move_info

    def send_move(self):
        result = ''
        full_translated_moves = []
        for i in self.move_info:
            piece_name = translate_move(i)
            piece_coordinate = translate_move_coordinate(i)
            full_translated_moves.append({piece_name: piece_coordinate})

        result = EngineOperations(driver).click_on_element(full_translated_moves)

        return print(result)

    def get_move(self):
        return self.move_info


EngineConnector(['piece br square-68', 'piece br square-88', 'piece bk square-78', 'piece bk square-58']).send_move()
#['piece br square-68', 'piece br square-88', 'piece bk square-78', 'piece bk square-58'] - black

