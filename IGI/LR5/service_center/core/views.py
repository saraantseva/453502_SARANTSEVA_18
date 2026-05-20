from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import RegisterForm
from core.models import News, CompanyInfo, Glossary, Employee, Vacancy, Promocode, Client, Service, ServiceType,Order
from .utils import get_timezone_context, utc_to_local 

from django.core.exceptions import PermissionDenied
from django.db import models

from .forms import ReviewForm
from .models import Review

def home(request):
    context = get_timezone_context()
    context['last_news'] = News.objects.first()
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
    context['terms'] = Glossary.objects.all().order_by('-created_at')
    return render(request, 'core/glossary.html', context)

def contacts(request):
    context = get_timezone_context()
    context['employees'] = Employee.objects.all()
    return render(request, 'core/contacts.html', context)

def privacy(request):
    context = get_timezone_context()
    return render(request, 'core/privacy.html', context)

def vacancies(request):
    context = get_timezone_context()
    context['vacancies'] = Vacancy.objects.filter(is_active=True)
    return render(request, 'core/vacancies.html', context)

def promocodes(request):
    context = get_timezone_context()
    context['active_promocodes'] = Promocode.objects.filter(is_active=True)
    context['archived_promocodes'] = Promocode.objects.filter(is_active=False)
    return render(request, 'core/promocodes.html', context)

def reviews(request):
    context = get_timezone_context()
    return render(request, 'core/reviews.html', context)

def register(request):
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
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = get_timezone_context()
    context['form'] = form
    return render(request, 'registration/register.html', context)

class CustomLoginView(LoginView):
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



def service_list(request):
    services = Service.objects.all()
    
    # 1. ПОИСК по названию
    search_query = request.GET.get('search', '')
    if search_query:
        services = services.filter(name__icontains=search_query)
    
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
    return render(request, 'core/master_dashboard.html', context)

from .forms import OrderEditForm

@login_required
def master_edit_order(request, order_id):
    if not hasattr(request.user, 'employee'):
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id, employee=request.user.employee)
    
    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Заказ №{order.order_number} успешно обновлён')
            return redirect('core:master_dashboard')
    else:
        form = OrderEditForm(instance=order)
    
    context = get_timezone_context()
    context['order'] = order
    context['form'] = form
    return render(request, 'core/master_edit_order.html', context)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
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
        return redirect('core:reviews')
    
    context = get_timezone_context()
    context['review'] = review
    return render(request, 'core/review_confirm_delete.html', context)


from django.db import transaction
from .forms import ClientOrderForm, OrderServiceForm, OrderSparePartForm, PromocodeApplyForm

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
    return render(request, 'core/client_dashboard.html', context)
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
            return redirect('core:client_add_items', order_id=order.id)
    else:
        form = ClientOrderForm(user=request.user)
    
    context = get_timezone_context()
    context['form'] = form
    return render(request, 'core/client_create_order.html', context)

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
                order.update_total_cost()
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
        return redirect('core:client_add_items', order_id=order.id)
    
    if request.method == 'POST':
        if 'add_service' in request.POST and service_form.is_valid():
            with transaction.atomic():
                order_service = service_form.save(commit=False)
                order_service.order = order
                order_service.price_at_time = order_service.service.price
                order_service.save()
                order.update_total_cost()
            return redirect('core:client_add_items', order_id=order.id)
        
        if 'add_spare' in request.POST and spare_form.is_valid():
            with transaction.atomic():
                order_spare = spare_form.save(commit=False)
                order_spare.order = order
                order_spare.price_at_time = order_spare.spare_part.price
                order_spare.save()
                order.update_total_cost()
            return redirect('core:client_add_items', order_id=order.id)
                
        if 'complete_order' in request.POST:
            order.status = 'new'  
            order.save()
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
    return render(request, 'core/client_add_items.html', context)

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
    elif item_type == 'spare':
        OrderSparePart.objects.filter(id=item_id, order=order).delete()
    
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
    return render(request, 'core/client_order_summary.html', context)

from .models import OrderSparePart, OrderService
