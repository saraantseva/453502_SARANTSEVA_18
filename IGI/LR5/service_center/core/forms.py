from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date
import re

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'required': True}))
    full_name = forms.CharField(max_length=200, label="ФИО", widget=forms.TextInput(attrs={'required': True}))
    phone = forms.CharField(
        max_length=20,
        label="Телефон",
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) 123-45-67'})
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Удаляем всё, кроме цифр
        digits = re.sub(r'\D', '', phone)
        
        # Проверяем, что код 375 и оператор 29
        if len(digits) == 12 and digits.startswith('37529'):
            formatted = f'+375 ({digits[3:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:12]}'
        elif len(digits) == 9:
            formatted = f'+375 ({digits[:2]}) {digits[2:5]}-{digits[5:7]}-{digits[7:9]}'
        elif len(digits) == 11 and digits.startswith('8'):
            formatted = f'+375 ({digits[1:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}'
        else:
            raise forms.ValidationError('Телефон должен быть в формате +375 (29) XXX-XX-XX')
        
        # Проверяем итоговый формат старым валидатором
        validator = RegexValidator(
            regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
            message='Телефон должен быть в формате: +375 (29) XXX-XX-XX'
        )
        validator(formatted)
        
        return formatted
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
        fields = ['device', 'client_problem', 'address']
        widgets = {
            'client_problem': forms.Textarea(attrs={'rows': 3}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес (оставьте пустым, чтобы использовать адрес из профиля)'}),
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

from django import forms
from .models import Order, Client, Device, Employee

class AdminOrderCreateForm(forms.ModelForm):
    """Полная форма для создания заказа администратором"""
    
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Клиент",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        label="Устройство",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label="Ответственный сотрудник (мастер)",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        label="Статус",
        initial='new',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    address = forms.CharField(
        max_length=500,
        label="Адрес",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_address',
            'placeholder': 'Начните вводить адрес...'
        })
    )
    
    completion_date = forms.DateField(
        label="Дата завершения",
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    class Meta:
        model = Order
        fields = ['client', 'device', 'employee', 'status', 'client_problem', 'address', 'completion_date']
        widgets = {
            'client_problem': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Опишите проблему со слов клиента...'
            }),
        }
        labels = {
            'client_problem': 'Описание проблемы',
        }