import math
from datetime import datetime, timedelta

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from Doctor.views import Login_Validation
from Donor.models import Donor, Person, BloodType, Blood, BloodVolume, BloodComponent


# Create your views here.

# 添加献血者

class AddDonorView(View):
    @Login_Validation
    def get(self, request, donorid=""):
        return render(request, "adddonor.html", {"donorid": donorid})

    def post(self, request):
        donorid = request.POST.get('donorid', '').strip()
        donorname = request.POST.get('donorname', '').strip()
        # websex = request.POST.get('sex', '').strip()
        # webbirth = request.POST.get('birth', '').strip()

        bloodtype = request.POST.get('bloodtype', '').strip()
        mobile = int(request.POST.get('mobile', '').strip())
        address = request.POST.get('address', '').strip()
        sex = int(donorid[-2:-1])
        if sex % 2 == 1:
            sex = '男'
        else:
            sex = '女'
        birth = "{}-{}-{}".format(donorid[6:10], donorid[10:12], donorid[12:14])
        responsible = request.POST.get('responsible', '').strip()
        # print(websex, webbirth)
        # print(donorid, donorname, sex, birth, bloodtype, mobile, address, responsible)

        btype = BloodType.objects.get_or_create(bloodtype=bloodtype)
        # print(btype[0])

        try:
            Person.objects.get(mobile=mobile)
            return render(request, "adddonor.html", {"Error": "已有手机号"})
        except Person.DoesNotExist:
            donor = Donor.objects.get_or_create(donorid=donorid, donorname=donorname, sex=sex, birth=birth,
                                                bloodtype=btype[0])
            person = Person.objects.get_or_create(donor=donor[0], mobile=mobile, address=address,
                                                  personresponsible=responsible)
            # print(person)
            return render(request, "operate.html",{'result': "注册献血者成功"})


# 判断用户id是否存在
def CheckUserId(request):
    if request.method == 'GET':
        # 获取请求参数
        donorid = request.GET.get('donorid', '').strip()
        # print(donorid)
        # 根据献血者的身份证号去数据库中查询
        donoridList = Donor.objects.filter(donorid=donorid)
        flag = False
        # 判断是否存在
        if donoridList:
            flag = True
            # 根据献血者的身份证号获取献血者的姓名
            donorname = donoridList[0].donorname
            bloodtype = donoridList[0].bloodtype.bloodtype
            mobile = str(donoridList[0].person.mobile)
            address = donoridList[0].person.address
            # print(donorname, bloodtype, mobile, address)
            return JsonResponse(
                {'flag': flag, 'donorname': donorname, "bloodtype": bloodtype, "mobile": mobile, "address": address})
        return JsonResponse({'flag': flag})


# 判断血液是否存在
def CheckBloodId(request):
    if request.method == 'GET':
        # 获取请求参数
        bloodid = request.GET.get('bloodid', '').strip()
        # print(donorid)
        # 根据血液的bloodid去数据库中查询
        bloodidList = Blood.objects.filter(bloodid=bloodid)
        # 判断是否存在
        flag = False
        if bloodidList:
            flag = True
            # 根据血液的bloodid获取献血者的姓名
            donorid = bloodidList[0].blooddonor.donorid
            donorname = bloodidList[0].blooddonor.donorname
            bloodtype = bloodidList[0].blooddonor.bloodtype.bloodtype
            bloodplace = bloodidList[0].bloodplace
            bloodvolume = str(bloodidList[0].bloodvolume.bloodvolume)
            bloodcomponent = bloodidList[0].bloodcomponent.bloodcomponent
            bloodtime = bloodidList[0].bloodcreate
            # print(donorid, donorname, bloodtype, bloodplace, bloodvolume, bloodcomponent, bloodtime)
            return JsonResponse(
                {'flag': flag, 'donorid': donorid, 'donorname': donorname, "bloodtype": bloodtype,
                 'bloodplace': bloodplace, 'bloodvolume': bloodvolume, 'bloodcomponent': bloodcomponent,
                 "bloodtime": bloodtime})
        return JsonResponse({'flag': flag})


