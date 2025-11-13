from django import forms
from .models import Service, Category


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'state_duty']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название услуги'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание услуги',
                'rows': 4
            }),
            'state_duty': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            })
        }
        labels = {
            'name': 'Название услуги',
            'category': 'Категория',
            'description': 'Описание',
            'state_duty': 'Госпошлина (руб.)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Только категории, которые существуют
        self.fields['category'].queryset = Category.objects.all()
        # Делаем поле категории необязательным
        self.fields['category'].required = False