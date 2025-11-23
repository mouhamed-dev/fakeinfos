from django.contrib import admin
from . models import Identity

class IdentityAdmin(admin.ModelAdmin):
    list_display = ['prenom', 'nom', 'phone', 'genre', 'profession', 'pays', 'province', 'date']
    list_display_links = ['prenom', 'genre', 'province']
    list_per_page = 30

admin.site.register(Identity, IdentityAdmin)