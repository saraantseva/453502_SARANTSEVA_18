# core/middleware.py
import time
import logging
from .logger_config import setup_logging

# Инициализируем логгер
loggers = setup_logging()
request_logger = loggers['request']
debug_logger = loggers['debug']

class RequestLogMiddleware:
    """Middleware для логирования всех входящих запросов"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Логируем начало запроса (только в DEBUG режиме)
        start_time = time.time()
        
        # Обрабатываем запрос
        response = self.get_response(request)
        
        # Вычисляем время выполнения
        duration = (time.time() - start_time) * 1000
        
        # Логируем информацию о запросе
        log_msg = f"{request.method} {request.get_full_path()} | User: {request.user.username if request.user.is_authenticated else 'Anonymous'} | Status: {response.status_code} | Duration: {duration:.0f}ms"
        
        # Уровень логирования зависит от статуса ответа
        if response.status_code >= 500:
            request_logger.error(log_msg)
        elif response.status_code >= 400:
            request_logger.warning(log_msg)
        else:
            request_logger.info(log_msg)
        
        # Детальное логирование в DEBUG режиме
        debug_logger.debug(f"REQUEST: {request.method} {request.get_full_path()}")
        debug_logger.debug(f"USER: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        
        return response