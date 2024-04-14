from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    template_name = 'my_app/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

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