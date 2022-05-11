import copy
import random
import time
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from copy import deepcopy
from PIL import Image, ImageTk
from random import randint, choice
import numpy as np
from constants import *


def games_page_opening(welcome_page_canvas):
    global games_page_canvas
    welcome_page_canvas.destroy()
    games_page_canvas = Canvas(window, width=400, height=400, bg='black')
    games_page_canvas.pack(fill="both", expand=True)
    SnakeFrame(games_page_canvas)
    RockPaperScissors(games_page_canvas)
    TicTacToe()
    Pong(games_page_canvas)
    EggGame(games_page_canvas, window)
    # Balloon(games_page_canvas)


class SnakeFrame:

    def __init__(self, games_page_canvas):
        whole_snake_frame = Frame(games_page_canvas)
        whole_snake_frame.pack()
        self.speed = 80
        self.space_size = 40
        self.body_parts = 3
        self.food_color = "red"
        self.snake_color = "green"
        self.score = 0
        self.direction = 'down'
        frame1_window = games_page_canvas.create_window(675, 200, width=300, height=300, window=whole_snake_frame)
        button = Button(whole_snake_frame, text="Start the Game", width=110, bg='#063970', font=('Arial', 20, 'bold'),
                        fg='white', command=lambda: self.snake_start_game_onclick(games_page_canvas))
        button.pack(side=BOTTOM)
        self.snake_image_area_in_a_frame(whole_snake_frame)
        window.bind("<Left>", lambda event: self.change_direction('left'))
        window.bind("<Right>", lambda event: self.change_direction('right'))
        window.bind("<Up>", lambda event: self.change_direction('up'))
        window.bind("<Down>", lambda event: self.change_direction('down'))

    def snake_image_area_in_a_frame(self, whole_snake_frame):
        global snake_image
        snake_image = ImageTk.PhotoImage(Image.open("snake.png"))
        frame_canvas = Canvas(whole_snake_frame, width=300, height=300)
        frame_canvas.pack(fill="both", expand=True)
        frame_canvas.create_image(0, 0, image=snake_image, anchor="nw")

    def snake_start_game_onclick(self, game_page_canvas):
        game_page_canvas.destroy()
        self.snake_canvas = Canvas(window, width=400, height=400)
        self.snake_canvas.pack(fill="both", expand=True)
        self.game_canvas()

    def game_canvas(self):
        self.snake_canvas.config(bg='#BEBEBE')
        start_button = Button(self.snake_canvas, text="Start", font=('Arial', 20, 'bold'), bg='#00FF00', fg='white',
                              command=self.start)
        start_button.pack()
        button_frame = self.snake_canvas.create_window(600, 630, width=120, height=60,
                                                       anchor="nw",
                                                       window=start_button)

        self.black_canvas = Canvas(self.snake_canvas, bg='black')
        self.black_canvas.pack()
        window_frame = self.snake_canvas.create_window(230, 100, width=920, height=470,
                                                       anchor="nw",
                                                       window=self.black_canvas)
        self.score_label = Label(self.snake_canvas, text="Score: {}".format(self.score), font=('Arial', 25, 'bold'),
                                 fg='black', bg='#BEBEBE')
        self.score_label.place(x=620, y=30)
        go_back = Button(self.snake_canvas, text="Go Back", font=('Arial', 20, 'bold'), bg='blue', fg='white',
                         command=lambda: self.go_back(self.snake_canvas))
        go_back.pack()
        button_frame = self.snake_canvas.create_window(30, 20, width=150, height=60,
                                                       anchor="nw",
                                                       window=go_back)
        messagebox.showinfo("Instructions", "Use arrow keys for moving left,right,up and down")

    def start(self):
        self.food()
        self.snake()
        self.next_turn()

    def snake(self):
        self.coordinates = []
        self.squares = []
        for i in range(0, self.body_parts):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = self.black_canvas.create_rectangle(x, y, x + self.space_size, y + self.space_size,
                                                        fill=self.snake_color, tag='snake')
            self.squares.append(square)

    def next_turn(self):
        x, y = self.coordinates[0]
        if self.direction == 'up':
            y -= self.space_size
        elif self.direction == 'down':
            y += self.space_size
        elif self.direction == 'left':
            x -= self.space_size
        elif self.direction == 'right':
            x += self.space_size

        self.coordinates.insert(0, (x, y))
        square = self.black_canvas.create_rectangle(x, y, x + self.space_size, y + self.space_size,
                                                    fill=self.snake_color
                                                    )
        self.squares.insert(0, square)
        if x == self.food_coordinates[0] and y == self.food_coordinates[1]:
            self.score += 1
            self.score_label.config(text="Score: {}".format(self.score))
            self.black_canvas.delete("food")
            self.food()
        else:
            del self.coordinates[-1]
            self.black_canvas.delete(self.squares[-1])
            del self.squares[-1]
        if self.check_collisions():
            self.game_over()
        else:
            window.after(self.speed, self.next_turn)

    def check_collisions(self):
        x, y = self.coordinates[0]
        if x < 0 or x >= 920:
            return True
        elif y < 0 or y > 470:
            return True
        for body_part in self.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
        return False

    def game_over(self):
        self.snake_canvas.delete(ALL)
        self.score_label.destroy()
        self.snake_canvas.config(bg='black')
        label = Label(self.snake_canvas, text="Game Over", font=('consolas', 70), bg='black', fg='red')
        label.place(x=440, y=170)
        label_score = Label(self.snake_canvas, text='Your Score: {}'.format(self.score), font=('Arial', 40, 'italic'),
                            bg='black', fg='white')
        label_score.place(x=490, y=330)

        play_again_button = Button(self.snake_canvas, text='Play again', font=('Arial', 25, 'bold'), bg='#4a934a',
                                   fg='white', command=lambda: self.game_canvas())
        play_again_button.place(x=520, y=500)
        exit_button = Button(self.snake_canvas, text='Exit', font=('Arial', 25, 'bold'), bg='red', fg='white',
                             command=lambda: games_page_opening(self.snake_canvas))
        exit_button.place(x=740, y=500)

    def change_direction(self, new_direction):
        if new_direction == 'left':
            if self.direction != 'right':
                self.direction = new_direction
        if new_direction == 'right':
            if self.direction != 'left':
                self.direction = new_direction
        if new_direction == 'up':
            if self.direction != 'down':
                self.direction = new_direction
        if new_direction == 'down':
            if self.direction != 'up':
                self.direction = new_direction

    def food(self):
        x = randint(0, (920 // self.space_size) - 1) * self.space_size
        y = randint(0, (470 // self.space_size) - 1) * self.space_size
        self.food_coordinates = [x, y]
        self.black_canvas.create_oval(x, y, x + self.space_size, y + self.space_size, fill=self.food_color, tag='food')

    def go_back(self, snake_canvas):
        snake_canvas.destroy()
        games_page_opening(welcome_page_canvas)


class RockPaperScissors:
    def __init__(self, games_page_canvas):
        whole_rockpaper_frame = Frame(games_page_canvas)
        whole_rockpaper_frame.pack()
        frame1_window = games_page_canvas.create_window(280, 200, width=300, height=300, window=whole_rockpaper_frame)
        button = Button(whole_rockpaper_frame, text="Start the Game", width=110, bg='#063970',
                        font=('Arial', 20, 'bold'), fg='white',
                        command=lambda: self.start_game_onclick(games_page_canvas))
        button.pack(side=BOTTOM)

        self.rock_paper_bg_image(whole_rockpaper_frame)

    def rock_paper_bg_image(self, whole_rockpaper_frame):
        global rockpaper
        rockpaper = ImageTk.PhotoImage(Image.open("bg-rockpaper.png"))
        frame_canvas = Canvas(whole_rockpaper_frame, width=300, height=300)
        frame_canvas.pack(fill="both", expand=True)
        frame_canvas.create_image(0, 0, image=rockpaper, anchor="nw")

    def start_game_onclick(self, games_page_canvas):
        games_page_canvas.destroy()
        rock_paper_canvas = Canvas(window, width=400, height=400, bg='#b0d0b9')
        rock_paper_canvas.pack(fill="both", expand=True)
        go_back = Button(rock_paper_canvas, text="Go Back", font=('Arial', 20, 'bold'), bg='blue', fg='white',
                         command=lambda: self.go_back(rock_paper_canvas))
        go_back.pack()
        button_frame = rock_paper_canvas.create_window(30, 20, width=150, height=60,
                                                       anchor="nw",
                                                       window=go_back)

        global rock_image
        global scissor_image
        global paper_image
        global player, computer, computer_score, player_score

        player = 0
        computer = 0
        name = askstring('Your Name', 'Please Enter your name: ?')
        # messagebox.showinfo('Hello!', 'Hi, {}'.format(name))
        player_score = Label(rock_paper_canvas, text=f"{name}'s Score: " + str(player), font=('Arial', 25, 'bold'),
                             bg='#b0d0b9')
        player_score.place(x=550, y=10)
        computer_score = Label(rock_paper_canvas, text="Computer Score: " + str(computer), font=('Arial', 25, 'bold'),
                               bg='#b0d0b9')
        computer_score.place(x=520, y=330)
        self.open_page(rock_paper_canvas)

    def open_page(self, rock_paper_canvas):

        global rock_image
        global scissor_image
        global paper_image

        rock_image = ImageTk.PhotoImage(Image.open("rock.png"))
        rock_button = Button(rock_paper_canvas, image=rock_image, borderwidth=0, bg='#b0d0b9', height=240, width=180,
                             command=lambda: self.rock(rock_paper_canvas, paper_button, scissor_button, options,
                                                       computer_choice))
        rock_button.place(x=250, y=80)
        paper_image = PhotoImage(file='paper.png')
        paper_button = Button(rock_paper_canvas, image=paper_image, borderwidth=0, height=240, width=180, bg='#b0d0b9',
                              command=lambda: self.paper(rock_paper_canvas, rock_button, scissor_button, options,
                                                         computer_choice))
        paper_button.place(x=600, y=80)
        scissor_image = PhotoImage(file='scissor.png')
        scissor_button = Button(rock_paper_canvas, image=scissor_image, borderwidth=0, height=240, width=180,
                                bg='#b0d0b9',
                                command=lambda: self.scissor(rock_paper_canvas, rock_button, paper_button, options,
                                                             computer_choice))
        scissor_button.place(x=950, y=80)
        options = [rock_button, paper_button, scissor_button]
        computer_choice = options[randint(0, 2)]

    def go_back(self, rock_paper_canvas):
        rock_paper_canvas.destroy()
        games_page_opening(welcome_page_canvas)

    def rock(self, rock_paper_canvas, paper_button, scissor_button, options, computer_choice):
        paper_button.destroy()
        scissor_button.destroy()
        if computer_choice == options[0]:
            global computer_rock_image
            computer_rock_image = ImageTk.PhotoImage(Image.open("rock.png"))
            rock_button = Button(rock_paper_canvas, image=computer_rock_image, borderwidth=0, highlightcolor='#b0d0b9',
                                 height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="Oops! It's a Tie            ", font=('Arial', 25, 'bold'),
                                bg='#b0d0b9')
            acknowledge.place(x=750, y=500)
            self.open_page(rock_paper_canvas)

        elif computer_choice == options[1]:
            global computer_paper_image, computer, computer_score
            computer_paper_image = ImageTk.PhotoImage(Image.open("paper.png"))
            rock_button = Button(rock_paper_canvas, image=computer_paper_image, borderwidth=0, highlightcolor='#b0d0b9',
                                 height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="You lose                    ", font=('Arial', 25, 'bold'),
                                bg='#b0d0b9')
            acknowledge.place(x=750, y=500)

            self.computer_score_update(rock_paper_canvas)

        elif computer_choice == options[2]:
            global computer_scissor_image, player_score, player
            computer_scissor_image = ImageTk.PhotoImage(Image.open("scissor.png"))
            rock_button = Button(rock_paper_canvas, image=computer_scissor_image, borderwidth=0,
                                 highlightcolor='#b0d0b9', height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="Hurrah! You Won", font=('Arial', 25, 'bold'), bg='#b0d0b9')
            acknowledge.place(x=750, y=500)
            self.player_score_update(rock_paper_canvas)

    def paper(self, rock_paper_canvas, rock_button, scissor_button, options, computer_choice):
        rock_button.destroy()
        scissor_button.destroy()
        if computer_choice == options[0]:
            global computer_rock_image, player, player_score
            computer_rock_image = ImageTk.PhotoImage(Image.open("rock.png"))
            rock_button = Button(rock_paper_canvas, image=computer_rock_image, borderwidth=0, highlightcolor='#b0d0b9',
                                 height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="Hurrah! You Won", font=('Arial', 25, 'bold'), bg='#b0d0b9'
                                )
            acknowledge.place(x=750, y=500)
            self.player_score_update(rock_paper_canvas)
        elif computer_choice == options[1]:
            global computer_paper_image
            computer_paper_image = ImageTk.PhotoImage(Image.open("paper.png"))
            rock_button = Button(rock_paper_canvas, image=computer_paper_image, borderwidth=0, highlightcolor='#b0d0b9',
                                 height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="Oops! It's a Tie             ", font=('Arial', 25, 'bold'),
                                bg='#b0d0b9')
            acknowledge.place(x=750, y=500)
            self.open_page(rock_paper_canvas)
        elif computer_choice == options[2]:
            global computer_scissor_image, computer, computer_score
            computer_scissor_image = ImageTk.PhotoImage(Image.open("scissor.png"))
            rock_button = Button(rock_paper_canvas, image=computer_scissor_image, borderwidth=0,
                                 highlightcolor='#b0d0b9', height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="You lose                        ", font=('Arial', 25, 'bold'),
                                bg='#b0d0b9')
            acknowledge.place(x=750, y=500)
            self.computer_score_update(rock_paper_canvas)

    def scissor(self, rock_paper_canvas, rock_button, paper_button, options, computer_choice):
        rock_button.destroy()
        paper_button.destroy()
        if computer_choice == options[0]:
            global computer_rock_image, computer_score, computer
            computer_rock_image = ImageTk.PhotoImage(Image.open("rock.png"))
            rock_button = Button(rock_paper_canvas, image=computer_rock_image, borderwidth=0, highlightcolor='#b0d0b9',
                                 height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="You lose              ", font=('Arial', 25, 'bold'),
                                bg='#b0d0b9')
            acknowledge.place(x=750, y=500)
            self.computer_score_update(rock_paper_canvas)
        elif computer_choice == options[1]:
            global computer_paper_image, player, player_score
            computer_paper_image = ImageTk.PhotoImage(Image.open("paper.png"))
            rock_button = Button(rock_paper_canvas, image=computer_paper_image, borderwidth=0, highlightcolor='#b0d0b9',
                                 height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="Hurrah! You Won", font=('Arial', 25, 'bold'), bg='#b0d0b9')
            acknowledge.place(x=750, y=500)
            self.player_score_update(rock_paper_canvas)
        elif computer_choice == options[2]:
            global computer_scissor_image
            computer_scissor_image = ImageTk.PhotoImage(Image.open("scissor.png"))
            rock_button = Button(rock_paper_canvas, image=computer_scissor_image, borderwidth=0,
                                 highlightcolor='#b0d0b9', height=240, width=180, bg='#b0d0b9')
            rock_button.place(x=500, y=420)
            acknowledge = Label(rock_paper_canvas, text="Oops! It's a Tie            ", font=('Arial', 25, 'bold'),
                                bg='#b0d0b9')
            acknowledge.place(x=750, y=500)
            self.open_page(rock_paper_canvas)

    def computer_score_update(self, rock_paper_canvas):
        global computer, computer_score, player

        computer += 1
        computer_score.config(text='Computer Score: ' + str(computer))
        if computer == 3:
            rock_paper_canvas.destroy()
            result_canvas = Canvas(window, width=400, height=400, bg='#b0d0b9')
            result_canvas.pack(fill="both", expand=True)
            result_label = Label(result_canvas, text='You lose', font=('Arial', 50, 'bold'), bg='#b0d0b9')
            result_label.place(x=520, y=150)
            ratio = Label(result_canvas, text=str(player) + ' ' + ':' + ' ' + '3', font=('Arial', 50, 'bold'),
                          bg='#b0d0b9')
            ratio.place(x=600, y=250)
            play_again_button = Button(result_canvas, text='Play again', font=('Arial', 25, 'bold'), bg='#4a934a',
                                       fg='white', command=lambda: self.start_game_onclick(result_canvas))
            play_again_button.place(x=520, y=450)
            exit_button = Button(result_canvas, text='Exit', font=('Arial', 25, 'bold'), bg='red', fg='white',
                                 command=lambda: games_page_opening(result_canvas))
            exit_button.place(x=740, y=450)
        self.open_page(rock_paper_canvas)

    def player_score_update(self, rock_paper_canvas):
        global player, player_score
        player += 1
        player_score.config(text='Your Score: ' + str(player))
        if player == 3:
            rock_paper_canvas.destroy()
            result_canvas = Canvas(window, width=400, height=400, bg='#b0d0b9')
            result_canvas.pack(fill="both", expand=True)
            result_label = Label(result_canvas, text='You Won ', font=('Arial', 50, 'bold'), bg='#b0d0b9')
            result_label.place(x=520, y=150)
            ratio = Label(result_canvas, text='3' + ' ' + ':' + ' ' + str(computer), font=('Arial', 50, 'bold'),
                          bg='#b0d0b9')
            ratio.place(x=600, y=250)
            play_again_button = Button(result_canvas, text='Play again', font=('Arial', 25, 'bold'), bg='#4a934a',
                                       fg='white', command=lambda: self.start_game_onclick(result_canvas))
            play_again_button.place(x=520, y=450)
            exit_button = Button(result_canvas, text='Exit', font=('Arial', 25, 'bold'), bg='red', fg='white',
                                 command=lambda: games_page_opening(result_canvas))
            exit_button.place(x=740, y=450)
        self.open_page(rock_paper_canvas)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0


    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def is_full(self):
        return self.marked_sqrs == 9

    def is_empty(self):
        return self.marked_sqrs == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def final_state(self, show=False):
        # self.tictactoe=TicTacToe()
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    # TicTacToe().game_over_col(col)
                    messagebox.showinfo("Game Over","Game Over")
                    TicTacToe().reset()
                return self.squares[0][col]
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    # TicTacToe().game_over_row(row)
                    messagebox.showinfo("Game Over","Game Over")
                    TicTacToe().reset()
                else:
                    return self.squares[row][0]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                messagebox.showinfo("Game Over","Game Over")
                TicTacToe().reset()
                # TicTacToe().game_over_diagonally()
            else:
                return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                messagebox.showinfo("Game Over","Game Over")
                TicTacToe().reset()
                # TicTacToe().game_over_left()
            else:
                return self.squares[1][1]

        return 0


class AI:
    def __init__(self, player=2):
        self.player = player

    def eval_fun(self, main_board):
        # empty_sqrs=main_board.get_empty_sqrs()
        # idx=random.randrange(0,len(empty_sqrs))
        # return empty_sqrs[idx]
        eval_val, move = self.minimax(main_board, False)
        print(f"AI has chosen{eval_val}{move}")
        return move

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        elif board.is_full():
            return 0, None
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval_max = self.minimax(temp_board, False)[0]
                if eval_max > max_eval:
                    max_eval = eval_max
                    best_move = (row, col)
            return max_eval, best_move
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval_min = self.minimax(temp_board, True)[0]
                if eval_min < min_eval:
                    min_eval = eval_min
                    best_move = (row, col)
            return min_eval, best_move


class TicTacToe:
    def __init__(self):
        whole_tictactoe_frame = Frame(games_page_canvas)
        whole_tictactoe_frame.pack()
        self.player = 1
        self.game_mode = 'ai'
        self.running = True
        frame1_window = games_page_canvas.create_window(1050, 200, width=300, height=300, window=whole_tictactoe_frame)
        button = Button(whole_tictactoe_frame, text="Start the Game", width=110, bg='#063970',
                        font=('Arial', 20, 'bold'), fg='white',
                        command=lambda: self.onclick_start_game(games_page_canvas))
        button.pack(side=BOTTOM)

        self.tictactoe_bg_image(whole_tictactoe_frame)

    def tictactoe_bg_image(self, whole_tictactoe_frame):
        global tictactoe
        tictactoe = ImageTk.PhotoImage(Image.open("tictactoe.png"))
        frame_canvas = Canvas(whole_tictactoe_frame, width=300, height=300)
        frame_canvas.pack(fill="both", expand=True)
        frame_canvas.create_image(0, 0, image=tictactoe, anchor="nw")

    # def game_over_left(self):
    #     iPos = 20, height - 20
    #     fPos = width - 20, 20
    #     self.board_canvas.create_line(iPos, fPos, width=10, fill='red')
    #
    # def game_over_diagonally(self):
    #
    #     self.board_canvas.create_line(20, 20, width - 20, height - 20,  fill='red',width=10)

    def mouse_event(self, event):
        row = event.y // SQSIZE
        col = event.x // SQSIZE
        if self.board.empty_sqr(row, col):
            self.board.mark_sqr(row, col, self.player)
            self.draw_fig(row, col)
            # self.next_turn()
            if self.is_over():
                self.running = False
            else:
                self.next_turn()

    def draw_fig(self, row, col):
        col = col * SQSIZE + SQSIZE // 2
        row = row * SQSIZE + SQSIZE // 2
        if self.player == 1:
            player_label = Label(self.board_canvas, text="X", bg='black', fg='white', font=('Arial', 80, 'bold'))
            player_label.place(x=col, y=row, anchor=CENTER)

        elif self.player == 2:
            circle_label = Label(self.board_canvas, text="O", bg='black', fg='white', font=('Arial', 80, 'bold'))
            circle_label.place(x=col, y=row, anchor=CENTER)

    # def game_over_col(self, col):
    #     self.board_canvas.create_line(col * SQSIZE + SQSIZE // 2, 20, col * SQSIZE + SQSIZE // 2, height - 20, width=10, fill='red')
    #
    # def game_over_row(self, row):
    #     iPos = 20, row * SQSIZE + SQSIZE // 2
    #     fPos = width - 20, row * SQSIZE + SQSIZE // 2
    #     self.board_canvas.create_line(iPos, fPos, width=10, fill='red')

    def lines(self):
        self.board_canvas.create_line(SQSIZE, 0, SQSIZE, height, fill='white', width=10)
        self.board_canvas.create_line((width - SQSIZE), 0, (width - SQSIZE), height, fill='white', width=10)
        self.board_canvas.create_line(0, SQSIZE, width, SQSIZE, fill='white', width=10)
        self.board_canvas.create_line(0, (height - SQSIZE), width, (height - SQSIZE), fill='white', width=10)

    def next_turn(self):

        self.player = self.player % 2 + 1
        if self.mouse_event == 1:
            self.user()
        else:
            print("AI")
            self.ai_turn()

    def is_over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

    def ai_turn(self):
        if self.player == 2 and self.running==True:
            row, col = self.ai.eval_fun(self.board)
            self.board.mark_sqr(row, col, self.player)
            self.draw_fig(row, col)
            if self.is_over():
                self.running = False
            else:
                self.next_turn()

    def onclick_start_game(self, games_page_canvas):
        games_page_canvas.destroy()
        self.tictactoe_canvas = Canvas(window, width=400, height=400, bg='black')
        self.tictactoe_canvas.pack(fill="both", expand=True)
        go_back = Button(self.tictactoe_canvas, text="Go Back", font=('Arial', 20, 'bold'), bg='blue', fg='white',
                         command=lambda: self.go_back(self.tictactoe_canvas))
        go_back.pack()
        name = askstring('Your Name', 'Please Enter your name: ?')
        button_frame = self.tictactoe_canvas.create_window(30, 20, width=150, height=60, anchor="nw", window=go_back)
        label = Label(self.tictactoe_canvas, text=f"{name}: X" + "          " + "Computer: O", font=('Arial', 30, 'bold'),
                      bg="black", fg="#F2F7FF")
        label.place(x=430, y=10)
        self.board_canvas = Canvas(self.tictactoe_canvas, width=width, height=height, bg='black',
                                   highlightbackground='black')
        self.board_canvas.place(x=460, y=150)
        self.lines()

        self.board = Board()

        self.ai = AI()
        self.user()


    def user(self):
        window.bind("<Button>", self.mouse_event)

    def reset(self):

        self.tictactoe_canvas.destroy()
        self.onclick_start_game(games_page_canvas)


    def go_back(self, tictactoe_canvas):
        tictactoe_canvas.destroy()
        games_page_opening(welcome_page_canvas)


class Pong:
    def __init__(self, games_page_canvas):
        self.games_page_canvas = games_page_canvas
        whole_pong_frame = Frame(self.games_page_canvas)
        whole_pong_frame.pack()
        self.y = 0
        self.player1_score = 0
        self.player2_score = 0
        self.dx = 5
        self.dy = 5

        frame1_window = games_page_canvas.create_window(450, 550, width=300, height=270, window=whole_pong_frame)
        button = Button(whole_pong_frame, text="Start the Game", width=110, bg='#063970', font=('Arial', 20, 'bold'),
                        fg='white', command=lambda: self.onclick_pong())
        button.pack(side=BOTTOM)
        self.pong_bgimg(whole_pong_frame)

    def pong_bgimg(self, whole_pong_frame):
        global pong_image
        pong_image = ImageTk.PhotoImage(Image.open("pong_bgimg.png"))
        frame_canvas = Canvas(whole_pong_frame, width=300, height=300)
        frame_canvas.pack(fill="both", expand=True)
        frame_canvas.create_image(0, 0, image=pong_image, anchor="nw")

    def onclick_pong(self):
        self.games_page_canvas.destroy()

        self.pong_canvas = Canvas(window, width=400, height=400, bg='black')
        self.pong_canvas.pack(fill="both", expand=True)
        start_button = Button(self.pong_canvas, text="Start", font=('Arial', 20, 'bold'), bg='#00FF00', fg='white',
                              command=self.start_game)
        start_button.pack()
        button_frame = self.pong_canvas.create_window(520, 650, width=120, height=60,
                                                      anchor="nw",
                                                      window=start_button)
        stop_button = Button(self.pong_canvas, text="Stop", font=('Arial', 20, 'bold'), bg='red', fg='white',
                             command=self.stop)
        stop_button.pack()
        stop_frame = self.pong_canvas.create_window(670, 650, width=120, height=60,
                                                    anchor="nw",
                                                    window=stop_button)

        self.black_canvas = Canvas(self.pong_canvas, bg='black')
        self.black_canvas.pack()
        window_frame = self.pong_canvas.create_window(250, 30, width=800, height=600,
                                                      anchor="nw",
                                                      window=self.black_canvas)
        go_back = Button(self.pong_canvas, text="Go Back", font=('Arial', 20, 'bold'), bg='blue', fg='white',
                         command=lambda: self.go_back(self.pong_canvas))
        go_back.pack()
        button_frame = self.pong_canvas.create_window(30, 20, width=150, height=60,
                                                      anchor="nw",
                                                      window=go_back)

        self.center_line(self.black_canvas)
        self.paddle_left = self.black_canvas.create_rectangle(0, 200, 20, 310, fill='white')

        self.paddle_right = self.black_canvas.create_rectangle(780, 200, 800, 310, fill='white')
        self.ball = self.black_canvas.create_oval(400, 300, 420, 320, fill='white')
        self.score = self.black_canvas.create_text(380, 50, fill='white', font='Courier 24 normal',
                                                   text=(f'Player 1: 0   Player 2: 0'))
        messagebox.showinfo("Instructions: ",
                            "'w' for moving the left paddle Up,  's' for moving the left paddle Down,  'p' for right paddle Up,  'l' for moving the right paddle Down")
        window.bind("<Key>", self.key_pressed)

    def reset(self):

        self.playing = False
        self.player1_score = 0
        self.player2_score = 0
        self.black_canvas.delete(self.score)
        self.score = self.black_canvas.create_text(380, 50, fill='white', font='Courier 24 normal',
                                                   text=(f'Player 1: 0   Player 2: 0'))
        self.start_game()

    def stop(self):
        self.playing = False

    def start_game(self):
        self.playing = True
        while self.playing:
            self.moving_the_ball()

    def key_pressed(self, event):
        if event.keysym == 's':
            print("text")
            self.paddle_left_down(self.black_canvas, self.paddle_left)
        if event.keysym == 'w':
            self.paddle_left_up(self.black_canvas, self.paddle_left)
        if event.keysym == 'p':
            self.paddle_right_up(self.black_canvas, self.paddle_right)
        if event.keysym == 'l':
            self.paddle_right_down(self.black_canvas, self.paddle_right)

    def center_line(self, pong_frame):
        pong_frame.create_line(400, 0, 400, 700, fill='white', width=4)

    def paddle_left_down(self, black_canvas, paddle_left):
        y = black_canvas.coords(paddle_left)
        print(y)
        y_axis = []
        for i in range(len(y)):
            if i % 2 != 0:
                y[i] += 100
                y_axis.append(y[i])
            else:
                y_axis.append(y[i])
        print(y_axis)
        black_canvas.delete(paddle_left)
        self.paddle_left = black_canvas.create_rectangle(y_axis, fill='white')

    def paddle_left_up(self, black_canvas, paddle_left):
        y = black_canvas.coords(paddle_left)
        print(y)
        y_axis = []
        for i in range(len(y)):
            if i % 2 != 0:
                y[i] -= 100
                y_axis.append(y[i])
            else:
                y_axis.append(y[i])
        print(y_axis)
        black_canvas.delete(paddle_left)
        self.paddle_left = black_canvas.create_rectangle(y_axis, fill='white')

    def paddle_right_down(self, black_canvas, paddle_right):
        y = black_canvas.coords(paddle_right)
        print(y)
        y_axis = []
        for i in range(len(y)):
            if i % 2 != 0:
                y[i] += 100
                y_axis.append(y[i])
            else:
                y_axis.append(y[i])
        print(y_axis)
        black_canvas.delete(paddle_right)
        self.paddle_right = black_canvas.create_rectangle(y_axis, fill='white')

    def paddle_right_up(self, black_canvas, paddle_right):
        y = black_canvas.coords(paddle_right)
        print(y)
        y_axis = []
        for i in range(len(y)):
            if i % 2 != 0:
                y[i] -= 100
                y_axis.append(y[i])
            else:
                y_axis.append(y[i])
        print(y_axis)
        black_canvas.delete(paddle_right)
        self.paddle_right = black_canvas.create_rectangle(y_axis, fill='white')

    def moving_the_ball(self):
        time.sleep(0.017)
        self.black_canvas.move(self.ball, self.dx, self.dy)

        # Position of ball
        self.ball_pos = self.black_canvas.coords(self.ball)
        self.paddle1_pos = self.black_canvas.coords(self.paddle_left)
        self.paddle2_pos = self.black_canvas.coords(self.paddle_right)
        # coords makes a list with 4 values[top left x,y, bottom right x,y]

        # Ball bounce at top/bottom
        if self.ball_pos[1] <= 0 or self.ball_pos[3] >= 600:
            self.dy *= -1

        # Paddle 1:
        if self.ball_pos[0] <= self.paddle1_pos[2] and self.ball_pos[0] >= self.paddle1_pos[0] and self.dx < 0:
            if self.ball_pos[3] >= self.paddle1_pos[1] and self.ball_pos[1] <= self.paddle1_pos[3]:
                self.dx *= -1

        # Paddle 2:
        elif self.ball_pos[2] >= self.paddle2_pos[0] and self.ball_pos[2] <= self.paddle2_pos[2] and self.dx > 0:
            if self.ball_pos[3] >= self.paddle2_pos[1] and self.ball_pos[1] <= self.paddle2_pos[3]:
                self.dx *= -1

        # Score player 1:
        if self.ball_pos[2] >= 800:
            self.dx *= -1
            self.black_canvas.coords(self.ball, 400, 300, 420, 320)
            self.player1_score += 1

            self.black_canvas.delete(self.score)
            self.score = self.black_canvas.create_text(380, 50, fill='white', font='Courier 24 normal',
                                                       text=(
                                                           f'Player 1: {self.player1_score}   Player 2: {self.player2_score}'))
            if self.player1_score == 5:
                yes_no = messagebox.askyesno("yesorno",
                                             "Hurrah!! Player1 has Won the Game. Do You want to play again ?")
                if yes_no == True:
                    self.player1_score = 0
                    self.player2_score = 0
                    self.black_canvas.delete(self.score)
                    self.score = self.black_canvas.create_text(380, 50, fill='white', font='Courier 24 normal',
                                                               text=(f'Player 1: 0   Player 2: 0'))
                else:
                    self.pong_canvas.destroy()
                    games_page_opening(welcome_page_canvas)

        # Score player 2:
        if self.ball_pos[0] <= 0:
            self.dx *= -1
            self.black_canvas.coords(self.ball, 400, 300, 420, 320)
            self.player2_score += 1

            self.black_canvas.delete(self.score)
            self.score = self.black_canvas.create_text(380, 50, fill='white', font='Courier 24 normal',
                                                       text=(
                                                           f'Player 1: {self.player1_score}   Player 2: {self.player2_score}'))
            if self.player2_score == 5:
                yes_no = messagebox.askyesno("yesorno",
                                             "Hurrah!! Player2 has Won the Game. Do You want to play again ?")
                if yes_no == True:
                    self.player2_score = 0
                    self.player1_score = 0
                    self.black_canvas.delete(self.score)
                    self.score = self.black_canvas.create_text(380, 50, fill='white', font='Courier 24 normal',
                                                               text=(f'Player 1: 0   Player 2: 0'))
                else:
                    self.pong_canvas.destroy()
                    games_page_opening(welcome_page_canvas)

        window.update()

    def go_back(self, pong_canvas):
        self.playing = False
        pong_canvas.destroy()
        games_page_opening(welcome_page_canvas)


class ScoreBoard():

    def __init__(self, parent):
        self.parent = parent
        self.initGUI()
        self.reset()

    def initGUI(self):
        # Lives
        self.livesVar = IntVar()
        Label(self.parent, text="Lives:", font=("Arial", 20, "bold"), fg='black', bg='#BEBEBE').place(x=1100, y=180)
        Label(self.parent, textvariable=self.livesVar, font=("Arial", 20, "italic"), fg='red', bg='#BEBEBE').place(
            x=1120, y=230)

        # Score
        self.scoreVar = IntVar()
        Label(self.parent, text="Score:", font=("Arial", 20, "bold"), fg='black', bg='#BEBEBE').place(x=1100, y=360)
        Label(self.parent, textvariable=self.scoreVar, font=("Arial", 20, "italic"), bg='#BEBEBE', fg='red').place(
            x=1120, y=410)

    def reset(self):
        self.lives = 3
        self.score = 0

        self.livesVar.set(self.lives)
        self.scoreVar.set(self.score)

    def gameOver(self):
        if messagebox.askyesno("Game Over", "Want to Play Aga1n ?"):
            self.reset()
        else:
            self.parent.destroy()
            games_page_opening(welcome_page_canvas)

    def updateBoard(self, livesStatus, scoreStatus):
        self.lives += livesStatus;
        self.score += scoreStatus
        if self.lives < 0: self.gameOver()
        self.livesVar.set(self.lives);
        self.scoreVar.set(self.score)


class EggGame:
    def __init__(self, games_page_canvas, parent):
        whole_egg_frame = Frame(games_page_canvas)
        whole_egg_frame.pack()
        self.parent = parent
        frame1_window = games_page_canvas.create_window(900, 550, width=300, height=270, window=whole_egg_frame)
        button = Button(whole_egg_frame, text="Start the Game", width=110, bg='#063970', font=('Arial', 20, 'bold'),
                        fg='white', command=lambda: self.egg_onclick(games_page_canvas))
        button.pack(side=BOTTOM)
        self.egg_bg_frame(whole_egg_frame)

    def egg_bg_frame(self, whole_egg_frame):
        global egg_image
        egg_image = ImageTk.PhotoImage(Image.open("egg_bg.png"))
        frame_canvas = Canvas(whole_egg_frame, width=300, height=300)
        frame_canvas.pack(fill="both", expand=True)
        frame_canvas.create_image(0, 0, image=egg_image, anchor="nw")

    def egg_onclick(self, game_page_canvas):
        game_page_canvas.destroy()
        self.egg_canvas = Canvas(window, width=400, height=400, bg='#BEBEBE')
        self.egg_canvas.pack(fill="both", expand=True)
        self.score_board = ScoreBoard(self.egg_canvas)
        self.black_canvas = Canvas(self.egg_canvas, bg='black')
        self.black_canvas.pack()
        window_frame = self.egg_canvas.create_window(250, 20, width=800, height=620,
                                                     anchor="nw",
                                                     window=self.black_canvas)
        window.bind("<Key>", self.key_moments)
        self.basket = ImageTk.PhotoImage(Image.open("basket.png"))
        self.basket_place = self.black_canvas.create_image(475, 560, image=self.basket)

        go_back = Button(self.egg_canvas, text="Go Back", font=('Arial', 20, 'bold'), bg='blue', fg='white',
                         command=lambda: self.go_back(self.egg_canvas))
        go_back.pack()
        button_frame = self.egg_canvas.create_window(30, 20, width=150, height=60,
                                                     anchor="nw",
                                                     window=go_back)
        start_button = Button(self.egg_canvas, text="Start", font=('Arial', 20, 'bold'), bg='#00FF00', fg='white',
                              command=self.create_attacks)
        start_button.pack()
        button_frame = self.egg_canvas.create_window(620, 650, width=120, height=60,
                                                     anchor="nw",
                                                     window=start_button)
        messagebox.showinfo("Instructions: ", "Use '1' and '3' for moving the basket")

    def key_moments(self, event):
        if (event.keysym == "1") and (self.black_canvas.coords(self.basket_place)[0] > 50):
            self.black_canvas.move(self.basket_place, -50, 0)

        if (event.keysym == "3") and (self.black_canvas.coords(self.basket_place)[0] < 750):
            self.black_canvas.move(self.basket_place, 50, 0)

        window.update()

    def go_back(self, egg_canvas):
        egg_canvas.destroy()
        games_page_opening(welcome_page_canvas)

    def create_attacks(self):
        ItemsFallingFromSky(window, self.black_canvas, self.basket_place, self.egg_canvas, self.score_board)
        self.parent.after(1100, self.create_attacks)


class ItemsFallingFromSky():

    def __init__(self, parent, canvas, player, egg_canvas, board):
        self.parent = parent  # root form
        self.canvas = canvas  # canvas to display
        self.player = player  # to check touching
        self.egg_canvas = egg_canvas
        self.board = board
        # score board statistics

        self.fallSpeed = 50  # falling speed
        self.xPosition = randint(50, 750)  # random position
        self.isgood = randint(0, 1)  # random goodness

        self.goodItems = ["golden_egg.png", "brown_egg.png"]
        self.badItems = ["snake_falling.png", "rabbit.png"]

        # create falling items
        if self.isgood:
            self.itemPhoto = PhotoImage(file="{}".format(choice(self.goodItems)))
            self.fallItem = self.canvas.create_image((self.xPosition, 50), image=self.itemPhoto, tag="good")
        else:
            self.itemPhoto = PhotoImage(file="{}".format(choice(self.badItems)))
            self.fallItem = self.canvas.create_image((self.xPosition, 50), image=self.itemPhoto, tag="bad")

        self.move_object()

    def move_object(self):
        # dont move x, move y
        self.canvas.move(self.fallItem, 0, 15)

        if (self.check_touching()) or (self.canvas.coords(self.fallItem)[1] > 650):
            self.canvas.delete(self.fallItem)
        else:
            self.parent.after(self.fallSpeed, self.move_object)

    def check_touching(self):

        #     # find current coordinates
        x0, y0 = self.canvas.coords(self.fallItem)
        x1, y1 = x0 + 50, y0 + 50
        #
        # get overlapps
        overlaps = self.canvas.find_overlapping(x0, y0, x1, y1)

        if (self.canvas.gettags(self.fallItem)[0] == "good") and (len(overlaps) > 1) and (self.board.lives >= 0):
            self.board.updateBoard(0, 100)
            return True

        elif (self.canvas.gettags(self.fallItem)[0] == "bad") and (len(overlaps) > 1) and (self.board.lives >= 0):
            self.board.updateBoard(-1, 0)
            return True

        return False


# class Balloon:
#     def __init__(self, games_page_canvas):
#         whole_balloon_frame = Frame(games_page_canvas)
#         whole_balloon_frame.pack()
#         frame1_window = games_page_canvas.create_window(1050, 550, width=300, height=270, window=whole_balloon_frame)
#         button = Button(whole_balloon_frame, text="Start the Game", width=110, bg='#063970', font=('Arial', 20, 'bold'),
#                         fg='white')
#         button.pack(side=BOTTOM)
#         self.balloon_bg_frame(whole_balloon_frame)
#
#     def balloon_bg_frame(self, whole_egg_frame):
#         global balloon_image
#         balloon_image = ImageTk.PhotoImage(Image.open("balloon_bg.png"))
#         frame_canvas = Canvas(whole_egg_frame, width=300, height=300)
#         frame_canvas.pack(fill="both", expand=True)
#         frame_canvas.create_image(0, 0, image=balloon_image, anchor="nw")


if __name__ == "__main__":
    window = Tk()
    window.state("zoomed")
    window.title("OLDIE GAMES")
    icon = PhotoImage(file="dices.png")
    window.iconphoto(True, icon)
    window.resizable(False, False)
    bg = PhotoImage(file="bg.png")
    welcome_page_canvas = Canvas(window, width=400, height=400)
    welcome_page_canvas.pack(fill="both", expand=True)
    welcome_page_canvas.create_image(0, 0, image=bg, anchor="nw")
    button1 = Button(window, text="Let's Get Started", font=('Arial', 25, 'bold'), fg='white', bg='#6b98cf',
                     command=lambda: games_page_opening(welcome_page_canvas))
    button1_canvas = welcome_page_canvas.create_window(220, 560, width=280, height=70,
                                                       anchor="nw",
                                                       window=button1)
    global snake_image
    global rockpaper
    global rock_image
    global scissor_image
    global paper_image
    global pong_image
    global egg_image
    global balloon_image, games_page_canvas

    window.mainloop()
