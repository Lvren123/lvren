import json
import os
import time
from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponse,redirect,reverse
from rest_framework.views import APIView
from rest_framework.response import  Response
from md import models
from django.contrib.auth.hashers import make_password,check_password
from utils.response_code import RET,error_map
from .serializer import *
from meiduo import settings
# Create your views here.
# 首页
def index(request):
    admin_id = request.session.get('id')
    if admin_id:
        admin = models.Sadmin.objects.get(id=admin_id)
    return render(request,'admin/index.html',locals())
#注册
def reg(request):
    passwd = make_password('123')
    admin = models.Sadmin(username='admin',passwd=passwd,is_admin=1)
    admin.save()

    return HttpResponse('ok')

######################################################################
# 登录
class Login(APIView):
    def get(self,request):
        return render(request,'admin/login.html')
    def post(self,request):
        # jquer 接口
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')



        # Vue 接口
        # data = json.loads(request.body.decode())
        # print(data)
        # name = data['name']
        # pwd = data['passwd']



        mes = {}
        if not all([name,pwd]):
            mes['code'] = RET.DATAERR
            mes['message'] = error_map[RET.DATAERR]
        else:
            # 通过name 查询数据
            admin = models.Sadmin.objects.filter(username=name).first()
            if admin:
                # 比较密码
                if check_password(pwd,admin.passwd):
                    # 登录成功
                    request.session['id'] = admin.id
                    mes['code'] = RET.OK
                    mes['message'] = error_map[RET.OK]

                else:
                    mes['code'] = RET.PWDERR
                    mes['message'] = error_map[RET.PWDERR]
            else:
                mes['code'] = RET.USERERR
                mes['message'] = error_map[RET.USERERR]
        return HttpResponse(json.dumps(mes))
        # return render(request,'admin/login.html')

######################################################################
# 展示分类页面
def showCate(request):
    return render(request,'admin/news_type.html')


