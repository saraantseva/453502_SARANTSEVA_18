'''

    home()                - Главная страница (последняя новость, услуги, NASA, техновости)
    about()               - О компании
    news_list()           - Список новостей
    news_detail(pk)       - Полный текст новости
    glossary()            - Словарь терминов
    contacts()            - Сотрудники с фото и специализациями
    privacy()             - Политика конфиденциальности
    vacancies()           - Активные вакансии
    promocodes()          - Промокоды (активные и архивные)
    reviews()             - Список отзывов
    service_list()        - Услуги (поиск, фильтр по типу, сортировка по цене)
    statistics_page()     - Статистика: продажи, возраст, популярность, графики

ОТЗЫВЫ (CRUD) 224
    review_add()          - Добавление отзыва (только авторизованные)
    review_edit(pk)       - Редактирование своего отзыва
    review_delete(pk)     - Удаление своего отзыва

АВТОРИЗАЦИЯ 293
    register()            - Регистрация нового пользователя (создаёт Client)
    CustomLoginView       - Вход (редирект на master или client)

МАСТЕР 334
    master_dashboard()    - Личный кабинет мастера (список заказов с поиском/фильтром)
    master_edit_order(pk) - Редактирование заказа мастером (статус, заметки)

КЛИЕНТ 408
    client_dashboard()    - Личный кабинет клиента (список заказов)
    client_create_order() - Создание нового заказа
    client_add_items(pk)  - Добавление/удаление услуг/запчастей в заказ
    client_remove_order_item(pk, type, id) - Удаление услуги/запчасти из заказа
    client_order_summary(pk) - Подтверждение оформленного заказа

АДМИН 584
    admin_orders()        - Список всех заказов с поиском, фильтром, пагинацией
    admin_order_detail(pk)- Полное редактирование заказа (статус, услуги, запчасти)
    admin_order_create()  - Создание заказа администратором (все поля, адрес с подсказками)


'''

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator

from .forms import *
from core.models import * 
from .utils import * 
from .statistics import * 

from .logger_config import setup_logging
# логгеры из конфигурации
_loggers = setup_logging()
user_logger = _loggers['user']
error_logger = _loggers['error']
debug_logger = _loggers['debug']
###################################### PAGES #########################
def home(request):
    context = get_timezone_context()
    context['last_news'] = News.objects.first()
    context['services'] = Service.objects.all()[:3]
    if request.user.is_authenticated:
        context['nasa_apod'] = get_nasa_apod()
    context['tech_news'] = get_tech_news()  
    return render(request, 'core/home.html', context)

def about(request):
    context = get_timezone_context()
    context['company_info'] = CompanyInfo.objects.first()
    return render(request, 'core/about.html', context)

def news_list(request):
    context = get_timezone_context()
    context['news_list'] = News.objects.all()
    return render(request, 'core/news_list.html', context)

def news_detail(request, pk):
    news = News.objects.get(id=pk)
    context = get_timezone_context()
    context['news'] = news
    context['news_created_utc'] = news.created_at.strftime('%d/%m/%Y %H:%M')
    context['news_created_local'] = utc_to_local(news.created_at).strftime('%d/%m/%Y %H:%M')
    return render(request, 'core/news_detail.html', context)

def glossary(request):
    context = get_timezone_context()
    terms = Glossary.objects.all().order_by('-created_at')
    
    for term in terms:
        term.created_utc = term.created_at.strftime('%d/%m/%Y %H:%M')
        term.created_local = utc_to_local(term.created_at).strftime('%d/%m/%Y %H:%M')
    
    context['terms'] = terms
    return render(request, 'core/glossary.html', context)

def contacts(request):
    context = get_timezone_context()
    employees = Employee.objects.all()
    
    for employee in employees:
        employee.created_utc = employee.created_at.strftime('%d/%m/%Y %H:%M')
        employee.created_local = utc_to_local(employee.created_at).strftime('%d/%m/%Y %H:%M')
    
    context['employees'] = employees
    return render(request, 'core/contacts.html', context)

def privacy(request):
    context = get_timezone_context()
    return render(request, 'core/privacy.html', context)

def vacancies(request):
    context = get_timezone_context()
    vacancies_list = Vacancy.objects.filter(is_active=True)
    
    for vacancy in vacancies_list:
        vacancy.created_utc = vacancy.created_at.strftime('%d/%m/%Y %H:%M')
        vacancy.created_local = utc_to_local(vacancy.created_at).strftime('%d/%m/%Y %H:%M')
    
    context['vacancies'] = vacancies_list
    return render(request, 'core/vacancies.html', context)

