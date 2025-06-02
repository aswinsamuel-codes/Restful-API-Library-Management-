from flask import Flask, request, jsonify
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# In-memory data store for books
books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813}
]

# Counter for generating unique IDs
next_id = 4

# Helper function to find a book by ID
def find_book(book_id):
    """Find a book by its ID"""
    return next((book for book in books if book["id"] == book_id), None)

# Helper function to validate book data
def validate_book_data(data):
    """Validate required fields for a book"""
    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate year is an integer
    try:
        int(data["year"])
    except (ValueError, TypeError):
        return False, "Year must be a valid integer"
    
    return True, None

# GET /books - Retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    """Retrieve all books from the library"""
    return jsonify({
        "books": books,
        "total": len(books),
        "message": "Books retrieved successfully"
    }), 200

# POST /books - Add a new book
@app.route('/books', methods=['POST'])
def create_book():
    """Add a new book to the library"""
    global next_id
    
    # Check if request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request must contain JSON data"}), 400
    
    data = request.get_json()
    
    # Validate book data
    is_valid, error_message = validate_book_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # Create new book with unique ID
    new_book = {
        "id": next_id,
        "title": data["title"],
        "author": data["author"],
        "year": int(data["year"])
    }
    
    # Add book to the collection
    books.append(new_book)
    next_id += 1
    
    return jsonify({
        "book": new_book,
        "message": "Book created successfully"
    }), 201

# PUT /books/<id> - Update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update an existing book by ID"""
    # Find the book
    book = find_book(book_id)
    if not book:
        return jsonify({"error": f"Book with ID {book_id} not found"}), 404
    
    # Check if request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request must contain JSON data"}), 400
    
    data = request.get_json()
    
    # Validate book data
    is_valid, error_message = validate_book_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # Update book fields
    book["title"] = data["title"]
    book["author"] = data["author"]
    book["year"] = int(data["year"])
    
    return jsonify({
        "book": book,
        "message": "Book updated successfully"
    }), 200

# DELETE /books/<id> - Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book by ID"""
    global books
    
    # Find the book
    book = find_book(book_id)
    if not book:
        return jsonify({"error": f"Book with ID {book_id} not found"}), 404
    
    # Remove book from collection
    books = [b for b in books if b["id"] != book_id]
    
    return jsonify({
        "message": f"Book with ID {book_id} deleted successfully",
        "deleted_book": book
    }), 200

# GET /books/<id> - Get a specific book (bonus endpoint)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Retrieve a specific book by ID"""
    book = find_book(book_id)
    if not book:
        return jsonify({"error": f"Book with ID {book_id} not found"}), 404
    
    return jsonify({
        "book": book,
        "message": "Book retrieved successfully"
    }), 200

# Error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500 errors
@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({"error": "Internal server error"}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_books": len(books)
    }), 200

if __name__ == '__main__':
    print(" Starting Library Management API...")
    print(" Available endpoints:")
    print("  GET    /books       - Get all books")
    print("  POST   /books       - Create a new book")
    print("  GET    /books/<id>  - Get a specific book")
    print("  PUT    /books/<id>  - Update a book")
    print("  DELETE /books/<id>  - Delete a book")
    print("  GET    /health      - Health check")
    print("\n Test with curl or Postman at http://localhost:5000")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)