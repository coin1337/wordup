import random
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import requests

def start_new_game():
    global secret_word, attempts, guessed_letters
    guessed_letters = []
    secret_word = get_random_word()
    while secret_word is None:
        secret_word = get_random_word()
    attempts = 6
    result_label.config(text=f"Attempts left: {attempts}\nWord: {display_word(secret_word, guessed_letters)}")

def show_credits():
    credits_window = Toplevel(window)
    credits_window.title("Credits")
    credits_label = ttk.Label(credits_window, text="Composed by x5ee", font=("Arial", 14))
    credits_label.pack(padx=20, pady=20)

# initialize variables
attempts = 6
guessed_letters = []

def get_random_word():
    try:
        response = requests.get("https://api.datamuse.com/words?sp=?????")
        response.raise_for_status()
        data = response.json()
        # filter words to ensure they are 5 letters long and all lowercase
        five_letter_words = [word['word'] for word in data if word['word'].isalpha() and len(word['word']) == 5]
        if five_letter_words:
            return random.choice(five_letter_words)
        else:
            return None
    except Exception as e:
        print(f"Error fetching word: {e}")
        return None

# select a random word from the Datamuse API
secret_word = get_random_word()

while secret_word is None:
    secret_word = get_random_word()

def on_entry_click(event):
    if entry.get() == 'Enter word here..':
        entry.delete(0, "end")
    entry.config(foreground="black")

def check_guess():
    global attempts  # use global instead of nonlocal for a global variable
    guess = entry.get().lower()
    entry.delete(0, tk.END)
    
    if len(guess) != 5 or not guess.isalpha():
        messagebox.showerror("Invalid Guess", "Please enter a valid 5-letter word.")
        return
    
    if guess in guessed_letters:
        messagebox.showerror("Already Guessed", "You've already guessed that word.")
        return
    
    guessed_letters.append(guess)
    
    if guess == secret_word:
        messagebox.showinfo("Congratulations", f"You've guessed the word: {secret_word}")
        choice = messagebox.askquestion("New Game", "Do you want to start a new game?")
        if choice == 'yes':
            start_new_game()
        else:
            window.quit()
    else:
        result_text = f"Attempts left: {attempts}\nWord: {display_word(secret_word, guessed_letters)}"
        incorrect_positions = []
        for i, letter in enumerate(guess):
            if letter != secret_word[i]:
                incorrect_positions.append(letter)
        if incorrect_positions:
            result_text += f"\nIncorrect positions: {' '.join(incorrect_positions)}"
        if attempts == 1:
            result_text += "\nOut of Attempts: The word was not guessed."
            choice = messagebox.askquestion("New Game", "Do you want to start a new game?")
            if choice == 'yes':
                start_new_game()
            else:
                window.quit()
        else:
            attempts = attempts - 1
        result_label.config(text=result_text)

def display_word(secret_word, guessed_letters):
    displayed_word = ""
    for i, letter in enumerate(secret_word):
        if letter in guessed_letters:
            displayed_word += letter
        else:
            displayed_word += "_"
    return displayed_word


# create the GUI window
window = tk.Tk()
window.title("Wordup")
window.geometry("800x600")

# create and configure style
style = ttk.Style()
style.configure("TLabel", font=("Arial", 14))
style.configure("TButton", font=("Arial", 14))
style.configure("TEntry", font=("Arial", 14))

# create and configure widgets
instructions_label = ttk.Label(window, text="Welcome to Wordup! Guess the 5-letter word.")
instructions_label.pack(pady=(10, 20))

# entry box with hint text
entry = ttk.Entry(window, show='', foreground='gray')
entry.pack(pady=10)
entry.insert(0, 'Enter word here..')
entry.bind("<FocusIn>", on_entry_click)

submit_button = ttk.Button(window, text="Guess", command=check_guess)
submit_button.pack(pady=(10, 0))

result_label = ttk.Label(window, text=f"Attempts left: {attempts}\nWord: {display_word(secret_word, guessed_letters)}")
result_label.pack(pady=(20, 0))

# add the "Credits" button with adjusted padding
credits_button = ttk.Button(window, text="Credits", command=show_credits)
credits_button.pack(pady=(0, 20))

# adjust the font size for all ttk.Button widgets globally
style.configure("TButton", font=("Arial", 12))

# start the GUI event loop
window.mainloop()
