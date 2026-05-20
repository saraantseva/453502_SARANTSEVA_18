from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'required': True}))
    full_name = forms.CharField(max_length=200, label="ФИО", widget=forms.TextInput(attrs={'required': True}))
    phone = forms.CharField(
        max_length=20,
        label="Телефон",
        validators=[RegexValidator(regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$', message='Формат: +375 (29) XXX-XX-XX')],
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) 123-45-67', 'required': True})
    )
    birth_date = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date', 'required': True})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone', 'birth_date', 'password1', 'password2']
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'password1': forms.PasswordInput(attrs={'required': True}),
            'password2': forms.PasswordInput(attrs={'required': True}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError("Возраст должен быть не менее 18 лет.")
        return birth_date

from .models import Order

class OrderEditForm(forms.ModelForm):
    """Форма для редактирования заказа мастером"""
    class Meta:
        model = Order
        fields = ['status', 'master_note']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'master_note': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Заметки мастера...'})
        }
        labels = {
            'status': 'Статус заказа',
            'master_note': 'Заметки мастера'
        }
from .models import Review, Order, OrderService, OrderSparePart, Service, SparePart

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(),
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш отзыв...'}),
        }
from .models import Device

class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['device', 'client_problem']
        widgets = {
            'client_problem': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'client'):
            self.fields['device'].queryset = Device.objects.filter(client=user.client)

class OrderServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Услуга')
    quantity = forms.IntegerField(min_value=1, initial=1, label='Количество')

    class Meta:
        model = OrderService
        fields = ['service', 'quantity']

class OrderSparePartForm(forms.ModelForm):
    spare_part = forms.ModelChoiceField(queryset=SparePart.objects.all(), label='Запчасть')
    quantity = forms.IntegerField(min_value=1, initial=1, label='Количество')

    class Meta:
        model = OrderSparePart
        fields = ['spare_part', 'quantity']

class PromocodeApplyForm(forms.Form):
    code = forms.CharField(max_length=50, label='Промокод')