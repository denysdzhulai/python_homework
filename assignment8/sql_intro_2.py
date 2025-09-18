import sqlite3
import pandas as pd

DB_PATH = "../db/lesson.db"


def main():
    try:
        conn = sqlite3.connect(DB_PATH)

        query = """
            SELECT li.line_item_id, li.quantity, li.product_id, p.product_name, p.price
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
        """

        df = pd.read_sql(query, conn)
        print("\nFirst 5 rows:")
        print(df.head())

        # Add total column
        df["total"] = df["quantity"] * df["price"]
        print("\nWith total column:")
        print(df.head())

        # Group by product
        grouped = (
            df.groupby("product_id")
            .agg(
                line_item_count=("line_item_id", "count"),
                total_revenue=("total", "sum"),
                product_name=("product_name", "first"),
            )
            .reset_index()
        )

        grouped = grouped.sort_values("product_name")
        print("\nGrouped summary:")
        print(grouped.head())

        # Save to CSV
        grouped.to_csv("order_summary.csv", index=False)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
