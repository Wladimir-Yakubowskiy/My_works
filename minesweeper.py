from tkinter import *
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    0: 'white',
    1: 'blue',
    2: 'green',
    3: '#eb7434',
    4: 'orange',
    5: 'pink',
    6: 'grey',
    7: 'yellow',
    8: 'crimson'
}

class MyButton(Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs, ):
        super(MyButton, self).__init__(master, bg='silver', width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x     #координаты
        self.y = y
        self.number = number    #порядковый номер клетки
        self.is_mine = False    #является ли клетка миной
        self.count_bomb = 0     #сколько бомб вокруг, по умолчанию 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class MineSweeper:

    window = Tk()
    ROW = 10
    COLUMNS = 10
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True
    SUPPOSEDS_MINES = 0     #предполагаемые мины
    RIGHT_CHOISE = 0        #верно угаданные мины

    def __init__(self):

        self.buttons = []
        for i in range(MineSweeper.ROW+2):    #создаём клетки
            temp = []
            for j in range(MineSweeper.COLUMNS+2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda botton=btn: self.click(botton))   #обработка нажатия
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):       #правая кнопка мыши

        if MineSweeper.IS_GAME_OVER == True:    #чтобы не ставились флажки после проигрыша
            return

        cur_btn = event.widget
        if MineSweeper.SUPPOSEDS_MINES < MineSweeper.MINES and cur_btn['state'] == 'normal':

            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '!'
            MineSweeper.SUPPOSEDS_MINES += 1
            if cur_btn.is_mine:
                MineSweeper.RIGHT_CHOISE += 1



        elif cur_btn['text'] == '!':
            cur_btn['state'] = 'normal'
            cur_btn['text'] = ''
            MineSweeper.SUPPOSEDS_MINES -= 1
            if cur_btn.is_mine:
                MineSweeper.RIGHT_CHOISE -= 1

        if MineSweeper.RIGHT_CHOISE == MineSweeper.MINES:
            showinfo('Поздравляем!', 'Вы победили')
            MineSweeper.IS_GAME_OVER

    def click(self, clicked_button: MyButton):  # нажатие на кнопку

        if MineSweeper.IS_GAME_OVER:        #блокирует поле после конца игры
            return None

        if MineSweeper.IS_FIRST_CLICK:      #расстановки мин после первого нажатия
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()


        color = colors.get(clicked_button.count_bomb, 'black')
        if clicked_button.is_mine:
            clicked_button.config(text='*', bg='red')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('GAME OVER', 'ВЫ ПРОИГРАЛИ')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn.config(text='*', bg='red')
        else:
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color, bg='silver')
                clicked_button.config(state='disabled', relief=SUNKEN, bg='white')
                clicked_button.is_open = True
            else:
                self.bredth_first_search(clicked_button)

        if clicked_button.is_mine:
            clicked_button.config(bg='red')
        else:
            clicked_button.config(state='disabled', relief=SUNKEN, bg='white')

    def bredth_first_search(self, btn: MyButton):   #обход соседних кнопок

        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled', relief=SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        cur_btn.config(bg='white')
                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1<=next_btn.x<=MineSweeper.ROW and 1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            next_btn.config(bg='white')
                            queue.append(next_btn)

    def reload(self):       #перезапускаем игру
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        MineSweeper.IS_GAME_OVER = False
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.RIGHT_CHOISE = 0
        MineSweeper.SUPPOSEDS_MINES = 0
        self.create_widgets()

    def create_settings_win(self):
        win_settings = Toplevel(self.window)
        win_settings.wm_title('Настройки')

        row_entry = Entry(win_settings)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        row_entry.insert(0, MineSweeper.ROW)
        Label(win_settings, text='Строки (1-100').grid(row=0, column=0)

        column_entry = Entry(win_settings)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        column_entry.insert(0, MineSweeper.COLUMNS)
        Label(win_settings, text='Столбцы (1-100)').grid(row=1, column=0)

        mines_entry = Entry(win_settings)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        mines_entry.insert(0, MineSweeper.MINES)
        Label(win_settings, text='Мины (1-100)').grid(row=2, column=0)

        Ok = Button(win_settings, text='Применить',
               command=lambda: self.change_settings(row_entry, column_entry, mines_entry, win_settings))
        Ok.grid(row=3, column=0, columnspan=2)

    def change_settings(self, row: Entry, columns: Entry, mines: Entry, win_settings):

        try:
            int(row.get()), int(columns.get()), int(mines.get())
            row, columns, mines = int(row.get()), int(columns.get()), int(mines.get())
            if row == 0 or columns == 0 or mines == 0:
                showerror('Ошибка', 'Значение должно быть больше 0')
            elif mines >= row * columns:
                showerror('Ошибка', 'Количество бомб должно быть меньше количества клеток')
            elif row > 100 or columns > 100 or mines > 100:
                showerror('Ошибка', 'Будь скромнее')
            else:
                MineSweeper.ROW = row
                MineSweeper.COLUMNS = columns
                MineSweeper.MINES = mines
                win_settings.destroy()
                self.reload()

        except ValueError:
            showerror('Ошибка!', 'Вы ввели неправильное значение')

    def create_widgets(self):

        menubar = Menu(self.window)

        self.window.config(menu=menubar)
        settings_menu = Menu(self.window, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_settings_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)

        count = 1
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j, stick='WENS')
                btn.number = count
                count += 1

        for i in range(1, MineSweeper.ROW + 1):
            Grid.columnconfigure(self.window, i, weight=1)

        for i in range(1, MineSweeper.COLUMNS + 1):
            Grid.rowconfigure(self.window, i, weight=1)


    def open_all_buttons(self):
        for i in range(MineSweeper.ROW+2):
            for j in range(MineSweeper.COLUMNS+2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', bg='red')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()


    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbou = self.buttons[i+row_dx][j+col_dx]
                            if neighbou.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    def get_mines_spaces(self, exclude_number: int):     #генерирует индексы заминированных клеток
        indexes = list(range(1, MineSweeper.ROW*MineSweeper.COLUMNS + 1))
        indexes.remove(exclude_number)                  #исключает индекс первой нажатой кнопки
        shuffle(indexes)                                #перемешивает индексы кнопок
        return indexes[:MineSweeper.MINES]              #возвращает индексы мин

    def insert_mines(self, number: int):     #расставляет мины по клеткам
        MineSweeper.IS_FIRST_CLICK = False
        index_mines = self.get_mines_spaces(number)   #принимает индексы заминированных клеток
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True



game = MineSweeper()
game.start()










