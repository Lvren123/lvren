import json

from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponse
from rest_framework.views import  APIView
from rest_framework.response import  Response
from rest_framework_jwt.settings import api_settings

from md import models
from md.serializer import *
import uuid
# Create your views here.
#  获取一级列表下的所有数据，二级分类，标签，商品
class GetCateGoods(APIView):
    def get(self,request):
        # 获取一级分类
        cate = models.Cate.objects.filter(type=1).all()
        clist = []
        for i in cate:
            cdict = {}
            cdict['id'] = i.id
            cdict['name'] = i.name
            cdict['pic'] = i.pic
            # 获取一级分类下的二级
            cate2 = models.Cate.objects.filter(pid=i.id).all()
            c2 = Index_Cate(cate2,many=True)
            cdict['sublist']  = c2.data
            # 获取一级分类下的标签
            tags = models.Tags.objects.filter(cid=i.id).all()
            t = Index_Tags(tags,many=True)
            cdict['tags'] = t.data
            # 获取商品
            shop = models.Goods.objects.filter(top_id=i.id).all()
            g = Index_Good(shop,many=True)
            cdict['goods'] = g.data
            # 循环添加到列表   转换格式
            clist.append(cdict)
        mes = {}
        mes['code'] = 200
        mes['message'] = clist
        return Response(mes)

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# 动态获取标签下的商品
class getGoodsByTags(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self,request):
        # getGoods: function(tid, cid, index){
        cid = request.GET.get('cid')
        tid = request.GET.get('tid')
        mes = {}
        try:
            goods = models.Goods.objects.filter(top_id=cid,tagid=tid).all()
            g = Index_Good(goods,many=True)

            mes['code'] = 200
            mes['message'] = g.data
        except:
            mes['code'] = 10020
        return Response(mes)


# 商品一级分类 展示页面
class Cate_Name(APIView):
    def get(self,request):
        mes = {}
        cate = models.Cate.objects.filter(type=1).all()
        c= Index_Cate(cate,many=True)
        mes['code'] = 200
        mes['message'] = c.data


        return Response(mes)



# 焦点图展示
class Banner(APIView):
    def get(self,request):
        mes = {}
        ban = models.Banner.objects.filter(is_show=True).order_by('sort')[:4]
        b = Index_Banner(ban,many=True)
        mes['code'] = 200
        mes['message'] = b.data
        return Response(mes)


# 新闻展示
class News(APIView):
    def get(self,request):
        mes ={}
        news = models.News.objects.filter(is_recommend=True).all()
        n= NewsModelSerializer(news,many=True)

        mes['code'] = 200
        mes['message'] = n.data
        return Response(mes)


# 商品详情展示
class Detail(APIView):
    def post(self,request):
        id = request.POST.get('id')
        good = models.Goods.objects.get(id=id)
        g = ShopModelSerializer(good)
        mes={}
        two_good = models.Goods.objects.order_by('-sales')[:2]
        g2 = ShopModelSerializer(two_good,many=True)

        # 获取分类
        f1 = models.Cate.objects.get(id=int(good.cid.id))
        f2 = models.Cate.objects.get(id=int(f1.pid))

        # 获取评论
        co = models.Comment.objects.filter(good_id=id).all()
        alist = []
        for x in co:
            d  = {}
            if x.is_mo == 1:

                users = models.User.objects.get(id=x.user_id)
                d['name'] = users.username[0]+'***'+users.username[-1]
            else:
                d['name'] = users.username
            d['fen'] = x.fen
            d['comment'] = x.comment
            alist.append(d)



        d = {}
        d['f2'] = f1.name
        d['f1'] = f2.name

        mes['code'] = 200
        mes['message'] = g.data
        mes['message1'] = g2.data
        mes['fen'] = d
        mes['com'] = alist
        return Response(mes)

# 导入验证码
from utils.captcha.captcha import captcha
# from utils.captcha.captcha import captcha
# 获取验证码图片
def GetCode(request):
    name,text,image = captcha.generate_captcha()
    # 存入session,用户提交的时候进行对比
    request.session['code'] = text
    request.session['codes'] = text.lower()
    #
    return HttpResponse(image, 'image/jpg')



