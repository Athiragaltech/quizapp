from django.contrib import admin
from django.shortcuts import redirect
from .models import Course,QuizQuestion,QuizChoice,Quiz
class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('admin_index')  # Redirect superuser to admin_index page
        return super().index(request, extra_context)

custom_admin_site = CustomAdminSite(name='customadmin')

# Register your models with the custom admin site
custom_admin_site.register(Course)
admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(QuizChoice)
admin.site.register(QuizQuestion)