# 分类列表
class CateList(APIView):
    def get(self,request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有分页数据
        cate = models.Cate.objects.all()
        # 实例化分页对象  每页显示多少条(3)
        page = Paginator(cate,3)
        # 获取当前页的数据
        catelist = page.get_page(p)
        # 总页数
        tpage = page.num_pages
        # 因为是多个 所以需要 many=True
        c = CateModelSerializer(catelist,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['message'] = c.data
        mes['tpage'] = tpage
        mes['cpage'] = p

        return Response(mes)


# 展示添加分类页面
def AddCate(request):
    # 获取一级分类
    cate = models.Cate.objects.filter(pid=0).all()
    id = request.GET.get('id')
    cates = models.Cate.objects.filter(id=id).first()
    return render(request,'admin/add_cate.html',locals())

# 上传图片的方法  (因为多次用到)
def upload_img(img):
    if img:
        with open(os.path.join(settings.STATICFILES_DIRS[0],img.name),'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
            return 'http://127.0.0.1:8000/static/' + img.name
    return ''

# 添加分类
class SubmitAddcate(APIView):
    def post(self,request):
        content = request.data.copy()
        # 上传图片 更新图片路径
        img = request.FILES.get('pic')
        path = upload_img(img)
        content['pic'] = path
        try:
            pid = int(content['pid'])
        except:
            pid = 0
        #  通过pid构造top_id,type
        # 1手机   第一级    pid=0    type=1    top_id=0
        # 2华为手机   第二级  pid=1  type=2   top_id=1
        # 3c3   第三级   pid=2  type=3
        # 001 第四级    pid=3   type=4
        if pid == 0:
            type = 1
            top_id = 0
        else:
            cate = Cate.objects.get(id=pid)
            type = cate.type + 1
            if cate.top_id == 0:
                top_id = cate.id
            else:
                top_id = cate.top_id
        content['type'] = type
        content['top_id'] = top_id
        # 获取ID  实现修改
        try:
            id = int(request.data['id'])
        except:
            id = 0
        if id>0:
            # 修改
            cc= Cate.objects.get(id=id)
            c= CateSerializer(cc,data=content)
        else:
            c = CateSerializer(data=content)
        mes = {}
        if c.is_valid():
            c.save()
            mes['code'] = 200


        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)

# 删除
class DelCate(APIView):
    def post(self,request):
        mes = {}
        id = request.POST.get('id')
        if id:
            models.Cate.objects.get(id=id).delete()
            mes['code'] = 200
            mes['message'] = '删除成功'
        else:
            mes['code'] = 10020
            mes['message'] = '删除失败'

        return Response(mes)

######################################################################
# 展示新闻列表
def snew(request):
    return render(request,'admin/newlist.html')

# 新闻列表
class Newlist(APIView):
    def get(self,request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有分页数据
        cate = models.News.objects.all()
        # 实例化分页对象  每页显示多少条(3)
        page = Paginator(cate,3)
        # 获取当前页的数据
        catelist = page.get_page(p)
        # 总页数
        tpage = page.num_pages
        # 因为是多个 所以需要 many=True
        c = NewsModelSerializer(catelist,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['message'] = c.data
        mes['tpage'] = tpage
        mes['cpage'] = p

        return Response(mes)

# 添加新闻

class Addnews(APIView):
    def get(self,request):
        id = request.GET.get('id')
        news = ''
        if id:
            news = models.News.objects.get(id=id)
        else:
            news  = ''
        return render(request,'admin/addnews.html',locals())
    def post(self,request):
        content= request.data.copy()

        mes = {}
        try:
            id = int(content['id'])

        except:
            id = 0
        if id>0:
            # 修改
            nn = models.News.objects.get(id=id)
            n=  NewsSerializer(nn,data=content)
        else:
            n = NewsSerializer(data=content)
        if n.is_valid():
            n.save()
            mes['code'] = 200
        else:
            mes['code'] = 10020
            print(n.errors)

        return Response(mes)
        # return render(request,'admin/addnews.html')
# 删除新闻
class DelNews(APIView):
    def post(self,request):
        mes= {}
        id = request.POST.get('id')
        if id:
            models.News.objects.get(id=id).delete()
            mes['code'] = 200
            mes['message'] = '删除成功'
        else:
            mes['code'] = 10020
            mes['message'] = '删除失败，请重试！'
        return Response(mes)

######################################################################
# 展示标签列表
def tags(request):
    return render(request,'admin/tagslist.html')

# 标签列表
class TagsList(APIView):
    def get(self,request):
        try:
            p = request.GET.get('p')
        except:
            p = 1
        data = models.Tags.objects.all()
        # 实例化分页对象    每页显示多少条数据（3）
        page = Paginator(data,3)
        #  当前页
        tagslist = page.get_page(p)
        # 总页数
        tpage = page.num_pages
        # 必须序列化 转换格式   以便ajax 调用
        t = TagsModelSerializer(tagslist,many=True)
        mes={}
        mes['code'] = 200
        mes['message'] = t.data
        mes['cpage'] = p
        mes['tpage'] = tpage
        return Response(mes)

# 添加标签
class AddTags(APIView):
    def get(self,request):
        id = request.GET.get('id')
        cate = models.Cate.objects.filter(type=1).all()
        if id:
            one_tags = models.Tags.objects.get(id=id)
        return render(request,'admin/addtags.html',locals())
    def post(self,request):
        content = request.data.copy()


        try:
            id = int(content['id'])
        except:
            id = 0
        mes = {}
        if id>0:
           tt = models.Tags.objects.get(id=id)
           t = TagsSerializer(tt,data=content)
        else:
            t = TagsSerializer(data=content)
        if t.is_valid():
            t.save()
            mes['code'] = 200
            mes['message'] = '添加成功!'
        else:
            mes['code'] = 10020
            mes['message'] = '添加失败，请重试！'
            print(t.errors)





        return Response(mes)

# 删除标签
class DelTags(APIView):
    def get(self,request):
        mes = {}
        id = request.GET.get('id')
        if id:
            models.Tags.objects.get(id=id).delete()
            mes['code'] = 200
        else:
            mes['code'] = 10020
        return Response(mes)


######################################################################
# 焦点图 展示
def ban(reqeust):
    return render(reqeust,'admin/bannerlist.html')

# 焦点图 列表
class Banner(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有分页数据
        cate = models.Banner.objects.all()
        # 实例化分页对象  每页显示多少条(3)
        page = Paginator(cate,3)
        # 获取当前页的数据
        catelist = page.get_page(p)
        # 总页数
        tpage = page.num_pages
        # 因为是多个 所以需要 many=True
        c = BannerModelSerializer(catelist, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['message'] = c.data
        mes['tpage'] = tpage
        mes['cpage'] = p

        return Response(mes)

# 添加焦点
class Addban(APIView):
    def get(self,request):
        id = request.GET.get('id')
        ban = ''
        if id:
            ban = models.Banner.objects.get(id=id)
        return render(request,'admin/addban.html',locals())

    def post(self,request):
        conten = request.data.copy()
        print(conten)
        img = request.FILES.get('pic')
        path = upload_img(img)
        conten['pic'] = path

        try:
            id = int(conten['id'])
        except:
            id = 0

        if id > 0:
            ss = models.Banner.objects.get(id=id)
            s = BannerSerializer(ss, data=conten)
        else:
            s = BannerSerializer(data=conten)

        mes = {}
        if s.is_valid():
            s.save()
            mes['code'] = 200

        else:
            mes['code'] = 10020
            print(s.errors)

        return Response(mes)


# 删除焦点
class DelBan(APIView):
    def post(self,request):
        mes = {}
        id = request.POST.get('id')
        if id:
            models.Banner.objects.get(id=id).delete()
            mes['code'] = 200
            mes['message'] = '删除成功'
        else:
            mes['code'] = 10020
            mes['message'] = '删除失败,请重试！'
        return Response(mes)



##############################################################################
#  商品首页展示
def Shop(request):
    return render(request,'admin/shoplist.html')

# 商品首页
class ShopList(APIView):
    def get(self,reuqest):
        mes={}
        goods = models.Goods.objects.all()

        try:
            p = int(reuqest.GET.get('p'))
        except:
            p =  1
        # 实例化分页对象  每页显示多少条
        page = Paginator(goods,3)
        # 当前页数据
        goodlist = page.get_page(p)
        # 总页数
        tpage = page.num_pages
        g = ShopModelSerializer(goodlist, many=True)
        mes['code'] = 200
        mes['message'] = g.data
        mes['tpage'] = tpage
        mes['cpage'] = p
        return Response(mes)


# 添加商品页面
class AddShop(APIView):
    def get(self,request):
        id = request.GET.get('id')
        cate = models.Cate.objects.filter(type=2).all()
        tags = models.Tags.objects.all()
        if id:
            good = models.Goods.objects.get(id=id)
        return render(request,'admin/addshop.html',locals())
    def post(self,request):
        conten = request.data.copy()
        print(conten)
        img = request.FILES.get('pic')
        path = upload_img(img)
        conten['pic'] = path
        cid = int(conten['cid'])
        cate = models.Cate.objects.get(id=cid)
        conten['top_id'] = cate.top_id
        try:
            id=int(conten['id'])
        except:
            id= 0
        if id>0:
            ss = models.Goods.objects.get(id=id)
            s = ShopSerializer(ss,data=conten)
        else:
            s = ShopSerializer(data=conten)

        mes = {}
        if s.is_valid():
            s.save()
            mes['code'] = 200

        else:
            mes['code'] = 10020
            print(s.errors)



        return Response(mes)


# 删除商品
class DelGood(APIView):
    def get(self,request):
        mes = {}
        id= request.GET.get('id')
        if id:
            models.Goods.objects.get(id=id).delete()
            mes['code'] = 200
        else:
            mes['code'] = 10020
        return Response(mes)

#  动态获取下拉框
class ceshi(APIView):
    def get(self,request):
        mes = {}

        id1 = request.GET.get('id1')
        cate = models.Cate.objects.get(id=id1)
        id = cate.top_id
        data = models.Tags.objects.filter(cid_id=id)
        c = TagsModelSerializer(data,many=True)
        # print(c)
        mes['code'] = 200
        mes['message'] = c.data
        return Response(mes)


############################################################################
# 展示资源页面
def resoure(request):
    return render(request,'admin/resourelist.html')

# 资源列表页面
class Resoure_list(APIView):
    def get(self,reuqest):
        mes={}
        goods = models.Resoure.objects.all()

        try:
            p = int(reuqest.GET.get('p'))
        except:
            p =  1
        # 实例化分页对象  每页显示多少条
        page = Paginator(goods,3)
        # 当前页数据
        goodlist = page.get_page(p)
        # 总页数
        tpage = page.num_pages
        g = ResoureModelSerializer(goodlist, many=True)
        mes['code'] = 200
        mes['message'] = g.data
        mes['tpage'] = tpage
        mes['cpage'] = p
        return Response(mes)

# 添加资源页面
class AddRe(APIView):
    def get(self,request):
        id = request.GET.get('id')
        if id:
            re =  models.Resoure.objects.get(id=id)
        return render(request,'admin/addresoure.html',locals())

    def post(self,request):
        data = request.data


        try:
            id = int(data['id'])
        except:
            id=0

        mes={}
        if id>0:
            rr = models.Resoure.objects.get(id=id)
            r = ResoureSerializer(rr,data=data)
        else:
            r = ResoureSerializer(data=data)
        if r.is_valid():
            r.save()
            mes['code'] =200
        else:
            print(r.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除资源
class Delre(APIView):
    def get(self,request):
        id= request.GET.get('id')
        mes={}
        if id:
            models.Resoure.objects.get(id=id).delete()
            mes['code'] = 200
        else:
            mes['code'] = 10020
        return Response(mes)


############################################################################
# 展示角色页面
def role(request):
    return render(request,'admin/rolelist.html')

# 角色页面
class Role_List(APIView):
    def get(self,request):
        mes = {}
        ro = models.Role.objects.all()
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        page = Paginator(ro,3)
        rolelist  = page.get_page(p)
        tpage = page.num_pages

        r = RoleModelSerializer(rolelist, many=True)
        mes['code'] = 200
        mes['message'] = r.data
        mes['tpage'] = tpage
        mes['cpage'] = p
        return Response(mes)



# 添加角色
class Add_Role(APIView):
    def get(self,request):

        resoure = models.Resoure.objects.filter(status=1)
        id = request.GET.get('id')
        if id:
            role = models.Role.objects.get(id=id)
        return render(request,'admin/addrole.html',locals())
    def post(self,request):
        mes = {}
        cont = request.data.copy()
        name = cont['name']
        ids = request.POST.getlist('ids')

        try:
            id = int(cont['id'])
        except:
            id = 0

        if id>0:
            ll = models.Role.objects.get(id=id)
            l = RoleSerializer(ll,data=cont)
        else:
            l = RoleSerializer(data=cont)

        if l.is_valid():
            l.save()
            one_role = models.Role.objects.filter(name=name).first()
            # 先清空权限在重新写入
            one_role.resoure.clear()
            # print(ids)
            # print(one_role)
            res = models.Resoure.objects.filter(id__in=ids).all()
            # print(res)
            one_role.resoure.add(*res)
            mes['code'] = 200
        else:
            mes['code'] = 10020
            print(l.errors)

        return Response(mes)

# 删除
class Del_Re(APIView):
    def get(self,request):
        id= request.GET.get('id')
        mes = {}
        if id:
            models.Role.objects.get(id=id).delete()
            mes['code'] = 200
        else:
            mes['code'] = 10020

        return Response(mes)




################################################################
# 后台用户表
# 展示后台用户页面
def adminuser(request):
    return render(request,'admin/adminuser.html')

# 后台列表页面
class Auser_list(APIView):
    def get(self,reuqest):

        mes={}
        goods = models.Sadmin.objects.all()

        try:
            p = int(reuqest.GET.get('p'))
        except:
            p =  1
        # 实例化分页对象  每页显示多少条
        page = Paginator(goods,3)
        # 当前页数据
        goodlist = page.get_page(p)
        # 总页数
        tpage = page.num_pages
        g = SadminModelSerializer(goodlist, many=True)
        mes['code'] = 200
        mes['message'] = g.data
        mes['tpage'] = tpage
        mes['cpage'] = p
        return Response(mes)

# 添加后台用户页面
class addauser(APIView):
    def get(self,request):
        role = models.Role.objects.filter(status=1)
        id = request.GET.get('id')
        if id:
            sadmin =  models.Sadmin.objects.get(id=id)
        return render(request,'admin/addauser.html',locals())

    def post(self,request):
        data = request.data

        try:
            id = int(data['id'])
        except:
            id=0

        mes={}
        if id>0:
            rr = models.Sadmin.objects.get(id=id)
            r = SadminSerializer(rr,data=data)
        else:
            r = SadminSerializer(data=data)
        if r.is_valid():
            r.save()
            mes['code'] =200
        else:
            print(r.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除后台管理员
class Delauser(APIView):
    def get(self,request):
        id= request.GET.get('id')
        mes={}
        if id:
            models.Sadmin.objects.get(id=id).delete()
            mes['code'] = 200
        else:
            mes['code'] = 10020
        return Response(mes)







