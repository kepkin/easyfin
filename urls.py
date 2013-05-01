from django.conf.urls import patterns, url

urlpatterns = patterns('easyfin.views',
    url(r'^$', 'index'),
    url(r'^lala$', 'lala'),
    url(r'^debug$', 'debug'),
    url(r'^expenses$', 'getExpenses'),
    url(r'^ch_expense$', 'changeExpense'),
    url(r'^updateExpense$', 'updateExpense'),
    url(r'^newExpense$', 'newExpense'),
    url(r'^upload_file$', 'upload_file'),
    url(r'^getMoneyList$', 'getMoneyList'),
    #url(r'^(?P<poll_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
