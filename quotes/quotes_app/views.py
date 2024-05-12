from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode

from .forms import QuoteForm, AuthorForm, RegisterForm, LoginForm, CustomPasswordResetConfirmForm, \
    CustomPasswordResetForm
from .models import Quote, Author, User


def main(request):
    quotes = Quote.objects.all()
    context = {'quotes': quotes}
    return render(request, 'base.html', context)


def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'quote.html', {'form': form})

    return render(request, 'quote.html', {'form': QuoteForm()})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'author.html', {'form': form})

    return render(request, 'author.html', {'form': AuthorForm()})


def author_detail(request, fullname):
    quotes_by_author = Quote.objects.filter(author=fullname)

    author = Author.objects.get(fullname=fullname)

    context = {'author': author, 'quotes_by_author': quotes_by_author}
    return render(request, 'author_detail.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect(to='quotes_app:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'register.html', context={"form": form})

    return render(request, 'register.html', context={"form": RegisterForm()})


def user_login(request):
    if request.user.is_authenticated:
        return redirect(to='quotes_app:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='quotes_app:login')

        login(request, user)
        return redirect(to='quotes_app:main')

    return render(request, 'login.html', context={"form": LoginForm()})


@login_required
def custom_password_reset(request):
    if request.method == 'POST':
        send_mail(
            'Password reset request',
            'Here is the link to reset your password: {}'.format(
                request.build_absolute_uri(reverse_lazy('password_reset_confirm'))),
            'noreply',
            [request.POST['email']],
            fail_silently=False,
        )
        return redirect('password_reset_done')
    return render(request, 'password_reset_form.html', context={"form": CustomPasswordResetForm()})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordResetConfirmForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = CustomPasswordResetConfirmForm()

        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse('Password reset link is invalid or has expired.')


def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(to='quotes_app:main')
