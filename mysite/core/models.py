from django.db import models

from django.conf import settings
from django.db import models
from django.db.models import Q


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


class User_action(models.Model):
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
    Item = models.CharField(max_length=50)
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


class Thread(models.Model):
    first        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    
    objects      = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False