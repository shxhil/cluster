from django.urls import path
from adminside import views

urlpatterns = [
    path("list/",views.CutomersListView.as_view(),name="cust-list"),
    path("edit/<int:pk>",views.CustomerUpdateView.as_view(),name='cust-edit'),
    path("remove/<int:pk>",views.CustomerDeleteView.as_view(),name="cust-remove"),
    path("detail/<int:pk>",views.CustomeDetailview.as_view(),name="cust-detail"),
    path("upload/",views.UploadCustomerView.as_view(),name="exel-upload"),
    path("logout/",views.AdminLogoutView.as_view(),name="logout"),
 
]