def promocodes(request):
    context = get_timezone_context()
    context['active_promocodes'] = Promocode.objects.filter(is_active=True)
    context['archived_promocodes'] = Promocode.objects.filter(is_active=False)
    return render(request, 'core/promocodes.html', context)

def reviews(request):
    context = get_timezone_context()
    return render(request, 'core/reviews.html', context)

def statistics_page(request):
    """Страница со статистическими показателями"""
    # Получаем все данные для статистики
    clients_list, total_sales = clients_alphabetical()
    avg_amount, mode_amount, median_amount = order_amount_stats()
    avg_age, median_age = client_age_stats()
    popular_type = most_popular_service_type()
    profitable_type = most_profitable_service_type()
    monthly_orders = orders_by_month()
    status_distribution = order_status_distribution()

    # Генерация графиков с помощью matplotlib
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io
    import base64

    # График 1: Динамика заказов по месяцам (линейный)
    line_chart = None
    if monthly_orders:
        months = [item['month'] for item in monthly_orders]
        counts = [item['count'] for item in monthly_orders]

        plt.figure(figsize=(10, 5))
        plt.plot(months, counts, marker='o', linestyle='-', color='#e94560', linewidth=2, markersize=6)
        plt.title('Динамика заказов по месяцам')
        plt.xlabel('Месяц')
        plt.ylabel('Количество заказов')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        line_chart = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

    # График 2: Распределение заказов по статусам (круговая)
    pie_chart = None
    if status_distribution:
        labels = list(status_distribution.keys())
        sizes = list(status_distribution.values())

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Распределение заказов по статусам')
        plt.axis('equal')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        pie_chart = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

    context = get_timezone_context()
    context.update({
        'clients': clients_list,
        'total_sales': total_sales,
        'avg_amount': avg_amount,
        'mode_amount': mode_amount,
        'median_amount': median_amount,
        'avg_age': avg_age,
        'median_age': median_age,
        'popular_type': popular_type,
        'profitable_type': profitable_type,
        'line_chart': line_chart,
        'pie_chart': pie_chart,
    })
    return render(request, 'core/statistics.html', context)

def service_list(request):
    services = Service.objects.all()
    
    # 1. ПОИСК по названию
    search_query = request.GET.get('search', '')
    search_query = request.GET.get('search', '')
    if search_query:
        # Получаем все услуги и фильтруем в Python
        services = [s for s in services if search_query.lower() in s.name.lower()]
    # 2. ФИЛЬТР по типу услуги
    type_id = request.GET.get('type')
    if type_id:
        services = services.filter(service_type_id=type_id)
    
    # 3. СОРТИРОВКА по цене
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        services = services.order_by('price')
    elif sort == 'price_desc':
        services = services.order_by('-price')
    
    service_types = ServiceType.objects.all()
    
    context = get_timezone_context()
    context.update({
        'services': services,
        'service_types': service_types,
        'search_query': search_query,
        'selected_type': type_id,
        'selected_sort': sort,
    })
    return render(request, 'core/service_list.html', context)

################################## отзывы логика ##################

def reviews_list(request):
    """Список всех отзывов (доступен всем)"""
    all_reviews = Review.objects.all()
    context = get_timezone_context()
    context['reviews'] = all_reviews
    return render(request, 'core/reviews.html', context)


def reviews(request):
    all_reviews = Review.objects.all()
    context = get_timezone_context()
    context['reviews'] = all_reviews
    return render(request, 'core/reviews.html', context)

@login_required
def review_add(request):
    if not request.user.has_perm('core.can_add_review'):
        raise PermissionDenied("У вас нет права добавлять отзывы")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            user_logger.info(f"User {request.user.username} added a review (rating: {review.rating})")
            return redirect('core:reviews')
    else:
        form = ReviewForm()
    
    context = get_timezone_context()
    context['form'] = form
    return render(request, 'core/review_form.html', context)

@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if not request.user.has_perm('core.can_edit_own_review'):
        raise PermissionDenied("У вас нет права редактировать отзыв")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            user_logger.info(f"User {request.user.username} edited review #{review.id}")
            return redirect('core:reviews')
    else:
        form = ReviewForm(instance=review)
    
    context = get_timezone_context()
    context['form'] = form
    context['review'] = review
    return render(request, 'core/review_form.html', context)

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if not request.user.has_perm('core.can_delete_own_review'):
        raise PermissionDenied("У вас нет права удалять отзыв")
    
    if request.method == 'POST':
        review.delete()
        user_logger.info(f"User {request.user.username} deleted review #{review.id}")
        return redirect('core:reviews')
    
    context = get_timezone_context()
    context['review'] = review
    return render(request, 'core/review_confirm_delete.html', context)


