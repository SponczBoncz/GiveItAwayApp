from django.db.models import Count, Sum
from django.shortcuts import render, get_object_or_404
from django.views import View

from my_app.models import Donation


class LandingPageView(View):
    template_name = 'my_app/index.html'

    def get(self, request, *args, **kwargs):
        total_bags_quantity = Donation.objects.aggregate(Sum('quantity'))
        all_donated_institutions = len(Donation.objects.values('institution').annotate(count=Count('institution')))
        context = {
            'total_bags_quantity': total_bags_quantity,
            'all_donated_institutions': all_donated_institutions,
        }
        return render(request, self.template_name, context)

class LoginView(View):
    template_name = 'my_app/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class RegisterView(View):
    template_name = 'my_app/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class AddDonationView(View):
    template_name = 'my_app/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class TestView(View):
    template_name = 'my_app/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)