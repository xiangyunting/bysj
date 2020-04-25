from functools import wraps

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from Doctor.code import gene_code
from Doctor.models import Doctor


def Login_Validation(func):
    @wraps(func)
    def inner(self, request, *args, **kwargs):
        content = func(self, request, *args, **kwargs)
        try:
            # request.session.get("onlineuser", "")
            # print(request.session["onlineuser"]) #KeyError
            # print(request.session["onlineuser"]).dusername  #KeyError
            s = request.session.get("onlineuser","").dusername  #AttributeError:
            return content
        except AttributeError:
            return redirect('/doctor/login')
    return inner


class LoginView(View):
    def get(self, request):
        # 获取cookies
        if "doctoruser" in request.COOKIES and "doctorpwd" in request.COOKIES:
            # 不加盐
            username = request.COOKIES.get("doctoruser")
            # 加盐
            password = request.get_signed_cookie("doctorpwd", salt="xyt")
            return render(request, 'login.html', {"doctoruser": username, "doctorpwd": password})
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('doctoruser', '').strip()  # 取不到，返回空
        password = request.POST.get('doctorpwd', '').strip()  # 取不到，返回空
        flag = request.POST.get('flag', '').strip()  # 取不到，返回空
        print(username, password, flag)
        doctorList = Doctor.objects.filter(dusername=username, dpassword=password)
        # 判断
        if username and password:
            if doctorList.count() == 1:  # .objects.filter()取得匹配结果
                response = HttpResponseRedirect('/doctor/operate/')
                request.session['onlineuser'] = doctorList[0]
                if flag:
                    # 不加盐
                    response.set_cookie("doctoruser", username, max_age=30 * 24 * 60 * 60, path="/doctor/login/")
                    # 加盐
                    response.set_signed_cookie("doctorpwd", password, salt="xyt", max_age=30 * 24 * 60 * 60,
                                               path="/doctor/login/")
                return response
            # else:
            #     response = HttpResponseRedirect('/doctor/login/', reverse('error:error'))
            #     response.delete_cookie("doctoruser", path="/doctor/login/")
            #     response.delete_cookie("doctorpwd", path="/doctor/login/")
            #     response.content="登录失败"
            #     return response
        return render(request, 'login.html', {"errors": "登录失败"})


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', )

    def post(self, request):
        username = request.POST.get('doctoruser', '').strip()  # 取不到，返回空
        password = request.POST.get('doctorpwd', '').strip()  # 取不到，返回空
        print(username, password)
        if username and password:
            # # 创建模型对象
            # doctor = Doctor(dusername=username, dpassword=password)
            # # 插入数据库
            # doctor.save()
            Doctor.objects.create(dusername=username, dpassword=password)
            return HttpResponse('注册成功！')
        return HttpResponse('注册失败！')


class CheckUname(View):
    def get(self, request):
        # 获取请求参数
        uname = request.GET.get('uname', '')
        # 根据用户名去数据库中查询
        userList = Doctor.objects.filter(dusername=uname)

        flag = False

        # 判断是否存在
        if userList:
            flag = True

        return JsonResponse({'flag': flag})


class OperateView(View):
    def get(self, request):
        return render(request, 'operate.html')


class LogoutView(View):
    def post(self, request):
        # 删除session中登录用户信息
        if 'onlineuser' in request.session:
            del request.session['onlineuser']

        return JsonResponse({'delflag': True})


class LoadCodeView(View):
    def get(self, request):
        img, strs = gene_code()
        # 将生成的验证码存放至session中
        request.session['sessionCode'] = strs
        return HttpResponse(img, content_type='image/png')


class CheckCodeView(View):
    def get(self, request):
        # 获取输入框中的验证码
        code = request.GET.get('code', '')
        # 获取生成的验证码
        sessionCode = request.session.get('sessionCode', None)
        # 比较是否相等
        flag = code == sessionCode
        return JsonResponse({'checkFlag': flag})


class LoginRedirect(View):
    def get(self, request):
        return redirect('/doctor/login')
