# Create your views here.
from easyfin.models import MoneyHolder, Period, RegularExpenses
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core import serializers
import json
import datetime
from exceptions import Exception

def index(request):
    latest_poll_list = RegularExpenses.objects.all()
    t = loader.get_template('easyfin/index.html')
    c = RequestContext(request, {
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

def lala(request):
    data = []
    for o in RegularExpenses.objects.all():
        c = o.money.get_income(Period.this_month())
        data.append("{0}.{1}".format(*c))
    json_data = serializers.serialize("json", RegularExpenses.objects.all())
    return HttpResponse(json_data, content_type="application/json")

def debug(request):
    p = Period.this_month()
    mh = MoneyHolder.objects.get(pk=2)
    data = mh.get_income(p)
    return HttpResponse(json.dumps(data), content_type="application/json")

def getExpenses(request):
    data = []
    p = Period.this_month()
    for i in RegularExpenses.objects.all():
        plan = "{0}.{1}".format(i.amount, i.cents)
        real = "{0}.{1}".format(*i.money.get_income(p))
        data.append({'pk': i.pk, 'name': i.money.name, 'plan': plan, 'real': real})
    return HttpResponse(json.dumps(data), content_type="application/json")

def updateExpense(request):
    amount, cents = request.POST['plan'].split(".")
    amount = int(amount)
    cents = int(cents)
    
    data = RegularExpenses.objects.get(pk=request.POST['pk'])
    data.money.name = request.POST['name']
    data.amount = amount
    data.cents = cents
    data.money.save()
    data.save()
    
    return HttpResponse("", content_type="application/json")

def newExpense(request):
    amount, cents = request.POST['plan'].split(".")
    amount = int(amount)
    cents = int(cents)
    
    m = MoneyHolder.objects.create(name=request.POST['name'], initial=0, amount=0, cents=0)
    p = RegularExpenses.objects.create(money=m, amount=amount, cents=cents, start=datetime.date.today(), stop=datetime.date.today())
    
    return HttpResponse("", content_type="application/json")

def AlfaBankRowToHash(row):
    row = row.split(';')
    result_row = {}
    result_row['date'] = row[3]
    result_row['comment'] = row[5]
    result_row['income'] = row[6]
    result_row['outcome'] = row[7]
    return result_row

def upload_file(request):
    if request.method != 'POST':
        return HttpResponse("", content_type="application/json")
    
    file_data = request.FILES['file']
    data = reduce(lambda x,y: x + y.decode('cp1251'), file_data, u"")
    
    arr = data.split("\n")
    arr.remove("")
    del arr[0]
    
    result_arr = map(AlfaBankRowToHash, arr)
    result_arr.sort(lambda x,y: cmp(x['comment'],y['comment']))
    
    file_response = {}
    file_response['name'] = 'lala'
    file_response['data'] = result_arr
    test_response = {}
    test_response['files']=[]
    test_response['files'].append(file_response)
    
    return HttpResponse(json.dumps(test_response), content_type="application/json")

def changeExpense(request):
    
    return HttpResponse(str(request.GET), content_type="application/json")