# 修改献血者
class ChangeDonor(View):
    @Login_Validation
    def get(self, request, donorid=""):
        # print(donorid)
        return render(request, "changedonor.html", {"donorid": donorid})

    def post(self, request):
        donorid = request.POST.get('donorid', '').strip()
        donorname = request.POST.get('donorname', '').strip()
        bloodtype = request.POST.get('bloodtype', '').strip()
        mobile = int(request.POST.get('mobile', '').strip())
        address = request.POST.get('address', '').strip()
        sex = int(donorid[-2:-1])
        if sex % 2 == 1:
            sex = '男'
        else:
            sex = '女'
        birth = "{}-{}-{}".format(donorid[6:10], donorid[10:12], donorid[12:14])
        responsible = request.POST.get('responsible', '').strip()
        # print(donorid, donorname, sex, birth, bloodtype, mobile, address, responsible)
        btype = BloodType.objects.get_or_create(bloodtype=bloodtype)
        # print(btype[0])
        if donorid != Person.objects.filter(mobile=mobile)[0].donor_id:
            return render(request, "changedonor.html", {"Error": "已有手机号"})
        else:
            Donor.objects.filter(donorid=donorid).update(donorname=donorname, sex=sex, birth=birth, bloodtype=btype[0])
            # update()仅返回成功1，失败0
            # Donor.objects.get(donorid=donorid)    #返回对象
            donor = Donor.objects.filter(donorid=donorid)  # 返回列表
            # 总之 Donor.objects.filter()[0]==Donor.objects.get()
            person = Person.objects.filter(donor=donor[0]).update(mobile=mobile, address=address,
                                                                  personresponsible=responsible)
            print(person)
            return render(request, "operate.html", {'result': "修改献血者成功"})


# 查询献血者
class CheckDonor(View):
    @Login_Validation
    def get(self, request, num=1, size=8, showpage=5):  # size显示多少条 #showpage显示多少页

        searchid = request.GET.get('searchid', "").strip()
        searchname = request.GET.get('searchname', "").strip()
        if searchid != "":
            donors = Donor.objects.filter(donorid__contains=searchid).order_by('-person__modify')
        elif searchname != "":
            donors = Donor.objects.filter(donorname__contains=searchname).order_by('-person__modify')
        else:
            donors = Donor.objects.all().order_by('-person__modify')



        # 当前页内容对象
        pager = Paginator(donors, size)

        # try:
        #     perpage_data = pager.page(num)  # 返回当前页数据
        # except PageNotAnInteger:
        #     perpage_data = pager.page(1)  # 返回第一页数据
        # except EmptyPage:
        #     perpage_data = pager.page(pager.num_pages)  # 返回最后一页数据
        perpage_data = pager.get_page(num)  # 整合上面的内容
        # 开始页数
        begin = num - int(math.ceil(showpage / 2.0)) + 1
        if begin < 1:
            begin = 1
        # 结束页数
        end = begin + showpage - 1

        if end > pager.num_pages:
            end = pager.num_pages
        if end <= showpage:
            begin = 1
        else:
            begin = end - showpage + 1

        pagelist = range(begin, end + 1)
        return render(request, "donortable.html",
                      {'perpage_data': perpage_data, 'pager': pager, 'currentpage': num, 'pagelist': pagelist,
                       "png": "img/sousuo.png","searchid":searchid,'searchname':searchname})


# 添加血液
class AddBlood(View):
    @Login_Validation
    def get(self, request, donorid=""):
        return render(request, "addblood.html", {"donorid": donorid})

    def post(self, request):
        donorid = request.POST.get('donorid', '').strip()
        bloodvolume = int(request.POST.get('bloodvolume', '').strip())
        bloodcomponent = request.POST.get('bloodcomponent', '').strip()
        bloodtime = request.POST.get('bloodtime', '').strip()
        bloodplace = request.POST.get('bloodplace', '').strip()
        responsible = request.POST.get('responsible', '').strip()

        print(donorid, bloodvolume, bloodcomponent, bloodplace, responsible)

        blooddonor = Donor.objects.filter(donorid=donorid)
        bvolume = BloodVolume.objects.get_or_create(bloodvolume=bloodvolume)
        bcomponent = BloodComponent.objects.get_or_create(bloodcomponent=bloodcomponent)
        print(blooddonor[0], bvolume[0], bcomponent[0])
        blood = Blood.objects.create(blooddonor=blooddonor[0], bloodvolume=bvolume[0], bloodcomponent=bcomponent[0],
                                     bloodplace=bloodplace, bloodresponsible=responsible, bloodcreate=bloodtime)
        print(blood)
        return render(request, "operate.html", {'result': "添加献血记录成功"})


