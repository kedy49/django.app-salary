from django.db import models
from django.urls import reverse_lazy
import datetime


class Work(models.Model):
    class meta:
        verbose_name = "勤務管理"

    Worked_date = models.DateField(
        unique =True,
        default = datetime.date.today(),
        verbose_name="勤務日",
    )
    
    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])

    Worktime_h = models.PositiveIntegerField(
        verbose_name="勤務時間-時間",
    )

    Worktime_m = models.PositiveIntegerField(
        default = 0,
        verbose_name="勤務時間-分",
    )

    wage = models.PositiveIntegerField(
        verbose_name = "時給",
    )

    Worktime_h_2 = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name="勤務時間-時間",
    )

    Worktime_m_2 = models.PositiveIntegerField(
        blank = True,
        null = True,
        default = 0,
        verbose_name="勤務時間-分",
    )

    wage_2 = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name = "時給",
    )

    total_wage = models.PositiveIntegerField(
        editable=False,
        verbose_name = "日給",
    )

    yukyu = models.PositiveIntegerField(
        verbose_name = "有給",
    )

    zangyo_h = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name = "残業時間（時間）",
    )

    zangyo_m = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name = "残業時間（分）",
    )

    def __str__(self):
        return self.Worked_date.strftime("%Y/%m/%d")

    def save(self,*args,**kwargs):
        if not self.wage_2:
            self.total_wage = self.Worktime_h*self.wage+self.Worktime_m*self.wage/60
        else:
            if self.Worktime_h_2 == None:
                self.Worktime_h_2 = 0
            if self.Worktime_m_2 == None:
                self.Worktime_m_2 = 0
            self.total_wage = self.Worktime_h*self.wage+self.Worktime_m*self.wage/60+self.Worktime_h_2*self.wage_2+self.Worktime_m_2*self.wage_2/60
        super().save(*args,**kwargs)
        

class Wage(models.Model):
    name = models.PositiveIntegerField(
        unique=True,
        verbose_name ="時給",
    )
    


class Yearwage(models.Model):
    name = models.PositiveIntegerField(
        default=1000000,
        unique=True,
        verbose_name="年収",
    )


class total_yukyu(models.Model):
    name = models.PositiveIntegerField(
        verbose_name = "有給",
    )

class Zangyo(models.Model):
    name = models.PositiveIntegerField(
        verbose_name = "残業手当"
    )
