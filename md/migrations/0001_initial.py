# Generated by Django 2.1.4 on 2019-09-05 17:52

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import md.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=50)),
                ('image', models.CharField(default='', max_length=255)),
                ('signator', models.CharField(default='', max_length=255)),
                ('is_valide', models.IntegerField(default=0)),
                ('token', models.CharField(default='', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.CharField(default='', max_length=255)),
                ('is_show', models.BooleanField(default=0)),
                ('sort', models.IntegerField()),
                ('typ', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'banner',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('count', models.IntegerField()),
                ('good_name', models.CharField(max_length=50)),
                ('good_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('good_pic', models.CharField(max_length=255)),
                ('is_checked', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'cart',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Cate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('pid', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=1)),
                ('top_id', models.IntegerField(default=0)),
                ('pic', models.CharField(default='', max_length=255)),
                ('is_recommend', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'cate',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=51)),
                ('type', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'city',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('t_comment', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.CreateModel(
            name='Dizhi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=51)),
                ('city', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=20)),
                ('tel', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('is_mo', models.BooleanField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'dizhi',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('descrip', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pic', models.CharField(max_length=255)),
                ('store', models.IntegerField(default=0)),
                ('lock_store', models.IntegerField(default=0)),
                ('sales', models.IntegerField(default=0)),
                ('is_recommend', models.BooleanField(default=0)),
                ('content', models.TextField()),
                ('t_contnet', models.IntegerField(default=0)),
                ('top_id', models.IntegerField()),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='md.Cate')),
            ],
            options={
                'db_table': 'goods',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('is_recommend', models.BooleanField(default=0)),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'news',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gname', models.CharField(max_length=80)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('count', models.IntegerField()),
                ('image', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'order_detail',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(max_length=110, unique=True)),
                ('tmoney', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.IntegerField(default=0)),
                ('pay_type', models.IntegerField(default=1)),
                ('code', models.CharField(default='', max_length=200)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='md.Dizhi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'orders',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Resoure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'resoure',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=0)),
                ('resoure', models.ManyToManyField(to='md.Resoure')),
            ],
            options={
                'db_table': 'role',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Sadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('passwd', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=0)),
                ('rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='md.Role')),
            ],
            options={
                'db_table': 'sadmin',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_recommend', models.BooleanField(default=0)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='md.Cate')),
            ],
            options={
                'db_table': 'tags',
            },
            bases=(md.models.Base, models.Model),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_sn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='md.Orders', to_field='order_sn'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='goods',
            name='tagid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='md.Tags'),
        ),
        migrations.AddField(
            model_name='comment',
            name='sid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='md.Goods'),
        ),
    ]
