from  django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login.html")
def index(request):  ##首页
    return render(request, 'index.html')

def login_view(request):   #登陆
    if request.method == "GET":
        error_msg = "请登录"
        return render(request, 'login.html', {'error_msg': error_msg, })
    if request.method == "POST":
          u = request.POST.get("user")
          p = request.POST.get("password")
          user = authenticate(username=u, password=p)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  request.session['user'] = u
                  request.session['is_login'] =True
                  return redirect('/index.html')
              else:
                  error_msg1 = "用户名或密码错误,请重试"
                  return render(request, 'login.html', {'error_msg': error_msg1,})
          else:
                  error_msg1 = "用户名或密码错误,请重试"
                  return render(request, 'login.html', {'error_msg': error_msg1,})



def logout(requset):   #退出
    requset.session.clear()
    return  redirect('/login.html')



@login_required(login_url="/login.html")
def error(request):  ##错误页面
    return render(request, 'error.html')



