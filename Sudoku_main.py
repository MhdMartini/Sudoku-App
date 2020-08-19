from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
# from sudoku_generator import SudokuGenerator
from sudoku_gui import SudokuGenerator
import random
import numpy as np
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from itertools import combinations
from time import time


# TODO: Turn revealed_buttons into a dictionary of numbers as keys and buttons as values,\
#  when a button completes, remove its button from bottom_widget

class TopWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1


class GridWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 9


class BottomWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 9


class SudokuButton(Button):
    # Define colors
    black = (0, 0, 0)
    transparent = (3, 3, 3, 0.3)
    dark_gray = (0.2, 0.2, 0.2, 1)
    light_blue = (0, 0.4, 0.8, 1)
    dark_blue = (0, 0.1, 0.2, 1)
    sky_blue = (0.4, 0.7, 1, 0.3)
    blue = (0.4, 0.7, 1, 0.7)
    value = ""
    select = True
    revealed = False
    highlighted = False

    def __init__(self, value=None, row=0, col=0, **kwargs):
        super(SudokuButton, self).__init__(**kwargs)
        # Save Button value
        self.value = value

        # Configure Button
        self.background_color = self.transparent
        self.color = self.dark_blue
        self.font_size = 26

        # Save Button coordinates
        self.row = row
        self.col = col

        # self.revealed = False

    def __repr__(self):
        return str(self.value)


class PencilButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PencilButton, self).__init__(**kwargs)
        self.source = 'atlas://data/images/defaulttheme/checkbox_off'

    def on_state(self, widget, value):
        if value == 'down':
            self.source = "pencil.jpg"
        else:
            self.source = 'atlas://data/images/defaulttheme/checkbox_off'


class LowerButtons(Button):
    # Define colors
    black = (0, 0, 0)
    transparent = (3, 3, 3, 0)
    dark_gray = (0.2, 0.2, 0.2, 1)
    light_blue = (0, 0.4, 0.8, 1)
    dark_blue = (0, 0.1, 0.2, 1)
    sky_blue = (0.4, 0.7, 1, 0.3)
    blue = (0.4, 0.7, 1, 0.7)
    value = ""
    select = True
    revealed = False
    highlighted = False
    state = False

    def __init__(self, value=None, **kwargs):
        super(LowerButtons, self).__init__(**kwargs)
        # Save Button value
        self.value = value

        # Configure Button
        self.background_color = self.transparent
        self.color = self.dark_blue
        self.font_size = 26


