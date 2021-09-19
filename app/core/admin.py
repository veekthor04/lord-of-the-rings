from django.contrib import admin

from .models import CustomUser, Character, Quote


admin.site.register(CustomUser)
admin.site.register(Character)
admin.site.register(Quote)