from django.core.mail import EmailMessage
from meiduo import settings
class Reg(APIView):
    def post(self,request):
        data = request.data.copy()
        user = data['username']
        pwd = data['password']
        pwd2 = data['password2']
        email = data['email']
        co = data['sms_code']
        allow = data['allow']
        mes={}

        code = request.session['code']
        codes = request.session['codes']
        if not all([user, pwd, pwd2, email, co, allow]):
            mes['code'] = 10010
            mes['message'] = '参数不全'
        elif not co or (code != co and codes != co):
            mes['code'] = 10012
            mes['message'] = '验证码错误'
        elif allow == 'false':
            mes['code'] = 10013
            mes['message'] = '请认真阅读协议！'
        else:
            one_user = models.User.objects.filter(username=user).first()
            if one_user:
                mes['code'] = 10011
                mes['message'] = '账号已存在'
            if one_user and one_user.is_valide == 0:
                mes['code'] = 10021
                mes['message'] = '用户未激活！'
            else:
                if pwd2 !=pwd:
                    mes['code'] = 10015
                    mes['message'] = '两次密码输入不一致！'
                else:
                    token = str(uuid.uuid1())

                    data['token'] = token
                    u = UserSerializer(data=data)
                    if u.is_valid():
                        u.save()

                        send_m = EmailMessage('欢迎注册', '点击此链接<a href="http://localhost:8000/index/valid_email?code='
                                              + token + '&name=' + user + '">点此</a>链接进行用户激活', settings.EMAIL_FORM,[email])
                        send_m.content_subtype = 'html'
                        send_m.send()
                        mes['code'] = 200
                    else:
                        print(u.errors)
                        mes['code'] = 10020


        return Response(mes)

# 邮箱验证
class valid_email(APIView):
    def get(self,request):
        code = request.GET.get('code')
        name =request.GET.get('name')

        if code:
            user = models.User.objects.filter(username=name).first()
            user.is_valide = 1
            user.save()
        return render(request, 'email.html')



# 美多登录接口
class Login(APIView):
    def post(self,request):
        mes= {}
        data = request.data
        name = data['name']
        pwd = data['passwd']

        if not all([name,pwd]):
            mes['code'] = 10021
            mes['message'] = '参数不全！'
        else:
            one_user = models.User.objects.filter(username=name).first()
            if one_user:
                if one_user.is_valide == 1:

                    passwd = check_password(pwd,one_user.password)
                    if passwd:
                        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                        payload = jwt_payload_handler(one_user)
                        token = jwt_encode_handler(payload)
                        # one_user.token = token
                        u = {}
                        request.session['user_id'] = one_user.id
                        u['username']  = one_user.username
                        u['user_id'] = one_user.id
                        u['token'] = token

                        mes['code'] = 200
                        mes['message'] = u

                    else:
                        mes['code'] = 10010
                        mes['message'] = '密码错误！'
                else:
                    mes['code'] = 10030
                    mes['message']  = '用户未激活，请先激活！'
            else:
                mes['code'] = 10020
                mes['message'] = '用户名不存在！'
        return Response(mes)



# 购物车接口
class Cart(APIView):
    #  展示购物车接口
    def get(self,request):
        mes = {}
        user_id = request.GET.get('user_id')

        cart = models.Cart.objects.filter(user_id=user_id,is_checked=0).all()

        c = CartModelSerializer(cart, many=True)
        mes['message'] = c.data
        mes['code'] = 200

        return Response(mes)

    def post(self, request):
        mes = {}
        data = request.data.copy()
        # 查询购物车是否存在
        # g = models.Goods.objects.get(id=data['good_id'])
        cart = models.Cart.objects.filter(user_id=data['user_id'], good_id=data['good_id']).first()
        # 如果存在则累加
        if cart:
            cart.count += int(data['count'])
            # g.lock_store += int(data['count'])
            # g.save()
            cart.save()
            mes['code'] = 200
        # 不存在则写入
        else:
            g = models.Goods.objects.get(id=data['good_id'])
            data['good_name'] = g.name
            data['good_price'] = g.price
            data['good_pic'] = g.pic
            c = CartSerializer(data=data)
            if c.is_valid():
                c.save()
                # g.lock_store += int(data['count'])
                # g.save()
                mes['code'] = 200
            else:
                mes['code'] = 10050
                print(c.errors)

        return Response(mes)



