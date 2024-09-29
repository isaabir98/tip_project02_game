# admin.py
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from .models import User, Role
from .forms import UserCreationForm

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-user/', self.admin_site.admin_view(self.create_user), name='create-user'),
        ]
        return custom_urls + urls

    def create_user(self, request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin:your_app_user_changelist')  # Redirect to user list
        else:
            form = UserCreationForm()
        return render(request, 'admin/create_user.html', {'form': form})

# Register your User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Role)
