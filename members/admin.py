from django.contrib import admin

from .models import Member, MemberAgreement

class MemberAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'open_id', 'union_id', 'gender')
    search_fields = ('nickname', 'open_id', 'union_id')
    list_filter = ('gender',)

class MemberAgreementAdmin(admin.ModelAdmin):
    list_display = ('member', 'agreement_version', 'agreed_at')
    search_fields = ('member__nickname', 'agreement_version')
    list_filter = ('agreed_at',)

admin.site.register(Member, MemberAdmin)
admin.site.register(MemberAgreement, MemberAgreementAdmin)
# Register your models here.
