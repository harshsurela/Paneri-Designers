from django.db import models

from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db.models.expressions import Case
# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.country_name

class State(models.Model):
    state_name = models.CharField(max_length=15)
    country_id = models.ForeignKey(Country, on_delete=CASCADE)
    def __str__(self) -> str:
        return self.state_name

class City(models.Model):
    city_name = models.CharField(max_length=15)
    state_id = models.ForeignKey(State, on_delete=CASCADE)
    def __str__(self) -> str:
        return self.city_name


class Area(models.Model):
    area_name = models.CharField(max_length=15)
    city_id = models.ForeignKey(City, on_delete=CASCADE)
    def __str__(self) -> str:
        return self.area_name


class Company(models.Model):
    comp_name = models.CharField(max_length=25)
    comp_add = models.CharField(max_length=45)
    comp_phone = models.CharField(max_length=10)
    comp_email = models.EmailField(max_length=50)
    contact_person = models.CharField(max_length=45)
    area_id = models.ForeignKey(Area, on_delete=CASCADE)
    def __str__(self) -> str:
        return self.comp_name

# class Offer(models.Model):
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     offer_title=models.CharField(max_length=20,default="Not Specified")
#     offer_details = models.TextField(max_length=200)
#     discount = models.FloatField()
#     company_id = models.ForeignKey(Company, on_delete=CASCADE)
#     def __str__(self) -> str:
#         return "Offer {}".format(self.id)


class Sales(models.Model):
    sales_date = models.DateField(auto_now=True)
    d_date=models.DateField(null=True,blank=True)
    c_date=models.DateField(null=True)
    payment_status = models.CharField(max_length=10)
    sales_status=models.CharField(max_length=20,default="pending")
    payment_date = models.DateTimeField()
    # is_cancel = models.BooleanField(default=False)
    note=models.CharField(max_length=255,null=True,blank=True)
    # offer_id = models.ForeignKey(Offer, on_delete=CASCADE)
    userbase=models.ForeignKey('UserBase',on_delete=CASCADE)
    def __str__(self) -> str:
        return  "Sales: {} Sales Date: {}".format(self.id,self.sales_date)


class SalesDetails(models.Model):
    product_id = models.ForeignKey(
        'Product', on_delete=CASCADE, null=False)
    sales_id = models.ForeignKey(
        Sales, on_delete=CASCADE, null=False)
    final_price=models.IntegerField()
    qty=models.IntegerField()
    class Meta:
        ordering = ['-sales_id']
        unique_together = (('product_id', 'sales_id'),)
    def __str__(self) -> str:
        return "SalesDetails: {}".format(self.id) 


class SalesReturn(models.Model):
    salesRe_date=models.DateField(auto_now=True)
    sales_id=models.ForeignKey(Sales,on_delete=CASCADE)
    def __str__(self) -> str:
        return "SalesReturn: {}".format(self.salesRe_date)

class SalesReturnDetails(models.Model):
    product_id=models.ForeignKey('Product',on_delete=CASCADE,null=False)
    sales_ret_id=models.ForeignKey(SalesReturn,on_delete=CASCADE,null=False)
    class Meta:
        ordering = ['sales_ret_id']
        # unique_together = (('product_id', 'sales_ret_id'),)
    salRet_qty=models.IntegerField()
    salRet_reason=models.CharField(max_length=200)
    salRet_date=models.DateField(auto_now=True)
    def __str__(self) -> str:
        return "SalesReturnDetails: {} and the date {}".format(self.id,self.salRet_date)
# class Production(models.Model):
#     production_qty=models.IntegerField()
#     product_id=models.ForeignKey('Product',on_delete=CASCADE)
#     raw_matId=models.ForeignKey('RawMaterial',on_delete=CASCADE)
#     def __str__(self) -> str:
#         return "Production: {}".format(self.id)
class UserBase(models.Model):
    user_id=models.OneToOneField(User,on_delete=CASCADE,primary_key=True)
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    gender=models.BooleanField(default="Not Specified")
    dob=models.DateField(default="Not Specified")
    cus_add1=models.TextField(null=True,blank=True)
    cus_add2=models.TextField(null=True,blank=True)
    pincode=models.IntegerField()
    Cus_phone=models.CharField(max_length=10)
    # cus_email=models.EmailField()
    profile=models.ImageField(upload_to="profileImages/",max_length=1500)
    area_id=models.ForeignKey(Area,on_delete=CASCADE)
    class meta:
        ordering = ['user_id']
    def __str__(self) -> str:
        return self.user_id.username
