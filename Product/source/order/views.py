from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import RegisterForm # order의 RegisterForm
from product.models import Product
from bcuser.models import Bcuser
from .models import Order

from bcuser.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/order/' # 또는 /product/

    def form_valid(self, form):
        # transaction.atomic(): 데이터베이스 트랜잭션을 시작함. 
        # 이 블록 내에서 수행되는 모든 데이터베이스 연산은 원자성(atomicity)을 가짐. 
        # 즉, 블록 내의 연산 중 하나라도 실패하면 모든 연산이 취소됨
        with transaction.atomic():
            # 폼 데이터에서 제품 ID를 가져와 해당 제품을 데이터베이스에서 조회
            prod = Product.objects.get(pk=form.data.get('product'))
            # 주문객체를 생성
            order = Order(
                quantity=form.data.get('quantity'), #제품의 재고량을 가져와서 저장
                product=prod, #제품아이디 저장
                # 요청의 세션에서 'user' 키로 저장된 이메일 주소를 가져와 
                # Bcuser 테이블에서 해당 이메일을 가진 사용자를 검색하여 저장
                bcuser=Bcuser.objects.get(email=self.request.session.get('user'))
            )
            # 주문사항 저장
            order.save()
            # 제품의 재고를 줄임
            prod.stock -= int(form.data.get('quantity'))
            # 제품의 변경사항 저장
            prod.save()
        return super().form_valid(form)
    
    # 폼의 데이터가 유효하지 않을 때 호출되는 메서드
    def form_invalid(self, form):
        # 해당 제품의 페이지로 리다이렉트
        return redirect('/product/' + str(form.data.get('product')))

    # 폼을 초기화하는 데 필요한 인자들을 반환하는 메서드
    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs) # 기본 구현에서 반환되는 인자들
        # 추가로 request 객체를 포함
        # RegisterForm에서 request 객체를 사용할 수 있게 됨
        kw.update({
            'request': self.request
        })
        return kw
    
# 현재 세션에 있는 이메일에 해당하는 order객체를 필터링하여 주문 정보 가져옴
@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    # model=Order # 주문된 제품만 가져오므로 쿼리를 통해서 가져옴
    context_object_name='order_list'
    template_name='order.html'

    # bcuser__email : Order모델에 bcuser라는 외래키가 존재하므로 bcuser 필드의 email속성에 접근이 가능 
    def get_queryset(self, **kwargs):
        queryset=Order.objects.filter(bcuser__email=self.request.session.get('user'))
        return queryset
    
    




    
    

