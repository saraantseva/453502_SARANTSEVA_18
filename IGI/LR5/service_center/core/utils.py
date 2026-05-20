from datetime import datetime, date
from calendar import monthcalendar
from zoneinfo import ZoneInfo
from django.utils import timezone

def utc_to_local(dt):
    if dt is None:
        return None
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.utc)
    return dt.astimezone(ZoneInfo('Europe/Minsk'))


def get_timezone_context():
    """Возвращает словарь с временем, часовым поясом и календарём для всех страниц."""
    tz = ZoneInfo('Europe/Minsk')
    now_utc = datetime.now(ZoneInfo('UTC'))
    now_local = now_utc.astimezone(tz)

    today = date.today()
    cal = monthcalendar(today.year, today.month)
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    # Текстовый календарь с выделением текущего дня (звёздочкой)
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

    return {
        'user_timezone': 'Europe/Minsk',
        'current_user_time': now_local.strftime('%d/%m/%Y %H:%M:%S'),
        'current_utc_time': now_utc.strftime('%d/%m/%Y %H:%M:%S'),
        'calendar_text': '\n'.join(calendar_lines),
        'calendar_month': today.strftime('%B %Y'),
    }