#  购物车修改库存
class Addc(APIView):
     def post(self,request):
        mes={}
        data = request.data
        # g = models.Goods.objects.get(id=data['good_id'])
        cart = models.Cart.objects.filter(user_id=data['user_id'],
                                          good_id=data['good_id']).first()

        if data['is']=='1':
            cart.count += 1
            # g.lock_store += 1
            # g.save()
            cart.save()
            mes['code'] = 200
            mes['message'] = cart.count
        else:
            cart.count -= 1
            # g.lock_store -=1
            # g.save()
            cart.save()
            mes['code'] = 200
            mes['message'] = cart.count

        return Response(mes)

# 提交订单
class Confirm_order(APIView):
    def post(self,reuqest):
        mes={}
        data = reuqest.data


        # 查询购物车
        if data['ids']:

            ids = data['ids'].split(',')
            mes['code'] = 200
            models.Cart.objects.filter(user_id__in=data['user_id'],id__in=ids).all().update(is_checked=1)
        else:
            mes['code'] = 500
            mes['message'] = '未选中商品！'
        return Response(mes)


# 展示订单页面
class Order(APIView):
    def get(self,request):
        mes={}
        uid = request.GET.get('user_id')
        cart = models.Cart.objects.filter(user_id=uid,is_checked=1).all()
        c = CartModelSerializer(cart,many=True)
        di = models.Dizhi.objects.all()
        d = DizhiModelserializer(di,many=True)

        mes['code'] = 200
        mes['message'] = c.data
        mes['di'] = d.data


        return Response(mes)

# 生成订单
# 事务  # 为了保持操作的成功
from django.db import transaction
class CreatOrder(APIView):
    @transaction.atomic
    def post(self,request):
        mes ={}
        data = request.data.copy()
        print(data)
        user_id = data['user_id']
        did = data['address']
        pay_type = data['pay_type']

        # 生成order_sn 订单号
        order_sn = str(uuid.uuid1())

        # 生成订单

        c = models.Cart.objects.filter(user_id=user_id,is_checked=1).all()
        tmoney = 0
        for i in c:
            tmoney += i.count * i.good_price
        money =  tmoney+10

        sid = transaction.savepoint()
        # 建立事务开始的节点
        order = models.Orders.objects.create(order_sn=order_sn,user_id=user_id,tmoney=money,address_id=did,pay_type=pay_type)
        if int(pay_type) == 2:
            order.status=2
            order.save()


        # 写订单详情

        cart = models.Cart.objects.filter(user_id=user_id, is_checked=1).all()
        for i in cart:
            # 判断库存
            goods = models.Goods.objects.get(id=i.good_id)
            if i.count > goods.store - goods.lock_store:
                mes['code'] = 10021
                mes['message'] = '库存不足！'
                # 失败回滚！
                transaction.savepoint_rollback(sid)
            else:
                # 构造详情表数据，进行添加
                name = i.good_name
                price = i.good_price
                count = i.count
                goods = i.good_id

                image = i.good_pic
                try:
                    models.OrderDetail.objects.create(order_sn=order,name=name,price=price,count=count,user_id=user_id,image=image,goods=goods)
                    # 更新商品表中的锁定库存
                    goods.lock_store += i.count
                    goods.save()
                    # 清空购物车
                    models.Cart.objects.filter(user_id=user_id,is_checked=1).all().delete()
                    # 成功提交
                    mes['code'] = 200
                    mes['id'] = order.id
                    transaction.savepoint_commit(sid)
                except:
                    mes['code'] = 502
                    mes['message'] = '添加失败'
                    transaction.savepoint_rollback(sid)


        return Response(mes)
        # 根据address_id去address表查询地址详情信息



# 展示一级地址
class Address(APIView):
    def get(self,request):
        mes={}
        city1 = models.city.objects.filter(type=1).all()
        c = AddressModelSerializer(city1,many=True)

        mes['code'] = 200
        mes['message'] = c.data
        return Response(mes)

