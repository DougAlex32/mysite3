from django.contrib import admin
from django.db import models
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]



# class Artist(models.Model):
#   name = models.CharField(max_length=100)

#   def __str__(self):
#     return self.name

# class Album(models.Model):
#   title = models.CharField(max_length=100)
#   artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

#   def __str__(self):
#     return self.title

# class Song(models.Model):
#   title = models.CharField(max_length=100)
#   album = models.ForeignKey(Album, on_delete=models.CASCADE)
#   artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

#   def __str__(self):
#     return self.title

admin.site.register(Question, QuestionAdmin,)

