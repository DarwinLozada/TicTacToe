import tkinter as tk
from tkinter import FLAT, messagebox
from PIL import Image, ImageTk
from tkinter.font import Font


class GameBoard(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.config(bg="black")
        self.turn = "x"
        self.blank_image = Image.open(r"images\none.png")
        self.x_image = Image.open(r"images\equis.png")
        self.circle = Image.open(r"images\circulo.png")
        self.font = Font(family="Arial", size=12)

        def check_horizontal_win(range_list):
            for i in range_list:
                if self.num_pad[i].count('o') == len(self.num_pad[i]):
                    claim_victory("o")
                    return True

                elif self.num_pad[i].count('x') == len(self.num_pad[i]):
                    claim_victory("x")
                    return True

        def check_vertical_win(range_list, len_list):
            for sub_list in range_list:
                xv_counter = 0
                ov_counter = 0

                for num in range(len_list + 1):

                    if ov_counter == len_list:
                        claim_victory("o")
                        return True

                    elif xv_counter == len_list:
                        claim_victory("x")
                        return True

                    else:
                        try:

                            if self.num_pad[num][sub_list] == "o":
                                ov_counter += 1

                            if self.num_pad[num][sub_list] == "x":
                                xv_counter += 1

                        except IndexError:
                            break

        def check_inclined_win(len_list):
            x_left_counter = 0
            x_right_counter = 0
            o_left_counter = 0
            o_right_counter = 0

            for i in range(len_list + 1):
                if x_left_counter == len_list or x_right_counter == len_list:
                    claim_victory("x")
                    return True

                elif o_left_counter == len_list or o_right_counter == len_list:
                    claim_victory("o")
                    return True
                else:
                    try:
                        if self.num_pad[0 + i][0 + i] == "x":
                            x_left_counter += 1

                        if self.num_pad[0 + i][len_list - i - 1] == "x":
                            x_right_counter += 1

                        if self.num_pad[0 + i][0 + i] == "o":
                            o_left_counter += 1

                        if self.num_pad[0 + i][len_list - i - 1] == "o":
                            o_right_counter += 1

                    except IndexError:
                        break

        def check_if_tie(table_length):
            draw = False
            draw_counter = 0
            for sub_list in self.num_pad:
                if sub_list.count("~") == 0:
                    draw_counter += 1

                if draw_counter == table_length:
                    draw = True

            return draw

        def play(button_got):
            player_turn = self.turn
            if not button_got.played:
                if player_turn == "o":
                    button_got.symbol = "o"
                    self.turn = "x"

                    button_got.config(image=self.o_button)
                    button_got.played = True

                else:
                    button_got.symbol = "x"
                    self.turn = "o"
                    button_got.config(image=self.x_button)
                    button_got.played = True

            check_button(button_got)

            range_of_grid_length = range(len(self.num_pad[0]))
            len_num_pad = len(self.num_pad[0])

            if check_horizontal_win(range_of_grid_length) or check_vertical_win(range_of_grid_length,
                                                                                len_num_pad) or check_inclined_win(
                len_num_pad):
                pass

            elif check_if_tie(len_num_pad):
                claim_victory("~")

        def claim_victory(winner):
            if winner == "~":
                restart = tk.messagebox.askyesno("Play again", "There was a tie. Do you want to play again?")
            else:
                restart = tk.messagebox.askyesno("Play again", f"Player {winner.capitalize()} is the winner! Do you "
                                                               f"want to play again? ")

            if restart:
                return refresh()
            else:
                return root.destroy()

        def check_button(button_got):
            if button_got.symbol == "o":
                self.num_pad[button_got.list_num][button_got.position] = button_got.symbol
            elif button_got.symbol == "x":
                self.num_pad[button_got.list_num][button_got.position] = button_got.symbol

        self.num_pad = [["~", "~", "~"],
                        ["~", "~", "~"],
                        ["~", "~", "~"]]

        blank = self.blank_image.resize((110, 110))
        self.blank_button = ImageTk.PhotoImage(blank)

        for index, sublist in enumerate(self.num_pad):
            for sub_index, sub_value in enumerate(sublist):
                new_button = tk.Button(self, relief=FLAT, bg="white", image=self.blank_button,
                                       activebackground="white", width=110, height=110)
                x = self.x_image.resize((80, 80))
                o = self.circle.resize((80, 80))
                self.x_button = ImageTk.PhotoImage(x)
                self.o_button = ImageTk.PhotoImage(o)
                new_button.configure(command=lambda button=new_button: play(button))
                setattr(new_button, "list_num", index)
                setattr(new_button, "symbol", "-")
                setattr(new_button, "position", sub_index)
                setattr(new_button, "played", False)
                new_button.grid(row=index, column=sub_index, padx=4, pady=3, sticky="NSEW")


def main():
    global root
    root = tk.Tk()
    root.title("TicTacToe")
    root.minsize(350, 350)
    game = GameBoard(root)
    game.grid(sticky="NSEW")
    root.iconphoto(True, tk.PhotoImage(file=r"images\Tictactoe.png"))
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()


if __name__ == "__main__":
    def refresh():
        root.destroy()
        main()


    main()
