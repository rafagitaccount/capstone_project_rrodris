import requests
import random
import time
import re


class BookRetriever():
    __how_many_books = 40

    def __search_google_books(self):
        """
        Search for 40 random books on Google Books in a single request
        """
        url = "https://www.googleapis.com/books/v1/volumes"
        
        # Uses simpler and more effective terms to ensure results
        random_term = random.choice(["the", "health", "book", "story", "guide"])
        
        # Search parameters
        params = {
            "q": random_term,
            "printType": "books",
            "maxResults": 40,
            "startIndex": random.randint(0, 200),
            "orderBy": "relevance"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # raises error if there was a problem
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error searching for books: {error}\n")
            return None

    def __extract_publication_year(self, date_string):
        """
        Extracts only the year from publication date string.
        Returns None if no valid year is found.
        """
        if not date_string or date_string == "Unknown":
            return None
        
        # Try to extract a 4-digit year from the date string
        year_match = re.search(r'\b(19|20)\d{2}\b', str(date_string))
        if year_match:
            year = int(year_match.group())
            # Validate year range (reasonable publication years)
            if 1800 <= year <= 2024:
                return str(year)
        
        return None

    def __extract_book_data(self, book):
        """
        Gets the important information from a book
        Returns None if the book doesn't have a valid publication date
        """
        info = book.get("volumeInfo", {})
        
        # Publication date - must exist and be valid
        raw_date = info.get("publishedDate", "")
        publication_year = self.__extract_publication_year(raw_date)
        
        if not publication_year:
            return None
        
        title = info.get("title", "Untitled")
        
        authors = info.get("authors", [])
        if authors:
            authors_text = ", ".join(authors)
        else:
            authors_text = "Unknown"
        
        categories = info.get("categories", [])
        if categories:
            genres = ", ".join(categories)
        else:
            genres = "Unknown"
        
        google_id = book.get("id", "")
        
        return {
            "google_id": google_id,
            "title": title,
            "authors": authors_text,
            "publication_date": publication_year,  # Now only contains the year
            "genres": genres
        }

    def get_books(self):
        """
        Returns a list of dictionaries with books
        Only returns books with valid publication dates
        """
        print("\nRequesting some random books from Google Books API...")
        print("-" * 50)
        
        print("Waiting for the API response...\n")
        attempts = 0
        max_attempts = 3
        page_books = []
        
        while attempts < max_attempts:
            result = self.__search_google_books()
            
            if not result:
                attempts += 1
                continue
            
            page_books = result.get("items", [])
            
            if page_books:
                break  # found books, exit loop
            
            print(f"No books found (attempt {attempts + 1}). Trying again...")
            attempts += 1
        
        if not page_books:
            print(f"\nCould not find books after {max_attempts} attempts.")
            time.sleep(3)
            return []
        
        all_books = []
        books_without_date = 0
        
        for book in page_books:
            book_data = self.__extract_book_data(book)
            if book_data:  # Only add books with valid publication dates
                all_books.append(book_data)
            else:
                books_without_date += 1
        
        print(f"Retrieved: {len(all_books)} books with valid publication dates")
        if books_without_date > 0:
            print(f"Filtered out: {books_without_date} books without valid publication dates")
        print()
        
        time.sleep(4)
        return all_books