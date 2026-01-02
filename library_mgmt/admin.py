from django.contrib import admin
from .models import User,Resource,LibrarySession
from .models import Book  # Import your Book model

# This line tells Django to show "Books" in the admin panel
admin.site.register(Book)
admin.site.register(User)
admin.site.register(Resource)
admin.site.register(LibrarySession)
