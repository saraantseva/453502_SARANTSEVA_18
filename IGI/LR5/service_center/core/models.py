from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from datetime import date

class Client(models.Model):
    """Модель клиента"""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Связь c учетной записью пользователя"
    )

    full_name = models.CharField(
        max_length=200, 
        verbose_name="ФИО"
    )
    
    '''
    phone number.  format: +375 (29) XXX-XX-XX
    '''
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате: +375 (29) XXX-XX-XX'
            )
        ],
        verbose_name="Телефон"
    )
    
    birth_date = models.DateField(
        verbose_name="Дата рождения"
    )
    
    address = models.TextField(
        blank=True,
        verbose_name="Адрес"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    
    def __str__(self):
        """Строковое представление"""
        return "Клиент: " + self.full_name
    
    def get_absolute_url(self):
        """URL для просмотра клиента"""
        return reverse('client_detail', args=[str(self.id)])
    
    @property
    def age(self):
        """Вычисление возраста"""
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    def clean(self):
        """
        Валидация на уровне модели.
        Проверка возраста 18+
        """
        if self.age < 18:
            raise ValidationError({
                'birth_date': f'Клиент должен быть старше 18 лет. Ваш возраст: {self.age}'
            })
    
    def save(self, *args, **kwargs):
        """
        Полный вызов валидации перед сохранением
        """
        self.full_clean()  # вызывает clean() и валидаторы полей
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['full_name']  # сортировка по ФИО
        indexes = [
            models.Index(fields=['phone']),      # быстрый поиск по телефону
        ]


class Specialization(models.Model):
    """Модель специализации"""
    name = models.CharField(max_length=100)  # "Ремонт ПК", "Ремонт ноутбуков", "Диагностика"
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Специализации"


class Employee(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
        help_text="Связь c учетной записью сотрудника"
    )

    specialization = models.ManyToManyField(
        'Specialization',
        blank=True,
        verbose_name="Специализации"
    )

    full_name = models.CharField(
        max_length=30,
        verbose_name="ФИО"
    )

    photo = models.ImageField(
        upload_to='employees/',
        blank=True,
        null=True,
        verbose_name="Фото"
    )
    '''phone number.  format: +375 (29) XXX-XX-XX'''
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате: +375 (29) XXX-XX-XX'
            )
        ],
        verbose_name="Телефон"
    )

    birth_date = models.DateField(
    verbose_name="Дата рождения" 
    )

    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),  
        ]
    )
    created_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name="Дата регистрации"
        )
    

    def __str__(self):
        """Строковое представление"""
        return "Сотрудник: " + self.full_name 
    
    def get_absolute_url(self):
        """URL для просмотра сотрудника"""
        return reverse('employee_detail', args=[str(self.id)])
    
    @property
    def age(self):
        """Вычисление возраста"""
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    def clean(self):
        """
        Проверка возраста 18+
        """
        if self.age < 18:
            raise ValidationError({
                'birth_date': f'Клиент должен быть старше 18 лет. Ваш возраст: {self.age}'
            })
    
    def save(self, *args, **kwargs):
        """
        Полный вызов валидации перед сохранением
        """
        self.full_clean()  # вызывает clean() и валидаторы полей
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['full_name']  # сортировка по ФИО
        indexes = [
            models.Index(fields=['phone']),      # быстрый поиск по телефону
        ]

class DeviceType(models.Model):
    """Тип устройства (компьютер, ноутбук, принтер, монитор)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Типы устройств"


class Device(models.Model):
    """Устройство клиента"""
    device_type = models.ForeignKey(
        DeviceType, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тип устройства"
    )
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='devices'
    )
    
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    model = models.CharField(max_length=100, verbose_name="Модель")
    serial_number = models.CharField(max_length=100, blank=True, verbose_name="Серийный номер")
    description = models.TextField(blank=True, verbose_name="Описание проблемы")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.client.full_name}"
    
    class Meta:
        verbose_name_plural = "Устройства"
        ordering = ['-created_at']

class ServiceType(models.Model):
    """Тип услуги (диагностика, ремонт, профилактика, установка ПО)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Типы услуг"


