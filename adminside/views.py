from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View,FormView,ListView,UpdateView,DetailView
from adminside.forms import AdminLoginForm,CustomerUpdateForm,UploadForm
from django.contrib import messages
from publicuser.models import CustomerReg
from django.urls import reverse_lazy

import pandas as pd
from django.db import IntegrityError
from publicuser.utils import generate_username
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from tablib import Dataset
from .resource import UploadResource

# Create your views here.
def permission_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
desc=[permission_required,never_cache]

class AdminLoginView(FormView):
    template_name="main/login.html"
    form_class=AdminLoginForm

    def form_valid(self, form):
        uname=form.cleaned_data.get("username")
        pwd=form.cleaned_data.get("password")
        user_obj=authenticate(self.request,username=uname,password=pwd)
        print(user_obj)
        if user_obj is not None :
          if  user_obj.is_superuser:
                login(self.request,user_obj)
                messages.success(self.request,"login succesfully")
                return redirect("cust-list")
        
        messages.error(self.request,"Invalid username or Password")
        return super().form_invalid(form)

@method_decorator(desc,name="dispatch")
class CutomersListView(ListView):
    template_name="main/list.html"
    context_object_name="forms"
    model=CustomerReg

# class CustomerUpdateView(UpdateView):
#     template_name="main/update.html"
#     form_class=CustomerUpdateForm
#     model=CustomerReg
#     success_url=reverse_lazy("cust-list")

@method_decorator(desc,name="dispatch")
class CustomerUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user_obj=CustomerReg.objects.get(id=id)
        form=CustomerUpdateForm(instance=user_obj)
        return render(request,"main/update.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user_obj=CustomerReg.objects.get(id=id)
        form=CustomerUpdateForm(request.POST,instance=user_obj)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request,"succesfully updated")
            return render(request,"main/update.html",{"form":form})

        else:
            print("failed")
            return render(request,"main/update.html",{"form":form})




@method_decorator(desc,name="dispatch")
class CustomeDetailview(DetailView):
    template_name="main/detail.html"
    context_object_name="data"
    model=CustomerReg


@method_decorator(desc,name="dispatch")
class CustomerDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        CustomerReg.objects.get(id=id).delete()
        messages.success(request,"succesfully deleted")
        return redirect ('cust-list')

@method_decorator(desc,name="dispatch")
class AdminLogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.error(request,"logout succesfully ")
        return redirect("login")
    
# ----------------------

@method_decorator(desc,name="dispatch")
class UploadCustomerView(View):
    def get(self,request,*args,**kwargs):
        form=UploadForm()
        return render(request,"main/upload_customer.html",{"form":form})
    
    def post(self, request, *args, **kwargs):
        form = UploadForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            excel_file = request.FILES.get("file")
            print(excel_file)

            if excel_file is not None:
                df = pd.read_excel(excel_file)

                duplicate_usernames = []

                for index, row in df.iterrows():
                    name = row['name']
                    mobile_number =str (row['mobile_number'])
                    print(f"Mobiletype: {type(mobile_number)}")
                    whatsapp_number = row['whatsapp_number']
                    email = row['email']
                    date_of_birth = row['date_of_birth']
                    year = str(date_of_birth.year)
                    username = generate_username(name, mobile_number, year)

                #     customer = CustomerReg.objects.create(
                #     name=name,
                #     mobile_number=mobile_number,
                #     whatsapp_number=whatsapp_number,
                #     email=email,
                #     date_of_birth=date_of_birth,)
                #     username=username

                #     return redirect("cust-list")
                # else:
                #     return render(request,"main/upload_customer.html",{"form":form})

                    try:
                        customer = CustomerReg.objects.create(
                            name=name,
                            mobile_number=mobile_number,
                            whatsapp_number=whatsapp_number,
                            email=email,
                            date_of_birth=date_of_birth,
                            username=username  # Corrected typo
                        )

                    except IntegrityError:
                        duplicate_usernames.append(username)

                if duplicate_usernames:
                    messages.error(request,"Please fix the duplicate usernames and re-upload the file.")
                    return render(request, "main/upload_customer.html", {"form": form, 'duplicate_usernames': duplicate_usernames})
                else:
                     messages.success(request,"succesfull uploaded")
                     return redirect("cust-list")
        #     else:
        #         return render(request, "main/upload_customer.html", {"form": form})
        # else:
        #     return render(request, "main/upload_customer.html", {"form": form})
        return render(request,"main/upload_customer.html",{"form":form})


# def UploadCustomerView(request):
#     if request.method =='POST':
#          upload_resource=UploadResource()
#          dataset=Dataset()
#          excel_file = request.FILES['file']
#          imported_data=dataset.load(excel_file.read(),format='xlsx')
#          for data in imported_data:
#              value=CustomerReg(
#                  data[0],
#                  data[1],
#                  data[2],
#                  data[3],
#                  data[4]

#              )

#     return render(request, "main/upload_customer.html")
