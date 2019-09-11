from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password
from .models import Cate
from md import models
# 获取分类列表 序列化
class CateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cate
        fields = '__all__'
# 添加分类 反序列化
class CateSerializer(serializers.Serializer):
    name = serializers.CharField()
    pid = serializers.IntegerField()
    type = serializers.IntegerField()
    top_id = serializers.IntegerField()
    pic = serializers.CharField(default='')
    is_recommend = serializers.BooleanField()

    # 创建
    def create(self,data):
        cate = Cate.objects.create(**data)
        return cate

    # 修改
    def update(self,instance,data):
        instance.name = data.get('name')
        instance.pic = data.get('pic')
        instance.pid = data.get('pid')
        instance.top_id = data.get('top_id')
        instance.type=data.get('type')
        instance.is_recommend=data.get('is_recommend')
        instance.save()
        return instance

##########################################################################

# 序列化  新闻列表
class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = '__all__'
# 新闻列表 反序列化
class NewsSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    is_recommend = serializers.BooleanField()

    # 创建
    def create(self,data):
        news = models.News.objects.create(**data)
        return news

    def update(self, instance, data):
        instance.title = data.get('title')
        instance.is_recommend = data.get('is_recommend')
        instance.content = data.get('content')
        instance.save()
        return instance

##############################################################################
# 焦点图序列化
class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = '__all__'

# 添加焦点 反序列化
class BannerSerializer(serializers.Serializer):
    pic = serializers.CharField(default='')
    sort = serializers.IntegerField()
    is_show = serializers.BooleanField()
    typ = serializers.BooleanField()

    # 创建
    def create(self, data):
        ban = models.Banner.objects.create(**data)
        return ban

    # 修改
    def update(self, instance,data):

        instance.is_show = data.get('is_show')
        instance.pic = data.get('pic')
        instance.sort = data.get('sort')
        instance.typ = data.get('typ')
        instance.save()
        return instance

###################################################################################
# 标签 序列化
class TagsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = '__all__'

# 标签 反序列化
class TagsSerializer(serializers.Serializer):
    name= serializers.CharField()
    cid = serializers.IntegerField()
    is_recommend = serializers.BooleanField()
    # 创建
    def create(self, data):
        cid = data['cid']
        cate = models.Cate.objects.get(id=cid)
        tags = models.Tags.objects.create(name=data['name'],is_recommend=data['is_recommend'],cid=cate)
        return tags
    # 修改
    def update(self, instance, data):
        cid = data.get('cid')
        cate= models.Cate.objects.get(id=cid)
        instance.name = data.get('name')
        instance.is_recommend = data.get('is_recommend')
        instance.cid = cate
        instance.save()
        return instance

#####################################################################################################
# 序列化  商品表
class ShopModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goods
        fields = '__all__'

# 反序列化  商品
class ShopSerializer(serializers.Serializer):
    name = serializers.CharField()
    descrip = serializers.CharField()
    price = serializers.IntegerField()
    pic = serializers.CharField(default='')
    store = serializers.IntegerField()
    lock_store = serializers.IntegerField(default=0)
    sales = serializers.IntegerField(default=0)
    is_recommend = serializers.BooleanField()
    top_id = serializers.IntegerField(default=0)
    cid = serializers.IntegerField()
    tagid = serializers.IntegerField()
    content = serializers.CharField()
    t_content = serializers.IntegerField(default=0)

    # 创建
    def create(self, data):
        cid = data['cid']
        tagid = data['tagid']
        cate = models.Cate.objects.get(id=cid)
        tagsd = models.Tags.objects.get(id=tagid)
        shop = models.Goods.objects.create(name=data['name'],descrip=data['descrip'],store=data['store'],pic=data['pic'],lock_store=data['lock_store'],is_recommend=data['is_recommend'],price=data['price'],top_id=data['top_id'],tagid=tagsd,cid=cate,sales=data['sales'],
                                           content=data['content'],t_contnet=data['t_content'])
        return shop
    # 修改
    def update(self, instance, data):
        cid = data.get('cid')
        tagid = data['tagid']
        tagsd = models.Tags.objects.get(id=tagid)
        cate= models.Cate.objects.get(id=cid)
        instance.name = data.get('name')
        instance.descrip = data.get('descrip')
        instance.price = data.get('price')
        instance.pic = data.get('pic')
        instance.store = data.get('store')
        instance.lock_store = data.get('lock_store')
        instance.sales = data.get('sales')
        instance.top_id = data.get('top_id')
        instance.is_recommend = data.get('is_recommend')
        instance.content = data.get('content')
        instance.t_content = data.get('t_content')
        instance.cid = cate
        instance.tagid = tagsd
        instance.save()
        return instance


