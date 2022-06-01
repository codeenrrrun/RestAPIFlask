
## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

*LIST OF ALL API's Implemented*

1. Add and GET Author 
    *API* : /authors

    with GET request it will give all the available authors.

    with POST request and with below body it will save the details to DataBase

    body : {
    "author_id": "A1",
    "name": "Ritik Soni",
    "phone_number": "7987392909",
    "birth_date": "16-10-1999",
    "death_date": "None"
    }
2. Get and DELETE Author by Author ID
    *API* : /bookWithAuthorId/<string:author_id>
   
   with GET request it will give details of the given Author ID.

   with DELETE request it will delete that author data from the database 
   
3. Add and GET Book
    *API* : /books

    with GET request it will give all the available Books.

    with POST request and with below body it will save the details to DataBase
    
    body : {
            "author_id": "A1",
            "book_id": "B1",
            "category_id": "cat1",
            "price": "600",
            "publish_date": "16-10-1999",
            "publisher": "BBC",
            "sold_count": "455",
            "title": "Sherlock Holmes"
        }

4. Get and DELETE Book by Book ID
   *API* : /bookWithId/<string:book_id>

   with GET request it will give details of the given book ID.

   with DELETE request it will delete that book data from the database 

5. Get list of all categories available.
   *API* :/getAllCategories

    Will return all the available Categories in the database.

   
6. Get list of all Authors available.
   *API* : /getAllAuthors

   will return all the available authors in the database.
   
7. Get Most Books Sold by Author.
   *API* : /getMostBooksSoldByAuthor/<string:author_id>

   Will return the most sold book of the given author
   
8. Get Most Books Sold by Category
    *API* : /getMostBooksSoldByCategoryId/<string:category_id>

    Will return the most sold book of the given Category
   
9.  Search Books (On Patial Title, On Parital Author Name, on Both)
    *API* : /searchBookByTitle/<string:title>

    Will search on the title basis

    *API* : /searchBookByAuthor/<string:author_name>

    Will search on the Author Name basis

    *API* : /searchBookByAuthorAndTitle/<string:author_name>/<string:title>

    Will search on both Author Name and Title basis

   