# 查询血液
class CheckBlood(View):
    @Login_Validation
    def get(self, request, num=1, size=8, showpage=5):# size显示多少条 #showpage显示多少页

        searchid = request.GET.get('searchid', "").strip()
        searchname = request.GET.get('searchname', "").strip()
        if searchid != "":
            bloods = Blood.objects.filter(blooddonor__donorid__contains=searchid).order_by('-bloodmodify')
        elif searchname != "":
            bloods = Blood.objects.filter(blooddonor__donorname__contains=searchname).order_by('-bloodmodify')
        else:
            bloods = Blood.objects.all().order_by('-bloodmodify')

        # print(bloods)

        # 当前页内容对象
        pager = Paginator(bloods, size)
        perpage_data = pager.get_page(num)  # 返回当前页数据

        # 开始页数
        begin = num - int(math.ceil(showpage / 2.0)) + 1
        if begin < 1:
            begin = 1
        # 结束页数
        end = begin + showpage - 1

        if end > pager.num_pages:
            end = pager.num_pages
        if end <= showpage:
            begin = 1
        else:
            begin = end - showpage + 1

        pagelist = range(begin, end + 1)
        now = datetime.now().date()
        #delta = datetime(2020, 7, 1) - datetime(2020, 1, 3) #180天
        delta=timedelta(days=180)
        oldday = now -delta
        # print(oldday)
        return render(request, "bloodtable.html",
                      {'perpage_data': perpage_data, 'pager': pager, 'currentpage': num, 'pagelist': pagelist,
                       "png": "img/sousuo.png",'oldday':oldday,"searchid":searchid,'searchname':searchname})


# 删除献血者
class DeleteDonor(View):
    @Login_Validation
    def get(self, request, donorid, num=1):
        deldonor = Donor.objects.filter(donorid=donorid).delete()
        print(deldonor)
        return redirect('/donor/checkdonor/{}'.format(num))


# 删除血液
class DeleteBlood(View):
    @Login_Validation
    def get(self, request , bloodid, num=1):
        delblood = Blood.objects.filter(bloodid=bloodid).delete()
        print(delblood)
        return redirect('/donor/checkblood/{}'.format(num))


class ChangeBlood(View):
    @Login_Validation
    def get(self, request, bloodid=""):
        return render(request, "changeblood.html", {"bloodid": bloodid})

    def post(self, request, ):
        bloodid = int(request.POST.get('bloodid', '').strip())
        donorid = request.POST.get('donorid', '').strip()
        bloodplace = request.POST.get('bloodplace', '').strip()
        bloodvolume = int(request.POST.get('bloodvolume', '').strip())
        bloodcomponent = request.POST.get('bloodcomponent', '').strip()
        bloodtime = request.POST.get('bloodtime', '').strip()
        print('blooddonor')
        print(bloodid, donorid, bloodplace, bloodvolume, bloodcomponent, bloodtime)
        blooddonor = Donor.objects.filter(donorid=donorid)
        print('blooddonor')
        bvolume = BloodVolume.objects.get_or_create(bloodvolume=bloodvolume)
        bcomponent = BloodComponent.objects.get_or_create(bloodcomponent=bloodcomponent)
        print(blooddonor[0], bvolume[0], bcomponent[0])

        blood = Blood.objects.filter(bloodid=bloodid).update(blooddonor=blooddonor[0], bloodcreate=bloodtime,
                        bloodplace=bloodplace, bloodvolume=bvolume[0], bloodcomponent=bcomponent[0])
        print(blood)
        return render(request, "operate.html", {'result': "修改献血记录成功"})
