from django import forms
from .models import Loan, Review
from django.utils import timezone


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['due_date']
        labels = {
            'due_date': 'Fecha de vencimiento',
        }
        widgets = {
            'due_date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']

        if due_date < timezone.now().date():
            raise forms.ValidationError(
                'La fecha límite no puede ser anterior a hoy.'
            )

        return due_date


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'min': 1,
                    'max': 5
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'rows': 5
                }
            )
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                'La valoración debe estar entre 1 y 5.'
            )

        return rating