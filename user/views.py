from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from home.models import FAQ
from order.models import Order, OrderProduct
from product.models import Category, Comment
from user.forms import LoginForm, SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile
from django.views.generic import View

@login_required(login_url='/login') # Check login
def index(request):
    category = Category.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {'category': category,
               'profile':profile
               }
    return render(request,'user_profile.html',context)

class LoginView(View):
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = LoginForm(request.POST or None)
            context = {
                'form': form
            }
            return render(request, 'login_form.html', context)
        else:
            return HttpResponseRedirect('/')
    
    def post(self, request, *args, **kwargs):
        
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'login_form.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

class SignUpView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = SignUpForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'signup_form.html', context)
        else:
            messages.add_message(request, messages.INFO, 'Вы уже авторизованы')
            return HttpResponseRedirect('/')


    def post(self, request, *args, **kwargs):
        
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            data=UserProfile()
            data.user = request.user
            data.save()
            messages.success(request, 'Ваш профиль был успешно создан!')
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'signup_form.html', context)


@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлён!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Ваш пароль был успешно обновлён!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Пожалуйста введите корректные данные.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        #category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,#'category': category
                       })

@login_required(login_url='/login') # Check login
def user_orders(request):
    orders = Order.objects.filter(user=request.user)

    context = {
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    order = Order.objects.get(user=request.user, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login') # Check login
def user_order_product(request):
    order_product = OrderProduct.objects.filter(user=request.user).order_by('-id')
    context = {
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    order = Order.objects.get(user=request.user, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user=request.user)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


def user_comments(request):
    comments = Comment.objects.filter(user=request.user)
    context = {
        #'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    Comment.objects.filter(id=id, user=request.user).delete()
    messages.success(request, 'Комментарий далён..')
    return HttpResponseRedirect('/user/comments')