class SudokuGUI(FloatLayout):
    revealed_buttons = []
    # Highlighted buttons when a certain grid button is pressed
    last_button = None
    selected_buttons = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the three GridLayouts
        self.top_widget = TopWidget()
        self.grid_widget = GridWidget()
        self.bottom_widget = BottomWidget()

        # Configure position and size of GridLayouts
        self.top_widget.pos_hint = {"x": 0.02, "top": 1}
        self.top_widget.size_hint = (1 - 0.04, 1 / 6)
        self.grid_widget.pos_hint = {"x": 0.02, "y": 1 / 4}
        self.grid_widget.size_hint = (1 - 0.04, 1 / 2)
        self.bottom_widget.pos_hint = {"x": 0.02, "bottom": 1}
        self.bottom_widget.size_hint = (1 - 0.04, 1 / 4)

        # Add GridLayouts to FloatLayout
        self.add_widget(self.top_widget)
        self.add_widget(self.grid_widget)
        self.add_widget(self.bottom_widget)

        # TODO: Fill with useful stuff
        self.top_widget.add_widget(Label(text="Top"))
        self.fill_bottom_widget()

        # Create Buttons and find symmetric buttons
        self.raw_sheet, self.buttons_sheet = self.create_sheet()

    def fill_bottom_widget(self):
        # Pad with an empty upper and empty lower
        for _ in range(8):
            self.bottom_widget.add_widget(Label())

        # Add the pencil button
        self.pencil = PencilButton(on_press=lambda x: print(self.pencil.state))
        self.bottom_widget.add_widget(self.pencil)

        # Add other numbers buttons
        for i in range(1, 10):
            btn = LowerButtons(text=str(i), value=i, on_press=self.fill)

            self.bottom_widget.add_widget(btn)

        # Pad with an empty upper and empty lower
        for _ in range(9):
            self.bottom_widget.add_widget(Label())

    def fill(self, btn):
        valid_buttons = []
        for button in self.selected_buttons[::-1]:
            # If all buttons are valid, reveal buttons, else, mark wrong
            # TODO: ADD X Marking
            valid = self.validate(btn, button)

            if valid:
                valid_buttons.append(button)
                continue
            print("Wrong!!")
            return

        for btn in valid_buttons:
            self.reveal_button(btn, user=True)

    def create_sheet(self, difficulty=50, side_length=9):

        t = time()
        game_sheet, raw_sheet = SudokuGenerator().generate_sln()
        # print(game_sheet)
        buttons_sheet = np.array([[None for _ in range(side_length)] for _ in range(side_length)])

        for i in range(side_length):

            for j in range(side_length):
                # Create Buttons, add them to list, and show them on screen

                row, col = i, j
                button = SudokuButton(value=raw_sheet[i][j], row=row, col=col,
                                      on_press=self.highlight)

                buttons_sheet[i][j] = button
                self.grid_widget.add_widget(button)
                if game_sheet[row][col] != 0:
                    button.revealed = True
                else:
                    button.revealed = False

        for row in buttons_sheet:
            for btn in row:
                if btn.revealed:
                    self.reveal_button(btn)

        print(time() - t)
        return raw_sheet, buttons_sheet

    def reveal_button(self, btn, user=False):
        self.revealed_buttons.append(btn)
        if len(self.revealed_buttons) == 81:
            # TODO: Do more
            print("Congrats!!!")
        # btn.revealed = True

        btn.value = repr(btn)
        btn.text = f"[b]{repr(btn)}[/b]"
        btn.markup = True

        if user:
            btn.revealed = True
            del (self.selected_buttons[self.selected_buttons.index(btn)])
            self.highlight_row(btn)
            self.highlight_col(btn)
            self.highlight_sector(btn)

    def validate(self, btn, button):
        if button.value != btn.value:
            return False

        else:
            # self.reveal_button(button, user=True)
            return True

    def highlight(self, button):
        # Clear existing highlights
        # Collect coordinates of pressed button value across the grid
        # Highlight rows, columns, sectors, and numbers

        # Toggles at every button press
        # Used to change button color based on whether it is already selected or not
        # button.select = not button.select

        # If pressed on empty button, change that button's highlight based on whether it has been selected
        # and based on whether it is highlighted
        if not button.revealed:
            button.select = not button.select
            if button.select:
                if button.highlighted:
                    button.background_color = button.sky_blue
                    del (self.selected_buttons[self.selected_buttons.index(button)])
                else:
                    button.background_color = button.transparent
                    try:
                        del (self.selected_buttons[self.selected_buttons.index(button)])
                        button.highlighted = False
                        button.select = True
                    except ValueError:
                        pass
            else:
                button.background_color = button.blue
                self.selected_buttons.append(button)

            return

        # If the same button is pressed twice, clear all highlights
        if self.last_button == button:
            self.last_button = None
            self.reset_highlight(button)
            return

        self.last_button = button

        # If pressed on a revealed button, reset all highlights place new highlights
        self.reset_highlight(button)

        if not button.revealed:
            return

        buttons = []
        for row in self.buttons_sheet:
            for btn in row:
                # If the button has the same value as the pressed button,
                # highlight it and highlight its rows and columns and sector

                btn.select = True

                # Highlight all in place, then un-highlight remaining buttons
                if btn.revealed and (btn.value == button.value):
                    buttons.append(btn)

        for btn in buttons:
            # Highlight row, column, and sector, and return highlighted buttons
            self.highlight_row(btn)
            self.highlight_col(btn)
            self.highlight_sector(btn)

            # Highlight direct row and column and quadrant with darker shade
            # self.highlight_row(button, main_row=True)
            # self.highlight_col(button, main_col=True)
            # self.highlight_sector(button, main_sector=True)

    def reset_highlight(self, button):
        # Clear selected_buttons list
        self.selected_buttons = []
        # Reset buttons highlight and numbers color
        for row in self.buttons_sheet:
            for btn in row:
                btn.background_color = btn.transparent
                btn.color = btn.dark_blue
                btn.highlighted = False

    def highlight_row(self, btn, main_row=False):
        btn.color = btn.light_blue
        btn_row = btn.row
        row = self.buttons_sheet[btn_row]

        if main_row:
            color = btn.blue
        else:
            color = btn.sky_blue

        for button in row:
            button.background_color = color
            button.highlighted = True

    def highlight_col(self, btn, main_col=False):
        # Transpose the buttons sheet and highlight the column (now row)
        btn_row = btn.col
        temp_sheet = self.buttons_sheet.transpose()
        col = temp_sheet[btn_row]

        if main_col:
            color = btn.blue
        else:
            color = btn.sky_blue

        for button in col:
            button.background_color = color
            button.highlighted = True

    def highlight_sector(self, btn, main_sector=False):
        sector_buttons = self.sector_find(btn)
        linear_sector = sector_buttons.reshape(1, -1)[0]

        if main_sector:
            color = btn.blue
        else:
            color = btn.sky_blue

        for button in linear_sector:
            button.background_color = button.sky_blue
            button.highlighted = True

    def sector_find(self, btn):
        # Given a button's row and column, find its sector
        row, col = btn.row, btn.col
        # By induction:
        sector = btn.col // 3 + (btn.row // 3) * 3

        # Given a sector, find its beginning
        # By induction:
        starting_x = sector * 3 % 9
        starting_y = (sector // 3) * 3

        # Slice sector out of buttons sheet
        sector_buttons = self.buttons_sheet[starting_y: starting_y + 3, starting_x: starting_x + 3]
        return sector_buttons


class SudokuApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return SudokuGUI()


if __name__ == '__main__':
    SudokuApp().run()
