# Task 1
import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))


def logger_decorator(func):
    """Decorator that logs function name, parameters, and return value"""
    def wrapper(*args, **kwargs):
        pos_args = list(args) if args else "none"

        kw_args = dict(kwargs) if kwargs else "none"

        result = func(*args, **kwargs)

        log_message = f"function: {func.__name__} positional parameters: {pos_args} keyword parameters: {kw_args} return: {result}"
        logger.log(logging.INFO, log_message)

        return result
    return wrapper

# Function that takes no parameters and returns nothing


@logger_decorator
def hello_world():
    """Function with no parameters that returns nothing"""
    print("Hello, World!")
    return None

# Function that takes variable number of positional arguments and returns True


@logger_decorator
def variable_positional(*args):
    """Function that takes variable positional arguments and returns True"""
    print(f"Received positional args: {args}")
    return True

# Function that takes no positional arguments and variable keyword arguments, returns logger_decorator


@logger_decorator
def variable_keyword(**kwargs):
    """Function that takes variable keyword arguments and returns logger_decorator"""
    print(f"Received keyword args: {kwargs}")
    return logger_decorator


# Mainline code - call each function with appropriate parameters
if __name__ == "__main__":
    print("=== Testing Logger Decorator ===")

    # Call function with no parameters
    print("\n1. Calling hello_world():")
    hello_world()

    # Call function with positional arguments
    print("\n2. Calling variable_positional with args:")
    variable_positional(1, 2, "three", 4.0)

    # Call function with keyword arguments
    print("\n3. Calling variable_keyword with kwargs:")
    variable_keyword(name="John", age=25, city="New York")

    print("\nCheck the decorator.log file to see the logged information!")
