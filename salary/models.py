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

    user = models.ForeignKey(
        get_user_model(), 
        verbose_name='ログインユーザー', 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.Worked_date.strftime("%Y/%m/%d")

    def save(self,*args,**kwargs):
        wage_sum = self.Worktime_h*self.wage+self.Worktime_m*self.wage/60
        if not self.wage_2:
            self.total_wage = wage_sum
        else:
            if self.Worktime_h_2 == None:
                self.Worktime_h_2 = 0
            if self.Worktime_m_2 == None:
                self.Worktime_m_2 = 0
            self.total_wage = wage_sum+self.Worktime_h_2*self.wage_2+self.Worktime_m_2*self.wage_2/60
        super().save(*args,**kwargs)
        

class Wage(models.Model):
    class Meta:
        verbose_name ="時給"
    name = models.PositiveIntegerField(default=1000,verbose_name ="時給")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)
    


class Yearwage(models.Model):
    class Meta:
       verbose_name="年収"
    name = models.PositiveIntegerField(default=1000000,verbose_name="年収")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)


class total_yukyu(models.Model):
    class Meta:
        verbose_name = "有給"
    number = models.PositiveIntegerField(default=1)
    name = models.PositiveIntegerField(verbose_name = "有給")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)

class Zangyo(models.Model):
    class Meta:
        verbose_name = "残業手当"
    number = models.PositiveIntegerField(default=1)
    name = models.PositiveIntegerField(verbose_name = "残業手当")
    user = models.ForeignKey(get_user_model(), verbose_name='ログインユーザー', on_delete=models.CASCADE)