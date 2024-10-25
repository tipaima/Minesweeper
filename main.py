import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: '#A5260A',
    5: 'orange',
    6: 'purple',
    7: 'pink',
    8: 'black'
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibre 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_bomb = False
        self.count_bombs = 0
        self.is_open = False

    def __repr__(self):
        return f'Button x={self.x} y={self.y} №{self.number} {self.is_bomb}'


class bomber:
    window = tk.Tk()
    row = 12
    columns = 12
    bombs = 24
    game_status = False
    first_try = True
    key = 0
    not_flag = 0
    all_open = 0
    end = row * columns - bombs

    # Конструктор
    def __init__(self):
        self.buttons = []
        for i in range(bomber.row + 2):
            # Список столбцов\вложенный типо
            temp = []
            for j in range(bomber.columns + 2):
                # Вызываем класс с измененной настройкой кнопочек для создания кнопочек
                button = MyButton(bomber.window, x=i, y=j)
                button.config(command=lambda btn=button: self.click(btn))
                button.bind('<Button-3>', self.pkm)
                temp.append(button)
            # Добавляем в список кнопок строку с кнопками
            self.buttons.append(temp)

    # Обработка нажатия пкм/установка флага
    def pkm(self, event):
        button = event.widget
        if button['state'] == 'normal':
            button['state'] = 'disabled'
            button['text'] = '🚩'
            button['disabledforeground'] = 'red'
            if button.is_bomb:
                bomber.key += 1
            if not button.is_bomb:
                bomber.not_flag += 1
        elif button['text'] == '🚩':
            button['text'] = ''
            button['state'] = 'normal'
            if button.is_bomb:
                bomber.key -= 1
            if not button.is_bomb:
                bomber.not_flag -= 1

        if bomber.key == bomber.bombs and bomber.not_flag == 0 and bomber.all_open == bomber.end:
            showinfo("Игра окончена", "К сожалению вы смогли")
            self.win_open()

    # Зовем всех друзей чтобы игра заработала
    def start(self):

        self.create_widgets()

        bomber.window.mainloop()

    # Размер окна
    @staticmethod
    def size(x, y):
        bomber.window.geometry(f"{x}x{y}")

    # Перезапуск игры
    def restart_game(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        bomber.first_try = True
        bomber.game_status = False

    # Настройки
    def settings(self):
        settings = tk.Toplevel(self.window)
        settings.wm_title('Настройки')
        tk.Label(settings, text='Сложность').grid(row=0, column=0)
        entry = tk.Entry(settings)

        tk.Button(settings, text='Применить', command=lambda: self.change_settings())

    # Тут визуал менюшки настройки
    def change_settings(self):
        settings = tk.Toplevel(self.window)
        settings.wm_title('Корректировка')

        tk.Label(settings, text='Строки').grid(row=0, column=0)
        row_change = tk.Entry(settings)
        row_change.insert(0, bomber.row)
        row_change.grid(row=0, column=1, padx=30, pady=30)

        tk.Label(settings, text='Столбцы').grid(row=1, column=0)
        column_change = tk.Entry(settings)
        column_change.insert(0, bomber.columns)
        column_change.grid(row=1, column=1, padx=30, pady=30)

        tk.Label(settings, text='Бомбы').grid(row=2, column=0)
        bomb_change = tk.Entry(settings)
        bomb_change.insert(0, bomber.bombs)
        bomb_change.grid(row=2, column=1, padx=30, pady=30)

        (tk.Button(settings, text='Сохранить', command=lambda: self.change(row_change, column_change, bomb_change))
         .grid(row=3, column=0, columnspan=2))

    # Метод для смены настроек
    def change(self, row, column, bomb):
        try:
            int(row.get()), int(column.get()), int(bomb.get())
        except ValueError:
            showerror('Ошибка', 'Не верно введены строки или столбцы')
            return

        try:
            if 5 < int(row.get()) < 33 and 5 < int(column.get()) < 33 and 0 < int(bomb.get()):
                bomber.row = int(row.get())
                bomber.columns = int(column.get())
                bomber.bombs = int(bomb.get())
                bomber.end = bomber.row * bomber.columns - bomber.bombs
                self.restart_game()
        except ValueError:
            showerror('Ошибка', 'Не верно введены строки или столбцы')
            return

    # Делаем кнопочки видимыми
    def create_widgets(self):

        bomber.all_open = 0
        bomber.key = 0
        bomber.not_flag = 0

        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        settings = tk.Menu(menu, tearoff=0)
        settings.add_command(label='Играть', command=self.restart_game)
        settings.add_command(label='Настройки', command=self.change_settings)
        settings.add_command(label='Выход', command=self.window.destroy)
        menu.add_cascade(label='Сапер', menu=settings)

        bomb_count = 1
        for i in range(1, bomber.row + 1):
            for j in range(1, bomber.columns + 1):
                button = self.buttons[i][j]
                button.number = bomb_count
                button.grid(row=i, column=j, stick='NWES')
                bomb_count += 1

        for i in range(1, bomber.row + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, bomber.columns + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    # Вывод в консоль для удобства проверки
    def console_print(self):
        for i in range(1, bomber.row + 1):
            for j in range(1, bomber.columns + 1):
                button = self.buttons[i][j]
                if button.is_bomb:
                    print("B", end=' ')
                else:
                    print(button.count_bombs, end=' ')
            print('')

    # Надо подумать где будут бомбы
    @staticmethod
    def were_is_bombs(number):
        Seryozha = list(range(1, bomber.columns * bomber.row + 1))
        Seryozha.remove(number)
        shuffle(Seryozha)
        return Seryozha[:bomber.bombs]

    # А это Артем, он не правильный сапер
    def Artem(self, number: int):
        were = self.were_is_bombs(number)
        print(were)
        for i in range(1, bomber.row + 1):
            for j in range(1, bomber.columns + 1):
                btn = self.buttons[i][j]
                if btn.number in were:
                    btn.is_bomb = True

    # Тут начинается веселье:
    # Обработаем нажатие
    def click(self, clicked_button: MyButton):

        if bomber.first_try:
            bomber.first_try = False
            self.Artem(clicked_button.number)
            self.how_many_bombs()
            self.console_print()

        if clicked_button.is_bomb:
            clicked_button.config(text="*", disabledforeground='black')
            clicked_button.is_open = True
            bomber.game_status = True
            showinfo("Игра окончена", "Мина оказалась сильнее!")
            self.lose_open()
        else:
            color = colors.get(clicked_button.count_bombs)
            if clicked_button.count_bombs:
                clicked_button.config(text=clicked_button.count_bombs, disabledforeground=color)
                clicked_button.is_open = True
                bomber.all_open += 1
            else:
                self.open_buttons(clicked_button)

        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)
        if bomber.key == bomber.bombs and bomber.not_flag == 0 and bomber.all_open == bomber.end:
            showinfo("Игра окончена", "К сожалению вы смогли")
            self.win_open()

    # Найдем бомбы
    def how_many_bombs(self):
        for i in range(1, bomber.row + 1):
            for j in range(1, bomber.columns + 1):
                button = self.buttons[i][j]
                count_bombs = 0
                if not button.is_bomb:
                    for x in [-1, 0, 1]:
                        for y in [-1, 0, 1]:
                            around = self.buttons[i + x][j + y]
                            if around.is_bomb:
                                count_bombs += 1
                button.count_bombs = count_bombs

    # Супер-пупер-мега-сложное-многоходовочное открытие зон без кнопок
    def open_buttons(self, clicked_button: MyButton):
        # Гига-мага список для кнопок
        spisok = [clicked_button]
        while spisok:

            # Убераем текущую кнопку из списка и записываем ее в переменную
            it_button = spisok.pop()
            # задаем цвет
            color = colors.get(it_button.count_bombs, 'black')

            # ну собственно открываем кнопку
            if it_button.count_bombs:
                it_button.config(text=it_button.count_bombs, disabledforeground=color)
            else:
                it_button.config(text='', disabledforeground=color)

            # Ставик в кнопке пометку об открытии
            it_button.is_open = True
            it_button.config(state='disabled')
            it_button.config(relief=tk.SUNKEN)
            bomber.all_open += 1

            # Гига-мага и дт
            if it_button.count_bombs == 0:
                # Задаем координаты
                x, y = it_button.x, it_button.y
                # Перебор соседей
                for neighbour_x in [-1, 0, 1]:
                    for neighbour_y in [-1, 0, 1]:
                        # Ниже идет проверка координат: нам нужны только соседи сверху\снизу\слыва\справа без диагоналей

                        # Вычисляем следующую кнопку:
                        # координата х + координата-сдивг по х для вычисления соседа
                        # координата у + координата-сдивг по у для вычисления соседа
                        next_button = self.buttons[x + neighbour_x][y + neighbour_y]
                        # Гига проверка
                        # Открыта ли кнопка
                        # убераем невидимые столбики и строчки (обводку)
                        # Проверяем была ли уже эта кнопка
                        if not next_button.is_open and 1 <= next_button.x <= bomber.row and \
                                1 <= next_button.y <= bomber.columns and next_button not in spisok:
                            # Добавляем кнопку
                            spisok.append(next_button)

    # Показываем где были мины при поражении
    def lose_open(self):
        for i in range(1, bomber.row + 1):
            for j in range(1, bomber.columns + 1):
                button = self.buttons[i][j]
                if button.is_bomb:
                    button.config(text="*", disabledforeground='black')
                else:
                    color = colors.get(button.count_bombs)
                    if button.count_bombs:
                        button.config(text=button.count_bombs, disabledforeground=color)
                        button.is_open = True
                    else:
                        self.open_buttons(button)
                button.config(state='disabled')
                button.config(relief=tk.SUNKEN)

    def win_open(self):
        for i in range(1, bomber.row + 1):
            for j in range(1, bomber.columns + 1):
                button = self.buttons[i][j]
                if button.is_bomb:
                    button.config(text="🚩", disabledforeground='red')
                else:
                    color = colors.get(button.count_bombs)
                    if button.count_bombs:
                        button.config(text=button.count_bombs, disabledforeground=color)
                        button.is_open = True
                    else:
                        self.open_buttons(button)
                button.config(state='disabled')
                button.config(relief=tk.SUNKEN)


game = bomber()
game.start()
