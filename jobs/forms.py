from django import forms
from .models import Job
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5*1024*1024:  # 5MB limit
                raise forms.ValidationError("Resume file size should not exceed 5MB.")
        return resume

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'salary', 'location']
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title