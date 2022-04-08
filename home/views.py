import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import ContactForm, ContactMessage
from product.models import Category, Product, Images, Comment, Variants
from django.db.models import Q
from django.views.generic import ListView
from specs.models import ProductFeatures
from django.shortcuts import get_object_or_404
from user.views import OrderProduct

class MyQ(Q):

    default = 'OR'


def index(request):
    catdata = Category.objects.filter(parent__isnull=True)
    subcatdata = Category.objects.filter(parent__id__in=catdata)
    categories = Category.objects.all()
    images = Images.objects.all()
    variant = Variants.objects.all()

    products_latest = Product.objects.all().order_by('-id')[:4]  # last 4 products
    products_slider = Product.objects.all().order_by('id')[:4]  #first 4 products
    products_picked = Product.objects.all().order_by('?')[:4]   #Random selected 4 products
    context={'products_slider': products_slider,
             'products_latest': products_latest,
             'products_picked': products_picked,
             'images': images,
             'variant': variant,
             'catdata': catdata,
             'subcatdata': subcatdata,
             'categories': categories
            }
    return render(request,'index.html',context)

def aboutus(request):

    context={}
    return render(request, 'about.html', context)

def contactus(request):
    
    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Ваше сообщение было отправлено. Мы обязательно его просмотрим.")
            return HttpResponseRedirect('/contact')
    form = ContactForm
    context={'form':form}
    return render(request, 'contactus.html', context)
    
class CategoryDetailView(ListView):
    model = Product
    context_object_name = 'category_products'
    template_name = 'category_products.html'
    paginate_by = 20


    def querystring_url(self):
        data = self.request.GET.copy()
        data.pop(self.page_kwarg, None)
        return data.urlencode()

    def get_queryset(self):
        
        qs = super().get_queryset().filter(
            category__slug=self.kwargs['slug']
        )
        if 'sort' in self.request.GET and 'search' not in self.request.GET:
                qs = qs.order_by(self.request.GET['sort'])
                return qs
        qd = self.request.GET.copy()
        qd.pop(self.page_kwarg, None)
        if 'search' in self.request.GET:
            qs = qs.filter(title__icontains=self.request.GET['search'])
        elif qd:
            url_kwargs = {}
            for item in self.request.GET:
                if len(self.request.GET.getlist(item)) > 1:
                    url_kwargs[item] = self.request.GET.getlist(item)
                else:
                    url_kwargs[item] = self.request.GET.get(item)
            q_condition_queries = Q()
            for key, value in url_kwargs.items():
                if isinstance(value, list):
                    q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
                else:
                    q_condition_queries.add(Q(**{'value': value}), Q.OR)
            pf = ProductFeatures.objects.filter(
                q_condition_queries
            ).prefetch_related('product', 'feature').values('product_id')
            qs = qs.filter(id__in=[pf_['product_id'] for pf_ in pf])
            if 'sort' in self.request.GET and 'search' in self.request.GET:
                qs = qs.order_by(self.request.GET['sort'])
                return qs
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['id'], slug=self.kwargs['slug'])
        return context 

def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def product_detail(request,id, slug):

    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    orderitems = OrderProduct.objects.filter(id=id,user=request.user)
    context = {'product': product,'category': category,
               'images': images, 'comments': comments,
               'orderitems': orderitems
               }
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    return render(request,'product_detail.html',context)

def faq(request):

    context = {
        'faq': faq,
    }
    return render(request, 'faq.html', context)