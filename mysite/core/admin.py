from django.contrib import admin
from .models import *

class user_actionAdmin(admin.ModelAdmin):
    list_display = ["user","last_seen","action"]
    list_filter = ["user","action","last_seen"]
    search_fields = ["user","action","last_seen"]
    class Meta:
        model = user_action

class user_recordAdmin(admin.ModelAdmin):
    list_display = ["User_ID","Role","last_seen"]
    list_filter = ["User_ID","Role","last_seen"]
    search_fields = ["User_ID","Role","last_seen"]
    class Meta:
        model = user_record

class ProductAdmin(admin.ModelAdmin):
    list_display = ["Barcodes","Brand","Name","PackSize","CtnQty","RCP","RSP","RetailerMargin","FastPay","UlkPurchase"]
    list_filter = ["Brand","PackSize","CtnQty"]
    search_fields = ["Barcodes","Brand","Name","PackSize","CtnQty","RCP","RSP","RetailerMargin","FastPay","UlkPurchase"]
    class Meta:
        model = Product

class orderAdmin(admin.ModelAdmin):
    list_display = ["Item","RCP","RSP","Bal","Order","D_Qty","D_FP","UAD","Remark","Invoice"]
    list_filter = ["Remark"]
    search_fields = ["Invoice"]
    class Meta:
        model = order

class invoiceAdmin(admin.ModelAdmin):
    list_display = ["Inv_no","Status","last_seen"]
    list_filter = ["Status"]
    search_fields = ["Inv_no"]
    class Meta:
        model = invoice

class outletdAdmin(admin.ModelAdmin):
    list_display = ["CompanyName","AccOpenDate","Status","Address","CreditLimit","Email","BusinessNature","Code","CompanyCategory","Attention","Phone1","Area","Agent","CreditTerm"]
    list_filter = ["CompanyCategory","Status","Agent","CreditTerm"]
    search_fields = ["CompanyName","CompanyCategory","CreditTerm","Code","Area","Agent"]
    class Meta:
        model = outlet

#admin.site.register(user_action,user_actionAdmin)
#admin.site.register(user_record,user_recordAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(order,orderAdmin)
admin.site.register(invoice,invoiceAdmin)
admin.site.register(outlet,outletdAdmin)