################################ авторизация регистрация ###########
def register(request):
    '''/register/'''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                birth_date=form.cleaned_data['birth_date'],
            )
            login(request, user)
            user_logger.info(f"New user registered: {user.username} (ID: {user.id})")
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = get_timezone_context()
    context['form'] = form
    return render(request, 'registration/register.html', context)

class CustomLoginView(LoginView):
    '''/accounts/login/'''
    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'employee'):
            return '/master/'
        elif hasattr(user, 'client'):
            return '/client/'
        return '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_timezone_context())
        return context
    
    def form_valid(self, form):
        """Логирование успешного входа"""
        response = super().form_valid(form)
        user_logger.info(f"User logged in: {self.request.user.username}")
        return response




##################### личный кабинет мастера ###########################
@login_required
def master_dashboard(request):
    if not hasattr(request.user, 'employee'):
        return redirect('core:home')
    
    employee = request.user.employee
    orders = Order.objects.filter(employee=employee)
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            models.Q(order_number__icontains=search_query) |
            models.Q(client__full_name__icontains=search_query)
        )
    
    sort = request.GET.get('sort', '')
    if sort == 'newest':
        orders = orders.order_by('-created_at')
    elif sort == 'oldest':
        orders = orders.order_by('created_at')
    
    context = get_timezone_context()
    context.update({
        'employee': employee,
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
        'selected_sort': sort,
    })
    return render(request, 'core/master/master_dashboard.html', context)



@login_required
def master_edit_order(request, order_id):
    if not hasattr(request.user, 'employee'):
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id, employee=request.user.employee)
    
    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            user_logger.info(f"Master {request.user.username} edited order #{order.order_number}")
            messages.success(request, f'Заказ №{order.order_number} успешно обновлён')
            return redirect('core:master_dashboard')
    else:
        form = OrderEditForm(instance=order)
    
    context = get_timezone_context()
    context['order'] = order
    context['form'] = form
    return render(request, 'core/master/master_edit_order.html', context)

@receiver(post_save, sender=Employee)
def add_master_permissions(sender, instance, created, **kwargs):
    """Автоматически даёт права мастеру при создании Employee"""
    if created:
        # Получаем или создаём группу "Мастера"
        master_group, _ = Group.objects.get_or_create(name='Мастера')
        # Получаем нужные права
        permissions = Permission.objects.filter(
            codename__in=['can_change_order_status', 'can_edit_master_note']
        )
        # Добавляем права в группу
        master_group.permissions.add(*permissions)
        # Добавляем пользователя в группу
        instance.user.groups.add(master_group)
        user_logger.info(f"Master permissions assigned to user {instance.user.username} (Employee ID: {instance.id})")

################################# личный кабинет клиента ############

@receiver(post_save, sender=Client)
def add_client_permissions(sender, instance, created, **kwargs):
    if created:
        client_group, _ = Group.objects.get_or_create(name='Клиенты')
        permissions = Permission.objects.filter(
            codename__in=[
                'can_add_review',
                'can_edit_own_review',
                'can_delete_own_review',
                'can_create_order',
                'can_use_promocode',
            ]
        )
        client_group.permissions.add(*permissions)
        instance.user.groups.add(client_group)
        user_logger.info(f"Client permissions assigned to user {instance.user.username} (Client ID: {instance.id})")


@login_required
def client_dashboard(request):
    if not hasattr(request.user, 'client'):
        return redirect('core:home')
    
    client = request.user.client
    orders = Order.objects.filter(client=client)
    
    context = get_timezone_context()
    context.update({
        'client': client,
        'orders': orders,
        'discount': request.session.get('discount', 0),  # если нужно
    })
    return render(request, 'core/client/client_dashboard.html', context)

@login_required
def client_create_order(request):
    if not hasattr(request.user, 'client'):
        return redirect('core:home')
    if not request.user.has_perm('core.can_create_order'):
        raise PermissionDenied("У вас нет права создавать заказы")
    
    if request.method == 'POST':
        form = ClientOrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user.client
            order.status = 'new'
            order.save()  # ← сначала сохраняем заказ, чтобы появился pk
            form.save_m2m()  # ← потом сохраняем связи (device)
            user_logger.info(f"Client {request.user.username} created order #{order.order_number}")
            return redirect('core:client_add_items', order_id=order.id)
    else:
        form = ClientOrderForm(user=request.user)
    
    context = get_timezone_context()
    context['form'] = form
    return render(request, 'core/client/client_create_order.html', context)

