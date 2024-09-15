from django.contrib import admin
from django.urls import path
from Employee.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #path("",home),
    #path("", read),
    path("search/",read),
    path("display/",read),
    path('edit_employee/<int:id>/', edit_employee, name='edit_employee'),
    path('update_employee/<int:id>/', update_employee, name='update_employee'),
    path("add_employee/", add_employee, name='add_employee'),
    path("delete_employee/<id>/", delete_employee, name='delete_employee'),
    path("admin/", admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
