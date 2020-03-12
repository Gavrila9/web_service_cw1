from django.shortcuts import render
from django.http import HttpResponse
from rating_system import models
from decimal import *
import json

def index(request):
    return HttpResponse("Hello, world. You're at the rating_system index.")
def professer_id_list(self):
    return ','.join([i.professor_id for i in self.taughtBy.all()])
def showMoudles(request):
    # if request.session.get("userName")== None:
    #     return HttpResponse("please login or register first")
    # print(request.session.get("userName"))
    modules_list = models.Moudles.objects.all()
    professors = models.Professors.objects.all()
    outList = list()
    professorsList = list()
    for e in modules_list:
        # print(e)
        # print(professer_id_list(e))
        for id in professer_id_list(e).split(","):
            professorsList.append(professors.get(professor_id=id).__str__())
        dict = {"Code":e.code, "Name":e.name, "Year":e.year, "Semester":e.semester,"Taught by":professorsList}
        outList.append(dict)
    return HttpResponse(json.dumps(outList))

def showRatings(request):
#     if request.session.get("userName")== None:
#         return HttpResponse("please login or register first")
    professors = models.Professors.objects.all()
    ratings = models.Rating.objects.all()
    ratings_list =list(ratings.values_list('professer_id'))
    temp_rating_list=list()
    cal_rating_list = list()
    for id in ratings_list:
        if id not in temp_rating_list:
            temp_rating_list.append(id)
    for id in temp_rating_list:
        cal_rating_list.append(models.Rating.objects.filter(professer_id=id))
    cal_list = list()
    for items in cal_rating_list:
        total_star = 1
        number = 0;
        p_id = 0;
        for idx,item in enumerate(items):
            total_star+=int(item.stars)
            number = idx+1
            p_id = item.professer_id
        p_list = list(models.Professors.objects.filter(id=p_id))
        avg_star = str(int(Decimal(total_star / number).quantize(Decimal('1'), rounding=ROUND_HALF_UP))*'*')
        cal_list.append("The rating of Professpr " + p_list[0].first_name + "." + p_list[0].last_name + " (" + p_list[0].professor_id + ") is:" + avg_star)
    return HttpResponse(cal_list)
def showRatings4Moudles(request):
    # if request.session.get("userName")== None:
    #     return HttpResponse("please login or register first")
    professor_id = request.GET.get('professor_id',None)
    module_code = request.GET.get('module_code',None)
    print(professor_id,module_code)
    if professor_id ==None or module_code==None:
        return HttpResponse("please make sure all input params are not null")
    try:
        ratings = list(models.Rating.objects.filter(professer__professor_id=professor_id,professer__moudles__code=module_code))
        print(ratings)
        p = list(models.Professors.objects.filter(professor_id=professor_id))
        m = list(models.Moudles.objects.filter(code=module_code))
    except:
        return HttpResponse("please make sure professor_id and module_code are correct")
    total_star = 0
    number = 0;
    # p_id = 0;
    out_list = list()
    for idx,item in enumerate(ratings):
        total_star += int(item.stars)
        number = idx + 1
    avg_star = str(int(Decimal(total_star / number).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) * '*')
    out_list.append("The rating of Professor " + p[0].first_name + "." + p[0].last_name + " (" + p[
        0].professor_id + ") in "+ m[0].name+"("+m[0].code+") "+" is:" + avg_star)
    return HttpResponse(out_list)
def login(request):
    username = request.GET.get('userName',None)
    password = request.GET.get('password',None)
    if username and password:
        username = username.strip()
        try:
            user = models.Users.objects.get(userName=username)
        except:
            return HttpResponse("Not exist user,please reigister first")
        if user.password == password:
            # request.session['userName'] = user.userName
            try:
                models.Users.objects.filter(userName=user.userName).update(is_active='1')
            except:
                return HttpResponse("is_active update failed")
            return HttpResponse("login success, welcome "+user.userName)
        return HttpResponse("wrong password, please try again")
    return HttpResponse("please make sure your input params are not null")
def loginOut(request):
    user_list = list(models.Users.objects.all())
    for item in user_list:
        models.Users.objects.filter(userName=item.userName).update(is_active='0')
    return HttpResponse("login out success")
def register(request):
    username = request.GET.get("userName",None)
    if username:
        try:
            user = models.Users.objects.get(userName=username)
        except models.Users.DoesNotExist:
            user = None
        if user!=None:
            return  HttpResponse("this user name has registered,please use another one")
    else:
        return HttpResponse("please input username")
    password = request.GET.get("password",None)
    email = request.GET.get("email",None)
    if password and email:
        try:
            u = models.Users(userName=username,password=password,email=email)
            u.save()
            return HttpResponse("register success")
        except:
            return HttpResponse("insert wrong")
    return HttpResponse("please input password or email")

def rate(request):
    user_list = list(models.Users.objects.all())
    active_list = list()
    for item in user_list:
        if item.is_active == '1':
            active_list.append(item.userName)
            active_list.append('1')
    if '1' not in active_list:
        return HttpResponse("please login or register first")
    professor_id = request.GET.get("professor_id",None)
    module_code = request.GET.get("module_code",None)
    year = request.GET.get("year", None)
    semester = request.GET.get("semester", None)
    rating = request.GET.get("rating", None)
    print(professor_id,module_code,year,semester,rating)
    if professor_id ==None or module_code==None or year==None or semester==None or rating ==None:
        return HttpResponse("please make sure all input params are not null")
    try:
        stars = int(rating)
        print(stars)
        if stars <1 or stars>5:
            return HttpResponse("please input a int param which is in range of 1 to 5")
    except:
        return HttpResponse("please input a int param")
    try:
        p = models.Professors.objects.get(professor_id=professor_id)
    except models.Professors.DoesNotExist:
        return HttpResponse("the professor is not in the school list yet")
    try:
        m =models.Moudles.objects.get(code=module_code,year=year,semester=semester)
    except models.Moudles.DoesNotExist:
        return HttpResponse("the module is not in the school's moudle list")
    r = models.Rating(professer=p,stars=stars,module=m)
    r.save()
    return HttpResponse("rating success")

def showRatings4MoudlesYearSemester(request):
    # if request.session.get("userName")== None:
    #     return HttpResponse("please login or register first")
    ratings = list(models.Rating.objects.filter(professer__professor_id="JE1",professer__moudles__code="CD1",module__year='2017',module__semester='1'))
    try:
        p = list(models.Professors.objects.filter(professor_id="JE1"))
    except models.Professors.DoesNotExist:
        return HttpResponse("the professor is not in the school list yet")
    try:
        m = list(models.Moudles.objects.filter(code='CD1',year='2017',semester='1'))
    except:
        return HttpResponse("the module is not in the school's moudle list")
    total_star = 0
    number = 0;
    # p_id = 0;
    out_list = list()
    for idx,item in enumerate(ratings):
        total_star += int(item.stars)
        number = idx + 1
    avg_star = str(int(Decimal(total_star / number).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) * '*')
    out_list.append("The rating of Professor " + p[0].first_name + "." + p[0].last_name + " (" + p[
        0].professor_id + ") in "+ m[0].name+"("+m[0].code+") "+"in " +m[0].year+" at semester"+m[0].semester+" is:" + avg_star)
    return HttpResponse(out_list)


