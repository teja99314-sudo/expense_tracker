import json
from datetime import date
from pathlib import Path
import requests


# Load existing expenses
if Path("expenses.json").exists():
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
else:
    expenses = []


def add_expense():
    if expenses:
        last_id = expenses[-1]["id"]
        expense_id = last_id + 1
    else:
        expense_id = 1

    # Validate amount
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    # Validate categoryhttps://github.com/teja99314-sudo/expense_tracker.git
    while True:
        category = input("Enter category: ").strip()

        if category:
            break

        print("Category cannot be empty.")

    # Validate description
    while True:
        description = input("Enter description: ").strip()

        if description:
            break

        print("Description cannot be empty.")

    today = date.today()

    expense = {
        "id": expense_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(today)
    }

    expenses.append(expense)

    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

    print("\n✓ Expense added successfully!")
def view_expenses():
    if not expenses:
        print("\nNo current expenses.")
        return

    print("\n------------- EXPENSES -------------")
    print("ID   Category    Description    Amount    Date")
    print("-----------------------------------------------")

    total = 0

    for expense in expenses:
        print(
            expense["id"],
            expense["category"],
            expense["description"],
            f"₹{expense['amount']:.2f}",
            expense["date"]
        )

        total += expense["amount"]

    print("-----------------------------------------------")
    print(f"Total Expenses: ₹{total:.2f}")


def search_expenses():
    category = input("Enter category to search: ")

    found = False

    for expense in expenses:
        if expense["category"].lower() == category.lower():
            print(
                expense["id"],
                expense["category"],
                expense["description"],
                f"₹{expense['amount']:.2f}",
                expense["date"]
            )
            found = True

    if not found:
        print("\nNo expenses found for this category.")


def currency_conversion():
    amount = float(input("Enter amount in INR: "))
    target_currency = input("Convert to: ").upper()

    url = f"https://api.frankfurter.dev/v2/rate/INR/{target_currency}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        rate = data["rate"]

        converted_amount = amount * rate

        print(
            f"\n₹{amount:.2f} ≈ "
            f"{converted_amount:.2f} {target_currency}"
        )

    except requests.exceptions.RequestException as error:
        print("Currency conversion failed:", error)


def main():
    while True:
        print("\n========================================")
        print("        PERSONAL EXPENSE TRACKER")
        print("========================================")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expenses")
        print("4. Currency Conversion")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        match choice:
            case "1":
                add_expense()

            case "2":
                view_expenses()

            case "3":
                search_expenses()

            case "4":
                currency_conversion()

            case "5":
                print("\nThank you for using Personal Expense Tracker!")
                break

            case _:
                print("\nInvalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()