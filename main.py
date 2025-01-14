#---------- Importing necessary modules and constants -----------#
from constants import *
from tkinter import *
import pandas
import random


#---------- Main FlashCardApp Class -----------#
class FlashCardApp:
    def __init__(self):
        """Initialize the FlashCardApp, including data setup, main window setup, 
        and UI elements."""
        # Dictionary to store the current card and words to learn
        self.current_card = {}
        self.to_learn = {}

        # Load the data file or fall back to the original data if not found
        try:
            self.data = pandas.read_csv("data/words_to_learn.csv")
        except FileNotFoundError:
            self.original_data = pandas.read_csv("data/french_words.csv")
            self.to_learn = self.original_data.to_dict(orient="records")
        else:
            self.to_learn = self.data.to_dict(orient="records")

        # Initialize the main application window
        self.main_window_setup()
        
        # Timer for flipping the card
        self.flip_timer = self.main_window.after(3000, func=self.flip_card)
        
        # Set up UI components
        self.canvas_field()
        self.right_button_field()
        self.wrong_button_field()
        
        # Load the first word
        self.get_words()

    #---------- Setting up the Main Window -----------#
    def main_window_setup(self):
        """Set up the main Tkinter window."""
        self.main_window = Tk()
        self.main_window.config(padx=40, pady=40, bg=BACKGROUND_COLOR)
        self.main_window.title("Flash Card App")
        self.main_window.resizable(1, 1)

    #---------- Setting up the Canvas Field -----------#
    def canvas_field(self):
        """Set up the canvas field with card images, title text, and word text."""
        self.canvas = Canvas(width=800, height=800, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.card_front_img = PhotoImage(file=FRONT_CARD_IMG)
        self.card_back_img = PhotoImage(file=BACK_CARD_IMG)
        self.canvas_image = self.canvas.create_image(400, 400, image=self.card_front_img)
        self.canvas.grid(row=1, column=1, columnspan=2)

        # Create text fields for card title and word
        self.title_text = self.canvas.create_text(400, 250, text="", font=(FONT, 40, "italic"))
        self.word_text = self.canvas.create_text(400, 400, text="", font=(FONT, 60, "bold"))

    #---------- Adding the Right Button -----------#
    def right_button_field(self):
        """Set up the right button for marking a word as known."""
        self.right_button_img = PhotoImage(file=RIGHT_IMG)
        self.right_button = Button(image=self.right_button_img, width=100, height=100, 
                                   highlightthickness=0, command=self.is_known)
        self.right_button.grid(row=2, column=1)

    #---------- Adding the Wrong Button -----------#
    def wrong_button_field(self):
        """Set up the wrong button for skipping a word."""
        self.wrong_button_img = PhotoImage(file=WRONG_IMG)
        self.wrong_button = Button(image=self.wrong_button_img, width=100, height=100, 
                                   highlightthickness=0, command=self.get_words)
        self.wrong_button.grid(row=2, column=2)

    #---------- Getting a New Word -----------#
    def get_words(self):
        """Choose a new word to display on the card."""
        self.main_window.after_cancel(self.flip_timer)  # Cancel previous flip timer
        self.current_card = random.choice(self.to_learn)  # Pick a random word

        # Update the card with the new word
        self.canvas.itemconfig(self.canvas_image, image=self.card_front_img)
        self.canvas.itemconfig(self.title_text, text="French", fill="black")
        self.canvas.itemconfig(self.word_text, text=self.current_card["French"], fill="black")

        # Reset the flip timer
        self.flip_timer = self.main_window.after(3000, func=self.flip_card)

    #---------- Flipping the Card -----------#
    def flip_card(self):
        """Flip the card to show the English translation."""
        self.canvas.itemconfig(self.canvas_image, image=self.card_back_img)
        self.canvas.itemconfig(self.title_text, text="English", fill="white")
        self.canvas.itemconfig(self.word_text, text=self.current_card["English"], fill="white")

    #---------- Marking a Word as Known -----------#
    def is_known(self):
        """Remove the current word from the learning list and save the updated list."""
        self.to_learn.remove(self.current_card)  # Remove the known word
        self.data = pandas.DataFrame(self.to_learn)  # Convert back to DataFrame
        self.data.to_csv("data/words_to_learn.csv", index=False)  # Save updated list
        self.get_words()  # Load a new word

    #---------- Running the Application -----------#
    def run(self):
        """Run the Tkinter event loop to start the application."""
        self.main_window.mainloop()


#---------- Starting the Application -----------#
if __name__ == "__main__":
    app = FlashCardApp()
    app.run()
