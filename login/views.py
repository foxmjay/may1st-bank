from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views import View


class DashboardLogout(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


class DashboardLogin(View):

    form_class = LoginForm
    template_name = 'login/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard')
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/dashboard')
            else:
                # Return an 'invalid login' error message.
                context = {}
                return HttpResponseRedirect('/login')
