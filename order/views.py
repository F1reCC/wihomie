from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from order.models import ShopCart, Order, OrderProduct
from order.forms import OrderForm
from product.models import Category, Product, Variants
from user.models import UserProfile


def index(request):
    return HttpResponse ("Order Page")

@login_required(login_url='/login') # Check login
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    product= Product.objects.get(pk=id)

    if product.variant != 'None':
        
        variantid = request.POST.get('variantid')  # from variant add to cart
        sizeid = request.POST.get('size')
        if variantid: 
            checkinvariant = ShopCart.objects.filter(variant_id=variantid, user=request.user)  # Check product in shopcart
        if sizeid: 
            checkinvariant = ShopCart.objects.filter(variant_id=sizeid, user=request.user)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user=request.user) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        qty = int(request.POST.get('quantity'))
        size = request.POST.get('size')
        if control == 0:
            data = ShopCart()
            data.user = request.user
            data.product_id = id
            
            if product.variant != 'None':
                if size:
                    data.variant_id = size
                else:
                    data.variant_id = variantid
            data.quantity = qty
            data.save()
            messages.success(request, "Товар успешно добавлен в корзину")
        else:
            messages.warning(request, "Товар уже в корзине")
        return HttpResponseRedirect(url)

@login_required(login_url='/login') # Check login
def updateshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    
    if request.method == 'POST':  # if there is a post
        qty = int(request.POST.get('quantity'))
        variantid = request.POST.get('variantid')  # from variant add to cart
        product= Product.objects.get(pk=id)

        if product.variant != 'None':
            data = ShopCart.objects.get(variant_id=variantid, product_id=id, user=request.user)
            if qty <= data.variant.quantity:
                data.quantity = qty
                data.save()
                messages.success(request, "Количество товаров успешно обновлено")
            else:
                messages.warning(request, "Такого количества нет на складе")
        else:
            data = ShopCart.objects.get(product_id=id, user=request.user)
            if qty <= data.product.amount:
                data.quantity = qty
                data.save()
                messages.success(request, "Количество товаров успешно обновлено")
            else:
                messages.warning(request, "Такого количества нет на складе")
        
        return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user=request.user)
    total=0

    for rs in shopcart:
        total += rs.price * rs.quantity
    #return HttpResponse(str(total))
    context={'shopcart': shopcart,
             'category':category,
             'total': total,
             }
    return render(request,'shopcart_products.html',context)

@login_required(login_url='/login') # Check login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Товар успешно удалён из корзины.")
    return HttpResponseRedirect("/shopcart")

def order_completed(request):
    order = Order.objects.filter(user=request.user).last()
    context = {'order': order}
    return render(request,'order_completed.html', context)

def orderproduct(request):
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user=request.user)
    user_profile = UserProfile.objects.filter(user=request.user)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST or None)
       
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            if total == 0:
                return HttpResponseRedirect("/shopcart")
            data = form.save(commit=False)
            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.buying_type = form.cleaned_data['buying_type']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.paying_type = form.cleaned_data['paying_type']
            data.comment = form.cleaned_data['comment']
            data.user = request.user
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(7).upper() # random cod
            data.code =  ordercode
            data.save() #

            user_profile.update(
                address = form.cleaned_data['address'],
                city = form.cleaned_data['city'],
                phone = form.cleaned_data['phone'],
            )
            
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user      = request.user
                detail.quantity     = rs.quantity
                detail.price    = rs.product.price
                detail.variant_id   = rs.variant_id
                detail.amount        = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if  rs.product.variant=='None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.variant_id)
                    variant.quantity -= rs.quantity
                    variant.save()
                #************ <> *****************

            ShopCart.objects.filter(user=request.user).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            return HttpResponseRedirect("/order/order-completed")
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form=OrderForm()
    profile = UserProfile.objects.get(user=request.user)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'Order_Form.html', context)