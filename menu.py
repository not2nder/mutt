from InquirerPy import inquirer
from InquirerPy import get_style

name = inquirer.text(message="sdfsd:", qmark="", amark="").execute()

cap = inquirer.select(
    message="What's your favourite programming language:",
    choices=["Go", "Python", "Rust", "JavaScript"],
    multiselect=True,
    pointer="->",
    marker="# "
).execute()

print(name)