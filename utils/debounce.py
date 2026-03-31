import json
import time
from django.http import JsonResponse

# 用于防抖的缓存
debounce_cache = {}

def debounce(seconds=1):
    """
    防抖装饰器
    :param seconds: 防抖时间窗口（秒）
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                data = json.loads(request.body)
                open_id = data.get('open_id')
                if open_id:
                    current_time = time.time()
                    if open_id in debounce_cache:
                        last_time = debounce_cache[open_id]
                        if current_time - last_time < seconds:
                            return JsonResponse({
                                'code': 429,
                                'message': f'open_id请求过于频繁，请稍后再试，当前防抖时间窗口：{seconds}秒',
                                'data': None
                            }, status=429)
                    debounce_cache[open_id] = current_time
            except json.JSONDecodeError:
                pass
            return func(request, *args, **kwargs)
        return wrapper
    return decorator



