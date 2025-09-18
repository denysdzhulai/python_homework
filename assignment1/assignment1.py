# Write your code here.

# pytest -v -x assignment1-test.py

# Task 1: Hello
def hello():
    return "Hello!"


# Task 2: Greet with a Formatted String
def greet(name):
    return f"Hello, {name}!"


# Task 3: Calculator
def calc(a, b, operation="multiply"):
    try:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b
        elif operation == "modulo":
            return a % b
        elif operation == "int_divide":
            return a // b
        elif operation == "power":
            return a ** b
        else:
            return "Unsupported operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"

# Task 4: Data Type Conversion


def data_type_conversion(value, data_type):
    try:
        if data_type == "float":
            return float(value)
        elif data_type == "str":
            return str(value)
        elif data_type == "int":
            return int(value)
        else:
            return f"You can't convert {value} into a {data_type}."
    except ValueError:
        return f"You can't convert {value} into a {data_type}."

# Task 5: Grading System, Using *args


def grade(*args):
    try:
        avg = sum(args) / len(args)
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"
    except:
        return "Invalid data was provided."

# Task 6: Use a For Loop with a Range


def repeat(string, count):
    result = ""
    for i in range(count):
        result += string
    return result

# Task 7: Student Scores, Using **kwargs


def student_scores(mode, **kwargs):
    try:
        if not kwargs:
            return "No student data provided."
        if mode == "best":
            best_student = max(kwargs, key=kwargs.get)
            return best_student
        elif mode == "mean":
            return sum(kwargs.values()) / len(kwargs)
        else:
            return "Invalid mode."
    except:
        return "An error occurred."

# Task 8: Titleize, with String and List Operations


def titleize(text):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
    words = text.split()

    if not words:
        return ""

    result = []

    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1:
            result.append(word.capitalize())
        elif word.lower() in little_words:
            result.append(word.lower())
        else:
            result.append(word.capitalize())

    return " ".join(result)

# Task 9: Hangman, with more String Operations


def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

# Task 10: Pig Latin, Another String Manipulation Exercise


def pig_latin(text):
    vowels = "aeiou"
    words = text.split()
    result = []

    for word in words:
        if word.startswith(("a", "e", "i", "o", "u")):
            result.append(word + "ay")
        elif word.startswith("qu"):
            result.append(word[2:] + "quay")
        else:
            i = 0
            while i < len(word) and word[i] not in vowels:
                if word[i] == "q" and i + 1 < len(word) and word[i+1] == "u":
                    i += 2
                    break
                i += 1
            result.append(word[i:] + word[:i] + "ay")

    return " ".join(result)
