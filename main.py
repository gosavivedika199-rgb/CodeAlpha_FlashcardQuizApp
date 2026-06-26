import customtkinter as ctk
import json
from tkinter import messagebox, simpledialog

# ---------------------------------------
# App Settings
# ---------------------------------------

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# ---------------------------------------
# Load Flashcards
# ---------------------------------------

try:
    with open("flashcards.json", "r") as file:
        flashcards = json.load(file)
except:
    flashcards = []

current_card = 0

# ---------------------------------------
# Save Flashcards
# ---------------------------------------

def save_flashcards():
    with open("flashcards.json", "w") as file:
        json.dump(flashcards, file, indent=4)

# ---------------------------------------
# Display Card
# ---------------------------------------

def display_card():

    if len(flashcards) == 0:
        question_label.configure(text="No Flashcards Available")
        card_number.configure(text="Card 0 of 0")
        return

    question_label.configure(
        text=flashcards[current_card]["question"]
    )

    card_number.configure(
        text=f"Card {current_card+1} of {len(flashcards)}"
    )

# ---------------------------------------
# Show Answer
# ---------------------------------------

def show_answer():

    if len(flashcards) == 0:
        return

    question_label.configure(
        text=flashcards[current_card]["answer"]
    )

# ---------------------------------------
# Next Card
# ---------------------------------------

def next_card():

    global current_card

    if len(flashcards) == 0:
        return

    current_card = (current_card + 1) % len(flashcards)

    display_card()

# ---------------------------------------
# Previous Card
# ---------------------------------------

def previous_card():

    global current_card

    if len(flashcards) == 0:
        return

    current_card = (current_card - 1) % len(flashcards)

    display_card()

# ---------------------------------------
# Add Card
# ---------------------------------------

def add_card():

    question = simpledialog.askstring("Question", "Enter Question")

    if not question:
        return

    answer = simpledialog.askstring("Answer", "Enter Answer")

    if not answer:
        return

    flashcards.append({
        "question": question,
        "answer": answer
    })

    save_flashcards()

    messagebox.showinfo("Success", "Flashcard Added!")

    display_card()

# ---------------------------------------
# Edit Card
# ---------------------------------------

def edit_card():

    if len(flashcards) == 0:
        return

    question = simpledialog.askstring(
        "Edit Question",
        "Question",
        initialvalue=flashcards[current_card]["question"]
    )

    if not question:
        return

    answer = simpledialog.askstring(
        "Edit Answer",
        "Answer",
        initialvalue=flashcards[current_card]["answer"]
    )

    if not answer:
        return

    flashcards[current_card]["question"] = question
    flashcards[current_card]["answer"] = answer

    save_flashcards()

    messagebox.showinfo("Updated", "Flashcard Updated!")

    display_card()

# ---------------------------------------
# Delete Card
# ---------------------------------------

def delete_card():

    global current_card

    if len(flashcards) == 0:
        return

    result = messagebox.askyesno(
        "Delete",
        "Delete this flashcard?"
    )

    if result:

        flashcards.pop(current_card)

        if len(flashcards) == 0:
            current_card = 0
        elif current_card >= len(flashcards):
            current_card = len(flashcards)-1

        save_flashcards()

        display_card()

# ---------------------------------------
# Main Window
# ---------------------------------------

app = ctk.CTk()

app.title("Flashcard Quiz App")
app.geometry("900x620")
app.resizable(False, False)

title = ctk.CTkLabel(
    app,
    text="📚 Flashcard Quiz App",
    font=("Segoe UI",30,"bold")
)

title.pack(pady=(20,5))

subtitle = ctk.CTkLabel(
    app,
    text="Study Smart • Learn Better",
    font=("Segoe UI",16)
)

subtitle.pack()

card_number = ctk.CTkLabel(
    app,
    text="",
    font=("Segoe UI",14,"bold")
)

card_number.pack(pady=5)

card_frame = ctk.CTkFrame(
    app,
    width=700,
    height=250,
    corner_radius=20
)

card_frame.pack(pady=25)

card_frame.pack_propagate(False)

question_label = ctk.CTkLabel(
    card_frame,
    text="",
    font=("Segoe UI",24),
    wraplength=600,
    justify="center"
)

question_label.pack(expand=True)

button_frame = ctk.CTkFrame(app,fg_color="transparent")
button_frame.pack(pady=15)

ctk.CTkButton(
    button_frame,
    text="⬅ Previous",
    width=120,
    command=previous_card
).grid(row=0,column=0,padx=10)

ctk.CTkButton(
    button_frame,
    text="👁 Show Answer",
    width=150,
    command=show_answer
).grid(row=0,column=1,padx=10)

ctk.CTkButton(
    button_frame,
    text="Next ➡",
    width=120,
    command=next_card
).grid(row=0,column=2,padx=10)

bottom_frame = ctk.CTkFrame(app,fg_color="transparent")
bottom_frame.pack(pady=25)

ctk.CTkButton(
    bottom_frame,
    text="➕ Add",
    width=120,
    command=add_card
).grid(row=0,column=0,padx=10)

ctk.CTkButton(
    bottom_frame,
    text="✏ Edit",
    width=120,
    command=edit_card
).grid(row=0,column=1,padx=10)

ctk.CTkButton(
    bottom_frame,
    text="🗑 Delete",
    width=120,
    command=delete_card
).grid(row=0,column=2,padx=10)

display_card()

app.mainloop()