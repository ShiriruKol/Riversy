import copy

# Размер доски
SIZE_BOARD = 8

# Значение ячейки на доске
EMPTY = 0
BLACK = 1
WHITE = 2

# Для обозначения направлений
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

# Создание начальной доски
def initialize_board():
    # Инициализация пустой доски
    board = [[EMPTY for _ in range(SIZE_BOARD)] for _ in range(SIZE_BOARD)]
    # Расставление начальных фишек
    mid = SIZE_BOARD // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid] = WHITE
    board[mid - 1][mid] = BLACK
    board[mid][mid - 1] = BLACK
    return board

# Отрисовка доски
def print_brd(board):
    # Вывод буквенных обозначений столбцов
    print("  ", end="")
    for i in range(SIZE_BOARD):
        print(chr(ord('a') + i), end=" ")
    print()
    # Вывод номеров строк и значений клеток
    for i in range(SIZE_BOARD):
        print(i + 1, end=" ")
        for j in range(SIZE_BOARD):
            if board[i][j] == EMPTY:
                print('.', end=" ")
            elif board[i][j] == BLACK:
                print('B', end=" ")
            else:
                print('W', end=" ")
        print()

# Проверка возможности хода для определенного цвета
def is_valid(board, row, col, color):
    # Проверка, что клетка пуста
    if board[row][col] != EMPTY:
        return False
    # Проверка в каждом направлении
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        # Проверка на нахождение в пределах доски
        if not (0 <= r < SIZE_BOARD and 0 <= c < SIZE_BOARD):
            continue
        # Проверка, что соседняя клетка - противник
        if board[r][c] == color:
            continue
        # Проход по направлению и поиск своей фишки
        while board[r][c] != EMPTY:
            r, c = r + dr, c + dc
            if not (0 <= r < SIZE_BOARD and 0 <= c < SIZE_BOARD):
                break
            # Если найдена своя фишка, ход валиден
            if board[r][c] == color:
                return True
    return False

# Переворот фишек при ходе
def make_flip(board, row, col, color):
    # Проверка валидности хода
    if not is_valid(board, row, col, color):
        return False
    # Установка фишки на доске
    board[row][col] = color
    # Переворот фишек в каждом направлении
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if not (0 <= r < SIZE_BOARD and 0 <= c < SIZE_BOARD):
            continue
        if board[r][c] == color:
            continue
        to_flip = []
        # Сбор фишек для переворота
        while board[r][c] != EMPTY:
            to_flip.append((r, c))
            r, c = r + dr, c + dc
            if not (0 <= r < SIZE_BOARD and 0 <= c < SIZE_BOARD):
                break
            if board[r][c] == color:
                # Переворот фишек
                for flip_r, flip_c in to_flip:
                    board[flip_r][flip_c] = color
                break
    return True

# Подсчет фишек на доске
def count_discs(board):
    # Подсчет черных и белых фишек на доске
    black_discs = sum(row.count(BLACK) for row in board)
    white_discs = sum(row.count(WHITE) for row in board)
    return black_discs, white_discs

# Получение доступных ходов для определенного цвета
def get_valid_moves(board, color):
    # Поиск всех доступных ходов для цвета
    valid_moves = []
    for i in range(SIZE_BOARD):
        for j in range(SIZE_BOARD):
            if is_valid(board, i, j, color):
                valid_moves.append((i, j))
    return valid_moves

def computer_move_easy(board, color):
    return minimax(board, 2, color)

def computer_move_hard(board, color):
    return minimax(board, 4, color)

