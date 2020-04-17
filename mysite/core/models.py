from django.db import models

from django.conf import settings
from django.db import models
from django.db.models import Q

class user_record(models.Model):
    User_ID = models.CharField(max_length=30)
    Role = models.CharField(max_length=20)
    last_seen = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.User_ID+","+self.Role+","+str(self.last_seen)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)


class user_action(models.Model):
    user = models.CharField(max_length=100)
    last_seen = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user+","+str(self.last_seen)+","+str(self.action)


class Item(models.Model):
	text = models.CharField(max_length=300)
	complete = models.BooleanField()

	def __str__(self):
		return self.text

class Product(models.Model):
    Brand = models.CharField(max_length=20)
    Barcodes = models.CharField(max_length=20)
    Name = models.CharField(max_length=50)
    PackSize = models.CharField(max_length=10)
    CtnQty = models.CharField(max_length=10)
    RCP = models.CharField(max_length=10)
    RSP = models.CharField(max_length=10)
    RetailerMargin = models.CharField(max_length=10)
    FastPay = models.CharField(max_length=10)
    UlkPurchase = models.CharField(max_length=10)

    def __str__(self):
    	return str(self.Barcodes)+","+str(self.Brand)+","+str(self.Name)
    
    def list(self):
    	return [self.Barcodes,self.Brand,self.Name,self.PackSize,self.CtnQty,self.RCP,self.RSP,self.RetailerMargin,self.FastPay,self.UlkPurchase]

class notifications(models.Model):
    notification = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    last_seen = models.DateTimeField(auto_now=True)
    complete = models.BooleanField()
    
    def __str__(self):
        return self.notification+","+str(self.last_seen)+","+str(self.complete)

class invoice(models.Model):
    Inv_no = models.CharField(max_length=15)
    Status = models.CharField(max_length=10)
    last_seen = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.inv_no+","+str(self.last_seen)

class order(models.Model):
    Item = models.ForeignKey(Product, on_delete=models.CASCADE)
    RCP = models.CharField(max_length=5)
    RSP = models.CharField(max_length=5)
    Bal = models.CharField(max_length=5)
    Order = models.CharField(max_length=5)
    D_Qty = models.CharField(max_length=5)
    D_FP = models.CharField(max_length=5)
    UAD = models.CharField(max_length=5)
    Remark = models.CharField(max_length=50)
    Invoice = models.ForeignKey(invoice, on_delete=models.CASCADE)

    last_seen = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user+","+str(self.last_seen)+","+str(self.action)

class outlet(models.Model):
    CompanyName  = models.CharField(max_length=50)
    AccOpenDate  = models.CharField(max_length=15)
    Status  = models.CharField(max_length=15)
    Address  = models.CharField(max_length=100)
    CreditLimit  = models.CharField(max_length=10)
    Email  = models.CharField(max_length=20)
    BusinessNature  = models.CharField(max_length=20)
    Code  = models.CharField(max_length=20)
    CompanyCategory  = models.CharField(max_length=15)
    Attention  = models.CharField(max_length=20)
    Phone1  = models.CharField(max_length=20)
    Area  = models.CharField(max_length=25)
    Agent  = models.CharField(max_length=25)
    CreditTerm  = models.CharField(max_length=15)
    AddTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.CompanyName)+","+str(self.AccOpenDate)+","+str(self.Status)+","+str(self.Address)+","+str(self.CreditLimit)+","+str(self.Email)+","+str(self.BusinessNature)+","+str(self.Code)+","+str(self.CompanyCategory)+","+str(self.Attention)+","+str(self.Phone1)+","+str(self.Area)+","+str(self.Agent)+","+str(self.CreditTerm)

    def list(self):
        return [self.CompanyName, self.AccOpenDate, self.Status, self.Address, self.CreditLimit, self.Email, self.BusinessNature, self.Code, self.CompanyCategory, self.Attention, self.Phone1, self.Area, self.Agent, self.CreditTerm]

class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False

