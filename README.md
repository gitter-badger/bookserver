A simple django server for serving ebooks written years ago - now updating for modern technologies.

Uses django-inspectional-registration for user managment

Library api is exposed under /shelves
books/ lists all books
books/<book_slug> gives detail on a specific book
authors/ lists all authors
authors/<author_slug> gives detail on a specific book


/shelves/ is a jquery interface that lets you search for books - it was only ever half finished and is quite rough. Current project is to replace it with a moble friendly page.
