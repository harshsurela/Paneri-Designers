from django import template
from datetime import timedelta
from django.utils import timezone
register = template.Library()
@register.filter(name='times') 
def times(number):
    return range(1,int(number)+1)

@register.simple_tag 
def calcdisc(price,dis,qty):
    print("filter"+str(price))
    print(dis)
    disprice=price-(price*dis)
    print("dis"+str(disprice))
    print(qty)
    mainprice=int(disprice)*qty
    print("main"+str(mainprice))
    return mainprice
@register.filter(name='perc') 
def perc(discount):
    dis=discount*100
    return dis

@register.filter(name='checkcancel')
def checkcancel(sales_date):
    canceldate = sales_date + timedelta(days=1)
    # print("sales date: ",sales_date)
    # print("cancel date",canceldate)
    # print(timezone.now().date())
    if  timezone.now().date()<=canceldate:
        return True
    else:
        return False
@register.filter(name='checkret')
def checkeret(sales_date):
    retdate = sales_date + timedelta(days=7)
    # print("sales date: ",sales_date)
    # print("cancel date",canceldate)
    # print(timezone.now().date())
    if  timezone.now().date()<=retdate:
        return True
    else:
        return False

@register.filter(name='calcprice')
def calcprice(price,dis):
    return price-(price*dis)


