from django import forms

from TodoApp.Application.models import Assignment


class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'description']
        exclude = ['created_on', 'modified']
        widgets = {
            "description": forms.Textarea,
        }
