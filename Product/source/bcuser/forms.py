from django import forms
from django.contrib.auth.hashers import check_password
from .models import Bcuser

class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )
    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )

    def clean(self):
        # 부모 클래스의 clean 메소드를 호출하고, 그 결과인 cleaned_data를 가져옴. 
        # cleaned_data는 폼 필드에서 유효성 검사를 통과한 데이터를 담은 딕셔너리임.
        cleaned_data = super().clean() 
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('password', '비밀번호가 서로 다릅니다.')
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                bcuser = Bcuser.objects.get(email=email)
            except Bcuser.DoesNotExist:
                self.add_error('email', '아이디가 없습니다')
                return

            if not check_password(password, bcuser.password):
                self.add_error('password', '비밀번호를 틀렸습니다')
            # else:
            #     self.email=bcuser.email
