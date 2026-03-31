import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import LoginForm
from .services import LoginService
from utils.debounce import debounce
from utils.rate_limit import rate_limit


def index(request):
    return JsonResponse({"message": "Hello, world. You're at the members index."})


def agreement(request):
    return JsonResponse({"message": "Hello, world. You're at the members agreement."})


@csrf_exempt
@require_http_methods(["POST"])
@debounce(seconds=1)  # 1秒内防抖
@rate_limit(ip_rate='5/m', open_id_rate='3/m')  # IP限流每分钟5次，open_id限流每分钟3次

def login(request):
    try:
        data = json.loads(request.body)
        form = LoginForm(data=data)

        if not form.is_valid():
            return JsonResponse({
                'code': 400,
                'message': list(form.errors.values())[0][0],
                'data': None
            }, status=400)

        open_id = form.cleaned_data['open_id']
        union_id = form.cleaned_data['union_id']

        member = LoginService.authenticate(open_id, union_id)
        if not member:
            return JsonResponse({
                'code': 401,
                'message': '登录失败，用户不存在',
                'data': None
            }, status=401)

        tokens = LoginService.generate_tokens(member)
        user_info = LoginService.get_user_info(member)

        return JsonResponse({
            'code': 200,
            'message': '登录成功',
            'data': {
                **tokens,
                'user': user_info
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'code': 400,
            'message': '无效的JSON格式',
            'data': None
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器内部错误: {str(e)}',
            'data': None
        }, status=500)
