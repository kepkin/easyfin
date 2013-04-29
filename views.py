# Create your views here.
from easyfin.models import MoneyHolder, Period, RegularExpenses
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core import serializers
import json
import datetime
from exceptions import Exception
from collections import defaultdict

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
    
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    
    p = Period.specific_month(year, month)
    for i in RegularExpenses.actual(p):
        plan = "{0}.{1}".format(i.amount, i.cents)
        real = "{0}.{1}".format(*i.money.get_income(p))
        data.append({'pk': i.pk, 'name': i.money.name, 'plan': plan, 'real': real})
    return HttpResponse(json.dumps(data), content_type="application/json")

def updateExpense(request):
    amount, cents = request.POST['plan'].split(".")
    amount = int(amount)
    cents = int(cents)
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    
    data = RegularExpenses.objects.get(pk=request.POST['pk'])
    
    per = Period.specific_month(year, month)
    data.Update(amount, cents, per.date_from)
    
    return HttpResponse("", content_type="application/json")

def newExpense(request):
    amount, cents = request.POST['plan'].split(".")
    amount = int(amount)
    cents = int(cents)
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    
    per = Period.specific_month(year, month)
    m = MoneyHolder.objects.create(name=request.POST['name'], initial=0, amount=0, cents=0)
    p = RegularExpenses.objects.create(money=m, amount=amount, cents=cents, start=per.date_from, stop=None)
    
    return HttpResponse("", content_type="application/json")

def AlfaReduce(result, row):
    def GetShortComment(comment):
        return " ".join([i for i in comment.split(" ") if not i == ''][1:-4])
    
    result_row = {}
    result_row['raw'] = row
    row = row.split(';')
    
    result_row['date'] = row[3]
    result_row['short_comment'] = GetShortComment(row[5])
    result_row['comment'] = row[5]
    # TODO: float is incorrect for money
    result_row['income'] = float(row[6].replace(",", "."))
    result_row['outcome'] = float(row[7].replace(",", "."))
    
    result[AlfaCategory(result_row['comment'])].append(result_row)
    return result
    
def AlfaCategory(comment):
    if comment.find("PEREK") != -1:
        return "food"
    else:
        return "unknown"
    
    
def upload_file(request):
    if request.method != 'POST':
        return HttpResponse("", content_type="application/json")
    
    file_data = request.FILES['file']
    #data = reduce(lambda x,y: x + y.decode('cp1251'), file_data, u"")
    
    def ignoreEmptyLine(x,y, delegate):
        if y != "":
            return delegate(x,y)
        else:
            return x
    
    #arr = data.split("\n")
    #arr.remove("")
    #del arr[0]
    
    #result_arr = map(AlfaBankRowToHash, arr)
    #result_arr = reduce(AlfaReduce, arr, defaultdict(list))
    #result_arr.sort(lambda x,y: cmp(x['comment'],y['comment']))
    file_iter = file_data.__iter__() #ignore title
    file_iter.next()
    result_arr = reduce(lambda x,y: ignoreEmptyLine(x,y.decode('cp1251'),AlfaReduce), file_iter, defaultdict(list))
    
    file_response = {}
    file_response['data'] = []
    
    for k,v in result_arr.iteritems():
        new_v = {}
        
        new_v['category'] = k
        new_v['data'] = v
        file_response['data'].append(new_v)
    
    file_response['name'] = 'lala'
    test_response = {}
    test_response['files']=[]
    test_response['files'].append(file_response)
    
    return HttpResponse(json.dumps(test_response), content_type="application/json")

def changeExpense(request):
    
    return HttpResponse(str(request.GET), content_type="application/json")
