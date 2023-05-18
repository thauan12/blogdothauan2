from django.contrib import admin
from core.models import Post, Comentario

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'autor', 'criado', 'status')
    list_filter = ('status', 'criado', 'autor', 'publicado')
    search_fields = ('titulo', 'corpo')
    prepopulated_fields = {'slug':('titulo',)}
    raw_id_fields = ('autor',)
    date_hierarchy = 'publicado'
    ordering = ('status', 'publicado')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('post', 'nome', 'email', 'criado', 'status')
    list_filter = ('criado', 'status', 'post')
    ordering = ('post', 'criado', 'status')
