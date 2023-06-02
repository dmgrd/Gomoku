import random
import tkinter as tk
from typing import Tuple
from tkinter import messagebox

class AI:
    def __init__(self, gomoku):
        self.gomoku = gomoku
        self.player_id = self.gomoku.current_player

    def get_move(self) -> Tuple[int, int]:
        # проверка на 5 фишек в ряд
        for row in range(self.gomoku.size):
            for col in range(self.gomoku.size):
                if self.gomoku.board[row][col] == 0:
                    self.gomoku.board[row][col] = self.player_id
                    if self.gomoku.is_win(row, col):
                        self.gomoku.board[row][col] = 0
                        return row, col
                    self.gomoku.board[row][col] = 0

        # блокирование ходов, если есть 2 фишки в ряд
        for row in range(self.gomoku.size):
            for col in range(self.gomoku.size):
                if self.gomoku.board[row][col] == 0:
                    self.gomoku.board[row][col] = self.player_id
                    if self.check_num_in_row(row, col, 2):
                        self.gomoku.board[row][col] = 0
                        continue
                    self.gomoku.board[row][col] = 0
                    
                    self.gomoku.board[row][col] = 3 - self.player_id
                    if self.check_num_in_row(row, col, 2):
                        self.gomoku.board[row][col] = 0
                        return row, col
                    self.gomoku.board[row][col] = 0

        # попытка сделать 3 фишки в ряд
        for row in range(self.gomoku.size):
            for col in range(self.gomoku.size):
                if self.gomoku.board[row][col] == 0:
                    self.gomoku.board[row][col] = self.player_id
                    if self.check_num_in_row(row, col, 3):
                        self.gomoku.board[row][col] = 0
                        return row, col
                    self.gomoku.board[row][col] = 0

        # случайный ход
        return random.choice([(i, j) for i in range(self.gomoku.size) for j in range(self.gomoku.size)])

    def check_num_in_row(self, row: int, col: int, num: int) -> bool:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for d in directions:
            count = 0
            for i in range(-num + 1, num):
                r, c = row + i * d[0], col + i * d[1]
                if not (0 <= r < self.gomoku.size and 0 <= c < self.gomoku.size):
                    continue
                if self.gomoku.board[r][c] == self.player_id:
                    count += 1
                else:
                    count = 0
                if count == num - 1 and (r + d[0] < 0 or r + d[0] >= self.gomoku.size or
                                         c + d[1] < 0 or c + d[1] >= self.gomoku.size or
                                         self.gomoku.board[r + d[0]][c + d[1]] == 0):
                    return True

class Gomoku:
    def __init__(self, size: int = 15):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.current_player = 1
        self.winner = None
        self.moves_left = size * size

    def play(self, row: int, col: int) -> bool:
        if self.board[row][col] != 0 or self.winner is not None:
            return False

        self.board[row][col] = self.current_player
        self.moves_left -= 1
        if self.is_win(row, col):
            self.winner = self.current_player
        elif self.moves_left == 0:
            self.winner = 0
        self.current_player = 3 - self.current_player
        return True

    def is_win(self, row: int, col: int) -> bool:
        def count(dx: int, dy: int) -> int:
            r, c, cnt = row + dx, col + dy, 0
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.current_player:
                r, c, cnt = r + dx, c + dy, cnt + 1
            return cnt

        return any(count(dx, dy) + count(-dx, -dy) + 1 >= 5 for dx, dy in ((0, 1), (1, 0), (1, 1), (1, -1)))