class Product(models.Model):
    product_name=models.CharField(max_length=45)
    price=models.IntegerField()
    qty_on_hand=models.IntegerField()
    discount=models.FloatField(null=True)
    desc=models.TextField()
    product_img=models.ImageField(upload_to="ProductImg/",max_length=100)
    size_id=models.ForeignKey('ProductSize',on_delete=CASCADE,null=False)
    color_id=models.ForeignKey('ProductColor',on_delete=CASCADE,null=False)
    company_id=models.ForeignKey(Company,on_delete=CASCADE)
    cat_id=models.ForeignKey('Category',on_delete=CASCADE)
    class Meta:
        ordering = ['id']
        unique_together = (('size_id','id', 'color_id'),)
    def __str__(self) -> str:
        return self.product_name

class CustomizedProdoct(models.Model):
    cus_productName=models.CharField(max_length=45)
    cus_productImg=models.ImageField(upload_to="CustomizedProduct",max_length=150)
    cus_productDetails=models.TextField()
    cus_productPrice=models.IntegerField()
    size_id=models.ForeignKey('ProductSize',on_delete=CASCADE,null=False,default=1)
    color_id=models.ForeignKey('ProductColor',on_delete=CASCADE,null=False,default=1)
    def __str__(self) -> str:
        return self.cus_productName 

class Complaint(models.Model):
    title=models.CharField(max_length=45)
    com_desc=models.CharField(max_length=200)
    com_date=models.DateField(auto_now=True)
    com_resolve=models.BooleanField(default=False)
    product_id=models.ForeignKey(Product,on_delete=CASCADE)
    userbase=models.ForeignKey(UserBase,on_delete=CASCADE)
    def __str__(self):
        return self.title
class Wishlist(models.Model):
    userbase=models.ForeignKey(UserBase,on_delete=CASCADE,null=False)
    product_id=models.ForeignKey(Product,on_delete=CASCADE,null=False)
    class Meta:
        unique_together = (('userbase', 'product_id'),)
    def __str__(self) -> str:
        return "{}".format(self.id)

class Cart(models.Model):
    userbase=models.ForeignKey(UserBase,on_delete=CASCADE,null=False)
    product_id=models.ForeignKey(Product,on_delete=CASCADE,null=False)
    cart_qty=models.IntegerField()
    # cart_price=models.IntegerField()
    class Meta:
        unique_together = (('userbase', 'product_id'),)
    def __str__(self) -> str:
        return "{}".format(self.userbase)

# class productHasOffer(models.Model):
#     product_id=models.ForeignKey(Product,on_delete=CASCADE)
#     offer_id=models.ForeignKey(Offer,on_delete=CASCADE)
#     class Meta:
#         unique_together=(('product_id','offer_id'),)
#     def __str__(self) -> str:
#         return "{}".format(self.id)
class ProductColor(models.Model):
    color_name=models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.color_name
class ProductSize(models.Model):

    details=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.details

class Appointment(models.Model):
    app_date=models.DateField()
    app_status=models.IntegerField(default=0)
    app_time=models.TimeField()
    app_desc=models.CharField(max_length=30)
    userbase=models.ForeignKey(UserBase,on_delete=CASCADE)
    def __str__(self) -> str:
        return str(self.id)
class Rating(models.Model):
    userbase=models.ForeignKey(UserBase,on_delete=CASCADE,null=False)
    product_id=models.ForeignKey(Product,on_delete=CASCADE,null=False)
    value=models.CharField(max_length=1)
    class Meta:
        unique_together = (('userbase', 'product_id'),)
    def __str__(self) -> str:
        return str(self.value)
class Feedback(models.Model):
    userbase=models.ForeignKey(UserBase,on_delete=CASCADE,null=False)
    product_id=models.ForeignKey(Product,on_delete=CASCADE,null=False)
    fb_title=models.CharField(max_length=45)
    fb_desc=models.TextField()
    fb_date=models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('userbase', 'product_id'),)
    def __str__(self) -> str:
        return self.fb_title

class Category(models.Model):
    cat_name=models.CharField(max_length=15)
    # sub_cat_name=models.CharField(max_length=15)
    cat_id=models.ForeignKey('self',default=1,null=True,related_name='category',on_delete=CASCADE,blank=True)
    def __str__(self):
        return str(self.cat_name)

    def __repr__(self):
        return self.__str__()


