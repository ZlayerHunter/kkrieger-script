import cv2
import pyautogui as pag
import numpy as np
from time import sleep
import win32gui, win32ui, win32con
import sys
import os

# Описание применения скрипта
text = '''
Для работы программы:
    1) Запуск скрипта должен быть произведен от имени администратора.
    2) Fraps должен быть установлен в папку по умолчанию C:/Fraps/fraps.exe или измените 112 строку.
    3) Необходимо указать существующие папки.
Необходимо указать путь до корневого каталога или до исполняемого файла игры "pno0001.exe".
        Примеры:
   - script.py D:/Games/kkrieger
   - script.py D:/Games/kkriger/pno0001.exe
При использовании ключа(им можно пренебречь) "-o" необходимо указать путь до сохранения скриншотов и файла со средним FPS.
Если ключ будет отсутствовать или будет пустым, то файлы сохранятся в корневом каталоге игры.
        Примеры:
   - script.py D:/Games/kkrieger -o D:/output_path/kkrieger
   - script.py D:/Games/kkriger/pno0001.exe -o D:/output_path/kkrieger
   - script.py D:/Games/kkrieger D:/output_path/kkrieger
   - script.py D:/Games/kkriger/pno0001.exe D:/output_path/kkrieger'''

# Описание аргументов скрипта
if __name__ == "__main__":
    # Проверка на нулевые аргументы
    if len(sys.argv) == 1:
        print(text)
        sys.exit(1)

    # Проверка на верно указанный путь к файлу по 1-му аргументу
    if len(sys.argv) >= 2:
        path_game = os.path.abspath(sys.argv[1])
        if os.path.exists(path_game):
            if path_game[-11:] == 'pno0001.exe':
                path_output_files = path_game[:-11]
            else:
                path_output_files = path_game
                path_game = path_game + '\\pno0001.exe'
        else:
            print(text)
            sys.exit(1)
    
    # Проверка на ключ или указания каталога для загрузки файлов 2-ым аргументом
    if len(sys.argv) >= 3:
        if sys.argv[2].strip() == '-o':
            path_output_files = path_game[:-11]
        else:
            path_output_files = os.path.abspath(sys.argv[2])
            if os.path.exists(path_output_files):
                pass
            else:
                print(text)
                sys.exit(1)

    # Проверка на ключ или указания каталога для загрузки файлов 3-им аргументом
    if len(sys.argv) == 4:
        path_output_files = os.path.abspath(sys.argv[3])
        if os.path.exists(path_output_files):
            pass
        else:
            print(text)
            sys.exit(1)

# Функция захвата изображения
def window_capture():
    # Разрешение окна игры
    w = 1024
    h = 512
    hwnd = None
    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 128), win32con.SRCCOPY)
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)
    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return img

# Входные метки
print('Начинаем начинать!')
print('Наслаждаемся и ничего не трогаем')
check_logo = False
check_start_lobby = False
check_screenshot_1 = False
check_run = False
check_finish = False
check_fraps = False

# Подсчет количества поворотов до 5, 196 строка подсчета
check_rotate = 0

# Запуск программы записи FPS и пропуск программы при неудачи
try:
    print('Запуск программы Fraps')
    os.startfile('C:\\Fraps\\Fraps.exe')
except:
    print('Установите Fraps в папку по умолчанию')
    check_logo = True
    check_start_lobby = True
    check_screenshot_1 = True
    check_run = True
    check_finish = True
    check_fraps = True
    sys.exit(1)
fps = 'FRAPS fps'

# Ожидание загрузки Fraps
while not win32gui.FindWindow(None, fps):
    pass
sleep(2)

# Запуск игры
if not check_fraps:
    print('Запуск игры Kkrieger')
    os.startfile(path_game)
game_win = 'kk'

# Ожидание загрузки игры
while not win32gui.FindWindow(None, game_win):
    pass
sleep(2)

# Сохранение предыдущих кадров
frames = []