class GomokuAIGUI:
    def __init__(self, master: tk.Tk, size: int = 15, cell_size: int = 30):
        self.master = master
        self.size = size
        self.cell_size = cell_size
        self.canvas_size = cell_size * size

        self.frame = tk.Frame(master, bg='#D8DE87', bd=70)
        self.frame.pack()

        # Создание кнопки "Перезапустить игру"
        instruction_button = tk.Button(root, text="Перезапустить игру", font=("Arial", 24), width=20, height=1, command=start_ai, bg='#D19C58')
        instruction_button.place(relx=0.5, rely=0.06, anchor=tk.CENTER)

        # Создание кнопки "В главное меню"
        instruction_button = tk.Button(root, text="В главное меню", font=("Arial", 24), width=20, height=1, command=menu, bg='#D19C58')
        instruction_button.place(relx=0.5, rely=0.94, anchor=tk.CENTER)

        self.canvas = tk.Canvas(self.frame, width=self.canvas_size, height=self.canvas_size)
        self.canvas.configure(background='#D19C58')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.handle_click)

        self.gomoku = Gomoku(size)

        self.draw_board()

    def draw_board(self):
        for i in range(self.size):
            x0, y0, x1, y1 = i * self.cell_size, 0, i * self.cell_size, self.canvas_size
            self.canvas.create_line(x0, y0, x1, y1)
            x0, y0, x1, y1 = 0, i * self.cell_size, self.canvas_size, i * self.cell_size
            self.canvas.create_line(x0, y0, x1, y1)

    def draw_piece(self, row: int, col: int):
        x, y = col * self.cell_size, row * self.cell_size
        r = self.cell_size // 2 - 2
        if self.gomoku.board[row][col] == 1:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black')
        else:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='white')

    def handle_click(self, event: tk.Event):
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if self.gomoku.play(row, col):
            self.draw_piece(row, col)
            if self.gomoku.winner is not None:
                self.show_winner()
            else:
                ai = AI(self.gomoku)
                row, col = ai.get_move()
                if self.gomoku.play(row, col):
                    self.draw_piece(row, col)
                    if self.gomoku.winner is not None:
                        self.show_winner()

    def show_winner(self):
            if self.gomoku.winner == 1:
                tk.messagebox.showinfo("Игра окончена", "Победитель: Игрок!")
            elif self.gomoku.winner == 2:
                tk.messagebox.showinfo("Игра окончена", "Победитель: Компьютер!")
            else:
                tk.messagebox.showinfo("Игра окончена", "Ничья!")

class GomokuFriendGUI:
    def __init__(self, master: tk.Tk, size: int = 15, cell_size: int = 30):
        self.master = master
        self.size = size
        self.cell_size = cell_size
        self.canvas_size = cell_size * size

        self.frame = tk.Frame(master, bg='#D8DE87', bd=70)
        self.frame.pack()

        # Создание кнопки "Перезапустить игру"
        instruction_button = tk.Button(root, text="Перезапустить игру", font=("Arial", 24), width=20, height=1, command=start_friend, bg='#D19C58')
        instruction_button.place(relx=0.5, rely=0.06, anchor=tk.CENTER)

        # Создание кнопки "В главное меню"
        instruction_button = tk.Button(root, text="В главное меню", font=("Arial", 24), width=20, height=1, command=menu, bg='#D19C58')
        instruction_button.place(relx=0.5, rely=0.94, anchor=tk.CENTER)

        self.canvas = tk.Canvas(self.frame, width=self.canvas_size, height=self.canvas_size)
        self.canvas.configure(background='#D19C58')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.handle_click)

        self.gomoku = Gomoku(size)

        self.draw_board()

    def draw_board(self):
        for i in range(self.size):
            x0, y0, x1, y1 = i * self.cell_size, 0, i * self.cell_size, self.canvas_size
            self.canvas.create_line(x0, y0, x1, y1)
            x0, y0, x1, y1 = 0, i * self.cell_size, self.canvas_size, i * self.cell_size
            self.canvas.create_line(x0, y0, x1, y1)

    def draw_piece(self, row: int, col: int):
        x, y = col * self.cell_size, row * self.cell_size
        r = self.cell_size // 2 - 2
        if self.gomoku.board[row][col] == 1:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black')
        else:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='white')

    def handle_click(self, event: tk.Event):
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if self.gomoku.play(row, col):
            self.draw_piece(row, col)
            if self.gomoku.winner is not None:
                self.show_winner()

    def show_winner(self):
            if self.gomoku.winner == 1:
                tk.messagebox.showinfo("Игра окончена", "Победитель: Игрок №1!")
            elif self.gomoku.winner == 2:
                tk.messagebox.showinfo("Игра окончена", "Победитель: Игрок №2!")
            else:
                tk.messagebox.showinfo("Игра окончена", "Ничья!")

# Функция для запуска новой игры против друга
def start_friend():
    # Удаляем все виджеты в главном окне
    for widget in root.winfo_children():
        widget.destroy()
    # Создаем объект класса GomokuFriendGUI и отрисовываем доску
    friend_gui = GomokuFriendGUI(root)

# Функция для запуска новой игры против компьютера
def start_ai():
    # Удаляем все виджеты в главном окне
    for widget in root.winfo_children():
        widget.destroy()
    # Создаем объект класса GomokuAIGUI и отрисовываем доску
    ai_gui = GomokuAIGUI(root)

# Функция для закрытия окна программы
def exit():
    root.destroy()

