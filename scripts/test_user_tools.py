from src.tools.user_tools import get_user_loan_history


def main():

    user_id = "user-001"

    result = get_user_loan_history.invoke({"user_id": user_id})

    print("=== USER LOAN HISTORY ===")

    for loan in result:
        print(loan)


if __name__ == "__main__":
    main()
