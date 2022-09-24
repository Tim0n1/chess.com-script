import first_page_operations
import chess_engine
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time
import threading


driver = first_page_operations.driver
time.sleep(2)

class FigureLocation:
    def __init__(self):
        self.page_source = BeautifulSoup(driver.page_source, 'html.parser')
        self.pattern = re.compile(r'piece [wb]. square\-\d\d')
        #print(self.page_source)

    def all_current_positions(self):
        html_string = ''
        matches_list = []
        html_list = (self.page_source.find_all(class_=self.pattern))
        for i in html_list:
            html_string += str(i)
        matches = self.pattern.findall(html_string)
        for i in matches:
            matches_list.append(i)
        return matches_list

    def get_pieces_color(self):
        time.sleep(2)
        result = driver.find_element(By.CSS_SELECTOR, 'text[y="99"]').text
        if result == 'a':
            print('You are playing white!')
            return 'w'
        else:
            print('You are playing black!')
            return 'b'



first_page_operations.start_game.click()
flag = False

t1 = threading.Thread(target=FigureLocation().get_pieces_color)
t1.start()


while True:
    current_moves = []
    if flag == False:

        previous_move = FigureLocation().all_current_positions()
    time.sleep(0.5)
    current_move = FigureLocation().all_current_positions()
    if previous_move != current_move:
        current_moves = []
        for i in previous_move:
            for j in current_move:
                if j not in previous_move and j not in current_moves:
                    current_moves.append(j)
                if i not in current_move and i not in current_moves:
                    current_moves.append(i)

        print(f'opa {current_moves}')
        move = chess_engine.EngineConnector(current_moves).send_move()
        #todo connect the main and the engine
    flag = True
    previous_move = current_move



