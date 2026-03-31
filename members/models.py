from django.db import models

# Create your models here.
class Member(models.Model):
    nickname = models.CharField(max_length=30)
    open_id = models.CharField(max_length=30)
    union_id = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '会员'
        verbose_name_plural = '会员'

# 会员同意的服务条款和隐私政策
class MemberAgreement(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    # 服务条款和隐私政策的版本号 json 格式
    agreement_version = models.TextField()
    agreed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '会员同意的服务条款和隐私政策'
        verbose_name_plural = '会员同意的服务条款和隐私政策'
        db_table = 'members_member_agreement'
