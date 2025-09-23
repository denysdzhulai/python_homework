# Task 2

def type_converter(type_of_output):
    """Decorator factory that converts function return value to specified type"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

# Returns integer 5, decorated to convert to string
@type_converter(str)
def return_int():
    """Returns integer 5, but will be converted to string"""
    return 5

# Returns string "not a number", decorated to convert to int
@type_converter(int)
def return_string():
    """Returns string 'not a number', will attempt to convert to int"""
    return "not a number"

# Mainline code
if __name__ == "__main__":
    print("=== Testing Type Converter Decorator ===")
    
    # Test return_int() - should return string "5"
    print("\n1. Testing return_int() with str conversion:")
    y = return_int()
    print(f"Value: {y}")
    print(f"Type: {type(y).__name__}")  # This should print "str"
    
    # Test return_string() - should raise ValueError
    print("\n2. Testing return_string() with int conversion:")
    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")
