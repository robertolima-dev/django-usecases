import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def log_task_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_name = func.__name__
        print(f"🚀 Iniciando task: {task_name}")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            print(f"✅ Finalizou task: {task_name} em {duration:.2f} segundos")
            return result
        except Exception as e:
            print(f"❌ Erro na task: {task_name} | Erro: {str(e)}")
            raise e
    return wrapper


def log_api_execution(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        start = time.perf_counter()
        response = func(request, *args, **kwargs)
        duration = time.perf_counter() - start
        logger.info(f"⏱ Tempo de execução: {duration:.4f} segundos | {request.path}")  # noqa: E501
        return response
    return wrapper
