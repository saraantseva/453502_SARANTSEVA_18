# core/logger_config.py
import logging
import os
from logging.handlers import RotatingFileHandler
from django.conf import settings

log_dir = os.path.join(settings.BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    
def setup_logging():
    """
    Настройка логирования с уровнем из конфигурации приложения
    Уровень логирования берётся из settings.LOG_LEVEL
    """
    
    # Создаём папку для логов, если её нет
    log_dir = os.path.join(settings.BASE_DIR, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Берём уровень логирования из настроек (по умолчанию INFO)
    log_level_str = getattr(settings, 'LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Формат для всех логов
    log_format = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # === 1. Логирование действий пользователей ===
    user_logger = logging.getLogger('user_actions')
    user_logger.setLevel(log_level)
    
    user_handler = RotatingFileHandler(
        os.path.join(log_dir, 'user_actions.log'),
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    user_formatter = logging.Formatter(log_format, date_format)
    user_handler.setFormatter(user_formatter)
    user_logger.addHandler(user_handler)

    # === 2. Логирование ошибок ===
    error_logger = logging.getLogger('errors')
    error_logger.setLevel(logging.ERROR)  # Ошибки всегда пишем
    
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    error_formatter = logging.Formatter(log_format, date_format)
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)

    # === 3. Логирование всех запросов (Middleware) ===
    request_logger = logging.getLogger('requests')
    request_logger.setLevel(log_level)
    
    request_handler = RotatingFileHandler(
        os.path.join(log_dir, 'requests.log'),
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    request_formatter = logging.Formatter(
        '%(asctime)s | %(message)s',
        date_format
    )
    request_handler.setFormatter(request_formatter)
    request_logger.addHandler(request_handler)
    
    # === 4. Отладочный логгер (для DEBUG) ===
    debug_logger = logging.getLogger('debug')
    debug_logger.setLevel(logging.DEBUG)
    
    debug_handler = RotatingFileHandler(
        os.path.join(log_dir, 'debug.log'),
        maxBytes=5*1024*1024,
        backupCount=2,
        encoding='utf-8'
    )
    debug_formatter = logging.Formatter(log_format, date_format)
    debug_handler.setFormatter(debug_formatter)
    debug_logger.addHandler(debug_handler)
    
    # === 5. Консольный вывод (только если DEBUG=True) ===
    if settings.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            '%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # Добавляем консоль для всех логгеров
        user_logger.addHandler(console_handler)
        error_logger.addHandler(console_handler)
        debug_logger.addHandler(console_handler)
    
    # Подавляем лишние логи от сторонних библиотек
    logging.getLogger('django.request').setLevel(logging.WARNING)
    logging.getLogger('django.server').setLevel(logging.WARNING)
    
    return {
        'user': user_logger,
        'error': error_logger,
        'request': request_logger,
        'debug': debug_logger,
    }