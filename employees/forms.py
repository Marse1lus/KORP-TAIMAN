from django import forms
from .models import Employee, Department, Position

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['department', 'position', 'phone', 'bio', 'skills', 'hire_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap для всех полей
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'department', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 