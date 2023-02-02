from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from salary.models import Work, Yearwage, Wage, total_yukyu, Zangyo
from datetime import date
from django.db.models import Sum, Min, Max, Avg, Count, Q
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from .forms import SignUpForm, ZangyoForm, YukyuForm
import math
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from . import graph

l=1

def apptop_template(request,year_wage_id):
    global l
    l=1
    work1 = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month__lte = date.today().month,user_id=request.user.id)
    work2 = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month__lt = date.today().month,user_id=request.user.id)
    work1_2 = Work.objects.filter(Q(Worked_date__year = date.today().year,Worked_date__month__lte = date.today().month,user_id=request.user.id),Q(zangyo_m__isnull=False)|Q(zangyo_h__isnull=False))
    work2_2 = Work.objects.filter(Q(Worked_date__year = date.today().year,Worked_date__month__lt = date.today().month),Q(zangyo_m__isnull=False,user_id=request.user.id)|Q(zangyo_h__isnull=False))
    
    if Zangyo.objects.filter(user_id=request.user.id).exists():
        zangyo = int(Zangyo.objects.get(user_id=request.user.id).name)
    else:
        zangyo = 0
        l=0
    if work1.all().exists():
        sum_wage1_2 = int(work1.aggregate(Sum("total_wage")).get("total_wage__sum"))
    else:
        sum_wage1_2 = 0
    if work2.all().exists():
        sum_wage2_2 = int(work2.aggregate(Sum("total_wage")).get("total_wage__sum"))
    else:
        sum_wage2_2 = 0

    # 残業時間の整理
    if work1_2.all().exists():
        re_zangyo_h = work1_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum")
        re_zangyo_m = work1_2.aggregate(Sum("zangyo_m")).get("zangyo_m__sum")
        if re_zangyo_h:
            zangyo_h_1 = int(re_zangyo_h)
        else:
            zangyo_h_1 =0
        if re_zangyo_m:
            zangyo_m_1 = int(re_zangyo_m)
        else:
            zangyo_m_1 =0
    else:
        zangyo_h_1 = 0
        zangyo_m_1 =0
    if work2_2.all().exists():
        re_zangyo_h = work2_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum")
        re_zangyo_m = work2_2.aggregate(Sum("zangyo_m")).get("zangyo_m__sum")
        if re_zangyo_h:
            zangyo_h_2 = int(re_zangyo_h)
        else:
            zangyo_h_2 =0
        if re_zangyo_m:
            zangyo_m_2 = int(re_zangyo_m)
        else:
            zangyo_m_2 =0
    else:
        zangyo_h_2 = 0
        zangyo_m_2 =0

    if not work1_2:
        sum_wage1 = sum_wage1_2
    else:
        sum_wage1 = sum_wage1_2+zangyo*zangyo_h_1+zangyo*zangyo_m_1/60
    if not work2_2:
        sum_wage2 = sum_wage2_2
    else:
        sum_wage2 = sum_wage2_2+zangyo*zangyo_h_2+zangyo*zangyo_m_2/60

    if Wage.objects.filter(user_id=request.user.id).exists():
        pass
    else:
        l=0
    
    if Yearwage.objects.filter(user_id=request.user.id).exists():
        if year_wage_id == 1:
            num = int(Yearwage.objects.filter(user_id=request.user.id).aggregate(Min("id")).get("id__min"))
            yearwage = Yearwage.objects.filter(user_id=request.user.id).get(id = num).name
        else:
            yearwage = Yearwage.objects.filter(user_id=request.user.id).get(id = year_wage_id).name
        
        if yearwage-sum_wage1>=0:
            # 円グラフ設定
            pie = [sum_wage1, yearwage-sum_wage1]
            # Plot_Piechart関数の「l」に渡す配列（円グラフのラベル）
            label = ["累計給与","残り"]
        else:
            pie = [sum_wage1]
            label = ["累計給与"]
        chart = graph.Plot_PieChart(pie, label)
    else:
        yearwage=0
        l=0

    if total_yukyu.objects.filter(user_id=request.user.id).exists():
        Total_yukyu = total_yukyu.objects.filter(user_id=request.user.id).get(number=1).name
    else:
        Total_yukyu = 0
        l=0

    day = date.today() + relativedelta(months=-1)
    month = int(date.today().month)
    year_wage = Yearwage.objects.filter(user_id=request.user.id)

    work_year=Work.objects.filter(Worked_date__year = date.today().year,user_id=request.user.id)
    if not work_year:
        sum_yukyu=0
    else:
        sum_yukyu = Work.objects.filter(Worked_date__year = date.today().year,user_id=request.user.id).aggregate(Sum("yukyu")).get("yukyu__sum")
    
    if not work_year.filter(Worked_date__month = day.month):
        wage_avg=Wage.objects.filter(user_id=request.user.id).aggregate(Avg("name")).get("name__avg")
    else:
        wage_avg = Work.objects.filter(Worked_date__year = day.year,Worked_date__month = day.month,user_id=request.user.id).aggregate(Avg("wage")).get("wage__avg")
    
    if not work_year.filter(Worked_date__month = date.today().month):
        wage_avg_2=Wage.objects.filter(user_id=request.user.id).aggregate(Avg("name")).get("name__avg")
    else:
        wage_avg_2 = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month = date.today().month,user_id=request.user.id).aggregate(Avg("wage")).get("wage__avg")

    if l == 0:
        return render(request,"salary/setting.html",{"wage":Wage.objects.filter(user_id=request.user.id),"yearwage":yearwage,"totalyukyu":Total_yukyu,"zangyo":zangyo})
    else:
        return render(
            request, 
            'salary/apptop.html',
            {
                'sum_wage1':sum_wage1,
                'sum_wage2':sum_wage2,
                'wage_avg':wage_avg,
                'wage_avg_2':wage_avg_2,
                'tomonth':13-month,
                'nextmonth':12-month,
                'yearwage':yearwage,
                'sum_yukyu':sum_yukyu,
                'total_yukyu':Total_yukyu,
                'year_wage':year_wage,
                'zangyo':zangyo,
                'id':year_wage_id,
                'chart':chart,
            }
        )

