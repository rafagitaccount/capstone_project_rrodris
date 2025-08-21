# System Functions

import time
import pandas as pd
import os
from colorama import Fore

from book_retriever import BookRetriever

CSV_FILE = 'book_database.csv'


def load_books():
    # it loads a book dataset
    data = BookRetriever()
    books = data.get_books()
    if books:
        df = pd.DataFrame(books)
        save_df_to_csv(df)
    else:
        clear_screen()
        print("No books were retrieved. Please try again later.\n")
        os.abort()


def load_df():
    """Reads the CSV into a Pandas DataFrame and performs basic cleaning."""
    load_books()
    try:
        df = pd.read_csv(CSV_FILE)
        # Basic cleaning
        df = df.dropna()
        df = df.drop_duplicates(subset=['title', 'authors'])
    except Exception as e:
        clear_screen()
        print(f"Error trying to read the CSV file: {e}")
        time.sleep(5)
        os.abort()
    return df


def save_df_to_csv(df):
    """Saves the DataFrame to CSV."""
    try:
        df.to_csv(CSV_FILE, index=False)
    except Exception as e:
        clear_screen()
        print(f"Error trying to save the CSV file: {e}")
        time.sleep(5)
        os.abort()


def show_menu():
    clear_screen()
    print("\n" + "="*40)
    print(Fore.GREEN + "    BOOK RECOMMENDATION SYSTEM")
    print("="*40 + '\n')
    print("1. View all books")
    print("2. Filter books by genre")
    print("3. Filter books by publication date")
    print("4. Random book suggestion")
    print("5. Exit")
    print("="*40)


def show_books(df):
    if df.empty:
        print("No books found!")
        return
    print(f"\nFound {len(df)} book(s):")
    print("-" * 60)
    for _, row in df.iterrows():
        print(f"Title: {row['title']}")
        print(f"Author: {row['authors']}")
        print(f"Publication Date: {row['publication_date']}")
        print(f"Genre: {row['genres']}")
        print("-" * 30)


def get_genres(df):
    return sorted(df['genres'].dropna().unique())


def get_publication_years(df):
    """Gets the unique publication years sorted"""
    years = df['publication_date'].dropna().unique()
    # Convert to string and filter only values that are digits
    valid_years = [str(year) for year in years if str(year).isdigit()]
    # Sort by converting to int temporarily
    sorted_years = sorted(valid_years, key=int)
    return sorted_years


def filter_books_by_genre(df):
    """Filters books by genre"""
    print(Fore.GREEN + "\nFILTER BOOKS BY GENRE")
    genres = get_genres(df)

    print("\nAvailable genres:")
    for i, g in enumerate(genres, 1):
        print(f"{i}. {g}")
    print(f"{len(genres)+1}. All")

    choice = input("\nChoose a genre (by numeric index): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(genres):
        chosen_genre = genres[int(choice) - 1]
        filtered_df = df[df['genres'] == chosen_genre]
    else:
        filtered_df = df.copy()

    show_books(filtered_df)


def filter_books_by_date(df):
    """Filters books by publication date"""
    print(Fore.GREEN + "\nFILTER BOOKS BY PUBLICATION DATE")
    years = get_publication_years(df)

    if not years:
        print("No publication dates available!")
        return

    print("\nAvailable years:")
    for i, year in enumerate(years, 1):
        print(f"{i}. {year}")
    print(f"{len(years)+1}. All books")

    choice = input("\nChoose a year (by numeric index): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(years):
        chosen_year = years[int(choice) - 1]
        # Ensures comparison is done with strings
        filtered_df = df[df['publication_date'].astype(str) == str(chosen_year)]
    else:
        filtered_df = df.copy()

    show_books(filtered_df)


def random_suggestion(df):
    clear_screen()
    print(Fore.GREEN + "\nRANDOM SUGGESTION")
    print("\nChoose a filter type:")
    print("1. By genre")
    print("2. By publication date")
    print("3. No filter (all books)")

    filter_option = input("\nYour choice: ").strip()

    if filter_option == "1":
        # Filter by genre
        genres = get_genres(df)
        print("\nChoose a genre:")
        for i, g in enumerate(genres, 1):
            print(f"{i}. {g}")
        print(f"{len(genres)+1}. All")

        choice = input("\nYour choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(genres):
            chosen_genre = genres[int(choice) - 1]
            available = df[df['genres'] == chosen_genre]
        else:
            available = df

    elif filter_option == "2":
        # Filter by publication date
        years = get_publication_years(df)
        if not years:
            print("No publication dates available! Using all books.")
            available = df
        else:
            print("\nChoose a year:")
            for i, year in enumerate(years, 1):
                print(f"{i}. {year}")
            print(f"{len(years)+1}. All")

            choice = input("\nYour choice: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(years):
                chosen_year = years[int(choice) - 1]
                available = df[df['publication_date'].astype(str) == str(chosen_year)]
            else:
                available = df
    else:
        # No filter
        available = df

    if available.empty:
        print("No books available with the selected filters!")
        return

    # Choose a random row from the dataframe, and return it as a series
    book = available.sample(1).iloc[0]

    print("\n" + "="*40)
    print(Fore.GREEN + "         SUGGESTION FOR YOU!")
    print("="*40)
    print(f"Title: {book['title']}")
    print(f"Author: {book['authors']}")
    print(f"Genre: {book['genres']}")
    print(f"Publication Date: {book['publication_date']}")  
    print("="*40)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')