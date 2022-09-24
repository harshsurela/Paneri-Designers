from datetime import date, datetime,timedelta
from email.message import Message
import soundfile
from django.db.models import Q
from paneri.settings import BASE_DIR
import os
import fleep
from django.db.models import IntegerField, Value
import wave
import math

from os import path
from this import d
from time import time
from xml.dom.minidom import Element
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from scipy.io.wavfile import write
import customer
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import  send_mail
from django.conf import settings
from django.core.paginator import Paginator
from io import BytesIO
#from xhtml2pdf import pisa
from django.template.loader import get_template
from django.core.files import File
from django.http import FileResponse
import random
from django.utils import timezone
from dateutil.relativedelta import relativedelta, MO
import librosa
from pathlib import Path
import speech_recognition as sr


# Create your views here.
def checksuper(request):
    if request.user.is_staff==True:
        logout(request)
def checklocal(request):
    if request.user.is_staff==False:
        logout(request)

# Accounts Views Goes Here...
def registration(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        upass = request.POST.get('pass')
        ucpass = request.POST.get('cpass')
        email = request.POST.get('email')
        if upass != ucpass:
            print("Inside")
            messages.warning(request, "Password Has To Be same")
            return redirect("registration")
        try:
            user = User.objects.get(username=uname)
            messages.warning(request, "User Already Registered !!")
            return redirect("registration")

        except Exception as e:
            print(e)
            user = User.objects.create_user(
                username=uname, password=upass, email=email)
            user.is_staff = True
            user.is_superuser=True
            user.save()
            login(request, user)
            request.session.set_expiry(0)
            return redirect("registration_2")
    else:
        return render(request, "accounts/sign-up2.html")


def registration_2(request):

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        print(user)
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        # email=request.POST.get('email')
        profile = request.FILES['profile']
        add1 = request.POST.get('add1')
        try:
            area_id = Area(request.POST.get('area'))
        except Exception as e:
            print(e)
        print(area_id)
        UserBaseInstance = UserBase()
        UserBaseInstance.first_name = fname
        UserBaseInstance.last_name = lname
        if gender == "male":
            UserBaseInstance.gender = True
        else:
            UserBaseInstance.gender = False
        UserBaseInstance.dob = dob
        UserBaseInstance.pincode = pincode
        UserBaseInstance.Cus_phone = phone
        # UserBaseInstance.cus_email=email
        UserBaseInstance.profile = profile
        UserBaseInstance.cus_add1 = add1
        UserBaseInstance.user_id = user
        # UserBaseInstance.user_id=uid
        UserBaseInstance.area_id = area_id
        UserBaseInstance.save()
        messages.success(request,"Registration Succesfull !")
        return render(request, "accounts/sign-in.html")
    country = Country.objects.all()
    return render(request, "accounts/sign-up.html", {"country": country, })


def signIn(request):
    if request.method == "POST":
        uname = request.POST['username']
        upass = request.POST['password']
        user = authenticate(username=uname, password=upass)
        if user is not None:
            if user.is_superuser==True:
                login(request, user)
                request.session.set_expiry(0)
                messages.success(request, "Login Successfull!")
                return redirect("index")
            else:
                messages.warning(request, "Invalid Username And Password!!")
                redirect("sign-in")
        else:
            messages.warning(request, "Invalid Username And Password!!")
            redirect("sign-in")
    return render(request, "accounts/sign-in.html")


@login_required(login_url='sign-in')
def index(request):
    checklocal(request)
    sales=SalesDetails.objects.all().count()
    purchase=PurchaseDetails.objects.all().count()
    users=UserBase.objects.filter(user_id__is_staff=False).count()
    app=Appointment.objects.filter(app_status=0).count()
    
    context={
        'sales':sales,
        'purchase':purchase,
        'users':users,
        'app':app,
    }
    return render(request, "Mainadmin/home.html",{"context":context})


def country_ajax_data(request):
    if request.method == "POST":
        c_id = request.POST.get("country_id")
        print(c_id)
        try:
            country = Country.objects.filter(id=c_id).first()
            print(country)
            state = State.objects.filter(country_id=country)
        except Exception:
            data = "Error"
            return JsonResponse(data)
        return JsonResponse(list(state.values('id','state_name')), safe=False)


def c_ajax_data(request):
    if request.method=="GET":
        try:
            country=Country.objects.all()
            try:    
                cartobj=Cart.objects.filter(userbase__user_id=request.user).count()
                if cartobj==0:
                    cartobj=""
            except Exception as e:
                print(e)
                cartobj=""
            data=list(country.values('id','country_name'))
            for d in data:
                d.update({'count':cartobj})
            print(data)
            # data.update(cartobj)
            return JsonResponse(data, safe=False)
        except Exception:
            data="Error"
            return JsonResponse(data)
def comp_data(request):
    if request.method=="GET":
        try:
            comp=Company.objects.all()
            return JsonResponse(list(comp.values('comp_name','comp_add','comp_phone','comp_email')), safe=False)
        except Exception:
            data="Error"
            return JsonResponse(data)
    
def saveappo(request):
    checksuper(request)
    if request.method=="POST":
        adate=request.POST.get("date")
        time=request.POST.get("time")
        desc=request.POST.get("desc")
        app=Appointment()
        app.app_date=adate
        app.app_time=time
        app.app_desc=desc
        user=UserBase.objects.get(user_id=request.user)
        app.userbase=user
        app.save()
        return redirect("home")
def usercheck(request):
    checksuper(request)
    if request.method=="POST":
        username = request.POST.get("username")
        try:
            user=User.objects.get(username=username)
            print(user)
            data=False
        except Exception :
            data=True
            return JsonResponse({'data':data})
        return JsonResponse({'data':data},safe=False)
def emailcheck(request):
    checksuper(request)
    if request.method=="POST":
        email = request.POST.get("email")
        try:
            user=User.objects.get(email=email)
            print(user)
            data=False
        except Exception :
            data=True
            return JsonResponse({'data':data})
        return JsonResponse({'data':data},safe=False)
            
def state_ajax_data(request):
    if request.method == "POST":
        s_id = request.POST.get("state_id")
        print(s_id)
        try:
            state = State.objects.filter(id=s_id).first()
            print(state)
            city = City.objects.filter(state_id=state)
        except Exception:
            data = "Error"
            return JsonResponse(data)
        return JsonResponse(list(city.values('id', 'city_name')), safe=False)


def city_ajax_data(request):
    if request.method == "POST":
        ct_id = request.POST.get("city_id")
        print(ct_id)
        try:
            city = City.objects.filter(id=ct_id).first()
            print(city)
            area = Area.objects.filter(city_id=city)
        except Exception:
            data = "Error"
            return JsonResponse(data)
        return JsonResponse(list(area.values('id', 'area_name')), safe=False)

def area_ajax_data(request):
    if request.method == "POST":
        area_id = request.POST.get("area_id")
        print(area_id)
        try:
           
            area = Area.objects.filter(id=area_id)
        except Exception:
            data = "Error"
            return JsonResponse(data)
        return JsonResponse(list(area.values('id', 'area_name')), safe=False)
# def test(request):
#     return render(request,"sign-in.html")

@login_required(login_url='sign-in')
def logout_user(request):
    if request.user.is_superuser:
        logout(request)
        messages.success(request, "Logout Successfull!!")
    return redirect("sign-in")

@login_required(login_url='sign-in')
def resetDone(request):
    return render(request, "accounts/reset-done.html")

@login_required(login_url='sign-in')
# Admin Views Goes Here...

def products(request):
    checklocal(request)
    category=Category.objects.all()
    cat=category.filter(cat_id__isnull=True)
    sub_cat=category.filter(cat_id__isnull=False)
    company=Company.objects.first()
    pcolor=ProductColor.objects.all()
    psize=ProductSize.objects.all()
    products=Product.objects.all()
    paginator=Paginator(products,5)
    page_number=request.GET.get('page')
    prod=paginator.get_page(page_number)
    
    return render(request,"Mainadmin/product.html",{'cat':cat,'sub_cat':sub_cat,'company':company,'pcolor':pcolor,'psize':psize,'products':prod})
@login_required(login_url='sign-in')
def addProduct(request):
    checklocal(request)
    if request.method == "POST":
        pname = request.POST.get('pname')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        qty = request.POST.get('qty')
        cat = request.POST.get('subcat')
        size = request.POST.get('size')
        color = request.POST.get('color')
        pimg = request.FILES["pimg"]
        company=request.POST.get('company')
        print(pname,desc,price,discount,qty,cat,size,color, pimg,company)
        product=Product()
        product.product_name=pname
        product.desc=desc
        product.price=price
        product.discount=discount
        product.qty_on_hand=qty
        product.cat_id=Category(cat)
        product.size_id=ProductSize(size)
        product.color_id=ProductColor(color)
        product.product_img=pimg
        product.company_id=Company(company)
        product.save()
        return redirect("products")
    return HttpResponse("Not A Post Request")
@login_required(login_url='sign-in')
def viewproduct(request,id):
    checklocal(request)
    product=Product.objects.get(pk=id)
    print(type(product))
    category=Category.objects.all()
    cat=category.filter(cat_id__isnull=True)
    sub_cat=category.filter(cat_id__isnull=False)
    company=Company.objects.first()
    pcolor=ProductColor.objects.all()
    psize=ProductSize.objects.all()
    return render(request,"Mainadmin/view_added_product.html",{'cat':cat,'sub_cat':sub_cat,'company':company,'pcolor':pcolor,'psize':psize,"product":product})

@login_required(login_url='sign-in')
def deleteRecord(request,id):
    checklocal(request)
    pi=Product.objects.get(pk=id)
    pi.delete()
    return redirect("products")
def cat_ajax_data(request):
    if request.method=="POST":
        try:
            cat_id = request.POST.get("cat_id")
            print(cat_id)
            sub_cat=Category.objects.filter(cat_id=cat_id)
            print(sub_cat)
            return JsonResponse(list(sub_cat.values('id', 'cat_name')), safe=False)
        except Exception as e:
            print(e)
    return redirect("index")
@login_required(login_url='sign-in')
def updateproduct(request,id):
    checklocal(request)
    if request.method == "POST":
        pname = request.POST.get('pname')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        qty = request.POST.get('qty')
        cat = request.POST.get('subcat')
        size = request.POST.get('size')
        color = request.POST.get('color')
        pimg = request.FILES["pimg"]
        company=request.POST.get('company')
        print(pname,desc,price,discount,qty,cat,size,color, pimg,company)
        product=Product.objects.get(pk=id)
        product.product_name=pname
        product.desc=desc
        product.price=price
        product.discount=discount
        product.qty_on_hand=qty
        product.cat_id=Category(cat)
        product.size_id=ProductSize(size)
        product.color_id=ProductColor(color)
        product.product_img=pimg
        product.company_id=Company(company)
        product.save()
        return redirect("products")
    return HttpResponse("Not POST")
@login_required(login_url='sign-in')
def cusProduct(request):
    checklocal(request)
    pcolor=ProductColor.objects.all()
    psize=ProductSize.objects.all()
    products=CustomizedProdoct.objects.all()
    paginator=Paginator(products,5)
    page_number=request.GET.get('page')
    prod=paginator.get_page(page_number)
    return render(request,"Mainadmin/add_cusmis_ord.html",{'pcolor':pcolor,'psize':psize,'products':prod})

@login_required(login_url='sign-in')
def addcusproduct(request):
    checklocal(request)
    if request.method=="POST":
        pname = request.POST.get('pname')
        desc = request.POST.get('pdesc')
        price = request.POST.get('price')
        size = request.POST.get('size')
        color = request.POST.get('color')
        pimg = request.FILES['cpimg']
        print(pname,desc,price,size,color,pimg)
        cusp=CustomizedProdoct()
        cusp.cus_productName=pname
        cusp.cus_productPrice=price
        cusp.cus_productDetails=desc
        cusp.cus_productImg=pimg
        cusp.color_id=ProductColor(color)
        cusp.size_id=ProductSize(size)
        cusp.save()
        return redirect("cusproduct")    
    return render(request,"Mainadmin/add_cusmis_ord.html")

@login_required(login_url='sign-in')
def viewcus(request,id):
    checklocal(request)
    product=CustomizedProdoct.objects.get(pk=id)
    return render(request,"Mainadmin/view_cusmis_ord.html",{'product':product})

@login_required(login_url='sign-in')
def delcus(request,id):
    checklocal(request)
    cp=CustomizedProdoct.objects.get(pk=id)
    cp.delete()
    return redirect("cusproduct")

@login_required(login_url='sign-in')
def customers(request):
    checklocal(request)
    customers=UserBase.objects.filter(user_id__is_staff=False)
    print(customers)
    paginator=Paginator(customers,5)
    page_number=request.GET.get('page')
    cus=paginator.get_page(page_number)
    print(cus)
    return render(request,"Mainadmin/cus.html",{'customers':cus})

@login_required(login_url='sign-in')
def customerdet(request,id):
    checklocal(request)
    print(id)
    customer=UserBase.objects.get(pk=id)
    orders=SalesDetails.objects.filter(sales_id__userbase__user_id=customer.user_id)
    main=[]
    p=0
    for i in orders:
        p=p+i.final_price
        main.append(p)
    # orders = orders.annotate(final=Value(main, output_field=IntegerField()))
    print(main)
    paginator=Paginator(orders,5)
    page_number=request.GET.get('page')
    order=paginator.get_page(page_number)
    context=zip(order, main)
    print(order)
    return render(request,"Mainadmin/cus_det.html",{'customer':customer,'orders':context})

@login_required(login_url='sign-in')
def gallary(request):
    checklocal(request)
    images=Gallary.objects.all()
    paginator=Paginator(images,4)
    page_number=request.GET.get('page')
    img=paginator.get_page(page_number)
    print(images)
    return render(request,"Mainadmin/gallary.html",{'images':img})

@login_required(login_url='sign-in')
def addimage(request):
    checklocal(request)
    if request.method=="POST":
        image=request.FILES['add']
        gl=Gallary()
        gl.gallary_img=image
        gl.save()
        return redirect("gallary")
    else:
        return redirect("gallary")

@login_required(login_url='sign-in')
def delimg(request,id):
    checklocal(request)
    img=Gallary.objects.get(pk=id)
    img.delete()
    return redirect("gallary")

@login_required(login_url='sign-in')
def vieworders(request):
    checklocal(request)
    orders=Sales.objects.filter(sales_status="pending").order_by('-id','sales_date')
    main=[]
    for i in orders:
        sd=SalesDetails.objects.filter(sales_id=i)
        p=0
        for j in sd:
            p=p+j.final_price
        main.append(p)
    # orders = orders.annotate(final=Value(main, output_field=IntegerField()))
    print(main)
    paginator=Paginator(orders,5)
    page_number=request.GET.get('page')
    order=paginator.get_page(page_number)
    context=zip(order, main)
    return render(request,"Mainadmin/view_rec_ord.html",{'order':context})

@login_required(login_url='sign-in')
def view_det_orders(request,id):
    checklocal(request)
    order=SalesDetails.objects.get(pk=id)
    return render(request,"Mainadmin/view_det_rec_ord.html",{'order':order})

@login_required(login_url='sign-in')
def delrorder(request,id):
    checklocal(request)
    order=SalesDetails.objects.get(pk=id)
    order.delete()
    return redirect("vieworders")

@login_required(login_url='sign-in')
def returnorder(request):
    checklocal(request)
    orders=SalesReturn.objects.all()
    rorder=SalesReturnDetails.objects.all()
    zip_data=list(zip(orders,rorder))
    paginator=Paginator(zip_data,5)
    page_number=request.GET.get('page')
    order=paginator.get_page(page_number)
    return render(request,"Mainadmin/ret_ord.html",{'context':order})

@login_required(login_url='sign-in')
def viewretorders(request,id):
    checklocal(request)
    order=SalesReturnDetails.objects.get(pk=id)
    sorder=SalesDetails.objects.get(sales_id=order.sales_id)
    return render(request,"Mainadmin/view_ret_ord.html",{'order':order,'sorder':sorder})

@login_required(login_url='sign-in')
def completeorder(request):
    checklocal(request)
    corders=Sales.objects.filter(sales_status="Delivered").order_by('-id','sales_date')
    main=[]
    for i in corders:
        sd=SalesDetails.objects.filter(sales_id=i)
        p=0
        for j in sd:
            p=p+j.final_price
        main.append(p)
    paginator=Paginator(corders,5)
    page_number=request.GET.get('page')
    corder=paginator.get_page(page_number)
    context=zip(corder,main)
    return render(request,"Mainadmin/comp_ord.html",{'orders':context})

@login_required(login_url='sign-in')
def viewcomporder(request,id):
    checklocal(request)
    orders=SalesDetails.objects.get(pk=id)
    return render(request,"Mainadmin/view_comp_ord.html",{'order':orders})

@login_required(login_url='sign-in')
def appointment(request):
    checklocal(request)
    appointment=Appointment.objects.all().order_by('-id')
    paginator=Paginator(appointment,5)
    page_number=request.GET.get('page')
    appoint=paginator.get_page(page_number)
    return render(request,"Mainadmin/appointment.html",{'appointment':appoint})


@login_required(login_url='sign-in')
def complaints(request):
    checklocal(request)
    complaint=Complaint.objects.all().order_by('-id')
    paginator=Paginator(complaint,5)
    page_number=request.GET.get('page')
    comp=paginator.get_page(page_number)
    return render(request,"Mainadmin/pen-comp.html",{'complaint':comp})

@login_required(login_url='sign-in')
def rescomp(request,id):
    checklocal(request)
    comp=Complaint.objects.get(id=id)
    return render(request,"Mainadmin/resolved_comp.html",{'comp':comp})

@login_required(login_url='sign-in')
def sendanswer(request,id):
    checklocal(request)
    cus=Complaint.objects.get(pk=id)
    answer=request.POST.get('answer')
    print(answer)
    subject="Regarding Your Complaint "+cus.title
    recipient=[cus.userbase.user_id.email]
    print(recipient,subject)
    try:
        send_mail( subject, answer, settings.EMAIL_HOST_USER, recipient )
        cus.com_resolve=True
        cus.save()
        return redirect("complaints")

    except Exception as e:
        print(e)
        return HttpResponse("Error")

@login_required(login_url='sign-in')
def filtercomp(request):
    checklocal(request)
    if request.method=="POST":
        compdate=request.POST.get('compdate')
        print(compdate)
        complaint=Complaint.objects.filter(com_date__iexact=compdate)
        paginator=Paginator(complaint,5)
        page_number=request.GET.get('page')
        comp=paginator.get_page(page_number)
        return render(request,"Mainadmin/pen-comp.html",{'complaint':comp})
    return redirect("complaints")
@login_required(login_url='sign-in')
def feedback(request):
    checklocal(request)
    feedback=Feedback.objects.all()
    ratings=Rating.objects.all()
    print(feedback)
    print(ratings)
    zip_data=list(zip(feedback,ratings))
    paginator=Paginator(zip_data,5)
    page_number=request.GET.get('page')
    feed=paginator.get_page(page_number)
    return render(request,"Mainadmin/feedback-rating.html",{'context':feed})

# def delfeed(request,fid,rid):
#     delf=Feedback.objects.get(id=fid)
#     drat=Rating.objects.get(id=rid)
#     delf.delete()
#     drat.delete()
#     return redirect("feedback")

@login_required(login_url='sign-in')
def viewfeed(request,fid,rid):
    checklocal(request)
    feed=Feedback.objects.get(id=fid)
    rat=Rating.objects.get(id=rid)
    return render(request,"Mainadmin/view_feed_rat.html",{'feed':feed,'rat':rat})

@login_required(login_url='sign-in')
def addsup(request):
    checklocal(request)
    if request.method=="POST":
        sname=request.POST.get('sname')
        shopname=request.POST.get('shopname')
        sphone=request.POST.get('sphone')
        semail=request.POST.get('semail')
        sadd=request.POST.get('sadd')
        area=request.POST.get('area')
        company=request.POST.get('company')
        print(area)
        print(company)
        try:
            sup=Supplier.objects.get(sup_name=sname).exists()
        except Exception as e:
            sup=Supplier()
            sup.sup_name=sname
            sup.sup_phone=sphone
            sup.shop_name=shopname
            sup.sup_email=semail
            sup.sup_add=sadd
            sup.area_id=Area(area)
            sup.comp_id=Company(company)
            sup.save()
            return redirect("supplier")

@login_required(login_url='sign-in')
def supplier(request):
    checklocal(request)
    sup=Supplier.objects.all()
    country = Country.objects.all()
    company=Company.objects.first()
    paginator=Paginator(sup,5)
    page_number=request.GET.get('page')
    supp=paginator.get_page(page_number)
    return render(request,"Mainadmin/supplier.html",{'sup':supp,'country':country,'company':company})

def purchase(request):
    sp=Supplier.objects.all()
    un=UnitOfMeasurement.objects.all()
    raw=RawMaterial.objects.all()
    return render(request,"Mainadmin/pur-n-pay.html",{'supp':sp,'raw':raw,'un':un})

@login_required(login_url='sign-in')
def sendorder(request,id):
    checklocal(request)
    context=request.POST.get('desc')
    sup=Supplier.objects.get(pk=id)
    subject="Regarding To Order For Raw Materials"
    recipient=[sup.sup_email]
    print(recipient,subject)
    try:
        send_mail( subject, context, settings.EMAIL_HOST_USER, recipient )
        return redirect("supplier")

    except Exception as e:
        print(e)
        return HttpResponse("Error")

@login_required(login_url='sign-in')
def adminprofile(request):
    checklocal(request)
    user=request.user
    activeUser=UserBase.objects.get(user_id=user.id)
    # print(activeUser)
    # print(user)
    return render(request,"Mainadmin/profile.html",{'user':activeUser})

@login_required(login_url='sign-in')
def appointmentResult(request,id):
    if request.method=="POST":
        app=Appointment.objects.get(pk=id)
        print(app)
        if request.POST.get("accept"):
            answer="Hello Dear, {} {} We Are Happy To Tell You That You Appointment On {} At {} Is Confirmed And You Can Visit The Shop According To Appointment ...Thank You So Much For Choosing Us!!".format(app.userbase.first_name,app.userbase.last_name,app.app_date,app.app_time)
            subject="Regarding Your Appointment In Paneri Designers"
            recipient=[app.userbase.user_id.email]
            try:
                send_mail( subject, answer, settings.EMAIL_HOST_USER, recipient )
                app.app_status=1
                app.save()
                return redirect("appointment")
            except Exception as e:
                print(e)
                return redirect("appointment")

        elif request.POST.get("reject"):
            answer="Hello Dear, {} {} We Are Sorry To Tell You That You Appointment On {} At {} Is Rejected By Admin..You Can Take Appointment On Some other Time ...Thank You So Much For Choosing Us!!".format(app.userbase.first_name,app.userbase.last_name,app.app_date,app.app_time)
            subject="Regarding Your Appointment In Paneri Designers"
            recipient=[app.userbase.user_id.email]
            try:
                send_mail( subject, answer, settings.EMAIL_HOST_USER, recipient )
                app.app_status=2
                app.save()
                return redirect("appointment")
            except Exception as e:
                print(e)
                return redirect("appointment")
        return redirect("appointment") 
def gen_reports(request):
    checklocal(request)
    report=reports.objects.all()
    return render(request,"Mainadmin/gen-reps.html",{'report':report})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    print(type(pdf))
    if not pdf.err:
       return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def rp(request):
    checklocal(request)
    if request.method=="POST":
       report=reports.objects.all()
       s_date=request.POST.get('sdate')
       e_date=request.POST.get('edate')
       about=request.POST.get("field")
  
       d=date.today()

       if about=="sales":

           if s_date != "" and e_date != "":
                start_date=datetime.strptime(s_date,'%Y-%m-%d' )
                end_date=datetime.strptime(e_date,'%Y-%m-%d' )
                sales=SalesDetails.objects.filter(sales_id__sales_date__gte=start_date,sales_id__sales_date__lte=end_date) 
           elif s_date != "" and e_date == "":
                start_date=datetime.strptime(s_date,'%Y-%m-%d' )
                sales=SalesDetails.objects.filter(sales_id__sales_date__gte=start_date) 
           elif s_date == "" and e_date != "":
                end_date=datetime.strptime(e_date,'%Y-%m-%d' )
                sales=SalesDetails.objects.filter(sales_id__sales_date__lte=end_date) 
           else:
                sales=SalesDetails.objects.all() 

           print(sales)
           cp=Company.objects.first()
           user=UserBase.objects.get(user_id=request.user)
           if sales.count()>0:
               return render(request,"invoices/order_report.html",{'data':sales,'d':d,'cp':cp,'user':user})
           else:
               messages.warning(request,"No Data Found")
               return redirect("gen_reports")
       elif about=="purchase":

            if s_date != "" and e_date != "":
                start_date=datetime.strptime(s_date,'%Y-%m-%d' )
                end_date=datetime.strptime(e_date,'%Y-%m-%d' )
                pur=PurchaseDetails.objects.filter(pur_id__pur_date__gte=start_date,pur_id__pur_date__lte=end_date) 
            elif s_date != "" and e_date == "":
                start_date=datetime.strptime(s_date,'%Y-%m-%d' )
                pur=PurchaseDetails.objects.filter(pur_id__pur_date__gte=start_date) 
            elif s_date == "" and e_date != "":
                end_date=datetime.strptime(e_date,'%Y-%m-%d' )
                pur=PurchaseDetails.objects.filter(pur_id__pur_date__lte=end_date) 
            else:
                pur=PurchaseDetails.objects.all()
            cp=Company.objects.first()
            user=UserBase.objects.get(user_id=request.user)
            if pur.count()>0:
               return render(request,"invoices/purchase_report.html",{'data':pur,'d':d,'cp':cp,'user':user})
            else:
               messages.warning(request,"No Data Found")
               return redirect("gen_reports")
       elif about=="customer":
            ord=[]
            if s_date != "" and e_date != "":
                start_date=datetime.strptime(s_date,'%Y-%m-%d' )
                end_date=datetime.strptime(e_date,'%Y-%m-%d' )
                cus=UserBase.objects.filter(user_id__is_staff=False,user_id__date_joined__gte=start_date,user_id__date_joined__lte=end_date) 
                cus_count=UserBase.objects.filter(user_id__is_staff=False,user_id__date_joined__gte=start_date,user_id__date_joined__lte=end_date).count() 
                for c in cus:
                    orders=Sales.objects.filter(userbase__user_id=c.user_id).count()
                    ord.append(orders)
            elif s_date != "" and e_date == "":
                start_date=datetime.strptime(s_date,'%Y-%m-%d' )
                cus=UserBase.objects.filter(user_id__is_staff=False,user_id__date_joined__gte=start_date) 
                cus_count=UserBase.objects.filter(user_id__is_staff=False,user_id__date_joined__gte=start_date).count()
                for c in cus:
                    orders=Sales.objects.filter(userbase__user_id=c.user_id).count()
                    ord.append(orders)
            elif s_date == "" and e_date != "":
                print("in")

                end_date=datetime.strptime(e_date,'%Y-%m-%d' )
                cus=UserBase.objects.filter(user_id__is_staff=False,user_id__date_joined__lte=end_date) 
                cus_count=UserBase.objects.filter(user_id__is_staff=False,user_id__date_joined__lte=end_date).count() 
                for c in cus:
                    orders=Sales.objects.filter(userbase__user_id=c.user_id).count()
                    ord.append(orders)
            else:
                cus=UserBase.objects.filter(user_id__is_staff=False) 
                cus_count=UserBase.objects.filter(user_id__is_staff=False).count() 
                for c in cus:
                    orders=Sales.objects.filter(userbase__user_id=c.user_id).count()
                    ord.append(orders)
            cp=Company.objects.first()
            user=UserBase.objects.get(user_id=request.user)
            if cus.count()>0:
               data=zip(cus,ord)
               return render(request,"invoices/customer_report.html",{'data':data,'d':d,'cp':cp,'user':user,'cus_count':cus_count})
            else:
               messages.warning(request,"No Data Found")
               return redirect("gen_reports")

        
    return redirect("gen_reports")

def downloadPdf(request,id):
    checklocal(request)
    pdf=reports.objects.get(id=id)
    pdffile=pdf.report_file
    return HttpResponse(pdffile,content_type='application/pdf')

def delReport(request,id):
    checklocal(request)
    report=reports.objects.get(id=id)
    report.delete()
    return redirect("gen_reports")

def updateprofile(request):
    checklocal(request)
    if request.method=="POST":
        try:
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            add=request.POST.get('add')
            profile=request.FILES['profileimg']
            print(profile)
            user=UserBase.objects.get(user_id=request.user.id)
            user.first_name=fname
            user.last_name=lname
            user.Cus_phone=phone 
            user.cus_add1=add
            user.profile=profile
            main=User.objects.get(username=user.user_id.username)
            main.email=email
            print(main)
            main.save()
            user.save()
            print(user)
            return redirect("adminprofile")
        except Exception as e :
            print(e)
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            add=request.POST.get('add')
            
            user=UserBase.objects.get(user_id=request.user.id)
            user.first_name=fname
            user.last_name=lname
            user.Cus_phone=phone 
            user.cus_add1=add
            main=User.objects.get(username=user.user_id.username)
            main.email=email
            print(main)
            main.save()
            user.save()
            print(user)
            return redirect("adminprofile")

def searchCustomer(request):
    checklocal(request)
    if request.method=="POST":
        searchText=request.POST.get('search')
        print(searchText,"none")
        if searchText != "":
            customer=UserBase.objects.filter(first_name__icontains=searchText)
            print(customer)
            return render(request,"Mainadmin/cus.html",{'customers':customer})
        else:
            return redirect("customers")
    return redirect("customers")

def delappo(request,id):
    app=Appointment.objects.get(id=id)
    app.delete()
    return redirect("appointment")
# Customer Views..

def home(request):
    checksuper(request)
    country = Country.objects.all()
    comp=Company.objects.all()
    product=Product.objects.all()
    size=product[0:4]
    n=len(product)
    slides=n//4 + math.ceil((n/4)-(n//4))

    return render(request,"customer/home.html",{'country':country,'company':comp,'context':size,'slide':slides})

def womens(request):
    checksuper(request)
    products=Product.objects.all()
    cat=Category.objects.all()
    maincat = []
    subcat = []
    for c in cat:
        if c.cat_id == None:
            maincat.append(c)
            subcatlist = Category.objects.filter(cat_id=c)
            subcat.append(subcatlist)
    catzip = zip(maincat,subcat)

    return render(request,"customer/womens.html",{'context':products,"cats":catzip})


def aboutus(request):
    checksuper(request)
    return render(request,"customer/about.html")

def cart(request):
    checksuper(request)
    # cartpro = request.session['cart']
    print("the cart ids are =====>")
    # print(cartpro)
    mycart=Cart.objects.filter(userbase__user_id=request.user.id) 
    return render(request,"customer/cart.html",{'cart':mycart})

def wishlist(request):
    checksuper(request)
    wis=Wishlist.objects.all()
    return render(request,"customer/wishlist.html",{'wis':wis})    
def userprofile(request):
    checksuper(request)
    user=UserBase.objects.get(user_id=request.user.id)
    print(user)
    return render(request,"customer/profile.html",{"user":user})

def edit_profile(request,id):
    checksuper(request)
    user=UserBase.objects.get(user_id=id)
    if request.method=='POST':
        try:
            firstname=request.POST.get('fname')
            lastname=request.POST.get('lname')
            phone=request.POST.get('phone')
            email=request.POST.get('email')
            add=request.POST.get('address')
            profile=request.FILES['propic']
            UserBaseInstance = UserBase()
            UserBaseInstance.first_name = firstname
            UserBaseInstance.last_name = lastname
            UserBaseInstance.Cus_phone = phone
            # UserBaseInstance.cus_email=email
            UserBaseInstance.profile = profile
            UserBaseInstance.cus_add1 = add
            UserBaseInstance.user_id = user.user_id
            # UserBaseInstance.user_id=uid
            muser=User.objects.get(id=id)
            muser.email=email
            muser.save()
            UserBaseInstance.save()
            return redirect("home")
        except Exception as e:
            print(e)
            UserBaseInstance = UserBase()
            UserBaseInstance.first_name = firstname
            UserBaseInstance.last_name = lastname
            
            UserBaseInstance.Cus_phone = phone
            # UserBaseInstance.cus_email=email
            UserBaseInstance.profile = profile
            UserBaseInstance.cus_add1 = add
            UserBaseInstance.user_id = user.user_id
            # UserBaseInstance.user_id=uid
            muser=User.objects.get(id=id)
            muser.email=email
            muser.save()
            UserBaseInstance.save()
            return redirect("home")
    return render(request,"customer/edit-profile.html",{'user':user})

def single(request,id):
    checksuper(request)
    product=Product.objects.get(id=id)
    d_amount=product.price-(product.price*product.discount)
    feed=Feedback.objects.filter(product_id=product)
    rat=Rating.objects.filter(product_id=product)
    count=Rating.objects.filter(product_id=product).count()
    
    avg=0
    ratt=0
    for i in rat:
        ratt=ratt+int(i.value)
    if count == 0:
        avg=math.ceil(ratt/1)
    else:
        avg=math.ceil(ratt/count)
    try:
        user=UserBase.objects.get(user_id=request.user)
        sal=Sales.objects.filter(userbase=user)
        for s in sal:   
            sald=SalesDetails.objects.filter(sales_id=sal,product_id=product)
            # print("the sales details",sald)
            f=Feedback.objects.filter(product_id=product, userbase=user).exists()
            r=Rating.objects.filter(product_id=product,userbase=user).exists()
            if f and r:
                exist="yes"
            else:
                exist="no"
            return render(request,"customer/single.html",{'product':product,'d_amount':d_amount,'feed':feed,'rat':rat,'avg':avg,'sal':sald,'exist':exist})
    except Exception as e:
        
        print("hihi",e)
    return render(request,"customer/single.html",{'product':product,'d_amount':d_amount,'feed':feed,'rat':rat,'avg':avg})

def userregister(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        firstname=request.POST.get('fname')
        lastname=request.POST.get('lname')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        gender = request.POST.get('gender')
        dob=request.POST.get('dob')
        add=request.POST.get('address')
        pincode=request.POST.get('pin')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        profile=request.FILES['propic']
        try:
            area_id = Area(request.POST.get('area'))
        except Exception as e:
            print(e)
        print(area_id)
        print(uname,firstname,lastname,phone,email,gender,dob,add,pincode,password,cpassword,profile)
        user = User.objects.create_user(
            username=uname, password=password, email=email)
        user.save()
        UserBaseInstance = UserBase()
        UserBaseInstance.first_name = firstname
        UserBaseInstance.last_name = lastname
        if gender == "male":
            UserBaseInstance.gender = True
        else:
            UserBaseInstance.gender = False
        UserBaseInstance.dob = dob
        UserBaseInstance.pincode = pincode
        UserBaseInstance.Cus_phone = phone
        # UserBaseInstance.cus_email=email
        UserBaseInstance.profile = profile
        UserBaseInstance.cus_add1 = add
        UserBaseInstance.user_id = user
        # UserBaseInstance.user_id=uid
        UserBaseInstance.area_id = area_id
        UserBaseInstance.save()
        login(request, user)
        messages.success(request,"Login Successful")
        return redirect("home")

def userlogin(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        upass=request.POST.get('password')
        user = authenticate(request, username=uname, password=upass)
        if user is not None:
            login(request,user)
            request.session.set_expiry(0)
            messages.success(request,"Login Successful !")
            return redirect("home")
        else:
            messages.error(request,"Invalid Username Or Password!!")
            return redirect("home")
            
def userlogout(request):
    if request.user.is_superuser==False:
        logout(request)
        messages.success(request,"Logout Successful !")
    return redirect("home")

def addtowish(request,id):
    checksuper(request)
    product=Product.objects.get(id=id)
    mainuser=User.objects.get(username=request.user)
    user=UserBase.objects.get(user_id=mainuser)
    print(user.user_id.id)
    if user.user_id.is_superuser == False:
        try:
            wish=Wishlist()
            wish.userbase=user
            wish.product_id=product
            wish.save()
            messages.success(request,"Product Added To Wishlist")
        except Exception as e:
            print(e)
    return redirect("wishlist")
    
def addtocart(request,id):
    checksuper(request)
    product=Product.objects.get(id=id)
    try:
        mainuser=User.objects.get(username=request.user)
        user=UserBase.objects.get(user_id=mainuser)
        print(user.user_id.id)
        

        if user.user_id.is_superuser == False:
            try:
                mcart=Cart()
                mcart.userbase=user
                mcart.product_id=product
                mcart.cart_qty=1
                # mcart.cart_price=product.price
                # discount=product.price-(product.price*product.discount)
                mcart.save()
                
                
                cart = [mcart.id]
                # request.session["cart"]=cart
                messages.success(request,"Product Added To Cart")
            except Exception as e:
                mycart=Cart.objects.get(userbase=user,product_id=product.id)
                mycart.cart_qty+=1
                mycart.save()
                
                cart = [mcart.id]
                request.session["cart"]=cart
                print("success")
                messages.success(request,"Product Added To Cart")
    except:
                cart = [product.id]
                past_cart=[]
                try:
                    past_cart = request.session["cart"]
                except:
                    request.session["cart"]=cart.append(object)

                messages.success(request,"Product Added To Cart")
    return redirect("cart")

def removecart(request,id):
    checksuper(request)
    cart=Cart.objects.get(id=id)
    cart.delete()
    messages.success(request,"Product Removed From Cart")
    return redirect("cart")

def removewish(request,id):
    checksuper(request)
    wish=Wishlist.objects.get(id=id)
    wish.delete()
    messages.success(request,"Product Removed From Wishlist")
    return redirect("wishlist")
     
def checkout(request):
    checksuper(request)
    if request.method=="POST":
        final_price=request.POST.get("fp")
        print(final_price)
    mycart=Cart.objects.filter(userbase__user_id=request.user.id)
    cus=UserBase.objects.get(user_id=request.user)
    return render(request,"customer/checkout.html",{'mycart':mycart,'final_price':final_price,'cus':cus})
def catprod(request):
    if request.method=="POST":
        cat=request.POST.get("cat")
        print(cat)
        subcat=Category.objects.get(cat_name=cat)
        lst=[]
        try:
            products=Product.objects.filter(cat_id__cat_name=subcat)
            print(products.values('discount'))
            data=list(products.values('id','product_name','price','product_img'))
            for idx ,p in enumerate(products.values()):
                lst={"lst":(p.get("price")-p.get("price")*p.get("discount"))}
                print(lst)
                data[idx].update(lst)
            # data.append(lst)
            print(data)
            print(lst)
           
        except Exception:
            data="Error"
            return JsonResponse(data)
    return JsonResponse( data,safe=False)

def saveqty(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            produc_id=request.POST.get("produc_id")
            qty=request.POST.get("qty")
            print("qty",qty)
            mycart=Cart.objects.filter(userbase__user_id=request.user,product_id=produc_id)
            print(mycart)
            print(produc_id) 
            for items in mycart:
                items.cart_qty=qty
                items.save()
            # len_of_data=mycart.count()
            # len_of_str=len(selcted_qty)
            # qty=list(selcted_qty[len_of_str-len_of_data:])
            # print(qty)
            # cartobj=Cart.objects.filter(userbase__user_id=request.user).order_by('?')
            # for i,c in zip(qty,cartobj):
            #     c.cart_qty = i
            #     c.save()
            data="Success"
            return JsonResponse(data,safe=False)
        
       
def forgetpass(request):
    return render(request,"accounts/forgot-password.html")

def otp(request):
    if request.method=="POST":
        email=request.POST.get("email")
        print(email)
        try:
            user=User.objects.get(email=email)
            print(user)
            otpp = random.randint(100000, 999999)
            print("OTP:", otpp)
            print(user.email)
            subject="Your One Time Password"
            answer="Your One Time Password Is:{} ".format(otpp)
            try:
                send_mail( subject, answer, settings.EMAIL_HOST_USER, [user.email])
                expiretime=timezone.now()+timedelta(minutes = 10)
                myotp=generateotp(otp=otpp,otp_expire=expiretime,userbase=user)
                myotp.save()
                messages.success(request,"OTP Sent To Your Email !")
                return render(request,"accounts/otp.html")
            except Exception:
                # print(e)
                expiretime=timezone.now()+timedelta(minutes = 10)
                myotp=generateotp.objects.get(userbase=user)
                myotp.otp=otpp
                myotp.otp_expire=expiretime
                # myotp.userbase=user
                myotp.save()
                return render(request,"accounts/otp.html",{'user':user.id})
                # messages.error(request,"No User Registered On This Emaillll !!")
        except Exception as e:
            print(e)
            messages.error(request,"No User Registered On This Email !!")
            return redirect("forgetpass")
    return render(request,"accounts/otp.html")

def verifyotp(request,id):
    if request.method=="POST":
        o1=request.POST.get("o1")
        o2=request.POST.get("o2")
        o3=request.POST.get("o3")
        o4=request.POST.get("o4")
        o5=request.POST.get("o5")
        o6=request.POST.get("o6")
        verify=o1+o2+o3+o4+o5+o6
        print(verify)
        myotp=generateotp.objects.get(userbase=id)
        rn=timezone.now()
        if verify==myotp.otp:
            if rn < myotp.otp_expire:
                print("same and in time")
                return render(request,"customer/reset-password.html",{'user':myotp.userbase.id})
            else:
                messages.error(request,"OTP Expired!!")
                return render(request,"accounts/otp.html",{'user':myotp.userbase.id})

        else:
            messages.error(request,"Wrong OTP")
            return render(request,"accounts/otp.html",{'user':myotp.userbase.id})

def updateAdminpass(request,id):
    if request.method=="POST":
        upass=request.POST.get('upass')
        repass=request.POST.get('repass')
        if upass==repass:
            try:
                user=User.objects.get(id=id)
                user.set_password(upass)
                user.save()
                print(user) 
                request.session.set_expiry(0)
                messages.success(request, "Password Updated Successfully!")
                return redirect("sign-in")
            except Exception as e:
                print(e)
                messages.error(request,"something went wrong")
                return render(request,"customer/reset-password.html",{'user':id})  
        else:
            messages.error(request,"Password Has To Be Same !!")  
            return render(request,"customer/reset-password.html",{'user':id})
    else:
        return render(request,"customer/reset-password.html",{'user':id})

def myorders(request):
        checksuper(request)
        user=UserBase.objects.get(user_id=request.user)
        sales=Sales.objects.filter(userbase=user).order_by('-id')
        return render(request,"customer/orders.html",{'sales':sales})


    
def placeorder(request):
    if request.method=="POST":
        cartobj=Cart.objects.filter(userbase__user_id=request.user)
        print(cartobj)
        add2=request.POST.get("add2")
        fp=int(float(request.POST.get("final_price")))
        ptype=request.POST.get('pay')
        note=request.POST.get("note")
        # eachprice=[]
        # print(cartobj.__len__())
        # for i in range(1,cartobj.__len__()+1):
        #     eachprice.append()
        # print(eachprice)
        # print(ptype)
        # print(request.POST)
        user=UserBase.objects.get(user_id=request.user)
        if add2!="":
            user.cus_add2=add2
            user.save()
        if ptype == "Cash on Delivery":
            sales=Sales(payment_status="pending",sales_status="pending",payment_date=timezone.now(),userbase=user,note=note)
            sales.save()
        else:
            sales=Sales(payment_status="paid",sales_status="pending",payment_date=timezone.now(),userbase=user,note=note)
            sales.save()
        count=1
        for items in cartobj:
            print(items.product_id)
            salesdetail=SalesDetails(product_id=items.product_id,sales_id=sales,final_price=request.POST.get("eachprice"+str(count)),qty=items.cart_qty)
            salesdetail.save()
            print(salesdetail)
            on_hand=qty=Product.objects.get(id=items.product_id.id)
            on_hand.qty_on_hand=on_hand.qty_on_hand-items.cart_qty
            if on_hand.qty_on_hand <=0:
                noti=Notification(not_title=on_hand.product_name+" Is Out Of Stock!!",not_read=False,not_date=datetime.now().date()     ) 
                noti.save()
            on_hand.save()
            count=count+1
        cartobj.delete()
        messages.success(request, "Order Placed Successfully!! {} is Your Order Id".format(sales.id))
        return redirect("myorders")
    else:
        return redirect("placeorder")

def makecomp(request,id):
    if request.method=="POST":
        c_title=request.POST.get('title')
        c_desc=request.POST.get('complaint')
        try:
            product=Product.objects.get(id=id)
            user=UserBase.objects.get(user_id=request.user)
            com=Complaint(title=c_title,com_desc=c_desc,product_id=product,userbase=user)
            com.save()
            return redirect("myorders")
        except Exception as e:
            print(e)
    return redirect("myorders")

def view_ord(request,id):
    try:
        sale=Sales.objects.get(id=id)
        print(sale)
        sales=SalesDetails.objects.filter(sales_id=sale)
        try:
            sr=SalesReturn.objects.get(sales_id=sale)
            srd=SalesReturnDetails.objects.filter(sales_ret_id=sr)
            # main=0
            # for qty in srd:
            #     main=main+qty.salRet_qty
            # print(main)
            
            return render(request,"customer/view_order.html",{'sales':sales,'ret':srd})
        except Exception as e:
            print(e)
            return render(request,"customer/view_order.html",{'sales':sales})
            
    except Exception as e:
        print(e)
        return redirect("home")
    return render(request,"customer/view_order.html",{'sales':sales})
        
def searchprod(request):
    if request.method=="POST":
        keyword=request.POST.get("search")
        print(keyword)
        d_amount=[]
        catobj=Category.objects.filter(cat_name__icontains=keyword)
        subcat = []
        for c in catobj:
            if c.cat_id == None:
                subcat = Category.objects.filter(cat_id = c)
        catobj = list(catobj)+list(subcat)
        catobj = set(catobj)
        print(catobj)
        product=Product.objects.filter(Q(product_name__icontains=keyword) | Q(desc__icontains=keyword ) | Q(cat_id__in = catobj))
        print(product)
        
        return render(request,"customer/search.html",{"context":product})
        
def cancelsale(request,id):
    sale=Sales.objects.get(id=id)
    print(sale)
    details=SalesDetails.objects.filter(sales_id=sale)
    for pro in details:
        on_hand=Product.objects.get(id=pro.product_id.id)
        on_hand.qty_on_hand=on_hand.qty_on_hand+pro.qty
        on_hand.save()
    sale.sales_status="Cancelled"
    sale.c_date=datetime.now().date()
    sale.save()
    return redirect("myorders")
def purchasehistory(request):
    final_list=[]
    pur=Purchase.objects.all()
    for p in pur:
        purd=PurchaseDetails.objects.filter(pur_id=p)
        eachsum=[]
        final_amount=0
        for i in purd:
            eachsum.append(i.pur_price*i.pur_qty)
            for j in eachsum:
                print("easum",j)

            final_amount=final_amount+j
            print("final",final_amount)
        print("before final list ",final_list)
        final_list.append(final_amount)
        print("final list ",final_list)
        final_amount=0

    print(pur)
    print(final_list)
    context=zip(pur,final_list)
    return render(request,"Mainadmin/pur-pay.html",{'pur':context})

        
def testaudio(request):
     if request.method == "POST":
        blobdata = request.FILES.get('data') 
        print(type(blobdata)) 
        
        destination = open('audio.wav', 'wb')
        for chunk in blobdata.chunks():
            destination.write(chunk)
        destination.close()
        
        with open("audio.wav", "rb") as file:
            info = fleep.get(file.read())

            print(info.type)
            print(info.extension)
            print(info.mime)
        
        AUDIO_FILE="audio.wav"
        # AUDIO_FILE="Welcome.wav"
        # print(type(AUDIO_FILE))
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)  
        try:
            print("The audio file contains: " + r.recognize_google(audio))
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
     return render(request,'customer/testvoice.html')


def applyfilter(request):
    if request.method=="POST":
        size=request.POST.get('sizefilter')
        price=request.POST.get('pricefilter')
        print(size)
        print(price)
        price=price[0:]
        print(price)
       
        if price ==  "500-1000" and size == "Default":
            print("IN")
            products=Product.objects.filter(price__lte=1000,price__gte=500)
        elif price == "1000-1500" and size == "Default":
            products=Product.objects.filter(price__lte=1500,price__gte=1000)
        elif price == "1500-2500" and size == "Default":
            products=Product.objects.filter(price__lte=2500,price__gte=1500)
        elif price == "2500-higher" and size == "Default":
            products=Product.objects.filter(price__gte=2500)
        elif price ==  "500-1000":
            products=Product.objects.filter(size_id__details=size,price__lte=1000,price__gte=500)
        elif price == "1000-1500":
            products=Product.objects.filter(size_id__details=size,price__lte=1500,price__gte=1000)
        elif price == "1500-2500":
            products=Product.objects.filter(size_id__details=size,price__lte=2500,price__gte=1500)
        elif price == "2500-higher":
            products=Product.objects.filter(size_id__details=size,price__gte=2500)
        elif price == "Default" and size=="Default":
            products=Product.objects.all()
        cat=Category.objects.all()
        maincat = []
        subcat = []
        for c in cat:
            if c.cat_id == None:
                maincat.append(c)
                subcatlist = Category.objects.filter(cat_id=c)
                subcat.append(subcatlist)
        catzip = zip(maincat,subcat)
        delta = relativedelta(day=1)
        return render(request,"customer/womens.html",{'context':products,"cats":catzip})
    
def purDet(request,id):
        pur=Purchase.objects.get(id=id)
        purd=PurchaseDetails.objects.filter(pur_id=pur).order_by('-pur_id')
        return render(request,"Mainadmin/pur-det.html",{'pur':purd})

def det_rec_ord(request,id):
    order=SalesDetails.objects.filter(sales_id=id)
    try:
        for o in order:
            sr=SalesReturn.objects.get(sales_id=o.sales_id)
        srd=SalesReturnDetails.objects.filter(sales_ret_id=sr)
        return render(request,"Mainadmin/details_rec_ord.html",{'order':order,'sr':srd})
        
    except Exception as e:
            print(e)
            return render(request,"Mainadmin/details_rec_ord.html",{'order':order})

def cancelledorder(request):
    orders=Sales.objects.filter(sales_status="Cancelled").order_by('-id','sales_date')
    main=[]
    for i in orders:
        sd=SalesDetails.objects.filter(sales_id=i)
        p=0
        for j in sd:
            p=p+j.final_price
        main.append(p)
    # orders = orders.annotate(final=Value(main, output_field=IntegerField()))
    print(main)
    paginator=Paginator(orders,5)
    page_number=request.GET.get('page')
    order=paginator.get_page(page_number)
    context=zip(order, main)
    return render(request,"Mainadmin/can_ords.html",{'order':context})
def addrm(request):
    rm=RawMaterial.objects.all()
    return render(request,"Mainadmin/raw_mat.html",{'rm':rm})
def addcat(request):
    cat=Category.objects.filter(cat_id=None)
    return render(request,"Mainadmin/category.html",{'cat':cat})

def changepasswordfromold(request):
        return render(request,"accounts/change_password.html")        
def addfeed(request):
    if request.method=="POST":
        feedtit=request.POST.get("feedtit")
        feed=request.POST.get("Message")
        rat=request.POST.get("rat")
        pid=request.POST.get("pid")
        print(feedtit,"____",feed,"______",rat)
        user=UserBase.objects.get(user_id=request.user)
        prod=Product.objects.get(id=pid)
        feed=Feedback(fb_title=feedtit,fb_desc=feed,product_id=prod,userbase=user)
        rat=Rating(value=rat,product_id=prod,userbase=user)
        feed.save()
        rat.save()
        messages.success(request,"Thank You For Your Feedback !!")
        return redirect("home")

def savepur(request):
    if request.method=="POST":
        print(request.POST)
        purdate=request.POST.get('purdate')
        sup=request.POST.get('sup')
        details=request.POST.getlist('purdet')
        if len(details)==0:
            messages.warning(request,"Please Any Select Raw Materials !!")
            return redirect("purchase")
        else:
            print(details)
            sp=Supplier.objects.get(id=sup)
            user=UserBase.objects.get(user_id=request.user)
            pur=Purchase(pur_date=purdate,sup_id=sp,userbase=user)
            pur.save()
            print(pur)
            for i in details:
                j=0
                id=0
                price=0
                unit=0
                qty=0
                for x in i.split(','):
                    print(x)
                    if j == 0:
                        id=x
                        j=j+1
                    elif j == 1 :
                        qty=x
                        j=j+1
                    elif j== 2:
                        price=x
                        j=j+1
                    else:
                        unit=x
                        j=j+1

                print("id is ",id," qty is ",qty," price is ",price," unit is ",unit)
                purd=PurchaseDetails(pur_id=pur,raw_matId=RawMaterial(id),unit=UnitOfMeasurement(unit),pur_price=price,pur_qty=qty)
                purd.save()
            messages.success(request,"Purchase Added Succesfully!!")
            return redirect("purchase")

def addraw(request):
    if request.method=="POST":
        raw_name=request.POST.get("raw")
        check=RawMaterial.objects.filter(raw_name__iexact=raw_name).exists()
        if check is False:        
            rawobj=RawMaterial(raw_name=raw_name)
            rawobj.save()
            messages.success(request,"Raw Material Added !!")
            return redirect("addrm")

        else:
            messages.warning(request,"Raw Material Already Exists !!")
        return redirect("addrm")
    else:
        redirect("addrm")

def delraw(request,id):
    raw=RawMaterial.objects.get(id=id)
    raw.delete()
    return redirect("addrm")

def addcatt(request):
    if request.method=="POST":
        cat=request.POST.get('category')
        check=Category.objects.filter(cat_name__iexact=cat).exists()
        if check is False:        
            catobj=Category(cat_name=cat,cat_id=None)
            catobj.save()
            messages.success(request,"Category Added !!")
            return redirect("addcat")

        else:
            messages.warning(request,"Category Already Exists !!")
            return redirect("addcat")



def addsubcat(request):
    if request.method=="POST":
        cat=Category(request.POST.get('category'))
        subcat=request.POST.get('subcat')
        print(cat,"___",subcat)
        check=Category.objects.filter(cat_name__iexact=subcat).exists()
        if check is False:        
            catobj=Category(cat_name=subcat,cat_id=cat)
            catobj.save()
            messages.success(request,"Sub Category Added !!")
            return redirect("addcat")
        else:
            messages.warning(request,"Sub Category Already Exists !!")
            return redirect("addcat")

def delcat(request,id):
    check=Product.objects.filter(cat_id=id).exists()
    cat=Category.objects.get(id=id)
    if check is False:
        cat.delete()
        messages.success(request, "Category Deleted !!")
    else:
        messages.warning(request,"Child Records Found !!")

    return redirect("addcat")

def deliver(request,id):
    sale=Sales.objects.get(id=id)
    sale.sales_status="Delivered"
    sale.d_date=timezone.now().date()
    sale.save()
    messages.success(request,"Product Added To Completed Orders..")
    return redirect("vieworders")

def noti(request):
    if request.method=="GET":
        try:
            noti=Notification.objects.all()
            n=Notification.objects.filter(not_read=False).count()
            data=list(noti.values('id','not_title','not_date','not_read'))
            for d in data:
                d.update({'counter':n})
            # data.update(cartobj)
            return JsonResponse(data, safe=False)
        except Exception:
            data="Error"
            return JsonResponse(data)

def readnot(request):
    if request.method=="GET":
        try:
            n=Notification.objects.filter(not_read=False)
            for i in n:
                i.not_read=True
                i.save()
            data="yess"
            return JsonResponse({'data':data}, safe=False)
        except Exception:
            data="Error"
            return JsonResponse(data)

def returnorder(request,id):
    if request.method=="POST":
        retqty=request.POST.get('retqty')
        retmsg=request.POST.get('retmsg')
        sale=SalesDetails.objects.get(id=id)
        try:
            salesret=SalesReturn.objects.get(sales_id=sale.sales_id)
        except Exception as e:
            salesret=SalesReturn(sales_id=sale.sales_id)
            salesret.save()
        try:
            salretdet=SalesReturnDetails.objects.get(sales_ret_id=salesret)
            salretdet.salRet_qty=salretdet.salRet_qty+int(retqty)
            salretdet.save()
        except Exception as e:
            print(e)
            salretdet=SalesReturnDetails(sales_ret_id=salesret,salRet_qty=retqty,salRet_reason=retmsg,product_id=sale.product_id)
            salretdet.save()
        # sale.save()
        print(retqty,"__",retmsg)
        return redirect("myorders")


def downinvoice(request,id):
    sale=Sales.objects.get(id=id)
    print(sale)
    main=[]
    sales=SalesDetails.objects.filter(sales_id=sale)
    p=0
    for j in sales:
        p=p+j.final_price
    main.append(p)
    
    print(sales)
    company=Company.objects.first()
    return render(request,"invoices/invoice.html",{'sales':sales,'company':company,'price':main})

def delsup(request,id):
    sup=Supplier.objects.get(id=id)
    print(sup)
    sup.delete()
    messages.success(request,"Supplier Deleted !!")
    return redirect("supplier")
    