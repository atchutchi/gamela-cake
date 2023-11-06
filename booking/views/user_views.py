# booking/views/user_views.py
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')  # Assuming you have a 'login' named URL

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)
