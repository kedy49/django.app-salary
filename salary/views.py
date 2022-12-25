from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from salary.models import Work, Yearwage, Wage, total_yukyu, Zangyo
from datetime import date
from django.db.models import Sum, Min, Avg, Count, Q
from dateutil.relativedelta import relativedelta
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import SignUpForm, ZangyoForm, YukyuForm
import math

l=1

def apptop_template(request,year_wage_id):
    global l
    l=1
    work1 = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month__lte = date.today().month,user_id=request.user.id)
    work2 = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month__lt = date.today().month,user_id=request.user.id)
    work1_2 = Work.objects.filter(Q(Worked_date__year = date.today().year,Worked_date__month__lte = date.today().month,user_id=request.user.id),Q(zangyo_m__isnull=False)|Q(zangyo_h__isnull=False))
    work2_2 = Work.objects.filter(Q(Worked_date__year = date.today().year,Worked_date__month__lt = date.today().month),Q(zangyo_m__isnull=False,user_id=request.user.id)|Q(zangyo_h__isnull=False))
    
    if Zangyo.objects.filter(user_id=request.user.id).exists():
        zangyo = Zangyo.objects.filter(user_id=request.user.id)
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
    if work1_2.all().exists():
        zangyo_h_1 = int(work1_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum"))
    else:
        zangyo_h_1 = 0
    if work1_2.all().exists():
        zangyo_m_1 = int(work1_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum"))
    else:
        zangyo_m_1 = 0
    if work2_2.all().exists():
        zangyo_h_2 = int(work2_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum"))
    else:
        zangyo_h_2 = 0
    if work2_2.all().exists():
        zangyo_m_2 = int(work2_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum"))
    else:
        zangyo_m_2 = 0

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
    else:
        yearwage=0
        l=0

    if total_yukyu.objects.filter(user_id=request.user.id).exists():
        Total_yukyu = total_yukyu.objects.filter(user_id=request.user.id).get(number=1).name
    else:
        Total_yukyu = 0
        l=0

    sum_yukyu = Work.objects.filter(Worked_date__year = date.today().year,user_id=request.user.id).aggregate(Sum("yukyu"))
    day = date.today() + relativedelta(months=-1)
    wage_avg = Work.objects.filter(Worked_date__year = day.year,Worked_date__month = day.month,user_id=request.user.id).aggregate(Avg("wage"))
    wage_avg_2 = Work.objects.filter(Worked_date__year = day.year,Worked_date__month = date.today().month,user_id=request.user.id).aggregate(Avg("wage"))
    month = int(date.today().month)
    if l == 0:
        return render(request,"salary/setting.html",{"wage":Wage.objects.filter(user_id=request.user.id),"yearwage":yearwage,"totalyukyu":Total_yukyu,"zangyo":zangyo})
    else:
        return render(
            request, 
            'salary/apptop.html',
            {
                'sum_wage1':sum_wage1,
                'sum_wage2':sum_wage2,
                'wage_avg':wage_avg.get("wage__avg"),
                'wage_avg_2':wage_avg_2.get("wage__avg"),
                'tomonth':13-month,
                'nextmonth':12-month,
                'yearwage':yearwage,
                'sum_yukyu':sum_yukyu.get("yukyu__sum"),
                'total_yukyu':Total_yukyu,
                'year_wage':Yearwage.objects.filter(user_id=request.user.id),
                'zangyo':zangyo,
                'id':year_wage_id
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

        if "lastyear" in request.POST:
            j = j - 1
        elif "nextyear" in request.POST:
            j = j + 1
        elif "toyear" in request.POST:
            j = 0

    month = date.today() + relativedelta(months=i)
    year = date.today() + relativedelta(years=j)
    work = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,user_id=request.user.id)
    work2 = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,wage_2__isnull=False,user_id=request.user.id)
    work3 = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,zangyo_h__isnull=False,user_id=request.user.id)
    work4 = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,zangyo_m__isnull=False,user_id=request.user.id)

    if not work:
        sum_time_h = 0
        sum_time_m = 0
    elif not work2:
        sum_time_h = int(work.aggregate(Sum('Worktime_h')).get("Worktime_h__sum"))
        sum_time_m = int(work.aggregate(Sum('Worktime_m')).get("Worktime_m__sum"))
    else:
        sum_time_h = int(work.aggregate(Sum('Worktime_h')).get("Worktime_h__sum"))+int(work2.aggregate(Sum('Worktime_h_2')).get("Worktime_h_2__sum"))
        sum_time_m = int(work.aggregate(Sum('Worktime_m')).get("Worktime_m__sum"))+int(work2.aggregate(Sum('Worktime_m_2')).get("Worktime_m_2__sum"))
    
    if sum_time_m >= 60:
        sum_time_h = sum_time_h + sum_time_m/60
        sum_time_m = sum_time_m%60

    if not work:
        sum_wage=0
    elif not work3:
        sum_wage = work.aggregate(Sum("total_wage")).get("total_wage__sum")
    else:
        zangyo = int(Zangyo.objects.get(ID="1").name)
        zangyo_h = int(work3.aggregate(Sum("zangyo_h")).get("zangyo_h__sum"))
        zangyo_m = int(work4.aggregate(Sum("zangyo_m")).get("zangyo_m__sum"))
        sum_wage = int(work.aggregate(Sum("total_wage")).get("total_wage__sum"))+zangyo*zangyo_h+zangyo*zangyo_m/60

    return render(
        request, 
        'salary/work_list.html', 
        {
            'work':work.order_by('Worked_date'),
            'sum_time_h':math.floor(sum_time_h),
            'sum_time_m':sum_time_m,
            'sum_wage':sum_wage,
            'month':month.month,
            'year':year.year,
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
        messages.add_message(self.request, messages.WARNING, "入力にエラーがあります！！")
        messages.add_message(self.request, messages.ERROR, "入力にエラーがあります！！")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra = {
            "hourly_wage":Wage.objects.filter(user_id=self.request.user.id),
            "sum_yukyu":Work.objects.filter(Worked_date__year = date.today().year,user_id=self.request.user.id).aggregate(Sum("yukyu")).get("yukyu__sum"),
            "total_yukyu":total_yukyu.objects.filter(user_id=self.request.user.id).get(number=1).name,
        }
        context.update(extra)
        return context

class Updatework(UpdateView):
    model = Work    
    template_name = "salary/work_update_form.html"
    fields = ["Worked_date","Worktime_h","Worktime_m","Worktime_h_2","Worktime_m_2","wage","wage_2","yukyu","zangyo_h","zangyo_m"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = Work.objects.get(id=self.kwargs['pk']) # pkを指定してデータを絞り込む
        extra = {"wage_2":work.wage_2,"yukyu" :work.yukyu}
        context.update(extra)
        return context


class Delete(DeleteView):
    model = Work
    template_name = "salary/work_confirm_delete.html"
    # 削除したあとに移動する先（トップページ）
    success_url=reverse_lazy('list')


def wagelist(request):
    wage=Wage.objects.filter(user_id=request.user.id)
    return render(request, 'salary/wage_list.html', {"wage":wage})

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
        messages.add_message(self.request, messages.ERROR, "入力にエラーがあります！！")
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
        messages.add_message(self.request, messages.ERROR, "入力にエラーがあります！！")
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
        messages.add_message(self.request, messages.ERROR, "入力にエラーがあります！！")
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
        messages.add_message(self.request, messages.ERROR, "入力にエラーがあります！！")
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