from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    banner = models.ImageField(upload_to="event_banners/", blank=True, null=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    events = models.ManyToManyField(Event, related_name="participants")

    def __str__(self):
        return self.name
