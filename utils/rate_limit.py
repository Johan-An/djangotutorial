import json
import time
from django.http import JsonResponse

# 用于限流的缓存
rate_limit_cache = {
    'ip': {},  # IP限流
    'open_id': {}  # open_id限流
}

def rate_limit(ip_rate='5/m', open_id_rate='3/m'):
    """
    限流装饰器
    :param ip_rate: IP限流规则，如 '5/m' 表示每分钟5次
    :param open_id_rate: open_id限流规则，如 '3/m' 表示每分钟3次
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            # 清理过期的限流记录
            current_time = time.time()
            for key, records in rate_limit_cache['ip'].items():
                rate_limit_cache['ip'][key] = [t for t in records if current_time - t < 60]
            for key, records in rate_limit_cache['open_id'].items():
                rate_limit_cache['open_id'][key] = [t for t in records if current_time - t < 60]

            # IP限流
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            if client_ip not in rate_limit_cache['ip']:
                rate_limit_cache['ip'][client_ip] = []
            rate_limit_cache['ip'][client_ip].append(current_time)
            if len(rate_limit_cache['ip'][client_ip]) > int(ip_rate.split('/')[0]):
                return JsonResponse({
                    'code': 429,
                    'message': f'IP请求过于频繁，请稍后再试，当前限流规则：{ip_rate}',
                    'data': None
                }, status=429)

            # open_id限流
            try:
                data = json.loads(request.body)
                open_id = data.get('open_id')
                if open_id:
                    if open_id not in rate_limit_cache['open_id']:
                        rate_limit_cache['open_id'][open_id] = []
                    rate_limit_cache['open_id'][open_id].append(current_time)
                    if len(rate_limit_cache['open_id'][open_id]) > int(open_id_rate.split('/')[0]):
                        return JsonResponse({
                            'code': 429,
                            'message': f'open_id请求过于频繁，请稍后再试，当前限流规则：{open_id_rate}',
                            'data': None
                        }, status=429)
            except json.JSONDecodeError:
                pass

            return func(request, *args, **kwargs)
        return wrapper
    return decorator