# 展示二级地址
class City2(APIView):
    def get(self,request):
        mes = {}
        id = request.GET.get('id')
        city = models.city.objects.filter(pid=id).all()
        c = AddressModelSerializer(city,many=True)
        mes['code'] = 200
        mes['message'] = c.data
        return Response(mes)

class City3(APIView):
    def get(self,request):
        mes = {}
        id = request.GET.get('id')
        city = models.city.objects.filter(pid=id).all()
        c = AddressModelSerializer(city,many=True)

        mes['code'] = 200
        mes['message'] = c.data


        return Response(mes)


class AddDi(APIView):
    # 查看地址
    def get(self,request):
        mes = {}
        id = request.GET.get('id')
        city = models.Dizhi.objects.filter(user_id=id).all()
        if len(city)==1:
            city.update(is_mo=1)
        c = DizhiModelserializer(city,many=True)
        mes['code'] = 200
        mes['message'] = c.data
        return Response(mes)
    # 添加地址
    def post(self,request):
        mes = {}
        data = request.data.copy()
        print(data)
        city1 = models.city.objects.get(id=data['province_id']).name
        city2 = models.city.objects.get(id=data['city_id']).name
        city3 = models.city.objects.get(id=data['district_id']).name
        data['city'] = city1+city2+city3+data['place']

        # 判断修改
        if int(data['update']) > 0:
            aa = models.Dizhi.objects.get(id=int(data['update']))
            a = Addressserializer(aa,data=data)
        else:
            # 添加
            a = Addressserializer(data=data)

        if a.is_valid():
            a.save()
            mes['code'] = 200
        else:
            print(a.errors)
            mes['code'] = 500

        return Response(mes)


# 删除地址
class DelDi(APIView):
    def get(self,request):
        mes ={}
        id = request.GET.get('id')
        try:
            models.Dizhi.objects.get(id=id).delete()
            mes['code'] = 200
        except:
            mes['code'] = 500

        return Response(mes)


# 设置默认地址
class Is_mo(APIView):
    def get(self,request):
        mes = {}
        id = request.GET.get('id')
        if id:
            models.Dizhi.objects.all().update(is_mo=0)
            di = models.Dizhi.objects.get(id=id)
            di.is_mo = 1
            di.save()
            mes['code'] = 200
        else:
            mes['code'] = 500
        return Response(mes)




# 我的订单页面
class Ding(APIView):
    def get(self,request):
        mes = {}
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        id = request.GET.get('id')


        alist = []
        ding = models.Orders.objects.filter(user_id=id).all()
        page = Paginator(ding,3)
        dinglist = page.get_page(p)
        tpage = page.num_pages
        for d in dinglist:
            items= {}
            items['order_sn'] = d.order_sn
            items['tmoney'] = d.tmoney
            items['pay_type'] = d.pay_type
            items['status'] = d.status
            items['id'] = d.id
            detail=d.orderdetail_set.all()
            d = DetailModelserializer(detail,many=True)
            items['detail'] = d.data

            alist.append(items)

        mes['code'] = 200
        mes['message'] = alist
        mes['tpage'] = tpage
        mes['cpage'] = p


        return Response(mes)


# 订单成功后跳转
class Dingc(APIView):
    def get(self,request):
        mes={}
        id = request.GET.get('id')

        order = models.Orders.objects.get(id=id)
        o = OrderModelserializer(order)
        mes['code'] = 200
        mes['message'] = o.data
        return Response(mes)