i = 0
j = 0

def List(request):
    global i, j
    if request.method == "POST":
        if "lastmonth" in request.POST:
            if(request.POST['month_data']=="1"):
                j = j - 1
            i = i - 1
        elif "nextmonth" in request.POST:
            if(request.POST['month_data']=="12"):
                j = j + 1
            i = i + 1
        elif "tomonth" in request.POST:
            i = 0
            j = 0

        if "lastyear" in request.POST:
            j = j - 1
        elif "nextyear" in request.POST:
            j = j + 1
        elif "toyear" in request.POST:
            j = 0

    month = date.today() + relativedelta(months=i)
    year = date.today() + relativedelta(years=j)
    work = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,user_id=request.user.id)
    if not work:
        total_worktime_h = 0
        total_worktime_m = 0
    else:
        total_worktime_h = int(work.aggregate(Sum('total_worktime_h')).get("total_worktime_h__sum"))
        total_worktime_m = int(work.aggregate(Sum('total_worktime_m')).get("total_worktime_m__sum"))
    if total_worktime_m >= 60:
        total_worktime_h = total_worktime_h + total_worktime_m/60
        total_worktime_m = total_worktime_m%60
    
    total_wage=work.aggregate(Sum('total_wage')).get("total_wage__sum")
    if not total_wage:
        total_wage = 0

    return render(
        request, 
        'salary/work_list.html', 
        {
            'work':work.order_by('Worked_date'),
            'total_worktime_h':total_worktime_h,
            'total_worktime_m':total_worktime_m,
            'total_wage':total_wage,
            'month':month.month,
            'year':year.year,
        }
    )

m = 0
n = 0

