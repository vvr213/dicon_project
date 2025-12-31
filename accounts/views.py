from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 複数AUTHENTICATION_BACKENDS対策：どれを使ったか明示する
            backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user, backend=backend)

            return redirect("dicon_app:home")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
