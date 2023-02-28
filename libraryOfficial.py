import requests

# load books first creates an empy dict of books, then takes the CSV file and looks at each line in the file to add to the dictionary & returns the dict
def load_books():
    book_dict = {}  # empty dict of books9780545459389

    with open("Book_Inventory.csv", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")
            isbn, title, author, quantity = line.split("|")
            book_dict[isbn] = (isbn, title, author, int(quantity))
            # book dictionary at current ISBN is = to the tuple...
    return book_dict


def bookPlaceholder(isbn):
    return (isbn, "unknown", "unknown")


# requests book info based on ISBN - returns ISBN, title, author (or ISBN, title, unknown if no author)
def bookLookUp(isbn):
    response = requests.get(
        "https://openlibrary.org/api/books?format=json&jscmd=details&bibkeys=ISBN:"
        + isbn
    )
    if response.status_code < 200 or response.status_code > 299:
        print("Non 200 response:", str(response.status_code))
        return None

    bookData = response.json()
    isbnData = bookData.get("ISBN:" + isbn)
    if isbnData == None:
        return None

    bookDetails = isbnData["details"]
    title = bookDetails.get("title")
    if title == None:
        return None
    authorsList = bookDetails.get("authors")
    if authorsList == None:
        return None
    author = authorsList[0]["name"]
    return (isbn, title, author)

    # bookData = response.json()
    # title = bookData["title"]
    # authorInfo = bookData.get("authors")
    # if authorInfo == None:
    #    return (isbn, title, "unknown")

    # firstAuthor = authorInfo[0]
    # authorURL = firstAuthor["key"]
    # authorResponse = requests.get("https://openlibrary.org" + authorURL + ".json")
    # authorData = authorResponse.json()
    # authorName = authorData["name"]
    # return (isbn, title, authorName)


print("Type in the book's ISBN:")

library = load_books()
# until user enters q, the loop will add book to library if doesn't exist, or will add to quantity if does
while True:
    isbn = input("ISBN: ")
    if isbn == "q":
        break

    # Don't look up isbn if we've already seen it
    existingBook = library.get(isbn)
    if existingBook == None:
        book = bookLookUp(isbn)
        if book == None:
            print("could not find ISBN. Type in next book's ISBN.")
            book = bookPlaceholder(isbn)
        library[isbn] = (book[0], book[1], book[2], 1)
    else:
        print("This book exists in your library. Quantity has been increased.")
        updatedBook = (
            existingBook[0],
            existingBook[1],
            existingBook[2],
            existingBook[3] + 1,
        )
        library[isbn] = updatedBook
    print(library[isbn])
    if input("Enter 'e' to edit: ") == "e":
        print("Update or leave blank to keep")
        newTitle = input("Title: ")
        newAuthor = input("Author: ")
        currentBook = library[isbn]
        if newTitle == "":
            newTitle = currentBook[1]
        if newAuthor == "":
            newAuthor = currentBook[2]
        library[isbn] = (currentBook[0], newTitle, newAuthor, currentBook[3])

    print()  # print an extra line


# this will take the loaded books & create a new CSV with the information, placing each variable into a separate column
# this will overwrite every time it runs b/c of the "W"
with open("Book_Inventory.csv", "w", encoding="utf-8") as file:
    for book in library.values():
        # take apart the tuple to show location of each variable, so can be addressed individually
        isbn = book[0]
        title = book[1]
        author = book[2]
        quantity = book[3]
        file.write(isbn + "|" + title + "|" + author + "|" + str(quantity) + "\n")