def data(request):
    global m, n
    if request.method == "POST":
        if "lastmonth_2" in request.POST:
            if(request.POST['month_data_2']=="1"):
                m = m - 1
            n = n - 1
        elif "nextmonth_2" in request.POST:
            if(request.POST['month_data_2']=="12"):
                m = m + 1
            n = n + 1
        elif "tomonth_2" in request.POST:
            n = 0
            m = 0

        if "lastyear_2" in request.POST:
            m = m - 1
        elif "nextyear_2" in request.POST:
            m = m + 1
        elif "toyear_2" in request.POST:
            m = 0

    month = date.today() + relativedelta(months=n)
    year = date.today() + relativedelta(years=m)
    work = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,user_id=request.user.id)
    total_wage=work.aggregate(Sum('total_wage')).get("total_wage__sum")
    if not work:
        total_worktime_h = 0
        total_worktime_m = 0
        total_wage = 0
    else:
        total_worktime_h = int(work.aggregate(Sum('total_worktime_h')).get("total_worktime_h__sum"))
        total_worktime_m = int(work.aggregate(Sum('total_worktime_m')).get("total_worktime_m__sum"))
    if total_worktime_m >= 60:
        total_worktime_h = total_worktime_h + total_worktime_m/60
        total_worktime_m = total_worktime_m%60
    #勤務時間の詳細について
    sum_worktime_h = work.aggregate(Sum('Worktime_h')).get("Worktime_h__sum")
    sum_worktime_m = work.aggregate(Sum('Worktime_m')).get("Worktime_m__sum")
    sum_worktime_h_2 = work.aggregate(Sum('Worktime_h_2')).get("Worktime_h_2__sum")
    sum_worktime_m_2 = work.aggregate(Sum('Worktime_m_2')).get("Worktime_m_2__sum")
    sum_zangyo_h = work.aggregate(Sum('zangyo_h')).get("zangyo_h__sum")
    sum_zangyo_m = work.aggregate(Sum('zangyo_m')).get("zangyo_m__sum")
    if not sum_worktime_h:
        sum_worktime_h = 0
    if not sum_worktime_m:
        sum_worktime_m = 0
    if not sum_worktime_h_2:
        sum_worktime_h_2 = 0
    if not sum_worktime_m_2:
        sum_worktime_m_2 = 0
    if not sum_zangyo_h:
        sum_zangyo_h = 0
    if not sum_zangyo_m:
        sum_zangyo_m = 0
    #時給について
    wage = work.aggregate(Min('wage')).get("wage__min")
    wage_2 = work.aggregate(Max('wage')).get("wage__max")
    wage_zangyo = work.aggregate(Min('zangyo_wage')).get("zangyo_wage__min")
    if not wage:
        wage = 0
    if not wage_2:
        wage_2 = 0
    if not wage_zangyo:
        wage_zangyo = 0
    #有給について
    yukyu = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,user_id=request.user.id,yukyu=True).aggregate(Count('wage')).get("wage__count")
    return render(
        request, 
        'salary/work_data.html', 
        {
            'total_worktime_h':total_worktime_h,
            'total_worktime_m':total_worktime_m,
            'total_wage':total_wage,
            'month':month.month,
            'year':year.year,
            'sum_worktime_h':sum_worktime_h,
            'sum_worktime_m':sum_worktime_m,
            'sum_worktime_h_2':sum_worktime_h_2,
            'sum_worktime_m_2':sum_worktime_m_2,
            'sum_zangyo_h':sum_zangyo_h,
            'sum_zangyo_m':sum_zangyo_m,
            'wage':wage,
            'wage_2':wage_2,
            'wage_zangyo':wage_zangyo,
            'yukyu':yukyu,
        }
    )

    
def Detail(request, work_id):
    work = Work.objects.get(id = work_id)
    zangyo = Zangyo.objects.filter(user_id=request.user.id).get(number="1")
    return render(
        request,
        'salary/work_detail.html', 
        {'work':work,'zangyo':zangyo.name},
    )


class Creatework(CreateView):
    model = Work
    fields = ["Worked_date","Worktime_h","Worktime_m","Worktime_h_2","Worktime_m_2","wage","wage_2","yukyu","zangyo_h","zangyo_m"]
    template_name = "salary/work_form.html"

    def form_valid(self, form):
        qryset = form.save(commit=False)
        qryset.user=self.request.user
        qryset.save()
        messages.add_message(self.request, messages.SUCCESS, "登録が完了しました！")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "入力にエラーがあります！！")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra = {
            "hourly_wage":Wage.objects.filter(user_id=self.request.user.id),
            "sum_yukyu":Work.objects.filter(Worked_date__year = date.today().year,user_id=self.request.user.id).aggregate(Sum("yukyu")).get("yukyu__sum"),
            "total_yukyu":total_yukyu.objects.filter(user_id=self.request.user.id).get(number=1).name,
        }
        context.update(extra)
        return context
    
    def clean_Wage(self):
        wage = self.cleaned_data.get("Wage")
        if not wage:
            self.add_error('wage', '時給を選択して下さい。')
            raise ValidationError("時給を選択して下さい。")
        return wage

class Updatework(UpdateView):
    model = Work
    template_name = "salary/work_update_form.html"
    fields = ["Worktime_h","Worktime_m","wage","yukyu","Worktime_h_2","Worktime_m_2","wage_2","zangyo_h","zangyo_m"]
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = Work.objects.get(id=self.kwargs['pk']) # pkを指定してデータを絞り込む
        extra = {
            "work":work,
            "hourly_wage":Wage.objects.filter(user_id=self.request.user.id),
            "sum_yukyu":Work.objects.filter(Worked_date__year = date.today().year,user_id=self.request.user.id).aggregate(Sum("yukyu")).get("yukyu__sum"),
            "total_yukyu":total_yukyu.objects.filter(user_id=self.request.user.id).get(number=1).name,
        }
        context.update(extra)
        return context