class Service(models.Model):
    """Услуга сервисного центра"""
    
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(default=1)  # сколько дней длится услуга
 
    
    def __str__(self):
        return f"{self.name} - {self.price} y.e."
    
    class Meta:
        verbose_name_plural = "Услуги"
        ordering = ['name']

class SparePartType(models.Model):
    """Тип запчасти (процессоры, ОЗУ, жесткие диски, блоки питания и т.д.)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Типы запчастей"


class SparePart(models.Model):
    """Запчасть для ремонта"""
    
    part_type = models.ForeignKey(
        SparePartType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.price} руб. (в наличии: {self.quantity_in_stock})"
    
    class Meta:
        verbose_name_plural = "Запчасти"
        ordering = ['name']

########################################################################
class Order(models.Model):
    """Заказ/Договор на ремонт - полностью по требованиям лабы"""

    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('diagnostics', 'На диагностике'),
        ('waiting_parts', 'Ожидает запчасти'),
        ('in_repair', 'В ремонте'),
        ('ready', 'Готов к выдаче'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]

    # Номер заказа (уникальный, обязательный)
    order_number = models.CharField(
        max_length=50, 
        unique=True,
        blank=True, 
        verbose_name="Номер заказа"
    )
        
    promocode = models.ForeignKey(
        'Promocode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Применённый промокод"
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Сумма скидки"
    )
    # Клиент (один клиент - много заказов)
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Клиент"
    )
    
    # Устройство (одно устройство - один заказ)
    device = models.OneToOneField(
        'Device',
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name="Устройство"
    )
    
    # Сотрудник (один сотрудник - много заказов)
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name="Ответственный сотрудник"
    )
    
    
    # Услуги (для хранения количества и цены)
    services = models.ManyToManyField(
        'Service',
        through='OrderService',
        related_name='orders',
        blank=True,
        verbose_name="Услуги"
    )
    
    # Запчасти
    spare_parts = models.ManyToManyField(
        'SparePart',
        through='OrderSparePart',
        related_name='orders',
        blank=True,
        verbose_name="Запчасти"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )
    
    # Даты
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    completion_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Дата завершения"
    )
    
    # Финансы
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False,  # ← нельзя редактировать в админке/формах
        verbose_name="Итоговая стоимость"
    )
    
    # Дополнительная информация
    client_problem = models.TextField(
        blank=True,
        verbose_name="Описание проблемы",
        help_text="Что случилось со слов клиента"
    )
    master_note = models.TextField(
        blank=True,
        verbose_name="Заметки мастера",
        help_text="Что сделано, рекомендации"
    )
    
    
    def __str__(self):
        return f"Заказ №{self.order_number} - {self.client.full_name}"
    
    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])
   
    def calculate_total_cost(self):
        """Стоимость услуг + запчастей без скидки"""
        services_total = sum(
            item.price_at_time * item.quantity 
            for item in self.order_services.all()
        )
        parts_total = sum(
            item.price_at_time * item.quantity 
            for item in self.order_spare_parts.all()
        )
        return services_total + parts_total

    def calculate_discount(self):
        """Рассчитывает сумму скидки"""
        if self.promocode:
            return self.total_cost * self.promocode.discount_percent / 100
        return 0

    def get_final_cost(self):
        """Итоговая стоимость со скидкой"""
        return self.total_cost - self.discount_amount

    def update_total_cost(self):
        self.total_cost = self.calculate_total_cost()
        self.discount_amount = self.calculate_discount()
        super().save(update_fields=['total_cost', 'discount_amount'])

    def save(self, *args, **kwargs):
        # Если номер не указан, сгенерировать автоматически
        if not self.order_number:
            from django.utils import timezone
            year = timezone.now().year
            last_order = Order.objects.filter(
                order_number__startswith=f'SC-{year}-'
            ).order_by('-order_number').first()
            
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.order_number = f'SC-{year}-{new_num:04d}'
        
        # Сохраняем сначала (чтобы появился pk)
        super().save(*args, **kwargs)
        
        # Обновляем стоимость только если есть связанные услуги/запчасти
        if self.pk and (self.order_services.exists() or self.order_spare_parts.exists()):
            self.update_total_cost()
        

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['client']),
        ]
        permissions = [
            ('can_change_order_status', 'Может менять статус заказа'),   # мастер
            ('can_edit_master_note', 'Может редактировать заметки мастера'),  # мастер
            ('can_create_order', 'Может создавать заказы'),       
            ('can_use_promocode', 'Может использовать промокоды'),
        ]

class OrderService(models.Model):
    """Услуга в заказе - промежуточная таблица для ManyToMany"""
    
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='order_services'
    )
    service = models.ForeignKey(
        'Service', 
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1, 
        validators=[MinValueValidator(1)],
        verbose_name="Количество"
    )
    price_at_time = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,   
        null=True,    
        verbose_name="Цена на момент заказа"
    )
    
    def save(self, *args, **kwargs):
        # Автоматически фиксируем цену на момент добавления
        if not self.price_at_time:
            self.price_at_time = self.service.price
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.service.name} x{self.quantity}"
    
    class Meta:
        verbose_name = "Услуга в заказе"
        verbose_name_plural = "Услуги в заказе"
        unique_together = [['order', 'service']]


class OrderSparePart(models.Model):
    """Запчасть в заказе - промежуточная таблица для ManyToMany"""
    
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='order_spare_parts'
    )
    spare_part = models.ForeignKey(
        'SparePart', 
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1, 
        validators=[MinValueValidator(1)],
        verbose_name="Количество"
    )
    price_at_time = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,   
        null=True,    
        verbose_name="Цена на момент заказа"
    )
    
    def save(self, *args, **kwargs):
        # Автоматически фиксируем цену на момент добавления
        if not self.price_at_time:
            self.price_at_time = self.spare_part.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.spare_part.name} x{self.quantity}"
    
    class Meta:
        verbose_name = "Запчасть в заказе"
        verbose_name_plural = "Запчасти в заказе"
        unique_together = [['order', 'spare_part']]


########################## модели для отобр страниц сайта  #################################


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_description = models.CharField(max_length=300, verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Полное содержание")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Картинка")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:news_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

class CompanyInfo(models.Model):
    """Информация о компании (хранится в БД)"""
    text = models.TextField(verbose_name="Текст о компании")
    logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name="Логотип")
    requisites = models.TextField(verbose_name="Реквизиты", blank=True)
    video_url = models.URLField(blank=True, verbose_name="Ссылка на видео")
    
    def __str__(self):
        return "Информация о компании"
    
    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

class Glossary(models.Model):
    term = models.CharField(max_length=200, verbose_name="Термин/Вопрос")
    definition = models.TextField(verbose_name="Определение/Ответ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Термин"
        verbose_name_plural = "Словарь терминов"
        ordering = ['-created_at']

    def __str__(self):
        return self.term
    
class Vacancy(models.Model):
    """Вакансия"""
    title = models.CharField(max_length=200, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание")
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата от", blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата до", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']


class Promocode(models.Model):
    """Промокод"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Код промокода")
    discount_percent = models.IntegerField(verbose_name="Скидка (%)", validators=[MinValueValidator(1), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True, verbose_name="Действующий")
    expires_at = models.DateField(verbose_name="Дата окончания", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        status = "Действует" if self.is_active else "В архиве"
        return f"{self.code} - {self.discount_percent}% ({status})"
    
    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ['-is_active', '-created_at']
        permissions = [
            ('can_use_promocode', 'Может использовать промокоды'),       # клиент
        ]

class Review(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Пользователь",
        related_name='reviews'
    )
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        verbose_name="Оценка"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.user.username} — {self.rating}★"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
        permissions = [
            ('can_add_review', 'Может добавлять отзывы'),      
            ('can_edit_own_review', 'Может редактировать свои отзывы'),
            ('can_delete_own_review', 'Может удалять свои отзывы'),
        ]