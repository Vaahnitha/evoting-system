from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.db import models
from django.utils.html import format_html
from .models import User, Candidate, Vote

class UserAdmin(BaseUserAdmin):
    # Add the role field to admin
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    # Make sure password is hashed automatically when creating/changing
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'department')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'timestamp')

# Register User model with custom admin
admin.site.register(User, UserAdmin)

# ----------------------------
# Election Results in Admin Sidebar
# ----------------------------

# Dummy proxy model
class Results(models.Model):
    class Meta:
        verbose_name_plural = "Election Results"
        managed = False  # No database table will be created

# Admin view for results
class ResultsAdmin(admin.ModelAdmin):
    # Disable add/change/delete
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    # Display results
    def changelist_view(self, request, extra_context=None):
        total_votes = Vote.objects.count()
        candidates = Candidate.objects.annotate(votes=Count('vote'))
        for c in candidates:
            c.percentage = round((c.votes / total_votes) * 100 if total_votes else 0, 2)
        context = {'total_votes': total_votes, 'candidates': candidates}
        return render(request, 'admin/results_dashboard.html', context)

# Register the dummy model in admin
admin.site.register(Results, ResultsAdmin)


