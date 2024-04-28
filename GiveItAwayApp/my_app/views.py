from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.views import View

from my_app.models import Donation, Institution, Category



class LandingPageView(View):
    template_name = 'my_app/index.html'

    def get(self, request, *args, **kwargs):
        active = request.GET.get("active",1)
        total_bags_quantity = Donation.objects.aggregate(Sum('quantity'))
        all_donated_institutions = len(Donation.objects.values('institution').annotate(count=Count('institution')))
        all_institutions = Institution.objects.all().order_by('name')
        all_foundations = all_institutions.filter(type=0)
        all_foundations_pages = len(all_foundations)
        all_foundations_paginator = Paginator(all_foundations, 2)  # Show 5 per page.
        all_foundations_page_number = request.GET.get("all_foundations_page")
        all_foundations_page_obj = all_foundations_paginator.get_page(all_foundations_page_number)
        all_non_governmental_foundations = all_institutions.filter(type=1)
        all_non_governmental_foundations_pages = len(all_non_governmental_foundations)
        all_non_governmental_foundations_paginator = Paginator(all_non_governmental_foundations, 1)  # Show 5 per page.
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


        return render(request, self.template_name, context)

class LoginView(View):
    template_name = 'my_app/login.html'

    def get(self, request, *args, **kwargs):
        message = request.GET.get('message')
        return render(request, self.template_name, {'message': message})

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





class AddDonationView(LoginRequiredMixin, View):
    template_name = 'my_app/form.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        all_categories = Category.objects.all().order_by('name')
        all_institutions = Institution.objects.all().order_by('name')
        context = {
            'all_categories': all_categories,
            'all_institutions': all_institutions,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        organization_name = request.POST.get('organization')
        quantity = request.POST.get('bags')
        street = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        date = request.POST.get('data')
        time = request.POST.get('time')
        comment = request.POST.get('more_info')
        choosenCategories = request.POST.getlist('categories')
        organization = get_object_or_404(Institution, name=organization_name)
        if organization and quantity and street and city and postcode and phone and date and time and choosenCategories:
            donation = Donation.objects.create(
                institution=organization,
                quantity=quantity,
                address=street,
                city=city,
                phone_number=phone,
                zip_code=postcode,
                pick_up_date=date,
                pick_up_time=time,
                pick_up_comment=comment,
                user=request.user,
            )
            for category in choosenCategories:
                donation_category = get_object_or_404(Category, name=category)
                donation.categories.add(donation_category)
            return redirect('form_confirmation')

        else:
            print('no organization')
            print(request.POST)
            all_categories = Category.objects.all().order_by('name')
            all_institutions = Institution.objects.all().order_by('name')
            context = {
                'all_categories': all_categories,
                'all_institutions': all_institutions,
                'warning': "Wszystkie pola muszą być poprawnie wypełnione!",
            }
            return render(request, self.template_name, {'context':context})

class FormConfirmationView(View):
    template_name = 'my_app/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ProfileView(View):
    template_name = 'my_app/profile.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        all_donations = Donation.objects.filter(user=request.user).order_by('is_taken', 'pick_up_date', 'pick_up_time')
        for donation in all_donations:
            print(donation.pick_up_date)
            print(donation.is_taken)
        return render(request, self.template_name, {'all_donations':all_donations})

    def post(self, request, *args, **kwargs):
        donation_id = request.POST.get('action')
        print(donation_id)
        donation = Donation.objects.get(pk=donation_id)
        if donation:
            if donation.is_taken == True:
                donation.is_taken = False
                donation.save()
            else:
                donation.is_taken = True
                donation.save()
            # all_donations = Donation.objects.filter(user=request.user).order_by('pick_up_date').order_by('is_taken')
            url_with_anchor = '/profile#donation-list'
            # template_name = '#donation-list'
            # return render(request, self.template_name, {'all_donations': all_donations})
            return redirect(url_with_anchor)

class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'my_app/profile-edition.html'

    def get(self, request, *args, **kwargs):
        message = request.GET.get('message')
        return render(request, self.template_name, {'message':message})

    def post(self, request, *args, **kwargs):
        user_password = request.POST.get('password')
        logged_in_user = request.user
        user = authenticate(username=logged_in_user.username, password=user_password)
        if user is not None:
            print('Password correct')
            new_user_first_name = request.POST.get('first_name')
            new_user_last_name = request.POST.get('last_name')
            new_user_email = request.POST.get('email')
            if new_user_first_name != "":
                user.first_name = new_user_first_name
            if new_user_last_name != "":
                user.last_name = new_user_last_name
            if new_user_email != "":
                try:
                    validate_email(new_user_email)
                except ValidationError:
                    url_redirect = '/profile_edition/?message=Błędny email!'
                    return redirect(url_redirect)
                    pass
                user.email = new_user_email
            user.save()
            url_redirect = '/profile_edition/?message=Profil zaktualizowany!'
        else:
            print('Wrong password')
            url_redirect = '/profile_edition/?message=Błędne hasło!'
        return redirect(url_redirect)

class ProfilePasswordUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'my_app/profile-password-edition.html'

    def get(self, request, *args, **kwargs):
        message = request.GET.get('message')
        return render(request, self.template_name, {'message':message})

    def post(self, request, *args, **kwargs):
        user_password = request.POST.get('password')
        logged_in_user = request.user
        user = authenticate(username=logged_in_user.username, password=user_password)
        if user is not None:
            print('Password correct')
            new_password_1 = request.POST.get('new_password_1')
            new_password_2 = request.POST.get('new_password_2')
            if new_password_1 != '':
                if new_password_1 == new_password_2:
                    logged_in_user.set_password(new_password_1)
                    logged_in_user.save()
                    url_redirect = reverse('login')
                    full_url = f"{url_redirect}?message=Hasło zmienione!"
                    return redirect(full_url)
                else:
                    url_redirect = '/profile_password_edition/?message=Nowe hasła są różne!'
            else:
                url_redirect = '/profile_password_edition/?message=Hasło nie może być puste!'
        else:
            print('Wrong password')
            context = "Wrong password!"
            url_redirect = '/profile_password_edition/?message=Błędne hasło!'
        return redirect(url_redirect)