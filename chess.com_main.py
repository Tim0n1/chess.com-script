import first_page_operations
import chess_engine
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import multiprocessing
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time
import threading

driver = first_page_operations.driver
time.sleep(2)
pieces_color = ''
numeration = 0
moves_to_chesscom_moves_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
pattern = re.compile(r'piece [wb]. square\-\d\d')

def get_pieces_color():
    while True:
        global pieces_color
        time.sleep(0.1)
        # element = WebDriverWait(driver, timeout=100)
        # element = element.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tab="game"]')))
        try:
            element2 = driver.find_element(By.CSS_SELECTOR, 'div[data-tab="game"]')
            element2 = element2.find_element(By.CSS_SELECTOR, 'span[class="tabs-label"]')
            if element2.text == 'Play' or 'Играй':
                result = driver.find_element(By.CSS_SELECTOR, 'text[y="99"]').text
                if result == 'a':
                    print('You are playing white!')
                    pieces_color = 'w'
                    return pieces_color
                else:
                    print('You are playing black!')
                    pieces_color = 'b'
                    return pieces_color
        except Exception:
            print('element not visible')


class FigureLocation:
    def __init__(self):
        self.page_source = BeautifulSoup(driver.page_source, 'html.parser')
        #print(self.page_source)

    def all_current_positions(self):
        html_string = ''
        matches_list = []
        html_list = (self.page_source.find_all(class_=pattern))
        for i in html_list:
            html_string += str(i)
        matches = pattern.findall(html_string)
        for i in matches:
            matches_list.append(i)
        return matches_list


def extract_best_move(best_move):
    best_move_list = best_move.split('.')
    if best_move_list[2] != '':
        best_move = best_move_list[2].split(' ')[0]
        return best_move
    elif best_move != '':
        best_move = best_move_list[4].split(' ')[0]
        return best_move


def find_class(move):
    match = ''
    pattern2 = re.compile(f'^piece [bw]. square\-{move}$')
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    match = page_source.find_all(class_=pattern2)
    print(match)
    piece = driver.find_element(By.CSS_SELECTOR, f'div[class="{str(match)[13:31]}"')
    print(piece.get_attribute('class'))

    return piece
    #todo fix itttt FIXIIIXXIXXIXIXX ITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

def translate_best_move(best_move):
    if len(best_move) == 3:
        best_move = best_move[1:3]
        best_move = best_move.replace(best_move[0], str(moves_to_chesscom_moves_dict[best_move[0]]))
        return best_move
    if len(best_move) == 2:
        best_move = best_move.replace(best_move[0], str(moves_to_chesscom_moves_dict[best_move[0]]))
        return best_move


def make_move(result, best_move):
    previous_move = result[1]
    previous_move = translate_best_move(previous_move)
    best_move = translate_best_move(extract_best_move(best_move))
    previous_move = find_class(previous_move)
    previous_move.click()
    # best_move = find_class(best_move)
    # best_move.click()
    #TODO FIX PREVIOUS MOVE DA E PREVIOUS MOVE NA BEST MOVA


def check_for_end():
    element = WebDriverWait(driver, timeout=100000)
    element = element.until(EC.presence_of_element_located((By.CLASS_NAME, "game-over-modal-content")))
    if element:
        return print('GG')


def start_new_game():
    first_page_operations.start_game.click()
    flag = False
    #p1 = multiprocessing.Process() for future performance updates
    t1 = threading.Thread(target=get_pieces_color)
    t2 = threading.Thread(target=check_for_end)
    t1.start()
    t2.start()

    global numeration
    numeration = 0

    while True:

        if flag == False:

            previous_move = FigureLocation().all_current_positions()
        current_move = FigureLocation().all_current_positions()
        #time.sleep(1)
        if previous_move != current_move:
            current_moves = []
            for i in previous_move:
                for j in current_move:
                    if j not in previous_move and j not in current_moves:
                        current_moves.append(j)
                    if i not in current_move and i not in current_moves:
                        current_moves.append(i)
            if current_moves != []:
                move = chess_engine.EngineConnector(current_moves).send_move()
                numeration += 1
                print(numeration)
                time.sleep(0.5)
                best_move = chess_engine.EngineOperations(chess_engine.driver).find_the_best_move()
                print(best_move)
                if (pieces_color == 'w' and numeration % 2 == 0) or (pieces_color == 'b' and numeration % 2 == 1):
                    print('making move')
                    make_move(move, best_move)
        flag = True
        previous_move = current_move


start_new_game()

#class="game-over-modal-content" - endgame prozorec