@login_required
def client_add_items(request, order_id):
    if not hasattr(request.user, 'client'):
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id, client=request.user.client)
    
    if order.status != 'new':
        messages.error(request, 'Заказ уже в работе, нельзя изменить')
        return redirect('core:client_dashboard')
        
    service_form = OrderServiceForm(request.POST or None, prefix='service')
    spare_form = OrderSparePartForm(request.POST or None, prefix='spare')
    
    promo_message = None
    
    # Применение промокода
    if request.method == 'POST' and 'apply_promo' in request.POST:
        code = request.POST.get('promo_code', '')
        try:
            promocode = Promocode.objects.get(code=code, is_active=True)
            if not order.promocode:
                order.promocode = promocode
                order.save()
                order.update_total_cost()
                user_logger.info(f"Client {request.user.username} applied promo code '{code}' to order #{order.order_number}")
                promo_message = f'Промокод {code} применён! Скидка {promocode.discount_percent}%'
            else:
                promo_message = 'Промокод уже был применён'
        except Promocode.DoesNotExist:
            promo_message = 'Неверный или неактивный промокод'
        
        return redirect('core:client_add_items', order_id=order.id)
    
    # Удаление промокода
    if request.method == 'POST' and 'remove_promo' in request.POST:
        order.promocode = None
        order.update_total_cost()
        promo_message = 'Промокод удалён'
        user_logger.info(f"Client {request.user.username} removed promo code from order #{order.order_number}")
        return redirect('core:client_add_items', order_id=order.id)
    
    if request.method == 'POST':
        if 'add_service' in request.POST and service_form.is_valid():
            with transaction.atomic():
                order_service = service_form.save(commit=False)
                order_service.order = order
                order_service.price_at_time = order_service.service.price
                order_service.save()
                order.update_total_cost()
                user_logger.info(f"Client {request.user.username} added service '{order_service.service.name}' to order #{order.order_number}")
            return redirect('core:client_add_items', order_id=order.id)
        
        if 'add_spare' in request.POST and spare_form.is_valid():
            with transaction.atomic():
                order_spare = spare_form.save(commit=False)
                order_spare.order = order
                order_spare.price_at_time = order_spare.spare_part.price
                order_spare.save()
                order.update_total_cost()
                user_logger.info(f"Client {request.user.username} added spare part '{order_spare.spare_part.name}' to order #{order.order_number}")
            return redirect('core:client_add_items', order_id=order.id)
                
        if 'complete_order' in request.POST:
            order.status = 'new'  
            order.save()
            user_logger.info(f"Client {request.user.username} completed order #{order.order_number}")
            return redirect('core:client_order_summary', order_id=order.id)
    
    context = get_timezone_context()
    context.update({
        'order': order,
        'service_form': service_form,
        'spare_form': spare_form,
        'services': order.order_services.all(),
        'spare_parts': order.order_spare_parts.all(),
        'promo_message': promo_message,
        'final_cost': order.get_final_cost(),
    })
    return render(request, 'core/client/client_add_items.html', context)

@login_required
def client_remove_order_item(request, order_id, item_type, item_id):
    if not hasattr(request.user, 'client'):
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id, client=request.user.client)  # ← проверка на своего клиента
    
    if order.status != 'new':
        messages.error(request, 'Заказ уже оформлен, нельзя изменить')
        return redirect('core:client_dashboard')
    
    if item_type == 'service':
        OrderService.objects.filter(id=item_id, order=order).delete()
        user_logger.info(f"Client {request.user.username} removed service from order #{order.order_number}")
    elif item_type == 'spare':
        OrderSparePart.objects.filter(id=item_id, order=order).delete()
        user_logger.info(f"Client {request.user.username} removed spare part from order #{order.order_number}")
    
    order.update_total_cost()
    return redirect('core:client_add_items', order_id=order.id)


@login_required
def client_order_summary(request, order_id):
    if not hasattr(request.user, 'client'):
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id, client=request.user.client)  # ← проверка на своего клиента
    
    discount = request.session.get(f'discount_{order.id}', 0)
    total = order.total_cost
    if discount:
        total = total * (100 - discount) / 100
    
    context = get_timezone_context()
    context.update({
        'order': order,
        'services': order.order_services.all(),
        'spare_parts': order.order_spare_parts.all(),
        'discount': discount,
        'total_with_discount': total,
    })
    return render(request, 'core/client/client_order_summary.html', context)



