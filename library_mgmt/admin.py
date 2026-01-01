from django.contrib import admin
from .models import User,Resource,LibrarySession

admin.site.register(User)
admin.site.register(Resource)
admin.site.register(LibrarySession)
