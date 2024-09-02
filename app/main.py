from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app import database
from app import models
from app import schemas
from app import crud
from app import utils
from app.dependencies import get_current_user

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost",  # Adjust as needed
    "http://localhost:8080",
    "http://localhost:3000"  # Add your frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if the username already exists
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create the new user
    new_user = crud.create_user(db=db, user=user)
    return new_user

@app.post("/login/")
def login(login_request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    username = login_request.username
    password = login_request.password
    db_user = crud.get_user(db, username=username)
    print(username)  # For debugging purposes
    print(password)  # For debugging purposes
    if not db_user or not utils.verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = utils.create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token, db)
    return crud.create_book(db=db, book=book, user_id=current_user.id)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    get_current_user(token, db)
    return crud.get_books(db, skip=skip, limit=limit)

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    get_current_user(token, db)
    db_book = crud.update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    get_current_user(token, db)
    db_book = crud.delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/dashboard/")
def user_dashboard(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token, db)
    total_books = db.query(models.Book).filter(models.Book.owner_id == current_user.id).count()
    return {"total_books": total_books}