#################################################################################
# 资源表 序列化
class ResoureModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resoure
        fields = '__all__'

# 反序列化 资源

class ResoureSerializer(serializers.Serializer):
    name =serializers.CharField()
    url = serializers.CharField()
    status = serializers.BooleanField(default=0)

    # 创建
    def create(self,data):
        tags = models.Resoure.objects.create(**data)
        return tags

    # 修改
    def update(self, instance,data):
        instance.name = data.get('name')
        instance.status = data.get('status')
        instance.url = data.get('url')
        instance.save()
        return instance

########################################################################
# 角色  序列化
class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'

# 角色 反序列化
class RoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.BooleanField()


    # 创建
    def create(self,data):
        role = models.Role.objects.create(name=data['name'],status=data['status'])
        return role

    # 修改
    def update(self, instance,data):
        instance.name = data.get('name')
        instance.status = data.get('status')
        instance.save()
        return instance


########################################################################
# 后台用户  序列化
class SadminModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sadmin
        fields = '__all__'

# 后台用户 反序列化
class SadminSerializer(serializers.Serializer):
    username = serializers.CharField()
    passwd = serializers.CharField()
    is_admin = serializers.BooleanField()
    rid = serializers.IntegerField()

    # 创建
    def create(self,data):
        rid = data['rid']
        role = models.Role.objects.get(id=rid)
        pwd = make_password(data['passwd'])
        role = models.Sadmin.objects.create(username=data['username'],passwd=pwd,is_admin=data['is_admin'],rid=role)
        return role

    # 修改
    def update(self, instance,data):
        rid = data['rid']
        role = models.Role.objects.get(id=rid)
        instance.username = data.get('username')
        instance.passwd = make_password(data.get('passwd'))
        instance.is_admin = data.get('is_admin')
        instance.rid = role
        instance.save()
        return instance






  ## 前台
#########################################----------------------------------
# 分类序列化
class Index_Cate(serializers.ModelSerializer):
    class Meta:
        model = Cate
        fields = ('id','name','pic')


# 标签序列化
class Index_Tags(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ('id', 'name')

# 商品序列化
class Index_Good(serializers.ModelSerializer):
    class Meta:
        model = models.Goods
        fields = ('id', 'name','descrip','pic','price','sales')

# 焦点图序列化
class Index_Banner(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ('id', 'pic')


# 用户表   注册用户
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()
    token = serializers.CharField( default='')

    # 创建
    def create(self, data):
        data['password'] = make_password(data['password'])
        user1 = models.User.objects.create(**data)
        return user1


# 购物车反序列化
class CartSerializer(serializers.Serializer):
    good_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    count = serializers.IntegerField()
    good_name = serializers.CharField()
    good_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    good_pic = serializers.CharField()

    def create(self, data):
        cart = models.Cart.objects.create(**data)
        return cart


# 购物车序列化

class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'

# 地址分类序列化
class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.city
        fields = '__all__'


# 地址序列化
class DizhiModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dizhi
        fields = '__all__'
# 地址反序列化
class Addressserializer(serializers.Serializer):
    name = serializers.CharField()
    city = serializers.CharField()
    mobile = serializers.CharField()
    tel = serializers.CharField()
    email = serializers.CharField()
    user_id = serializers.IntegerField()
    # 创建
    def create(self,data):
        return models.Dizhi.objects.create(**data)
    # 修改
    def update(self, instance, data):
        instance.name = data.get('name')
        instance.city = data.get('city')
        instance.mobile = data.get('mobile')
        instance.tel = data.get('tel')
        instance.email = data.get('email')
        instance.save()
        return instance


# 订单详情表展示
class DetailModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields = '__all__'



# 订单序列化
class OrderModelserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orders
        fields = '__all__'

