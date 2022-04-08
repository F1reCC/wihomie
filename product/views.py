from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import CommentForm, Comment


def index(request):
   return  HttpResponse("My Product Page")


def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
         data = Comment()  # create relation with model
         data.comment = form.cleaned_data['comment']
         data.comment_plus = form.cleaned_data['comment_plus']
         data.comment_minus = form.cleaned_data['comment_minus']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.product_id=id
         data.user = request.user
         data.save()  # save data to table
         messages.success(request, "Ваш отзыв успешно отправлен. Спасибо за Ваш интерес.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)


def colors(request):
    return render(request,'product_color.html')