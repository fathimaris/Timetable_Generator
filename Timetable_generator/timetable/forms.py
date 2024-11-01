from django import forms

from timetable.models import Course, Subject, Staff


class course_form(forms.ModelForm):
    class Meta:
        model=Course
        fields='__all__'

class subject_form(forms.ModelForm):
    class Meta:
        model=Subject
        fields='__all__'


class staff_form(forms.ModelForm):
    class Meta:
        model=Staff
        fields='__all__'
        widgets={
            'subjects': forms.CheckboxSelectMultiple(),
        }

class CourseSelectionForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label='Select Courses'
    )

