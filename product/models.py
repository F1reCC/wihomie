from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
#import mptt

class Category(MPTTModel):
    STATUS = (
        ('True', 'Показывать'),
        ('False', 'Скрыть'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_products', kwargs={'slug': self.slug, 'id' : self.id})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

class Product(models.Model):
    STATUS = (
        ('True', 'Показывать'),
        ('False', 'Скрыть'),
    )

    VARIANTS = (
        ('None', 'Нет'),
        ('Size', 'Размер'),
        ('Color', 'Цвет'),
        ('Size-Color', 'Размер-Цвет'),

    )
    category = TreeForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='images/', null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    detail=RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    features = models.ManyToManyField("specs.ProductFeatures", blank=True, related_name='features_for_product')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_features(self):
        return {f.feature.feature_name: ' '.join([f.value, f.feature.unit or ""]) for f in self.features.all()}

    def __str__(self):
        return self.title

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


class Images(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, verbose_name="Наименование изображения")
    image=models.ImageField(upload_to='images/',null=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('New', 'Новый'),
        ('True', 'Одобрен'),
        ('False', 'Отклонён'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250,blank=True, verbose_name="Комментарий")
    comment_plus = models.CharField(max_length=50, blank=True, verbose_name="Плюсы товара")
    comment_minus = models.CharField(max_length=50, blank=True, verbose_name="Минусы товара")
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New', verbose_name="Статус")
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'comment_plus', 'comment_minus', 'rate']


class Color(models.Model):
    name = models.CharField(max_length=20, verbose_name="Наименование цвета")
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Код цвета")
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Variants(models.Model):
    
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование варианта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Цвет")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Размер")
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    #price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Цена")

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""
