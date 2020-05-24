import random
import string

MIN_LENGTH = 4


"""
Spelling Bee is a game available in the New York Times puzzle section. This command line version
mimics Spelling Bee by generating a random list of 7 letters, collecting user word entries, and
tallying and grading a final score. 
"""
def main():
    start_game()
    letters = show_letters()
    word_bank = read_dictionary()
    enter_words(letters, word_bank)


# Prints welcome message at the beginning of the game, as well as the instructions if the user chooses.
def start_game():
    selection = input('Welcome to the Spelling Bee! Do you want to read the rules? (Enter Y or N) ')
    while selection != 'N' and selection != 'Y':
        selection = input('Please enter Y or N: ')
    if selection == 'Y':
        print('Create words using letters from the hive.')
        print('Words must contain at least 4 letters. \nWords must include the first letter. \n'
              'Letters can be used more than once.')
        print('4-letter words are worth 1 point each. \nLonger words earn 1 point per letter. \n'
              'Puzzles may include a “pangram” which uses every letter. '
              'These are worth 7 extra points!')


# Generates and displays a list of 7 random letters, including at least one vowel and no repeat
# letters. The center letter is stored as the second item in the list after the random vowel.
# The letters list will display with the center letter first.
# TODO: future versions should account for strange letter combinations, i.e. no Q without a U
def show_letters():

    # To include at least one vowel, the first letter will only be selected from the vowels list
    vowels = ['a', 'e', 'i', 'o', 'u']
    rand = random.randint(0, 4)
    vowel = vowels[rand]
    letters = [vowel]

    # Generate the other 6 letters in the list
    center_letter = choose_letter(letters)
    letter_1 = choose_letter(letters)
    letter_2 = choose_letter(letters)
    letter_3 = choose_letter(letters)
    letter_4 = choose_letter(letters)
    letter_5 = choose_letter(letters)

    print(center_letter, letter_1, letter_2, letter_3, letter_4, letter_5, vowel)
    return letters


# Reads through the lines of the dictionary text file and stores each word in a list
# Returns this list as a word bank for other functions to access
def read_dictionary():
    word_bank = []
    for line in open('word_list.txt'):
        line = line.strip()
        word_bank.append(line)
    return word_bank


# Generates a random letter. If the letter is already in the list of letters, choose a new letter.
# Append the new letter to the letter list and return the new letter.
def choose_letter(letters):
    choice = random.choice(string.ascii_lowercase)
    while choice in letters:
        choice = random.choice(string.ascii_lowercase)
    letters.append(choice)
    return choice


# Lets user continue entering words until they enter "". After each entry, checks that the word
# is greater than 3 letters, contains the center letter, doesn't contain letters that
# aren't in the letters list, and is a word in the dictionary. The same word may not be entered twice.
# Scores the word and adds to score counter.
def enter_words(letters, word_bank):
    score = 0
    submissions = []
    word = input('Enter a word (in lower case): ')
    while word != "":
        if len(word) < MIN_LENGTH:
            print('Sorry, words must be', MIN_LENGTH, 'or more letters. Try again.')
        elif missing_center_letter(word, letters):
            print('Sorry, words must contain the center letter. Try again.')
        elif letter_not_in_range(word, letters):
            print('Sorry, words must only use the letters available. Try again.')
        elif repeat_word(word, submissions):
            print('Sorry, word already entered. Try again.')
        elif not_a_word(word, word_bank):
            print('Sorry, entry not a word. Try again.')
        else:
            score = add_score(score, word, letters)
            submissions.append(word)
        print('Score:', score)
        word = input('Enter a word (in lower case): ')
    tally_game(score, submissions, letters, word_bank)


# Checks if the word string is missing the center letter. If missing, return true.
# Else return false.
def missing_center_letter(word, letters):
    for i in range(len(word)):
        if word[i] == letters[1]:
            return False
    return True


# Checks if the word contains letters that are not in the letters list. If so, return true.
# Else return false.
def letter_not_in_range(word, letters):
    for i in range(len(word)):
        if word[i] not in letters:
            return True
    return False


# Checks if the user has already entered the word (and collected points). If so, return True.
# Else return false.
def repeat_word(word, submissions):
    if word in submissions:
        return True
    return False


# Takes in a word as a parameter and checks to see if it is a viable entry. If word is not found
# in the word bank, return True. Otherwise, return false.
def not_a_word(word, word_bank):
    for item in word_bank:
        if word == item:
            return False
    return True


# Takes the word and the current total score as parameters and returns an updated total score.
# If the word is 4 letters long, adds 1 point. If the word is 5 or more letters long, add a point
# for each letter. If the word is a pangram (contains all 7 letters), add an additional 7 points
# on top of the score.
def add_score(score, word, letters):
    if len(word) == MIN_LENGTH:
        score += 1
    elif len(word) > MIN_LENGTH:
        score += len(word)
    # Add additional 7 points if the word is a pangram
    if pangram(word, letters):
        score += 7
        # print('Pangram!')
    return score


# Checks if the word contains all 7 letters in the list. If so, return true.
def pangram(word, letters):
    temp = []
    for i in range(len(word)):
        if word[i] in letters and word[i] not in temp:
            temp.append(word[i])
    if len(temp) == 7:
        return True
    else:
        return False


# Prints the final score, submitted words, calculated max score, and grade.
def tally_game(score, submissions, letters, word_bank):
    print('Final score:', score)
    for sub in submissions:
        print(sub)
    max_score = find_max_score(letters, word_bank)
    print('Max score:', max_score)
    grade(score, max_score)


# Given a list of letters, finds the max score possible. Reviews all the words in the word bank
# to see if they contain the letters in the game list and meet other parameters.
def find_max_score(letters, word_bank):
    max_score = 0
    for word in word_bank:
        count = 0
        has_center = False
        # Only check words that are 4 or more letters long
        if len(word) > MIN_LENGTH:
            for let in word:
                if let == letters[1]:
                    has_center = True
                # Count tracks the total number of letters in the word that match the letters list
                if let in letters:
                    count += 1
                else:
                    break
        # Only add to score if all letters in word are in letters list and word includes the
        # center letter
        if count == len(word) and has_center:
            max_score = add_score(max_score, word, letters)
            # print(word, max_score)
    return max_score


# Calculates the grade as a percent of max_score
def grade(score, max_score):
    grade = 0
    if score > 0:
        grade = round((score / max_score) * 100)
    print('Your grade: ' + str(grade) + '%')


# Runs program from main function
if __name__ == '__main__':
    main()