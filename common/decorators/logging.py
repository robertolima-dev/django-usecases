import time
from functools import wraps


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
