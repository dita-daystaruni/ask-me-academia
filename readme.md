# Ask-Me, a Daystar 🌟  Academia Study Assistant Project

## Overview

This Django project serves as a study assistant for university students. The application allows students to upload their lecture notes in PDF format, which are then analyzed to generate true or false questions to help with quick revision. The results are saved in a database and can be retrieved via API endpoints.

## Features

- **Upload Lecture Notes**: Students can upload lecture notes in PDF format.
- **Generate Questions and Answers**: The system processes the PDF to generate 10 true or false questions with answers based on the lecture notes.
- **Save Results**: The questions, answers, and other metadata are saved in the database.
- **Retrieve Saved Records**: Students can retrieve all their saved lecture notes records based on their user ID.

## Installation

### 1. Clone the Repository

```bash
git clone 
cd your-repository
```

### 2. Create and Activate a Virtual Environment

```bash 
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create a .env File
```bash
OPENAI_API_KEY=your_openai_api_key
```
### 6. Start the Development Server
```bash
python manage.py runserver
```

## API Endpoints

### 1. Upload Lecture Notes
### URL: /api/upload/
### Method: POST
Description: Uploads a PDF file containing lecture notes and generates 10 true or false questions with answers based on the notes.

Request:

Body:
- user_id (integer): The ID of the user uploading the notes.
- title (string): The title of the lecture notes.
- pdf_file (file): The PDF file containing the lecture notes.
- save_response (Boolian): if to save the reponse or not.

### 2. Get object by user
### URL: /api/notes/<str:user_id>/
Description: Gets the list of all the record saves by a user

Response:
```bash
[
    {
        "user_id": 1,
        "title": "Introduction to Python",
        "q_and_a": [
            {"question": "Is Python a statically typed language?", "answer": "False"},
            {"question": "Can you use Python for web development?", "answer": "True"},
            ...
        ],
        "uploaded_at": "2024-07-10T12:34:56Z"
    },
    ...
]
```

## Todos
1. Set up db server
2. Test and intergrated with frontend application 


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

