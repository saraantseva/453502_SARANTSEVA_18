from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from datetime import date
from unittest.mock import patch, Mock
import pytest

from core.models import (
    Client, Employee, Specialization, ServiceType, Service,
    SparePartType, SparePart, DeviceType, Device, Order,
    Promocode, News, CompanyInfo, Glossary, Vacancy, Review,
    OrderService, OrderSparePart
)
from core.forms import (
    RegisterForm, ReviewForm, ClientOrderForm,
    OrderServiceForm, OrderSparePartForm, AdminOrderCreateForm
)
from core.utils import (
    utc_to_local, get_timezone_context, get_tech_news, get_nasa_apod
)
from core.statistics import (
    clients_alphabetical, order_amount_stats, client_age_stats,
    most_popular_service_type, most_profitable_service_type,
    orders_by_month, order_status_distribution
)


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        cls.specialization = Specialization.objects.create(name='Ремонт ПК')
        cls.client_obj = Client.objects.create(
            user=cls.user,
            full_name='Иван Петров',
            phone='+375 (29) 123-45-67',
            birth_date='1990-05-20',
            address='ул. Нёманская, 25'
        )
        cls.employee = Employee.objects.create(
            user=cls.user,
            full_name='Сергей Мастер',
            phone='+375 (29) 111-22-33',
            birth_date='1985-10-10',
            salary=1500.00
        )
        cls.employee.specialization.add(cls.specialization)

    def test_client_creation(self):
        self.assertEqual(str(self.client_obj), 'Клиент: Иван Петров')

    def test_client_age_validation(self):
        young_client = Client(
            user=self.user,
            full_name='Юный Клиент',
            phone='+375 (29) 123-45-68',
            birth_date=date.today().replace(year=date.today().year - 17)
        )
        with self.assertRaises(ValidationError):
            young_client.full_clean()

    def test_employee_creation(self):
        self.assertEqual(str(self.employee), 'Сотрудник: Сергей Мастер')

    def test_employee_age_validation(self):
        young_emp = Employee(
            user=self.user,
            full_name='Юный Мастер',
            phone='+375 (29) 111-22-34',
            birth_date=date.today().replace(year=date.today().year - 16),
            salary=1000
        )
        with self.assertRaises(ValidationError):
            young_emp.full_clean()

    def test_specialization_str(self):
        self.assertEqual(str(self.specialization), 'Ремонт ПК')

    def test_service_creation(self):
        s_type = ServiceType.objects.create(name='Диагностика')
        service = Service.objects.create(
            service_type=s_type,
            name='Диагностика ноутбука',
            price=500.00,
            duration_days=1
        )
        self.assertEqual(str(service), 'Диагностика ноутбука - 500.00 y.e.')

    def test_spare_part_creation(self):
        part_type = SparePartType.objects.create(name='Оперативная память')
        part = SparePart.objects.create(
            part_type=part_type,
            name='DDR4 8GB',
            price=2500.00,
            quantity_in_stock=10
        )
        self.assertEqual(str(part), 'DDR4 8GB - 2500.00 руб. (в наличии: 10)')

    def test_device_creation(self):
        dev_type = DeviceType.objects.create(name='Ноутбук')
        device = Device.objects.create(
            device_type=dev_type,
            client=self.client_obj,
            brand='Dell',
            model='XPS 15'
        )
        self.assertEqual(str(device), f'Dell XPS 15 - {self.client_obj.full_name}')

    def test_order_creation(self):
        dev_type = DeviceType.objects.create(name='Ноутбук')
        device = Device.objects.create(
            device_type=dev_type,
            client=self.client_obj,
            brand='HP',
            model='Pavilion'
        )
        order = Order.objects.create(
            client=self.client_obj,
            device=device,
            employee=self.employee,
            client_problem='Не включается'
        )
        self.assertIsNotNone(order.order_number)

    def test_promocode_str(self):
        promocode = Promocode.objects.create(
            code='TEST10',
            discount_percent=10,
            is_active=True,
            expires_at=date.today()
        )
        self.assertIn('TEST10 - 10% (Действует)', str(promocode))

    def test_news_creation(self):
        news = News.objects.create(
            title='Тест новость',
            short_description='Кратко',
            content='Полный текст',
            is_published=True
        )
        self.assertEqual(str(news), 'Тест новость')

    def test_glossary_creation(self):
        term = Glossary.objects.create(term='Вопрос', definition='Ответ')
        self.assertEqual(str(term), 'Вопрос')

    def test_vacancy_creation(self):
        vacancy = Vacancy.objects.create(
            title='Мастер',
            description='Ремонт ПК',
            is_active=True
        )
        self.assertEqual(str(vacancy), 'Мастер')

    def test_review_creation(self):
        review = Review.objects.create(
            user=self.user,
            rating=5,
            text='Отлично!'
        )
        self.assertIn('Отзыв от testuser — 5★', str(review))


class FormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service_type = ServiceType.objects.create(name='Диагностика')
        cls.service = Service.objects.create(
            service_type=cls.service_type,
            name='Диагностика',
            price=500.00,
            duration_days=1
        )
        cls.spare_type = SparePartType.objects.create(name='ОЗУ')
        cls.spare = SparePart.objects.create(
            part_type=cls.spare_type,
            name='DDR4 8GB',
            price=2500.00,
            quantity_in_stock=5
        )

    def test_register_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@mail.ru',
            'full_name': 'Новый Клиент',
            'phone': '+375 (29) 123-45-67',
            'birth_date': '1990-01-01',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_age(self):
        form_data = {
            'username': 'younguser',
            'email': 'young@mail.ru',
            'full_name': 'Молодой Клиент',
            'phone': '+375 (29) 123-45-67',
            'birth_date': '2010-01-01',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

    def test_review_form_valid(self):
        form_data = {'rating': 5, 'text': 'Отлично!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_service_form_valid(self):
        form = OrderServiceForm(data={'service': self.service.id, 'quantity': 2})
        self.assertTrue(form.is_valid())

    def test_order_spare_part_form_valid(self):
        form = OrderSparePartForm(data={'spare_part': self.spare.id, 'quantity': 1})
        self.assertTrue(form.is_valid())


class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='123')
        cls.client_user = Client.objects.create(
            user=cls.user,
            full_name='Клиент',
            phone='+375 (29) 123-45-67',
            birth_date='1990-01-01'
        )
        cls.employee_user = User.objects.create_user(username='master', password='123')
        cls.employee = Employee.objects.create(
            user=cls.employee_user,
            full_name='Мастер',
            phone='+375 (29) 111-22-33',
            birth_date='1985-01-01',
            salary=2000
        )
        cls.superuser = User.objects.create_superuser(username='admin', password='123')
        cls.device_type = DeviceType.objects.create(name='Ноутбук')
        cls.device = Device.objects.create(
            device_type=cls.device_type,
            client=cls.client_user,
            brand='Lenovo',
            model='ThinkPad'
        )
        cls.order = Order.objects.create(
            client=cls.client_user,
            device=cls.device,
            employee=cls.employee,
            client_problem='Тестовая проблема'
        )
        cls.service_type = ServiceType.objects.create(name='Диагностика')
        cls.service = Service.objects.create(
            service_type=cls.service_type,
            name='Диагностика',
            price=500.00,
            duration_days=1
        )

    def test_home_page(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

    def test_news_list(self):
        response = self.client.get(reverse('core:news_list'))
        self.assertEqual(response.status_code, 200)

    def test_news_detail(self):
        news = News.objects.create(title='Test', short_description='Desc', content='Content')
        response = self.client.get(reverse('core:news_detail', args=[news.id]))
        self.assertEqual(response.status_code, 200)

    def test_services_list(self):
        response = self.client.get(reverse('core:service_list'))
        self.assertEqual(response.status_code, 200)

    def test_services_list_search(self):
        response = self.client.get(reverse('core:service_list'), {'search': 'диагностика'})
        self.assertEqual(response.status_code, 200)

    def test_services_list_filter(self):
        response = self.client.get(reverse('core:service_list'), {'type': self.service_type.id})
        self.assertEqual(response.status_code, 200)

    def test_services_list_sort(self):
        response = self.client.get(reverse('core:service_list'), {'sort': 'price_asc'})
        self.assertEqual(response.status_code, 200)

    def test_glossary_page(self):
        response = self.client.get(reverse('core:glossary'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page(self):
        response = self.client.get(reverse('core:contacts'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_page(self):
        response = self.client.get(reverse('core:privacy'))
        self.assertEqual(response.status_code, 200)

    def test_vacancies_page(self):
        response = self.client.get(reverse('core:vacancies'))
        self.assertEqual(response.status_code, 200)

    def test_promocodes_page(self):
        response = self.client.get(reverse('core:promocodes'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_page(self):
        response = self.client.get(reverse('core:reviews'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('core:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_client_dashboard_requires_login(self):
        response = self.client.get(reverse('core:client_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_client_dashboard_authenticated(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:client_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_client_create_order(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:client_create_order'))
        self.assertEqual(response.status_code, 200)

    def test_client_create_order_post(self):
        self.client.login(username='user', password='123')
        device = Device.objects.create(
            device_type=self.device_type,
            client=self.client_user,
            brand='Test',
            model='TestModel'
        )
        response = self.client.post(reverse('core:client_create_order'), {
            'device': device.id,
            'client_problem': 'Тестовая проблема'
        })
        self.assertEqual(response.status_code, 302)

    def test_client_add_items(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:client_add_items', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

    def test_client_order_summary(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:client_order_summary', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

    def test_master_dashboard_requires_login(self):
        response = self.client.get(reverse('core:master_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_master_dashboard_authenticated(self):
        self.client.login(username='master', password='123')
        response = self.client.get(reverse('core:master_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_master_edit_order(self):
        self.client.login(username='master', password='123')
        response = self.client.get(reverse('core:master_edit_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

    def test_admin_orders_superuser(self):
        self.client.login(username='admin', password='123')
        response = self.client.get(reverse('core:admin_orders'))
        self.assertEqual(response.status_code, 200)

    def test_admin_orders_regular_user(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:admin_orders'))
        self.assertEqual(response.status_code, 302)

    def test_admin_order_detail(self):
        self.client.login(username='admin', password='123')
        response = self.client.get(reverse('core:admin_order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)

    def test_admin_order_create(self):
        self.client.login(username='admin', password='123')
        response = self.client.get(reverse('core:admin_order_create'))
        self.assertEqual(response.status_code, 200)

    def test_review_add_authenticated(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:review_add'))
        self.assertEqual(response.status_code, 200)

    def test_review_add_post(self):
        self.client.login(username='user', password='123')
        response = self.client.post(reverse('core:review_add'), {
            'rating': 5,
            'text': 'Отличный сервис!'
        })
        self.assertEqual(response.status_code, 302)

    def test_review_edit(self):
        review = Review.objects.create(user=self.user, rating=5, text='Test')
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:review_edit', args=[review.id]))
        self.assertEqual(response.status_code, 200)

    def test_review_delete(self):
        review = Review.objects.create(user=self.user, rating=5, text='Test')
        self.client.login(username='user', password='123')
        response = self.client.post(reverse('core:review_delete', args=[review.id]))
        self.assertEqual(response.status_code, 302)

    def test_statistics_page_superuser(self):
        self.client.login(username='admin', password='123')
        response = self.client.get(reverse('core:statistics'))
        self.assertEqual(response.status_code, 200)

    def test_statistics_page_regular_user(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('core:statistics'))
        self.assertEqual(response.status_code, 200)


class UtilsTest(TestCase):
    def test_utc_to_local_conversion(self):
        now_utc = timezone.now()
        local = utc_to_local(now_utc)
        self.assertIsNotNone(local)

    def test_timezone_context_returns_dict(self):
        context = get_timezone_context()
        self.assertIn('user_timezone', context)
        self.assertIn('current_user_time', context)
        self.assertIn('current_utc_time', context)
        self.assertIn('calendar_text', context)
        self.assertIn('calendar_month', context)

    @patch('core.utils.requests.get')
    def test_get_tech_news_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [[12345], {'title': 'Test News'}]
        result = get_tech_news()
        self.assertIsNotNone(result)

    @patch('core.utils.requests.get')
    def test_get_tech_news_failure(self, mock_get):
        mock_get.side_effect = Exception('API error')
        result = get_tech_news()
        self.assertEqual(result, 'Технологии не стоят на месте! Будьте в курсе!')

    @patch('core.utils.requests.get')
    def test_get_nasa_apod_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'url': 'http://example.com/photo.jpg',
            'title': 'Test Photo',
            'explanation': 'Test explanation'
        }
        result = get_nasa_apod()
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], 'Test Photo')

    @patch('core.utils.requests.get')
    def test_get_nasa_apod_failure(self, mock_get):
        mock_get.side_effect = Exception('API error')
        result = get_nasa_apod()
        self.assertIsNone(result)


class StatisticsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='stat', password='123')
        cls.client = Client.objects.create(
            user=cls.user,
            full_name='Стат Клиент',
            phone='+375 (29) 123-45-67',
            birth_date='1990-01-01'
        )
        cls.device_type = DeviceType.objects.create(name='Ноутбук')
        cls.device = Device.objects.create(
            device_type=cls.device_type,
            client=cls.client,
            brand='Acer',
            model='Aspire'
        )
        cls.order = Order.objects.create(client=cls.client, device=cls.device, total_cost=5000)

    def test_clients_alphabetical(self):
        clients, total = clients_alphabetical()
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0]['name'], 'Стат Клиент')
        self.assertGreater(total, 0)

    def test_order_amount_stats(self):
        avg, mode, median = order_amount_stats()
        self.assertEqual(avg, 5000)
        self.assertEqual(mode, 5000)
        self.assertEqual(median, 5000)

    def test_client_age_stats(self):
        avg_age, median_age = client_age_stats()
        self.assertIsNotNone(avg_age)
        self.assertIsNotNone(median_age)

    def test_most_popular_service_type(self):
        result = most_popular_service_type()
        self.assertTrue(result is None or isinstance(result, str))

    def test_most_profitable_service_type(self):
        result = most_profitable_service_type()
        self.assertTrue(result is None or isinstance(result, str))

    def test_orders_by_month(self):
        result = orders_by_month()
        self.assertIsInstance(result, list)

    def test_order_status_distribution(self):
        result = order_status_distribution()
        self.assertIsInstance(result, dict)


class SignalTest(TestCase):
    def test_employee_creation_adds_permissions(self):
        user = User.objects.create_user(username='master_signal', password='123')
        Employee.objects.create(
            user=user,
            full_name='Мастер Сигнал',
            phone='+375 (29) 111-22-33',
            birth_date='1980-01-01',
            salary=2000
        )
        group = Group.objects.filter(name='Мастера').first()
        self.assertIsNotNone(group)
        self.assertIn(group, user.groups.all())

    def test_client_creation_adds_permissions(self):
        user = User.objects.create_user(username='client_signal', password='123')
        Client.objects.create(
            user=user,
            full_name='Клиент Сигнал',
            phone='+375 (29) 123-45-67',
            birth_date='1995-01-01'
        )
        group = Group.objects.filter(name='Клиенты').first()
        self.assertIsNotNone(group)
        self.assertIn(group, user.groups.all())


@pytest.mark.parametrize('name,age,valid', [
    ('Иван', 25, True),
    ('Петр', 17, False),
    ('Сидор', 18, True),
])
def test_client_age_parametrized(db, name, age, valid):
    user = User.objects.create_user(username=name, password='123')
    birth = date.today().replace(year=date.today().year - age)
    client = Client(user=user, full_name=name, phone='+375 (29) 123-45-67', birth_date=birth)
    if valid:
        client.full_clean()
        client.save()
        assert client.age == age
    else:
        with pytest.raises(ValidationError):
            client.full_clean()