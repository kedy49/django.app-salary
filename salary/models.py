from django.db import models
from django.urls import reverse_lazy
import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class meta:
        verbose_name = "ユーザー"
    email = models.EmailField('メールアドレス', unique=True)

    
class Work(models.Model):
    class meta:
        verbose_name = "勤務"
        
        constraints = [
            models.UniqueConstraint(
                fields=["Worked_date", "user",],
                name="work_unique"
            )
        ]
        
    Worked_date = models.DateField(
        default = timezone.now,
        verbose_name="勤務日",
    )
    
    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])

    Worktime_h = models.PositiveIntegerField(
        verbose_name="勤務時間 (時間)",
    )

    Worktime_m = models.PositiveIntegerField(
        default = 0,
        verbose_name="勤務時間 (分)",
    )

    wage = models.PositiveIntegerField(
        verbose_name = "時給",
    )

    Worktime_h_2 = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name="途中で時給が変わる場合の勤務時間 (時間) ※空欄可",
    )

    Worktime_m_2 = models.PositiveIntegerField(
        blank = True,
        null = True,
        default = 0,
        verbose_name="途中で時給が変わる場合の勤務時間 (分) ※空欄可",
    )

    total_worktime_h = models.PositiveIntegerField(
        editable=False,
        verbose_name="一日の勤務時間(時間)",
    )

    total_worktime_m = models.PositiveIntegerField(
        editable=False,
        verbose_name="一日の勤務時間(分)",
    )

    wage_2 = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name = "途中で時給が変わる場合の時給 ※空欄可",
    )

    total_wage = models.PositiveIntegerField(
        editable=False,
        verbose_name = "日給",
    )

    yukyu = models.BooleanField(
        verbose_name = "有給",
    )

    zangyo_h = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name = "残業時間（時間）※空欄可",
    )

    zangyo_m = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name = "残業時間（分）※空欄可",
    )

    zangyo_wage = models.PositiveIntegerField(
        verbose_name="残業時給",
        editable=False,
    )

    user = models.ForeignKey(
        get_user_model(), 
        verbose_name='ログインユーザー', 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.Worked_date.strftime("%Y/%m/%d")

    def save(self,*args,**kwargs):
        if self.Worktime_h_2 == None:
            self.Worktime_h_2 = 0
        if self.Worktime_m_2 == None:
            self.Worktime_m_2 = 0
        if self.zangyo_h==None:
            self.zangyo_h=0
        if self.zangyo_m==None:
            self.zangyo_m=0

        wage_sum_1 = self.Worktime_h*self.wage+self.Worktime_m*self.wage/60
        if self.wage_2:
            wage_sum_2 = self.wage_2*self.Worktime_h_2+self.Worktime_m_2*self.wage_2/60
        wage_sum_3 = Zangyo.objects.get(user_id=self.user).name*self.zangyo_h+self.zangyo_m*Zangyo.objects.get(user_id=self.user).name/60

        if not self.Worktime_h_2 and not self.Worktime_m_2:
            if not self.zangyo_h and not self.zangyo_m:
                self.total_worktime_h=self.Worktime_h
                self.total_worktime_m=self.Worktime_m
                self.total_wage = wage_sum_1
            else:
                self.total_worktime_h=self.Worktime_h+self.zangyo_h
                self.total_worktime_m=self.Worktime_m+self.zangyo_m
                self.total_wage = wage_sum_1+wage_sum_3
        else:
            if not self.zangyo_h and not self.zangyo_m:
                self.total_worktime_h=self.Worktime_h+self.Worktime_h_2
                self.total_worktime_m=self.Worktime_m+self.Worktime_m_2
                self.total_wage = wage_sum_1+wage_sum_2
            else:
                self.total_worktime_h=self.Worktime_h+self.Worktime_h_2+self.zangyo_h
                self.total_worktime_m=self.Worktime_m+self.Worktime_m_2+self.zangyo_m
                self.total_wage = wage_sum_1+wage_sum_2+wage_sum_3

        self.zangyo_wage=Zangyo.objects.get(user_id=self.user).name

        super().save(*args,**kwargs)
        

class Wage(models.Model):
    class Meta:
        verbose_name ="時給"
    name = models.PositiveIntegerField(default=1000,verbose_name ="時給")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)+"円"
    


class Yearwage(models.Model):
    class Meta:
       verbose_name="年収"
    name = models.PositiveIntegerField(default=1000000,verbose_name="年収")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)+"円"


class total_yukyu(models.Model):
    class Meta:
        verbose_name = "有給"
    number = models.PositiveIntegerField(default=1)
    name = models.PositiveIntegerField(verbose_name = "有給")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)+"日"

class Zangyo(models.Model):
    class Meta:
        verbose_name = "残業手当"
    number = models.PositiveIntegerField(default=1)
    name = models.PositiveIntegerField(verbose_name = "残業手当")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)+"円"