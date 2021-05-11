import random
from words import words
import string

def get_vaild_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()
def hangman():
    word = get_vaild_word(words)
    word_letter = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letter = set()
    lives = 10

    #getting input from user
    while len(word_letter) > 0 and lives > 0:
        print('you have ', lives,' lives left and You have already used ',' '.join(used_letter))
        word_lst = [letter if letter in used_letter else '-' for letter in word]
        print('Current word: ',''.join(word_lst))

        user_letter = input(f"Guess the word\n").upper()
        if user_letter in alphabet - used_letter:
            used_letter.add(user_letter)
            if user_letter in word_letter:
                word_letter.remove(user_letter)

            else:
                lives = lives-1  #takes away a life if wrong
                print(f'Letter is not in the word')
        elif user_letter in used_letter:
            print("already used, try something else")
        else:
            print(f"invalid input")
    if lives== 0:
        print(f'Sorry, you died. The word was ',word)
    else:
        print(f'You guessed the word ',word,'!!')
hangman()