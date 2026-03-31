from rest_framework_simplejwt.tokens import RefreshToken
from .models import Member


class LoginService:
    @staticmethod
    def authenticate(open_id, union_id):
        """
        验证用户是否存在
        :param open_id: 用户的open_id
        :param union_id: 用户的union_id
        :return: Member对象或None
        """
        try:
            return Member.objects.get(open_id=open_id, union_id=union_id)
        except Member.DoesNotExist:
            return None

    @staticmethod
    def generate_tokens(member):
        """
        生成JWT token
        :param member: Member对象
        :return: 包含access_token和refresh_token的字典
        """
        refresh = RefreshToken()
        refresh['user_id'] = member.id
        refresh['open_id'] = member.open_id
        refresh['union_id'] = member.union_id
        refresh['nickname'] = member.nickname

        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': 'Bearer',
            'expires_in': 86400,
        }

    @staticmethod
    def get_user_info(member):
        """
        获取用户信息
        :param member: Member对象
        :return: 用户信息字典
        """
        return {
            'id': member.id,
            'nickname': member.nickname,
            'open_id': member.open_id,
            'union_id': member.union_id,
            'gender': member.gender,
            'created_at': member.created_at.isoformat(),
            'registered_at': member.registered_at.isoformat(),
        }
