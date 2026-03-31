from django import forms


class LoginForm(forms.Form):
    open_id = forms.CharField(
        required=True,
        error_messages={'required': '缺少必要参数: open_id'}
    )
    union_id = forms.CharField(
        required=True,
        error_messages={'required': '缺少必要参数: union_id'}
    )
