# FastAPI Library Management System

A web application that allows users to manage their personal library of books.

## Features

- User registration and login with JWT-based authentication
- CRUD operations for managing books
- User dashboard with a summary of their library
- Responsive UI

## Prerequisites

- Python 3.7 or later
- Pip (Python package installer)
- Heroku CLI (for deployment)

## Installation

1. **Clone the repository**:

    ```bash
    git clone gh repo clone Kelum23/book_library_app_fastapi_jwt-backend
    cd book_library_app_fastapi_jwt
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application locally**:

    ```bash
    uvicorn app.main:app --reload
    ```

    Visit `http://127.0.0.1:8000` in your browser.

    Visit `http://127.0.0.1:8000/docs` in your browser.
   Preview fastAPI documentation

   ![image](https://github.com/user-attachments/assets/361087c4-42ab-467e-8d17-e92553008fe0)


## Deployment

The application is deployed on Heroku. To deploy it yourself:
![image](https://github.com/user-attachments/assets/deb64061-e68e-4a48-b9a9-0382df3d5da4)

