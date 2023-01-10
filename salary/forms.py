from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Work, Wage, Yearwage, Zangyo, total_yukyu
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from datetime import date
from django.db.models import Sum, Min, Avg, Count, Q

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        return user


# class WorkForm(ModelForm):
#     class Meta:
#         model = Work
#         fields = ["Worked_date","Worktime_h","Worktime_m","Worktime_h_2","Worktime_m_2","wage","wage_2","yukyu","zangyo_h","zangyo_m"]
    
#     def clean_Worked_date(self):
#         worked_date = self.cleaned_data.get("Worked_date")
#         if not worked_date:
#             raise ValidationError("空欄は許可されていません。")
#         return worked_date



class YukyuForm(ModelForm):
    class Meta:
        model = total_yukyu
        fields = ["name"] 

class ZangyoForm(ModelForm):
    class Meta:
        model = Zangyo
        fields = ["name"] 
