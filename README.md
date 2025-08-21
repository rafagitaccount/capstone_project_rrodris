# Book Recommendation System

A Python-based book query and recommendation system that fetches book data from the Google Books API and provides various filtering and suggestion features.

## Project Overview

This project is part of the RBS Training - Python Advanced Course and implements a comprehensive book recommendation system with the following features:

- **Book Data Retrieval**: Automatically fetches book information from Google Books API
- **Book Browsing**: View all available books in the database
- **Genre Filtering**: Filter books by specific genres
- **Date Filtering**: Filter books by publication year
- **Random Suggestions**: Get random book recommendations with optional filtering

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── functions.py         # Core system functions
│   └── book_retriever.py    # Google Books API integration
├── pyproject.toml           # Project configuration
├── README.md                # This file
├── screenshots/             # Folder containing project screenshots
```

## Features

### 1. View All Books
Display all books currently in the database with their details including title, author, publication date, and genre.

### 2. Filter by Genre
Browse books by selecting from available genres in the database.

### 3. Filter by Publication Date
Filter books by their publication year.

### 4. Random Book Suggestion
Get a random book recommendation with optional filtering by:
- Genre
- Publication date
- No filter (all books)

### 5. Data Management
- Automatic data fetching from Google Books API
- CSV-based local storage
- Data cleaning and deduplication

## Technical Details

### Dependencies
- `pandas`: Data manipulation and analysis
- `requests`: HTTP requests to Google Books API
- `colorama`: Terminal text styling and color formatting

### API Integration
The system uses the Google Books API to fetch book data with the following features:
- Random search terms to get diverse results
- Publication date validation
- Data extraction and cleaning
- Error handling and retry logic

### Data Storage
- Books are stored in a CSV file (`book_database.csv`)
- Automatic data cleaning removes duplicates and invalid entries
- Data persistence across application sessions

## Usage

Run the application:

```bash
cd src
python main.py
```

Follow the interactive menu to:
1. View all books
2. Filter books by genre
3. Filter books by publication date
4. Get random book suggestions
5. Exit the application

## Error Handling

The system includes comprehensive error handling for:
- API connection issues
- File I/O operations
- Data validation
- User input validation
- Unexpected errors with graceful degradation