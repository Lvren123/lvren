from django.db import models

# Create your models here.

# 添加时间 和 修改时间
class Base(object):
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)

    class Meta:
        abstract = True  # 不创建表




# 分类表
class Cate(Base,models.Model):
    name= models.CharField(max_length=50,unique=True)
    pid = models.IntegerField(default=0) # 上级分类Id 自关联
    type = models.IntegerField(default=1)  # 分类 （无限级分类为了识别几级分类）
    top_id = models.IntegerField(default=0)  # 标注顶级分类
    pic = models.CharField(max_length=255,default='') # 图片
    is_recommend = models.BooleanField(default=0) # 0为假，1为真 是否推荐
    class Meta:
        db_table = 'cate'

# 标签表
class Tags(Base,models.Model):
    name= models.CharField(max_length=50,unique=True)
    cid = models.ForeignKey('Cate',to_field='id',on_delete=models.CASCADE) # 外键关联到分类表的ID 给分类定义标签
    is_recommend = models.BooleanField(default=0) # 0为假，1为真 是否推荐
    class Meta:
        db_table = 'tags'


# 焦点图表
class Banner(Base,models.Model):
    pic = models.CharField(max_length=255,default='')
    is_show = models.BooleanField(default=0)  # 是否展示
    sort = models.IntegerField()  # 展示优先级
    typ = models.BooleanField(default=0) # 图片类型  # 1焦点图  0广告图

    class Meta:
        db_table = 'banner'

# 新闻表
class News(Base,models.Model):
    title = models.CharField(max_length=50)
    is_recommend = models.BooleanField(default=0) # 是否推送
    content = models.TextField()    # 内容

    class Meta:
        db_table = 'news'

from django.contrib.auth.models import AbstractUser
# 用户表
class User(AbstractUser):
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=11) # 手机
    email = models.CharField(max_length=50) # 邮箱
    image =  models.CharField(max_length=255,default='') # 头像
    signator = models.CharField(max_length=255,default='') # 个性签名
    is_valide = models.IntegerField(default=0)  # 0：未验证 1：验证成功 2：验证失败
    token = models.CharField(max_length=255,default='')
    class Meta:
        db_table = 'user'

# 商品表
class Goods(Base,models.Model):
    name = models.CharField(max_length=50)
    descrip = models.CharField(max_length=255) # 商品简介
    price = models.DecimalField(max_digits=10,decimal_places=2)
    pic = models.CharField(max_length=255)
    store = models.IntegerField(default=0) # 库存
    lock_store = models.IntegerField(default=0) # 锁定库存
    sales = models.IntegerField(default=0)  # 销量
    is_recommend = models.BooleanField(default=0)  # 是否推送首页
    content = models.TextField() # 商品详情
    t_contnet = models.IntegerField(default=0) # 总评论数 
    top_id = models.IntegerField() # 顶 级分类ID
    cid = models.ForeignKey('Cate',on_delete=models.CASCADE)  # 外键关联 分类表
    tagid = models.ForeignKey('Tags',on_delete=models.CASCADE)  # 外键关联 标签表

    class Meta:
        db_table = 'goods'

# 评论表
class Comment(models.Model):
    comment = models.TextField()  # 评论内容
    is_mo = models.BooleanField(default=0)
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    good = models.ForeignKey('Goods',on_delete=models.CASCADE)  # 外键关联商品表
    fen = models.IntegerField()

    class Meta:
        db_table = 'comment'



# 商家用户表
class Sadmin(Base,models.Model):
    username = models.CharField(max_length=50,unique=True) # 用户名
    passwd = models.CharField(max_length=255) # 密码
    is_admin = models.BooleanField(default=0) # 超级管理员
    rid = models.ForeignKey('Role', on_delete=models.CASCADE)  # 外键关联角色表
    class Meta:
        db_table = 'sadmin'


# 角色表
class Role(Base,models.Model):
    name = models.CharField(max_length=50)  # 角色名
    status = models.BooleanField(default=0)  #是否启用  1启用 0停用

    resoure = models.ManyToManyField('Resoure')  # ManyToMany 多对多
    class Meta:
        db_table = 'role'



# 资源表
class Resoure(Base,models.Model):
    name = models.CharField(max_length=50) # 资源名称
    url = models.CharField(max_length=200)  # 跳转地址
    status = models.BooleanField(default=0) # 是否启用  1启用 0停用


    class Meta:
        db_table = 'resoure'



# 购物车表
class Cart(Base,models.Model):
    good_id = models.IntegerField()
    user_id = models.IntegerField()
    count = models.IntegerField()
    good_name = models.CharField(max_length=50)
    good_price = models.DecimalField(max_digits=10,decimal_places=2)
    good_pic = models.CharField(max_length=255)
    is_checked = models.IntegerField(default=0)  # 是否提交订单
    class Meta:
        db_table = 'cart'



# 订单表
class Orders(Base,models.Model):
    order_sn = models.CharField(max_length=110,unique=True)  # 订单号
    user = models.ForeignKey('User',on_delete=models.CASCADE)  # 用户信息
    tmoney = models.DecimalField(max_digits=10,decimal_places=2)  # 总价
    address = models.ForeignKey('Dizhi',on_delete=models.CASCADE)  # 地址
    status = models.IntegerField(default=0) # 状态 0未支付 1已支付  2配送中 3未评论 4已评论
    pay_type = models.IntegerField(default=1) # 1支付宝 2货到付款 3网银
    code = models.CharField(max_length=200,default='') # 流水号

    class Meta:
        db_table = 'orders'


# 订单详情表
class OrderDetail(Base,models.Model):
    order_sn = models.ForeignKey('Orders',to_field='order_sn',on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    count = models.IntegerField()
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    goods = models.IntegerField() # 关联商品
    image = models.CharField(max_length=200)


    class Meta:
        db_table = 'order_detail'




# 地址表

class city(Base,models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=51)
    type = models.SmallIntegerField()

    class Meta:
        db_table = 'city'



# 收货地址表
class Dizhi(Base,models.Model):
    name = models.CharField(max_length=51)
    city = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    is_mo = models.BooleanField(default=0)

    class Meta:
        db_table = 'dizhi'