# Реализация алгоритма минимакса для выбора оптимального хода.
def minimax(board, depth, color):

    # Если достигнута максимальная глубина или конец игры, возвращаем оценку текущей ситуации
    if depth == 0:
        return None, evaluate_board(board, color)

    # Получаем список всех доступных ходов для текущего игрока
    valid_moves = get_valid_moves(board, color)

    # Если нет доступных ходов, возвращаем оценку текущей ситуации
    if not valid_moves:
        return None, evaluate_board(board, color)

    # Инициализация лучшего хода и его оценки в зависимости от цвета игрока
    best_move = None
    if color == WHITE:
        best_score = float('inf')
        # Проходим по всем доступным ходам
        for move in valid_moves:
            # Создаем копию доски для тестирования хода
            test_board = copy.deepcopy(board)
            make_flip(test_board, move[0], move[1], color)
            # Рекурсивно вызываем минимакс для следующего уровня дерева
            _, score = minimax(test_board, depth - 1, 3 - color)
            
            # Если текущий ход дает лучшую оценку, обновляем лучший ход и оценку
            if score < best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('-inf')
        # Проходим по всем доступным ходам
        for move in valid_moves:
            # Создаем копию доски для тестирования хода
            test_board = copy.deepcopy(board)
            make_flip(test_board, move[0], move[1], color)
            # Рекурсивно вызываем минимакс для следующего уровня дерева
            _, score = minimax(test_board, depth - 1, 3 - color)
            
            # Если текущий ход дает лучшую оценку, обновляем лучший ход и оценку
            if score > best_score:
                best_score = score
                best_move = move
    
    # Возвращаем лучший ход и его оценку
    return best_move, best_score

# Подсчет черных и белых фишек на доске
def evaluate_board(board, color):
    black_discs, white_discs = count_discs(board)
    # Разница между числом фишек заданного цвета и противоположного цвета
    if color == BLACK:
        return black_discs - white_discs
    else:
        return white_discs - black_discs

def main():

    # Инициализация доски
    board = initialize_board()
    # Начальный игрок - черные
    current_player = BLACK

    print("Добро пожаловать в игру Реверси!")

    # Ввод уровня сложности
    difficulty = input("Выберите уровень сложности легкий(цифра \"1\")/сложный(цифра \"2\"): ").strip().lower()

    # Проверка корректности выбора уровня сложности
    while difficulty not in ['1', '2']:
        print("Некорректный выбор уровня сложности.")
        difficulty = input("Выберите уровень сложности легкий(цифра \"1\")/сложный(цифра \"2\"): ").strip().lower()

    while True:
        # Отображение текущего состояния доски
        print_brd(board)
        # Подсчет фишек для обоих цветов
        black_discs, white_discs = count_discs(board)
        print(f"Black: {black_discs}, White: {white_discs}")

        # Ход человека (черных)
        if current_player == BLACK:
            valid_moves = get_valid_moves(board, BLACK)
            if valid_moves:
                print("Ход черных:")
                print("Доступные ходы:", ', '.join([f'{chr(move[1] + ord("a"))}{move[0] + 1}' for move in valid_moves]))
                while True:
                    user_input = input("Введите ход (пример ввода \"a1\"): ").strip().lower()
                    if user_input == 'exit':
                        return
                    # Проверка корректности ввода
                    if len(user_input) != 2 or not user_input[0].isalpha() or not user_input[1].isdigit():
                        print("Некорректный ввод. Попробуйте снова.")
                        continue
                    col = ord(user_input[0]) - ord('a')
                    row = int(user_input[1]) - 1
                    # Проверка, что введенный ход допустим
                    if (row, col) in valid_moves:
                        make_flip(board, row, col, BLACK)
                        current_player = WHITE
                        break
                    else:
                        print("Недопустимый ход, попробуйте снова.")
            else:
                print("Черные пропускают ход.")
                current_player = WHITE
        # Ход компьютера (белых)
        else:
            # Выбор уровня сложности и хода компьютера
            if difficulty == '1':
                move, _ = computer_move_easy(board, WHITE)
            else:
                move, _ = computer_move_hard(board, WHITE)

            if move:
                print(f"Компьютер выбрал ход: {chr(move[1] + ord('a'))}{move[0] + 1}")
                make_flip(board, move[0], move[1], WHITE)
                current_player = BLACK
            else:
                print("Белые пропускают ход.")
                current_player = BLACK

        # Проверка окончания игры (отсутствия доступных ходов для обоих цветов)
        if not get_valid_moves(board, BLACK) and not get_valid_moves(board, WHITE):
            break

    # Отображение окончательного состояния доски
    print_brd(board)
    black_discs, white_discs = count_discs(board)
    print(f"Игра окончена. Черные: {black_discs}, Белые: {white_discs}")
    # Определение победителя или ничьи
    if black_discs > white_discs:
        print("Победили черные!")
    elif white_discs > black_discs:
        print("Победили белые!")
    else:
        print("Ничья!")

if __name__ == "__main__":
    main()
