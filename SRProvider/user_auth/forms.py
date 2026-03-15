from django import forms
from resources.models import CourseModel, SemesterModel, Subject, Unit, Notes

class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        fields = ['course_name']   # user is set automatically in views
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SemesterForm(forms.ModelForm):
    class Meta:
        model = SemesterModel
        fields = ['semester', 'course']
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'unit_title']
        widgets = {
            'unit_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_title': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
        }


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'file', 'unit']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
        }
