from django.contrib import admin
from .models import Tutorial,Comment,FilesAdmin,Qcomment

admin.site.register(Tutorial)
admin.site.register(Comment)
admin.site.register(Qcomment)

admin.site.register(FilesAdmin)
