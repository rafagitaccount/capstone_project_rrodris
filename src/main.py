import functions as fn
from colorama import init

'''
    Book Query System
    Project: RBS Training - Python Advanced Course
'''

def main():
    init()
    init(autoreset=True)
    df = fn.load_df()

    while True:
        try:
            fn.show_menu()
            op = input("\nChoose an option: ").strip()

            if op == '1':
                fn.show_books(df)
            elif op == '2':
                fn.filter_books_by_genre(df)
            elif op == '3':
                fn.filter_books_by_date(df)
            elif op == '4':
                fn.random_suggestion(df)
            elif op == '5':
                print("\nCome back anytime!\n")
                break
            else:
                print("Invalid option!")

            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print("Unexpected error:", e)


if __name__ == "__main__":
    main()