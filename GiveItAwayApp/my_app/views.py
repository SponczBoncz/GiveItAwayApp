from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.views import View

from my_app.models import Donation, Institution



class LandingPageView(View):
    template_name = 'my_app/index.html'

    def get(self, request, *args, **kwargs):
        active = request.GET.get("active")
        if active == None:
            active = 1
        total_bags_quantity = Donation.objects.aggregate(Sum('quantity'))
        all_donated_institutions = len(Donation.objects.values('institution').annotate(count=Count('institution')))
        all_institutions = Institution.objects.all().order_by('name')
        all_foundations = all_institutions.filter(type=0)
        all_foundations_pages = len(all_foundations)
        all_foundations_paginator = Paginator(all_foundations, 5)  # Show 5 per page.
        all_foundations_page_number = request.GET.get("all_foundations_page")
        all_foundations_page_obj = all_foundations_paginator.get_page(all_foundations_page_number)
        all_non_governmental_foundations = all_institutions.filter(type=1)
        all_non_governmental_foundations_pages = len(all_non_governmental_foundations)
        all_non_governmental_foundations_paginator = Paginator(all_non_governmental_foundations, 5)  # Show 5 per page.
        all_non_governmental_foundations_page_number = request.GET.get("all_non_governmental_foundations_page")
        all_non_governmental_foundations_page_obj = all_non_governmental_foundations_paginator.get_page(all_non_governmental_foundations_page_number)
        all_local_crowdfunding = all_institutions.filter(type=2)
        all_local_crowdfunding_pages = len(all_local_crowdfunding)
        all_local_crowdfunding_paginator = Paginator(all_local_crowdfunding, 1)  # Show 5 per page.
        all_local_crowdfunding_page_number = request.GET.get("all_local_crowdfunding_page")
        all_local_crowdfunding_page_obj = all_local_crowdfunding_paginator.get_page(all_local_crowdfunding_page_number)
        context = {
            'total_bags_quantity': total_bags_quantity,
            'all_donated_institutions': all_donated_institutions,
            'all_foundations': all_foundations,
            'all_foundations_page_obj': all_foundations_page_obj,
            'all_foundations_pages': all_foundations_pages,
            'all_non_governmental_foundations': all_non_governmental_foundations,
            'all_non_governmental_foundations_page_obj': all_non_governmental_foundations_page_obj,
            'all_non_governmental_foundations_pages': all_non_governmental_foundations_pages,
            'all_local_crowdfunding': all_local_crowdfunding,
            'all_local_crowdfunding_page_obj': all_local_crowdfunding_page_obj,
            'all_local_crowdfunding_pages': all_local_crowdfunding_pages,
            'active': active,
        }

        print(context)
        return render(request, self.template_name, context)

class LoginView(View):
    template_name = 'my_app/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            return redirect('register')

class LogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('landing')

class RegisterView(View):
    template_name = 'my_app/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        first_name = request.POST['name']
        last_name = request.POST['surname']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        if first_name == "" or last_name == "" or password == "" or password2 == "" or email == "":
            context = "Wszystkie pola muszą być wypełnione!"
            return render(request, self.template_name, {'context':context})
        if password != password2:
            context = "Hasłą muszą być takie same!"
            return render(request, self.template_name, {'context':context})
        try:
            validate_email(email)
            user = User.objects.create_user(email, email, password, first_name=first_name, last_name=last_name)
            return redirect('login')
        except ValidationError:
            context = "Niepoprawny email!"
            return render(request, self.template_name, {'context':context})
            pass





class AddDonationView(View):
    template_name = 'my_app/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class TestView(View):
    template_name = 'my_app/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)