# 详情页面展示
class Xindex(APIView):
    def get(self,request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        mes = {}

        id = request.GET.get('id')

        rgood = models.Goods.objects.all().order_by('-sales')[:2]
        r = Index_Good(rgood,many=True)
        cate = models.Cate.objects.get(id=id)
            # print(cate.pid)
        alist = []
        alist.append(cate.id)
        while cate.pid != 0:
            cate1 = models.Cate.objects.get(id=cate.pid)
            cate.pid = cate1.pid
            alist.append(cate1.id)
        # print(alist)
        cates = models.Cate.objects.filter(id__in=alist).all()
        # print(cates)
        c = Index_Cate(cates,many=True)
        if len(alist) ==1:
            good =  models.Goods.objects.filter(top_id=id)
        else:
            good = models.Goods.objects.filter(cid_id=id)
        page = Paginator(good,20)
        goodlist = page.get_page(p)
        tpage = page.num_pages

        g = Index_Good(goodlist,many=True)

        mes['code'] = 200
        mes['message'] = g.data
        mes['cate'] = c.data
        mes['rgood'] = r.data
        mes['tpage'] = tpage
        mes['cpage'] = p
        return Response(mes)

from datetime import datetime,timedelta
def Echart(request):
    # 总用户数
    tcount = models.User.objects.count()
    # 当月注册数
    # 开始时间当月一号到现在
    start_time = datetime.now().strftime('%Y-%m-01')
    mcount = models.User.objects.filter(date_joined__gte=start_time,date_joined__lte=datetime.now()).count()

    # 当天注册数
    s_time = datetime.now().strftime('%Y-%m-%d')
    dcount = models.User.objects.filter(date_joined__gte=s_time,date_joined__lte=datetime.now()).count()


    # 一个月内每天注册人数
    countlist = []
    datalist = []
    for i in range(30,0,-1):
        stime = datetime.strptime(s_time,'%Y-%m-%d') - timedelta(i)
        etime = datetime.strptime(s_time,'%Y-%m-%d') - timedelta(i-1)
        count = models.User.objects.filter(date_joined__gte=stime,date_joined__lt=etime).count()
        countlist.append(count)
        datalist.append(stime.strftime('%Y-%m-%d'))
    return render(request, 'admin/echart.html',locals())


# websocket 连接推送数据
from dwebsocket.decorators import accept_websocket
import json
# 存储连接websocket 的用户
conn = {}
@accept_websocket
def finish_order(request,name):
    # 获取连接
    if request.is_websocket:
        # 新增 用户  连接信息
        conn[name] = request.websocket
        # 监听接收客户端发送的消息 或者 客户端断开连接
        for message in request.websocket:
            break  # 检测连接是否存在  必须要


def send(request):
    #支付宝已经支付成功，回调接口
    # 给商户发提醒
    name = 'admin'
    mes = json.dumps({'title':'我全情投入你却离场，如同我脸上画了滑稽的妆'},ensure_ascii=False).encode('utf-8')
    conn[name].send(mes)
    return HttpResponse('ok')



# redis操作
import json
from django_redis import get_redis_connection
def addcart(request):

    conn = get_redis_connection('default')
    user_id = str(1)
    goods_id = str(2)
    print(conn.hgetall('cart'+user_id))
    # conn.hset('cart'+ user_id,goods_id,json.dumps({'count':1,'is_check':1}))
    # goods_id = str(3)
    # conn.hset('cart'+ user_id,goods_id,json.dumps({'count':2,'is_check':1}))
    # #
    # all =  conn.hgetall('cart'+user_id)
    # # print(all)
    #
    # goods =conn.hget('cart'+user_id,'2').decode('utf-8')
    # goods = json.loads(goods)
    # goods['count'] += 9
    #
    # conn.hset('cart'+user_id,'2',json.dumps(goods))
    # print(conn.hgetall('cart'+user_id))
    # conn.set('cart'+user_id,[{'id':1,'count':3,'is_check':1},{'id':2,'count':3,'is_check':1}])


    return HttpResponse('如同我脸上画了滑稽的妆')



# 获取评论页面
class Getping(APIView):
    def get(self,request):
        mes = {}
        order_sn  = request.GET.get('order_sn')
        order = models.OrderDetail.objects.filter(order_sn=order_sn).all()
        o = DetailModelserializer(order,many=True)
        mes['code'] = 200
        mes['message'] = o.data
        return Response(mes)



# 添加评论
class Addp(APIView):
    def post(self,requets):
        mes = {}
        data = requets.data



        try:
            models.Comment.objects.create(comment=data['center'],is_mo=data['is_mo'],
            user_id=data['user_id'],good_id=data['goods_id'],fen=data['fen'])
            mes['code'] = 200
        except:
            mes['code'] = 500

        return Response(mes)