from django.contrib import admin
from post_thoughts.models import Thought,Comment
# Register your models here.

admin.site.register(Thought)
admin.site.register(Comment)