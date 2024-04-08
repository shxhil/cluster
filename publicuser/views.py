from django.views.generic import CreateView,View
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegistartionForm
from publicuser.models import CustomerReg
from django.shortcuts import render,redirect
from .utils import generate_username
from django.db import IntegrityError


# Create your views here.


# class CustomerRegView(CreateView):
#     template_name = 'user/registration.html'
#     form_class = RegistartionForm
#     success_url = reverse_lazy('register')

#     def form_valid(self, form):
#         uname=form.cleaned_data.get("username")
#         if CustomerReg.objects.filter(username=uname).exists():
#             messages.error(self.request,"username already existed.Please create another response")
#             return self.form_invalid(form)

        
#         messages.success(self.request, "Successfully created profile")
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(self.request, "Failed to create account")
#         return super().form_invalid(form)


class CustomerRegView(View):
    def get(self, request, *args, **kwargs):
        form = RegistartionForm()
        return render(request, "user/registration.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = RegistartionForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['name']
            number = form.cleaned_data['mobile_number']
            dob = form.cleaned_data["date_of_birth"]
            y = str(dob.year)
            generated_username = generate_username(uname, number, y)
            
            try:
        
                customer = CustomerReg.objects.create(
                    name=uname,
                    mobile_number=number,
                    date_of_birth=dob,
                    username=generated_username
                )
                messages.success(request, "Registration successful")
                return redirect('register')  
            except IntegrityError:
                # If a duplicate username is encountered, display an error message
                messages.error(request, "Username already exists. Please try again.")
                return render(request, "user/registration.html", {"form": form})
        
        # If form is not valid, render the form again
        return render(request, "user/registration.html", {"form": form})


    