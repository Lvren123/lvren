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

from django.urls import path
from md import views
app_name = 'md'
urlpatterns = [
    # 首页
    path('',views.index,name='in'),
    # 注册
    # path('reg',views.reg),
    # 用户
    path('showcate/',views.showCate),
    #  登陆
    path('login/',views.Login.as_view(),name='login'),

    # 分类表
    path('catelist/', views.CateList.as_view(), name='catel'),
    path('addcate/', views.AddCate),
    path('submitaddcate/',views.SubmitAddcate.as_view(),name='saddc'),
    path('delcate/',views.DelCate.as_view(),name='deldc'),

    # 焦点表
    path('ban/',views.ban),
    path('bannerlist/', views.Banner.as_view(), name='bannerlist'),
    path('addban/', views.Addban.as_view(), name='addban'),
    path('delban/', views.DelBan.as_view(), name='delban'),

    # 标签表
    path('tags/',views.tags),
    path('tagslist/', views.TagsList.as_view(), name='tagslist'),
    path('addtags/', views.AddTags.as_view(), name='addtags'),
    path('deltags/', views.DelTags.as_view(), name='deltags'),

    # 新闻表
    path('snew/',views.snew),
    path('newlist/', views.Newlist.as_view(), name='newlist'),
    path('addnews/', views.Addnews.as_view(), name='addnews'),
    path('delnews/', views.DelNews.as_view(), name='delnews'),

    # 商品表
    path('shop/', views.Shop),
    path('shoplist/',views.ShopList.as_view(),name='shoplist'),
    path('addshop/',views.AddShop.as_view(),name='addshop'),
    path('delgood/',views.DelGood.as_view(),name='delgood'),
    path('ceshi/',views.ceshi.as_view(),name='ceshi'),

    # 资源表
    path('re/',views.resoure),
    path('relist/',views.Resoure_list.as_view(),name='relist'),
    path('addre/',views.AddRe.as_view(),name='addre'),
    path('delre/',views.Delre.as_view(),name='delre'),
    # 角色表
    path('role/',views.role),
    path('rolelist/',views.Role_List.as_view(),name='rolelist'),
    path('addrole/',views.Add_Role.as_view(),name='addrole'),
    path('delro/',views.Del_Re.as_view(),name='delro'),
    # 后台用户表
    path('auser/',views.adminuser),
    path('auserlist/',views.Auser_list.as_view()),
    path('addauser/',views.addauser.as_view()),
    path('delauser/',views.Delauser.as_view()),
]