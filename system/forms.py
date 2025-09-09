from django import forms
from .models import Event, Participant, Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "time", "location", "category", "banner"]


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "avatar", "events"]
        widgets = {
            "events": forms.CheckboxSelectMultiple
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
