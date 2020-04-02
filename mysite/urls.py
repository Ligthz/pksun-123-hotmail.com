from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


from mysite.core import views


urlpatterns = [
    path('', views.Home, name='index'),
    path('login', views.login, name='login'),
    path('dashboard/', views.Home, name='home'),

    path('order/', views.order, name='order'),
    path('order_post/', views.order_post, name='order_post'),
    path('order_confirm/', views.order_confirm, name='order_post'),

    path('MQTT/', views.MQTT),
    path('up_graph/', views.up_graph),



    path('signup/', views.signup, name='signup'),
    path('secret/', views.secret_page, name='secret'),
    path('secret2/', views.SecretPage.as_view(), name='secret2'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('upload/', views.upload, name='upload'),
    path('books/', views.book_list, name='book_list'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('books/<int:pk>/', views.delete_book, name='delete_book'),

    path('class/books/', views.BookListView.as_view(), name='class_book_list'),
    path('class/books/upload/', views.UploadBookView.as_view(), name='class_upload_book'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
