from datetime import datetime, date
from calendar import monthcalendar
from zoneinfo import ZoneInfo
from django.utils import timezone
import requests

from django.utils import timezone
import pytz

def utc_to_local(dt):
    """Переводит UTC в локальное время (по времени сервера)"""
    if dt is None:
        return None
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.utc)
    # перевод в локальное время сервера
    return dt.astimezone()

def get_timezone_context():
    tz = timezone.get_current_timezone()
    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc)

    today = date.today()
    cal = monthcalendar(today.year, today.month)
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    calendar_lines = []
    calendar_lines.append(' '.join(weekdays))
    for week in cal:
        week_str = []
        for day in week:
            if day == 0:
                week_str.append('  ')
            elif day == today.day:
                week_str.append(f'*{day:2}')
            else:
                week_str.append(f'{day:2}')
        calendar_lines.append(' '.join(week_str))

    offset = now_local.utcoffset()
    offset_hours = int(offset.total_seconds() // 3600)
    offset_str = f'UTC{offset_hours:+d}'

    return {
        'user_timezone': f'{tz.key} ({offset_str})',
        'current_user_time': now_local.strftime('%d/%m/%Y %H:%M:%S'),
        'current_utc_time': now_utc.strftime('%d/%m/%Y %H:%M:%S'),
        'calendar_text': '\n'.join(calendar_lines),
        'calendar_month': today.strftime('%B %Y'),
    }

def get_tech_news():
    """Получает заголовок последней новости с Hacker News"""
    try:
        # гет ID последней новости
        response = requests.get('https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty', timeout=5)
        if response.status_code == 200:
            news_ids = response.json()
            # самая свежая новость
            news_item = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{news_ids[0]}.json?print=pretty', timeout=5)
            if news_item.status_code == 200:
                return news_item.json().get('title', 'Новостей пока нет')
    except:
        pass
    return 'Технологии не стоят на месте! Будьте в курсе!'

def get_nasa_apod():
    """Получает фото космоса от NASA APOD"""
    try:
        url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'url': data.get('url', ''),
                'title': data.get('title', 'Космическое фото'),
                'explanation': data.get('explanation', '')[:150] + '...'
            }
    except:
        pass
    return None

from django.core.cache import cache

def get_nasa_apod_cached():
    nasa = cache.get('nasa_apod')
    if nasa:
        return nasa
    
    try:
        url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            nasa = {
                'url': data.get('url', ''),
                'title': data.get('title', 'Космическое фото'),
                'explanation': data.get('explanation', '')[:150] + '...'
            }
            cache.set('nasa_apod', nasa, 3600)  # кэш на 1 час
            return nasa
    except:
        pass
    return None

