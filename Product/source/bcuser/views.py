from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import Bcuser


# Create your views here.

def index(request):
    # 'email'이라는 키에 세션에서 'user'라는 키로 가져온 값을 할당
    return render(request, 'index.html', { 'email': request.session.get('user') })

# FormView는 폼의 GET 요청과 POST 요청 처리 로직을 미리 정의해 놓은 뷰
class RegisterView(FormView):
    template_name = 'register.html' # 사용할 템플릿의 이름
    form_class = RegisterForm # 이 뷰에서 사용할 폼 클래스를 RegisterForm으로 설정
    success_url = '/login/' # 폼이 성공적으로 처리된 후 리다이렉트될 URL을 지정

    def form_valid(self, form): # 폼 데이터가 유효할 때 호출되는 메소드를 오버라이드
        # Bcuser 모델 인스턴스를 생성하여 사용자의 등록 요청을 처리하고 데이터베이스에 저장
        bcuser = Bcuser(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
            level='user' # level 필드는 'user'로 설정
        )
        if Bcuser.objects.filter(email=form.data.get('email')).exists(): #User의 email객체들 중 form에 입력한 email과 같은 대상이 존재하면,
            form.add_error('email', '이미 사용 중인 이메일입니다.')  # form에 email에러필드에 에러를 추가하라
            return self.form_invalid(form)
        else:    
            bcuser.save() 
        # 유효하면 입력 데이터를 데이터베이스에 저장하는 기능
        return super().form_valid(form)
        
        

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    # FormView에서 제공하는 form_valid() 메소드를 재정의(Overried)함. 
    # 즉 LoginForm 폼의 유효성 검사가 통과할 경우 호출
    def form_valid(self, form):
        # 세션 변수 'user'에 폼에서 가져온 'email' 데이터를 저장 -> 로그인 관리
        self.request.session['user'] = form.data.get('email')
        # 부모 클래스인 FormView의 form_valid 메소드를 호출하여, 정상적인 폼 처리 흐름을 계속 진행
        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')
