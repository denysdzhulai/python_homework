import sqlite3


def task1_complex_joins():
    conn = sqlite3.connect('../db/lesson.db')
    cursor = conn.cursor()

    query = """
    SELECT o.order_id, SUM(p.price * li.quantity) as total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("Task 1: Total price of first 5 orders")
    print("Order ID | Total Price")
    print("-" * 20)
    for row in results:
        print(f"{row[0]:8} | ${row[1]:.2f}")

    conn.close()


if __name__ == "__main__":
    task1_complex_joins()


def task2_subqueries():
    conn = sqlite3.connect('../db/lesson.db')
    cursor = conn.cursor()

    query = """
    SELECT c.name, AVG(order_totals.total_price) as average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id as customer_id_b, SUM(p.price * li.quantity) as total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id, o.customer_id
    ) order_totals ON c.customer_id = order_totals.customer_id_b
    GROUP BY c.customer_id, c.name
    HAVING AVG(order_totals.total_price) IS NOT NULL
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\nTask 2: Average order price per customer")
    print("Customer Name | Average Order Price")
    print("-" * 35)
    for row in results:
        print(f"{row[0]:20} | ${row[1]:.2f}")

    conn.close()


if __name__ == "__main__":
    task1_complex_joins()
    task2_subqueries()


def task3_insert_transaction():
    conn = sqlite3.connect('../db/lesson.db')
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    try:
        conn.execute("BEGIN TRANSACTION")

        cursor.execute(
            "SELECT customer_id FROM customers WHERE name = 'Perez and Sons'")
        customer_result = cursor.fetchone()
        if not customer_result:
            raise Exception("Customer 'Perez and Sons' not found")
        customer_id = customer_result[0]

        cursor.execute(
            "SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'")
        employee_result = cursor.fetchone()
        if not employee_result:
            raise Exception("Employee 'Miranda Harris' not found")
        employee_id = employee_result[0]

        cursor.execute(
            "SELECT product_id FROM products ORDER BY price LIMIT 5")
        products = cursor.fetchall()
        if len(products) < 5:
            raise Exception("Not enough products found")

        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, order_date) 
            VALUES (?, ?, date('now'))
            RETURNING order_id
        """, (customer_id, employee_id))

        order_result = cursor.fetchone()
        if not order_result:
            raise Exception("Failed to create order")
        order_id = order_result[0]

        for product_row in products:
            product_id = product_row[0]
            cursor.execute("""
                INSERT INTO line_items (order_id, product_id, quantity) 
                VALUES (?, ?, 10)
            """, (order_id, product_id))

        conn.commit()

        cursor.execute("""
            SELECT li.line_item_id, li.quantity, p.name
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            WHERE li.order_id = ?
            ORDER BY li.line_item_id
        """, (order_id,))

        results = cursor.fetchall()

        print(f"\nTask 3: New order created (Order ID: {order_id})")
        print("Line Item ID | Quantity | Product Name")
        print("-" * 45)
        for row in results:
            print(f"{row[0]:12} | {row[1]:8} | {row[2]}")

    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")

    finally:
        conn.close()


def task4_having_clause():
    conn = sqlite3.connect('../db/lesson.db')
    cursor = conn.cursor()

    query = """
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) as order_count
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    HAVING COUNT(o.order_id) > 5
    ORDER BY order_count DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\nTask 4: Employees with more than 5 orders")
    print("Employee ID | First Name | Last Name  | Order Count")
    print("-" * 55)
    for row in results:
        print(f"{row[0]:11} | {row[1]:10} | {row[2]:10} | {row[3]}")

    conn.close()


if __name__ == "__main__":
    task1_complex_joins()
    task2_subqueries()
    task3_insert_transaction()
    task4_having_clause()
