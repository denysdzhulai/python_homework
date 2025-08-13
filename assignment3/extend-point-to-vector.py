# Task 5
import math

class Point:
    """Represents a point in 2D space"""
    
    def __init__(self, x, y):
        """Initialize point with x and y coordinates"""
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        """Check equality between two points"""
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        """String representation of the point"""
        return f"Point({self.x}, {self.y})"
    
    def distance_to(self, other):
        """Calculate Euclidean distance to another point"""
        if not isinstance(other, Point):
            raise TypeError("Can only calculate distance to another Point")
        
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

class Vector(Point):
    """Vector class that inherits from Point"""
    
    def __str__(self):
        """Override string representation for vectors"""
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other):
        """Override + operator for vector addition"""
        if not isinstance(other, Vector):
            raise TypeError("Can only add vectors to other vectors")
        
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)

if __name__ == "__main__":
    print("=== Demonstrating Point and Vector Classes ===")
    
    # Create some points
    print("\n1. Creating Points:")
    p1 = Point(3, 4)
    p2 = Point(0, 0)
    p3 = Point(3, 4)
    
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    print(f"p3: {p3}")
    
    # Test equality
    print("\n2. Testing Point Equality:")
    print(f"p1 == p2: {p1 == p2}")  # Should be False
    print(f"p1 == p3: {p1 == p3}")  # Should be True
    
    # Test distance calculation
    print("\n3. Testing Distance Calculation:")
    distance = p1.distance_to(p2)
    print(f"Distance from {p1} to {p2}: {distance}")
    print(f"Distance from p2 to p1: {p2.distance_to(p1)}")
    
    # Create some vectors
    print("\n4. Creating Vectors:")
    v1 = Vector(2, 3)
    v2 = Vector(1, 4)
    v3 = Vector(-1, 2)
    
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    print(f"v3: {v3}")
    
    # Test vector addition
    print("\n5. Testing Vector Addition:")
    v4 = v1 + v2
    print(f"{v1} + {v2} = {v4}")
    
    v5 = v2 + v3
    print(f"{v2} + {v3} = {v5}")
    
    # Chain addition
    v6 = v1 + v2 + v3
    print(f"{v1} + {v2} + {v3} = {v6}")
    
    # Test inherited methods
    print("\n6. Testing Inherited Methods on Vectors:")
    print(f"v1 == v2: {v1 == v2}")  # Inherited equality
    
    # Distance between vectors (inherited from Point)
    distance_v = v1.distance_to(v2)
    print(f"Distance from {v1} to {v2}: {distance_v}")
    
    # Demonstrate that vectors can be compared to points
    print(f"v1 == Point(2, 3): {v1 == Point(2, 3)}")  # Should be True
    
    print("\n7. Error Handling:")
    try:
        # This should work - vector + vector
        result = v1 + v2
        print(f"Vector addition successful: {result}")
    except TypeError as e:
        print(f"Error: {e}")
    
    # Show that Points don't have + operator
    try:
        result = p1 + p2  # This will fail
    except TypeError as e:
        print(f"Points don't support addition: {e}")