# Generated by Django 4.1.1 on 2022-12-26 03:50

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Zangyo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1)),
                ('name', models.PositiveIntegerField(verbose_name='残業手当')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ログインユーザー')),
            ],
            options={
                'verbose_name': '残業手当',
            },
        ),
        migrations.CreateModel(
            name='Yearwage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveIntegerField(default=1000000, verbose_name='年収')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ログインユーザー')),
            ],
            options={
                'verbose_name': '年収',
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Worked_date', models.DateField(default=django.utils.timezone.now, verbose_name='勤務日')),
                ('Worktime_h', models.PositiveIntegerField(verbose_name='勤務時間-時間')),
                ('Worktime_m', models.PositiveIntegerField(default=0, verbose_name='勤務時間-分')),
                ('wage', models.PositiveIntegerField(verbose_name='時給')),
                ('Worktime_h_2', models.PositiveIntegerField(blank=True, null=True, verbose_name='勤務時間-時間')),
                ('Worktime_m_2', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='勤務時間-分')),
                ('wage_2', models.PositiveIntegerField(blank=True, null=True, verbose_name='時給')),
                ('total_wage', models.PositiveIntegerField(editable=False, verbose_name='日給')),
                ('yukyu', models.PositiveIntegerField(verbose_name='有給')),
                ('zangyo_h', models.PositiveIntegerField(blank=True, null=True, verbose_name='残業時間（時間）')),
                ('zangyo_m', models.PositiveIntegerField(blank=True, null=True, verbose_name='残業時間（分）')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ログインユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='Wage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveIntegerField(default=1000, verbose_name='時給')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ログインユーザー')),
            ],
            options={
                'verbose_name': '時給',
            },
        ),
        migrations.CreateModel(
            name='total_yukyu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1)),
                ('name', models.PositiveIntegerField(verbose_name='有給')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ログインユーザー')),
            ],
            options={
                'verbose_name': '有給',
            },
        ),
    ]
