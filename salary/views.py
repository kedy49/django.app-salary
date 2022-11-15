from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from salary.models import Work, Yearwage, Wage, total_yukyu, Zangyo
from datetime import date
from django.db.models import Sum, Avg, Q
from dateutil.relativedelta import relativedelta
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import math

k=0

def apptop_template(request,year_wage_id):
    global k
    k = year_wage_id
    work1 = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month__lte = date.today().month)
    work2 = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month__lt = date.today().month)
    work1_2 = Work.objects.filter(Q(Worked_date__year = date.today().year,Worked_date__month__lte = date.today().month),Q(zangyo_m__isnull=False)|Q(zangyo_h__isnull=False))
    work2_2 = Work.objects.filter(Q(Worked_date__year = date.today().year,Worked_date__month__lt = date.today().month),Q(zangyo_m__isnull=False)|Q(zangyo_h__isnull=False))
    
    zangyo = int(Zangyo.objects.get(pk="1").name)
    sum_wage1_2 = int(work1.aggregate(Sum("total_wage")).get("total_wage__sum"))
    sum_wage2_2 = int(work2.aggregate(Sum("total_wage")).get("total_wage__sum"))
    zangyo_h_1 = int(work1_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum"))
    zangyo_m_1 = int(work1_2.aggregate(Sum("zangyo_m")).get("zangyo_m__sum"))
    zangyo_h_2 = int(work2_2.aggregate(Sum("zangyo_h")).get("zangyo_h__sum"))
    zangyo_m_2 = int(work2_2.aggregate(Sum("zangyo_m")).get("zangyo_m__sum"))
    if not work1_2:
        if not work2_2:
            sum_wage1 = sum_wage1_2
            sum_wage2 = sum_wage2_2
        else:
            sum_wage1 = sum_wage1_2
            sum_wage2 = sum_wage2_2+zangyo*zangyo_h_2+zangyo*zangyo_m_2/60
    else:
        if not work2_2:
            sum_wage1 = sum_wage1_2+zangyo*zangyo_h_1+zangyo*zangyo_m_1/60
            sum_wage2 = sum_wage2_2
        else:
            sum_wage1 = sum_wage1_2+zangyo*zangyo_h_1+zangyo*zangyo_m_1/60
            sum_wage2 = sum_wage2_2+zangyo*zangyo_h_2+zangyo*zangyo_m_2/60

    wage_avg = Work.objects.filter(Worked_date__year = date.today().year,Worked_date__month = date.today().month).aggregate(Avg("wage"))
    month = int(date.today().month)
    yearwage = Yearwage.objects.get(pk = year_wage_id)
    sum_yukyu = Work.objects.filter(Worked_date__year = date.today().year).aggregate(Sum("yukyu"))
    return render(
        request, 
        'salary/apptop.html',
        {
            'sum_wage1':sum_wage1,
            'sum_wage2':sum_wage2,
            'wage_avg':wage_avg.get("wage__avg"),
            'tomonth':13-month,
            'nextmonth':12-month,
            'yearwage':yearwage.name,
            'sum_yukyu':sum_yukyu.get("yukyu__sum"),
            'total_yukyu':total_yukyu.objects.get(pk=1).name,
            'year_wage':Yearwage.objects.all(),
            'zangyo':zangyo,
            'id':k,
        }
    )

i = 0
j = 0

def List(request):
    global i, j
    if request.method == "POST":
        if "lastmonth" in request.POST:
                i = i - 1
        elif "nextmonth" in request.POST:
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
    work = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month)
    work2 = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,wage_2__isnull=False)
    work3 = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,zangyo_h__isnull=False)
    work4 = Work.objects.filter(Worked_date__year = year.year, Worked_date__month = month.month,zangyo_m__isnull=False)

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
        zangyo = int(Zangyo.objects.get(pk="1").name)
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
    zangyo = Zangyo.objects.get(pk="1")
    return render(
        request,
        'salary/work_detail.html', 
        {'work':work,'zangyo':zangyo.name},
    )


class Creatework(CreateView):
    model = Work
    template_name = "salary/work_form.html"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra = {
            "hourly_wage":Wage.objects.all(),
            "sum_yukyu":Work.objects.filter(Worked_date__year = date.today().year).aggregate(Sum("yukyu")).get("yukyu__sum"),
            "total_yukyu":total_yukyu.objects.get(pk=1).name,
        }
        context.update(extra)
        return context

class Updatework(UpdateView):
    model = Work    
    template_name = "salary/work_update_form.html"
    fields = "__all__"

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
    wage=Wage.objects.all()
    return render(request, 'salary/wage_list.html', {"wage":wage})

class Updatewage(UpdateView):
    model = Wage
    fields = "__all__"
    template_name = "salary/wage_update_form.html"
    success_url = reverse_lazy('wage_list')

class Createwage(CreateView):
    model = Wage
    template_name = "salary/wage_form.html"
    fields = "__all__"
    success_url = reverse_lazy('wage_list')

class Deletewage(DeleteView):
    model = Wage
    template_name = "salary/work_confirm_delete.html"
    success_url=reverse_lazy('wage_list')


def yearwagelist(request):
    yearwage=Yearwage.objects.all()
    return render(request, 'salary/yearwage_list.html', {"yearwage":yearwage})

class Createyearwage(CreateView):
    model = Yearwage
    template_name = "salary/yearwage_form.html"
    fields = "__all__"
    success_url = reverse_lazy('yearwage_list')

class Updateyearwage(UpdateView):
    model = Yearwage
    fields = "__all__"
    template_name = "salary/yearwage_update_form.html"
    success_url = reverse_lazy('yearwage_list')

class Deleteyearwage(DeleteView):
    model = Yearwage
    template_name = "salary/work_confirm_delete.html"
    success_url=reverse_lazy('yearwage_list')


class Updateyukyu(UpdateView):
    model = total_yukyu
    fields = "__all__"
    template_name = "salary/yukyu_update_form.html"
    def get_success_url(self):
        return reverse_lazy("top", kwargs={"year_wage_id": 1})

class Updatezangyo(SuccessMessageMixin,UpdateView):
    model = Zangyo
    fields = "__all__"
    template_name = "salary/zangyo_update_form.html"
    success_message = "更新完了！"
    def get_success_url(self):
        return reverse_lazy("top", kwargs={"year_wage_id": 1})