class Delete(DeleteView):
    model = Work
    template_name = "salary/work_confirm_delete.html"
    # 削除したあとに移動する先（トップページ）
    success_url=reverse_lazy('list')


def wagelist(request):
    wage=Wage.objects.filter(user_id=request.user.id)
    zangyo=Zangyo.objects.get(user_id=request.user.id).name
    return render(request, 'salary/wage_list.html', {"wage":wage,"zangyo":zangyo})

class Updatewage(UpdateView):
    model = Wage
    fields = ["name"]
    template_name = "salary/wage_update_form.html"
    success_url = reverse_lazy('wage_list')

class Createwage(CreateView):
    model = Wage
    template_name = "salary/wage_form.html"
    fields = ["name"]
    success_url= reverse_lazy('wage_list')

    def form_valid(self, form):
        qryset = form.save(commit=False)
        qryset.user=self.request.user
        qryset.number=int(Wage.objects.filter(user_id=self.request.user.id).aggregate(Count('id')).get("id__count"))+1
        qryset.save()
        messages.add_message(self.request, messages.SUCCESS, "登録が完了しました！")
        return super().form_valid(form)

# 時給の初期設定用
class FirstCreatewage(Createwage):
    success_url= reverse_lazy("top", kwargs={"year_wage_id": 1})

class Deletewage(DeleteView):
    model = Wage
    template_name = "salary/work_confirm_delete.html"
    success_url=reverse_lazy('wage_list')


def yearwagelist(request):
    yearwage=Yearwage.objects.filter(user_id=request.user.id)
    return render(request, 'salary/yearwage_list.html', {"yearwage":yearwage})

class Createyearwage(Createwage):
    model = Yearwage
    template_name = "salary/yearwage_form.html"
    success_url= reverse_lazy('yearwage_list')
    def form_valid(self, form):
        qryset = form.save(commit=False)
        qryset.user=self.request.user
        qryset.save()
        messages.add_message(self.request, messages.SUCCESS, "登録が完了しました！")
        return super().form_valid(form)

# 年収の初期設定用
class FirstCreateyearwage(Createyearwage):
    success_url= reverse_lazy("top", kwargs={"year_wage_id": 1})

class Updateyearwage(UpdateView):
    model = Yearwage
    fields = ["name"]
    template_name = "salary/yearwage_update_form.html"
    success_url = reverse_lazy('yearwage_list')

class Deleteyearwage(DeleteView):
    model = Yearwage
    template_name = "salary/work_confirm_delete.html"
    success_url=reverse_lazy('yearwage_list')


class Createyukyu(CreateView):
    model = total_yukyu
    template_name = "salary/yukyu_form.html"
    fields = ["name"]
    success_url = reverse_lazy("top", kwargs={"year_wage_id": 1})
    def form_valid(self, form):
        qryset = form.save(commit=False)
        qryset.user=self.request.user
        qryset.save()
        messages.add_message(self.request, messages.SUCCESS, "登録が完了しました！")
        return super().form_valid(form)

def Updateyukyu(request):
    yukyu = get_object_or_404(total_yukyu.objects.filter(user_id=request.user.id))
    if request.method == 'POST':
        form = YukyuForm(request.POST, instance=yukyu)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("top", kwargs={"year_wage_id": 1}))
    else:
        form = YukyuForm(instance=yukyu)
        return render(request, 'salary/yukyu_update_form.html', {'form': form,'yukyu': yukyu})


class Createzangyo(CreateView):
    model = Zangyo
    template_name = "salary/zangyo_form.html"
    fields = ["name"]
    success_url = reverse_lazy("top", kwargs={"year_wage_id": 1})
    def form_valid(self, form):
        qryset = form.save(commit=False)
        qryset.user=self.request.user
        qryset.save()
        messages.add_message(self.request, messages.SUCCESS, "登録が完了しました！")
        return super().form_valid(form)

def Updatezangyo(request):
    zangyo = get_object_or_404(Zangyo.objects.filter(user_id=request.user.id))
    if request.method == 'POST':
        form = ZangyoForm(request.POST, instance=zangyo)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("top", kwargs={"year_wage_id": 1}))
    else:
        form = ZangyoForm(instance=zangyo)
        return render(request, 'salary/zangyo_update_form.html', {'form': form,'zangyo': zangyo})


# エラー画面表示用
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "登録が完了しました！")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "入力にエラーがあります！！")
        return super().form_invalid(form)