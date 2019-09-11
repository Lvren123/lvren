"""meiduo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_jwt.views import obtain_jwt_token


from django.urls import path,re_path
from index import views
# 支付宝图标
from index import pay
app_name = 'dm'
urlpatterns = [
   path('',views.GetCateGoods.as_view()),
   path('getGoodsByTags/',views.getGoodsByTags.as_view()),
   path('cate/',views.Cate_Name.as_view()),
   path('banner/',views.Banner.as_view()),
   path('news/',views.News.as_view()),
   path('detail/',views.Detail.as_view()),
   path('reg/',views.Reg.as_view()),
   path('code/',views.GetCode),
   path('valid_email/',views.valid_email.as_view()),
   path('login/',views.Login.as_view()),
   path('addcart/',views.Cart.as_view()),
   path('addc/',views.Addc.as_view()),
   path('confirm_order/',views.Confirm_order.as_view()),
   path('addorder/',views.CreatOrder.as_view()),
   path('ord/',views.Order.as_view()),
   path('city/',views.Address.as_view()),
   path('city2/',views.City2.as_view()),
   path('city3/',views.City3.as_view()),
   path('adddi/',views.AddDi.as_view()),
   path('deldi/',views.DelDi.as_view()),
   path('mo/',views.Is_mo.as_view()),
   path('ding/',views.Ding.as_view()),
   path('dingc/',views.Dingc.as_view()),
   path('xindex/',views.Xindex.as_view()),
   path('ec/',views.Echart),
   path('getping/',views.Getping.as_view()),
   path('addp/',views.Addp.as_view()),
   path('getpayurl/',pay.page1),

   # re_path(r'login/', obtain_jwt_token, name='auths'),



]