####################################### админ панель №№№№№№№№№№№№№
@login_required
def admin_orders(request):
    """Страница управления заказами для администратора"""
    if not request.user.is_superuser:
        return redirect('core:home')
    
    orders = Order.objects.all().order_by('-created_at')
    
    # Поиск
    search = request.GET.get('search', '')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(client__full_name__icontains=search)
        )
    
    # Фильтр по статусу
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)
    
    # Пагинация
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = get_timezone_context()
    context.update({
        'orders': page_obj,
        'search': search,
        'status_filter': status,
        'status_choices': Order.STATUS_CHOICES,
    })
    return render(request, 'core/admin/admin_orders.html', context)


@login_required
def admin_order_detail(request, order_id):
    """Детальная страница заказа с возможностью редактирования"""
    if not request.user.is_superuser:
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id)
    
    # Формы для добавления услуг и запчастей
    service_form = OrderServiceForm(request.POST or None, prefix='service')
    spare_form = OrderSparePartForm(request.POST or None, prefix='spare')
    
    # Обновление статуса
    if request.method == 'POST' and 'update_status' in request.POST:
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            user_logger.info(f"Admin {request.user.username} changed status of order #{order.order_number} to {order.get_status_display()}")
            messages.success(request, 'Статус заказа обновлён')
        return redirect('core:admin_order_detail', order_id=order.id)
    
    # Добавление услуги
    if request.method == 'POST' and 'add_service' in request.POST:
        if service_form.is_valid():
            order_service = service_form.save(commit=False)
            order_service.order = order
            order_service.price_at_time = order_service.service.price
            order_service.save()
            order.update_total_cost()
            user_logger.info(f"Admin {request.user.username} added service to order #{order.order_number}")
            messages.success(request, 'Услуга добавлена')
        return redirect('core:admin_order_detail', order_id=order.id)
    
    # Добавление запчасти
    if request.method == 'POST' and 'add_spare' in request.POST:
        if spare_form.is_valid():
            order_spare = spare_form.save(commit=False)
            order_spare.order = order
            order_spare.price_at_time = order_spare.spare_part.price
            order_spare.save()
            order.update_total_cost()
            user_logger.info(f"Admin {request.user.username} added spare part to order #{order.order_number}")
            messages.success(request, 'Запчасть добавлена')
        return redirect('core:admin_order_detail', order_id=order.id)
    
    # Удаление услуги
    if request.method == 'POST' and 'delete_service' in request.POST:
        service_id = request.POST.get('service_id')
        OrderService.objects.filter(id=service_id, order=order).delete()
        order.update_total_cost()
        user_logger.info(f"Admin {request.user.username} removed service from order #{order.order_number}")
        messages.success(request, 'Услуга удалена')
        return redirect('core:admin_order_detail', order_id=order.id)
    
    # Удаление запчасти
    if request.method == 'POST' and 'delete_spare' in request.POST:
        spare_id = request.POST.get('spare_id')
        OrderSparePart.objects.filter(id=spare_id, order=order).delete()
        order.update_total_cost()
        messages.success(request, 'Запчасть удалена')
        user_logger.info(f"Admin {request.user.username} removed spare part from order #{order.order_number}")
        return redirect('core:admin_order_detail', order_id=order.id)
    
    # Удаление всего заказа
    if request.method == 'POST' and 'delete_order' in request.POST:
        order.delete()
        messages.success(request, 'Заказ удалён')
        user_logger.info(f"Admin {request.user.username} deleted order #{order.order_number}")
        return redirect('core:admin_orders')
    
    context = get_timezone_context()
    context.update({
        'order': order,
        'services': order.order_services.all(),
        'spare_parts': order.order_spare_parts.all(),
        'service_form': service_form,
        'spare_form': spare_form,
        'status_choices': Order.STATUS_CHOICES,
    })
    return render(request, 'core/admin/admin_order_detail.html', context)

@login_required
def admin_order_create(request):
    """Создание нового заказа администратором"""
    if not request.user.is_superuser:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AdminOrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Если адрес не заполнен, берём адрес клиента
            if not order.address and order.client.address:
                order.address = order.client.address
            order.save()
            user_logger.info(f"Admin {request.user.username} created order #{order.order_number}")
            messages.success(request, f'Заказ №{order.order_number} успешно создан')
            return redirect('core:admin_order_detail', order_id=order.id)
    else:
        # Предзаполняем начальные данные
        initial = {}
        if 'client_id' in request.GET:
            initial['client'] = request.GET.get('client_id')
        if 'device_id' in request.GET:
            initial['device'] = request.GET.get('device_id')
        form = AdminOrderCreateForm(initial=initial)
    
    context = get_timezone_context()
    context['form'] = form
    return render(request, 'core/admin/admin_order_create.html', context)