class Supplier(models.Model):
    sup_name=models.CharField(max_length=45)
    sup_add=models.CharField(max_length=200)
    sup_phone=models.CharField(max_length=10)
    sup_email=models.EmailField(max_length=30)
    shop_name=models.CharField(max_length=45)
    comp_id=models.ForeignKey(Company,on_delete=CASCADE)
    area_id=models.ForeignKey(Area,on_delete=CASCADE)
    def __str__(self) -> str:
        return self.sup_name
class RawMaterial(models.Model):
    raw_name=models.CharField(max_length=45)
    # raw_qtyHand=models.IntegerField()
    def __str__(self) -> str:
        return self.raw_name
# class RawMaterialDetails(models.Model):
    # userbase=models.ForeignKey(UserBase,on_delete=CASCADE,null=False)
    # product_id=models.ForeignKey(Product,on_delete=CASCADE,null=False)
    # raw_matId=models.ForeignKey(RawMaterial,on_delete=CASCADE,null=False)
    # raw_price=models.IntegerField()
    # class Meta:
    #     unique_together = (('userbase', 'product_id','raw_matId'),)
    # def __str__(self) -> str:
    #     return "{}".format(self.id)
# class ProductHasRawMaterials(models.Model):
#     product_id=models.ForeignKey(Product,on_delete=CASCADE,null=False)
#     raw_matId=models.ForeignKey(RawMaterial,on_delete=CASCADE,null=False)
#     class Meta:
#         unique_together = (('product_id','raw_matId'),)
#     def __str__(self) -> str:
#         return "{}".format(self.id)

class UnitOfMeasurement(models.Model):
    unitOfmes=models.CharField(max_length=15)
    def __str__(self) -> str:
        return self.unitOfmes
class Purchase(models.Model):
    pur_date=models.DateTimeField(auto_now=True)
    sup_id=models.ForeignKey(Supplier,on_delete=CASCADE)
    userbase=models.ForeignKey(UserBase,on_delete=CASCADE)
    def __str__(self) -> str:
        return "Purchase on:{}".format(self.pur_date)


class PurchaseDetails(models.Model):
    pur_id=models.ForeignKey(Purchase,on_delete=CASCADE)
    raw_matId=models.ForeignKey(RawMaterial,on_delete=CASCADE)
    unit=models.ForeignKey(UnitOfMeasurement, on_delete=CASCADE)
    pur_qty=models.IntegerField()
    pur_price=models.IntegerField()
    def __str__(self) -> str:
        return "{}".format(self.id)

# class PurchasePayment(models.Model):
#     pur_id=models.ForeignKey(Purchase,on_delete=CASCADE)
#     pur_discount=models.FloatField(null=True,blank=True)
#     pur_amt=models.IntegerField()
#     pur_status=models.CharField(max_length=10)
#     purPaymentDate=models.DateTimeField(auto_now=True)
#     def __str__(self) -> str:
#         return self.pur_status

# class PurchaseReturn(models.Model):
#     purRet_date=models.DateField(auto_now=True)
#     credit_amt=models.IntegerField()
#     pur_id=models.ForeignKey(Purchase,on_delete=CASCADE)
#     def __str__(self) -> str:
#         return "Purchase Returned on:{}".format(self.purRet_date)

# class PurchaseReturnDetails(models.Model):
#     purRetId=models.ForeignKey(PurchaseReturn,on_delete=CASCADE,null=False)
#     raw_matId=models.ForeignKey(RawMaterial,on_delete=CASCADE,null=False)
#     purRet_qty=models.IntegerField()
#     purReturn_Reason=models.CharField(max_length=200)
#     class Meta:
#         unique_together = (('purRetId', 'raw_matId'),)
#     def __str__(self) -> str:
#         return "{}".format(self.id)
class Gallary(models.Model):
    gallary_img=models.ImageField(upload_to="Gallary")
    def __str__(self) -> str:
        return str(self.id)

class reports(models.Model):
    report_name=models.CharField(max_length=25)
    report_date=models.DateField()
    report_file = models.FileField(upload_to='Reports/')
    def __str__(self) -> str:
        return self.report_name
    
class generateotp(models.Model):
    otp=models.CharField(max_length=6,default="None")
    otp_expire=models.DateTimeField()
    userbase=models.OneToOneField(User,on_delete=CASCADE,null=False)
    
class Notification(models.Model):
    not_title=models.CharField(max_length=150)
    not_date=models.DateTimeField(auto_now=True)
    not_read=models.BooleanField(default=False)