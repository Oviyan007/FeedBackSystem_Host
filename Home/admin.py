# admin.py
from django.contrib import admin
from .models import *



class StudentInline(admin.TabularInline):
    model = Subject_detail
    extra = 5  # Set the number of empty forms to display

class BatchSectionInline(admin.TabularInline):
    model = BatchSection
    extra = 1  # Number of empty sections to display in the admin panel

class BatchAdmin(admin.ModelAdmin):
    list_display = ('Batchyear', 'department')
    inlines = [BatchSectionInline]

admin.site.register(Batch, BatchAdmin)
admin.site.register(BatchSection)

admin.site.register(Faculty)
  # Add the SectionInline




admin.site.register(UserProfile)

admin.site.register(User)

admin.site.register(FeedbackRes)

admin.site.register(Subject_detail)
admin.site.register(Staff)