# Запуск основного цикла
sleep(5)
print('Это не ошибка (:')
pag.getWindowsWithTitle(game_win)[0].activate()
while True:
    # Изображение в текущей итерации
    game_cap = np.array(window_capture())
    
    # Сохранение последних 15 фреймов для проверки поворота
    frames.append(game_cap)
    frames = frames[-20:]

    # Ожидание LOGO игры, переход в главное меню и запуск сессии
    if not check_logo:
        img = cv2.cvtColor(game_cap, cv2.COLOR_RGB2GRAY)
        blackscreen = cv2.cvtColor(np.zeros((512,1024,3), np.uint8), cv2.COLOR_RGB2GRAY)
        # Инициализация загрузки игры
        if cv2.matchTemplate(img, blackscreen, cv2.TM_SQDIFF)[0][0] > 3025915400.0:
            # Прерывание начального лого для перехода в главное меню
            print('Script pressed enter 2 times')
            pag.keyDown('enter')
            pag.keyUp('enter')
            # Вход в игровую сессию
            pag.keyDown('enter')
            pag.keyUp('enter')
            # Обработка меток
            check_logo = True
            check_start_lobby = True

    # Вход в игровую сессию и 
    if check_start_lobby:
        if not check_screenshot_1:
            sleep(0.3)
            # Cнятие начального скриншота
            print('Сохранение первого скриншота:' + path_output_files + '\\screenshot_1.jpg')
            cv2.imwrite(path_output_files + '\\screenshot_1.jpg', np.array(window_capture()))
            # Начало записи FPS
            pag.keyDown('f11')
            pag.keyUp('f11')
            sleep(0.3)
            # Обработка метки
            check_screenshot_1 = True

        # Начать движение вперед
        if not check_run:
            print('Я иду вперед')
            pag.keyDown('w')
            sleep(0.2)
            # Обработка метки
            check_run = True
        
        # Поворот налево при неизменении изображения
        char_rotate = cv2.matchTemplate(frames[0][100:450, 320:1024-320], 
                                        frames[len(frames) - 1][100:450, 320:1024-320], 
                                        cv2.TM_CCOEFF_NORMED)[0][0]
        if char_rotate > 0.95:
            # Подсчет количества поворотов и выход при достижении 5 поворотов
            check_rotate += 1
            print('Поворот № ' + str(check_rotate))
            pag.moveRel(-50, 0, 0.06)
            if check_rotate > 4:
                # Обработка меток
                print('Я устал идти вперед')
                pag.keyUp('w')
                # Обработка меток
                check_in_lobby = False
                check_finish = True
    
    # Завершение игровой сессии
    if check_finish:
        # Окончание записи ФПС
        pag.keyDown('f11')
        pag.keyUp('f11')
        # Cнятие последнего скриншота
        print('Сохранение последнего скриншота:' + path_output_files + '\\screenshot_2.jpg')
        cv2.imwrite(path_output_files + '\\screenshot_2.jpg', np.array(window_capture()))
        # Выход из игры
        print('Нажатие на кнопку Escape')
        pag.keyDown('escape')
        pag.keyUp('escape')
        print('Нажатие на кнопку Вниз')
        pag.keyDown('down')
        pag.keyUp('down')
        print('Нажатие на кнопку Вниз')
        pag.keyDown('down')
        pag.keyUp('down')
        print('Нажатие на кнопку Enter')
        pag.keyDown('enter')
        pag.keyUp('enter')
        print('Нажатие на кнопку Вниз')
        pag.keyDown('down')
        pag.keyUp('down')
        print('Нажатие на кнопку Вниз')
        pag.keyDown('down')
        pag.keyUp('down')
        print('Нажатие на кнопку Enter')
        pag.keyDown('enter')
        pag.keyUp('enter')
        break
    
    # Проверка на самостоятельный выход из игры
    # И завершение всех процессов
    if not win32gui.FindWindow(None, game_win):
        os.system("taskkill /IM pno0001.exe /F")
        os.system("taskkill /IM Fraps.exe /F")
        os.system("taskkill /IM fraps64.dat /F")
        sys.exit(1)

# Запись среднего ФПС за сессию в файл
print('Сохранение среднего FPS в файле:' + path_output_files + '\\output.txt')
with open('C:\\Fraps\\FRAPSLOG.TXT', 'r') as file:
    text_tmp = file.readlines()[-2].split()[7]
    with open(path_output_files + '\\output.txt', 'a+', encoding="utf-8") as file_output:
        file_output.write('Количество среднего FPS: ' + text_tmp + '\n')

# Завершить вызванные процессы повторно (на всякий случай), если что-то пошло не так.
os.system("taskkill /IM pno0001.exe /F")
os.system("taskkill /IM Fraps.exe /F")
os.system("taskkill /IM fraps64.dat /F")
print('Конец')
sys.exit(1)