# Создание окна программы
root = tk.Tk()
root.geometry("562x562")
root.title("Gomoku")
root.resizable(False, False)
root.configure(bg='#D8DE87')

# Создание надписи "Gomoku"
title_label = tk.Label(root, text="Gomoku", font=("Arial", 36, "bold"), bg='#D8DE87')
title_label.place(relx=0.5, rely=0.10, anchor=tk.CENTER)

# Создание надписи "Играть:"
play_label = tk.Label(root, text="Играть:", font=("Arial", 24, "bold"), bg='#D8DE87')
play_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

# Создание кнопки "С другом"
play_button = tk.Button(root, text="С другом", font=("Arial", 24), width=20, height=1, command=start_friend, bg='#D19C58')
play_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Создание кнопки "С компьютером"
bot_button = tk.Button(root, text="С компьютером", font=("Arial", 24), width=20, height=1, command=start_ai, bg='#D19C58')
bot_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

# Функция для открытия инструкции
def instructions():
    # Удаляем все виджеты в главном окне
    for widget in root.winfo_children():
        widget.destroy()
    
    # Создание надписи "Правила игры:"
    title_label = tk.Label(root, text="Правила игры:", font=("Arial", 36, "bold"), bg='#D8DE87')
    title_label.place(relx=0.5, rely=0.08, anchor=tk.CENTER)
    
    # Создание текстового диапазона
    text_frame = tk.Frame(root)
    text_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=0.7, anchor=tk.CENTER)
    
    # Создание текста правил игры
    instructions_text = """Игра ведётся на квадратном поле («доске»), расчерченном вертикальными и горизонтальными линиями. Пересечения линий называются «пунктами». Наиболее распространённым является поле размером 15×15 линий.

Играют две стороны — «чёрные» и «белые». Каждая сторона использует фишки («камни») своего цвета.

Каждым ходом игрок выставляет камень своего цвета в один из свободных пунктов доски. Первый ход делают чёрные в любой пункт доски. Далее ходы делаются по очереди.

Цель игры — первым построить камнями своего цвета непрерывный ряд из пяти камней в горизонтальном, вертикальном или диагональном направлении.

Если доска заполнена и ни один из игроков не построил ряд из пяти камней, может быть объявлена ничья."""
    
    # Создание метки для текста правил игры и размещение её в текстовом диапазоне
    instructions_label = tk.Label(text_frame, text=instructions_text, font=("Arial", 14), justify="left", wraplength=562, bg='#D8DE87')
    instructions_label.pack(fill="both", expand=True)
    
    # Создание кнопки "В главное меню"
    instruction_button = tk.Button(root, text="В главное меню", font=("Arial", 24), width=20, height=1, command=menu, bg='#D19C58')
    instruction_button.place(relx=0.5, rely=0.92, anchor=tk.CENTER)

# Создание кнопки "Инструкция"
instruction_button = tk.Button(root, text="Инструкция", font=("Arial", 24), width=20, height=1, command=instructions, bg='#D19C58')
instruction_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Создание кнопки "Выход"
exit_button = tk.Button(root, text="Выход", font=("Arial", 24), width=20, height=1, command=exit, bg='#D19C58')
exit_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

def menu():
    # Удаляем все виджеты в главном окне
    for widget in root.winfo_children():
        widget.destroy()
    # Создание надписи "Gomoku"
    title_label = tk.Label(root, text="Gomoku", font=("Arial", 36, "bold"), bg='#D8DE87')
    title_label.place(relx=0.5, rely=0.10, anchor=tk.CENTER)

    # Создание надписи "Играть:"
    play_label = tk.Label(root, text="Играть:", font=("Arial", 24, "bold"), bg='#D8DE87')
    play_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    # Создание кнопки "С другом"
    play_button = tk.Button(root, text="С другом", font=("Arial", 24), width=20, height=1, command=start_friend, bg='#D19C58')
    play_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    # Создание кнопки "С компьютером"
    bot_button = tk.Button(root, text="С компьютером", font=("Arial", 24), width=20, height=1, command=start_ai, bg='#D19C58')
    bot_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    # Создание кнопки "Инструкция"
    instruction_button = tk.Button(root, text="Инструкция", font=("Arial", 24), width=20, height=1, command=instructions, bg='#D19C58')
    instruction_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Создание кнопки "Выход"
    exit_button = tk.Button(root, text="Выход", font=("Arial", 24), width=20, height=1, command=exit, bg='#D19C58')
    exit_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

root.mainloop()