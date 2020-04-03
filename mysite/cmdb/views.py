from django.shortcuts import render
from cmdb import models
# Create your views here.
from django.shortcuts import HttpResponse


user_list = [
    {'user': 'Jack', 'pwd': 'abc'},
    {'user': 'tom', 'pwd': '123'}
]
def index(request):
    #request.POST
    #resuest.GET
    # return HttpResponse("Hello World")
    # return render(request, "index.html")
    if request.method =="POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # print(username, password)
        # temp = {'user':username, 'pwd':password}
        # user_list.append(temp)
        #添加数据到数据库
        models.UserInfo.objects.create(user = username, pwd = password)
    user_list = models.UserInfo.objects.all()
    return render(request, 'index.html',{'data':user_list})
