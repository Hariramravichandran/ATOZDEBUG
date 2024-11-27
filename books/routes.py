from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from auth.utils import get_current_user
from books.models import Book
from books.dependencies import admin_required
from db import books_collection

router = APIRouter()

def is_valid_objectid(id_str: str) -> bool:
    """Check if the given string is a valid MongoDB ObjectId."""
    return ObjectId.is_valid(id_str)


@router.post("/books/", dependencies=[Depends(admin_required)])
def add_book(book: Book):
    
    result = books_collection.insert_one(book.dict())
    
    book_data = book.dict()
    book_data["_id"] = str(result.inserted_id)
    
    return {"message": "Book added successfully", "book": book_data}


@router.put("/books/{book_id}", dependencies=[Depends(admin_required)])
def update_book(book_id: str, book: Book):
    if not is_valid_objectid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    object_id = ObjectId(book_id)
    
    result = books_collection.update_one({"_id": object_id}, {"$set": book.dict()})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = books_collection.find_one({"_id": object_id})
    updated_book["_id"] = str(updated_book["_id"])
    
    return {"message": "Book updated successfully", "book": updated_book}

@router.delete("/books/{book_id}", dependencies=[Depends(admin_required)])
def delete_book(book_id: str):
    if not is_valid_objectid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    object_id = ObjectId(book_id)
    result = books_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


@router.get("/books/", dependencies=[Depends(get_current_user)])
def get_books():
    books = list(books_collection.find())
    for book in books:
        book["_id"] = str(book["_id"]) 
    return books


@router.get("/books/{book_id}", dependencies=[Depends(get_current_user)])
def get_book(book_id: str):
    if not is_valid_objectid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book["_id"] = str(book["_id"])
    return book