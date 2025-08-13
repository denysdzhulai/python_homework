# Task 4

def make_hangman(secret_word):
    """Creates a hangman closure game with the given secret word"""
    guesses = []
    
    def hangman_closure(letter):
        """Inner function that processes each guess"""
        guesses.append(letter.lower())
        
        display_word = ""
        for char in secret_word.lower():
            if char in guesses:
                display_word += char
            else:
                display_word += "_"
        
        print(f"Word: {display_word}")
        
        # Check if all letters have been guessed
        all_guessed = all(char.lower() in guesses for char in secret_word.lower())
        
        return all_guessed
    
    return hangman_closure

def play_hangman():
    """Main game function"""
    print("=== Welcome to Hangman! ===")
    
    secret_word = input("Enter the secret word: ").strip()


    game = make_hangman(secret_word)
    
    print("Let's play! Guess the letters one by one.")
    print(f"The word has {len(secret_word)} letters.")
    
    guessed_letters = set()
    
    while True:
        if guessed_letters:
            print(f"Already guessed: {sorted(list(guessed_letters))}")
        
        guess = input("Enter a letter: ").strip().lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter!")
            continue
            
        if guess in guessed_letters:
            print("You already guessed that letter!")
            continue
        
        guessed_letters.add(guess)
        
        if game(guess):
            print(f"\nCongratulations! You guessed the word: {secret_word}")
            break
        
        print()

if __name__ == "__main__":
    while True:
        play_hangman()
        
        play_again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if play_again != 'y' and play_again != 'yes':
            print("Thanks for playing!")
            break
        print()