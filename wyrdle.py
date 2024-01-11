from random import choice
from pandas import read_csv
from rich.console import Console

import sys

console = Console(width=60)

string = ''



with open("words.txt", "r") as words:
    wrds = words.readline()
    wrds.strip()
    WORD_LIST = wrds.split(',')

class Alphabet:
    def __init__(self) -> None: 
        self.correct: list = []
        self.misplaced: list = []
        self.wrong: list = []
        self.alphabet: list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
                               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    def add_letters(self, gs: str, sc: str) -> None:
        for idx in range(5):
            if gs[idx] not in sc:
                self.wrong.append(gs[idx])
            elif gs[idx] == sc[idx] and gs[idx]:
                if gs[idx] not in self.correct:
                    self.correct.append(gs[idx])
                    if gs[idx] in self.misplaced:
                        self.misplaced.remove(gs[idx])
            else:
                if gs[idx] not in self.correct:
                    self.misplaced.append(gs[idx])

    def display(self) -> list:
        rtn_lst = []
        for ltr in 'abcdefghijklmnopqrstuvwxyz':
            if ltr in self.wrong:
                rtn_lst.append(f"[red]{ltr}[/]")
            elif ltr in self.misplaced:
                rtn_lst.append(f"[yellow]{ltr}[/]")
            elif ltr in self.correct:
                rtn_lst.append(f"[green]{ltr}[/]")
            else:
                rtn_lst.append(ltr)
        return rtn_lst

def get_word() -> str:
    return choice(WORD_LIST)

def validate_guess(gs: str) -> bool:
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    if len(gs) != 5:
        print("Guesses must be exactly 5 letters long")
        return False
    for ltr in gs:
        if ltr not in alpha:
            print(f"{ltr} is not a valid letter")
            return False
    if gs not in WORD_LIST:
        console.print(f"[red]{gs} is not in the top 5000 five letter words.[/]")
        console.print(f"[red]Please guess again.[/]")
        return False
    return True


def judge(guess: str, secret: str) -> str:
    rtn_lst = ['', '', '', '', '']
    gsl, scl = list(guess), list(secret)

    # Get Exact locations
    for idx in range(5):
        if guess[idx] == scl[idx]:
            gsl[idx], scl[idx] = '+', '.'
            rtn_lst[idx] = f'[green]{guess[idx]}[/]'

    # Get non present
    for idx in range(5):
        if gsl[idx] not in scl and gsl[idx] != '+':
            rtn_lst[idx] = f'[red]{gsl[idx]}[/]'
    
    # Get misplaced letters
    for idx in range(5):
        if gsl[idx] in scl:
            rtn_lst[idx] = f'[yellow]{guess[idx]}[/]'
            scl[scl.index(guess[idx])] = '.'
            gsl[idx] = '+'

    return ''.join(rtn_lst)

def display_board(gs_lst: list, alphabet: list, secret):
    console.clear()
    console.rule(":rocket: [blue]Wrdle[/] :rocket:")
    console.rule(secret)
    for wrd in gs_lst:
        console.rule(wrd)
    console.rule(''.join(alphabet))

def validate_input(inp: str):
    if inp == 'y' or inp == 'N':
        return True
    return False

def main():
    while True:
        alpha = Alphabet()
        secret = get_word()
        guess_lst = ["*****", "*****", "*****", "*****", "*****", "*****"]
        crct = False
        for idx in range(6):
            display_board(guess_lst, alpha.display(), secret)
            guess = input("Guess a word[\quit to stop]: ").lower()
            if guess == '\quit':
                sys.exit()
            while not validate_guess(guess):
                guess = input("Guess a word[\quit to stop]: ").lower()
                if guess =='\quit':
                    sys.exit()
            guess_lst[idx] = judge(guess, secret)
            alpha.add_letters(guess, secret)
            if guess == secret:
                crct = True
                break
            display_board(guess_lst, alpha.display(), secret)
        
        console.rule(secret)

        if crct:
            display_board(guess_lst, alpha.display(), secret)
            console.rule(":star: [yellow]YOU WON[/] :star:")
        elif guess == "\QUIT":
            display_board(guess_lst, alpha.display(), secret)
            console.rule("Game Stopped")
        else:
            display_board(guess_lst, alpha.display(), secret)
            console.rule(f"[red]YOU LOST. The word was: {secret}.[/]")
        
        cont = input("Keep playing[y/N]: ")
        while not validate_input(cont):
            cont = input("Keep playing[y/N]: ")
        if cont == 'N':
            console.clear()
            console.print("[red]Stopping[/]")
            sys.exit()
        else:
            console.clear()
            console.print(":rocket: [blue]Playing again[/] :rocket:")

if __name__ == '__main__':
    main()