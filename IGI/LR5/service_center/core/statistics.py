import statistics
from django.db.models import Sum, Count
from .models import Order, Client, OrderService
from datetime import date
from collections import Counter

def clients_alphabetical():
    """Список клиентов в алфавитном порядке и общая сумма продаж по каждому"""
    clients = Client.objects.all().order_by('full_name')
    result = []
    total_sales_sum = 0
    for client in clients:
        total = Order.objects.filter(client=client).aggregate(total=Sum('total_cost'))['total'] or 0
        total_sales_sum += total
        result.append({
            'name': client.full_name,
            'total': total
        })
    return result, total_sales_sum

def order_amount_stats():
    """Среднее, мода, медиана по суммам заказов"""
    amounts = list(Order.objects.values_list('total_cost', flat=True))
    if not amounts:
        return None, None, None
    avg = sum(amounts) / len(amounts)
    # мода (наиболее часто встречающееся значение)
    mode = None
    if amounts:
        counter = Counter(amounts)
        mode = counter.most_common(1)[0][0]
    median = statistics.median(amounts)
    return avg, mode, median

def client_age_stats():
    """Средний и медианный возраст клиентов (только с датой рождения)"""
    ages = []
    for client in Client.objects.all():
        if client.birth_date:
            today = date.today()
            age = today.year - client.birth_date.year - ((today.month, today.day) < (client.birth_date.month, client.birth_date.day))
            ages.append(age)
    if not ages:
        return None, None
    avg_age = sum(ages) / len(ages)
    median_age = statistics.median(ages)
    return avg_age, median_age

def most_popular_service_type():
    """Тип услуг, который встречается чаще всего в заказах"""
    # считаем через OrderService (каждая услуга, добавленная в заказ)
    service_type_count = {}
    for order_service in OrderService.objects.all():
        st = order_service.service.service_type
        if st:
            service_type_count[st.name] = service_type_count.get(st.name, 0) + 1
    if not service_type_count:
        return None
    return max(service_type_count, key=service_type_count.get)

def most_profitable_service_type():
    """Тип услуг, приносящий наибольшую прибыль (сумма price_at_time * quantity)"""
    profit = {}
    for order_service in OrderService.objects.all():
        st = order_service.service.service_type
        if st:
            amount = order_service.price_at_time * order_service.quantity
            profit[st.name] = profit.get(st.name, 0) + amount
    if not profit:
        return None
    return max(profit, key=profit.get)

def orders_by_month():
    """Количество заказов по месяцам (для графика)"""
    from django.db.models.functions import TruncMonth
    monthly = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    return [(item['month'].strftime('%Y-%m'), item['count']) for item in monthly if item['month']]


def orders_by_month():
    """Количество заказов по месяцам (для линейного графика)"""
    from django.db.models.functions import TruncMonth
    monthly = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    
    result = []
    for item in monthly:
        if item['month']:
            month_name_ru = item['month'].strftime('%B %Y')
            result.append({
                'month': month_name_ru,
                'count': item['count'],
                'sort_key': item['month']
            })
    return sorted(result, key=lambda x: x['sort_key'])

def order_status_distribution():
    """Распределение заказов по статусам (для круговой диаграммы)"""
    status_counts = {}
    for status_code, status_name in Order.STATUS_CHOICES:
        count = Order.objects.filter(status=status_code).count()
        if count > 0:
            status_counts[status_name] = count
    return status_counts