from django.contrib import admin
from . models import Category,Tag,Post,Message,Article

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['title','create_time','modified_time','category','author']

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post,PostAdmin)
admin.site.register(Message)
admin.site.register(Article)

