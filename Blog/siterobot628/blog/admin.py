from django.contrib import admin
from blog.models import Post


#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс для управлением моделью Post в админке Django"""
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # отображение полей
    list_filter = ['status', 'created', 'publish', 'author']  # фильтрация по
    search_fields = ['title', 'body']  # поиск по
    prepopulated_fields = {'slug': ('title',)}  # создаёт данные этого поля на базе title
    raw_id_fields = ['author']  # вместо выпадающего меню поисковик автора
    date_hierarchy = 'publish'  # иерархия дат
    ordering = ['status', 'publish']  # сортировка по
