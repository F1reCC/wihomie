from collections import defaultdict
from django.db.models import Count

from django import template
from django.utils.safestring import mark_safe
from specs.models import ProductFeatures

from order.models import ShopCart
from product.models import Category
from django.urls import reverse

register = template.Library()


@register.simple_tag
def categorylist():
    return Category.objects.all()


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count

@register.simple_tag    
def categoryTree(id,menu):
    if id <= 0: # Main categories
        query = Category.objects.filter(parent_id__isnull=True).order_by("id")
        querycount = Category.objects.filter(parent_id__isnull=True).count()
    else: # Sub Categories
        query = Category.objects.filter(parent_id=id)
        querycount = Category.objects.filter(parent_id=id).count()
    if querycount > 0:
        for rs in query:
            subcount = Category.objects.filter(parent_id=rs.id).count()
            if subcount > 0:
                menu += '\t<li>\n'
                menu += '\t<input type="checkbox" name="toggle" class="toggleSubmenu" id="sub_' + str(rs.id) + '">\n'
                menu += '\t<a href="#">' + rs.title + '</a>\n'
                menu += '\t<label for="sub_' + str(rs.id) + '" class="toggleSubmenu"><i class="fa fa-plus right" aria-hidden="true"></i><i class="fa fa-minus" aria-hidden="true"></i></label>\n'
                menu += '\t\t<ul>\n'
                menu += categoryTree(int(rs.id),'')
                menu += '\t\t</ul>\n'
                menu += "\t</li>\n\n"
            else:
                menu += '\t\t\t\t<li><a href="' + reverse('category_products', args=(rs.id, rs.slug)) + '">' + rs.title + '</a></li>\n'

    return menu

@register.simple_tag    
def categoryIndexTree(id,menu):
    if id <= 0: # Main categories
        query = Category.objects.filter(parent_id__isnull=True).order_by("id")
        querycount = Category.objects.filter(parent_id__isnull=True).count()
    else: # Sub Categories
        query = Category.objects.filter(parent_id=id)
        querycount = Category.objects.filter(parent_id=id).count()
    if querycount > 0:
        for rs in query:
            menu += '\t<div class="col-12 col-md-6 col-lg-4 d-flex" style="margin-top: -30px;">\n'
            menu += '\t<div class="justify-content-between w-100 cat-index">\n'
            menu += '\t<div class="card category-card">\n'
            menu += '\t<div class="faces">\n'
            menu += '\t<div class="face front">\n'
            menu += '\t<div class="cat-index-header text-center">\n'
            menu += '\t<h1><p>' + rs.title + '</p></h1>\n'
            menu += '\t</div>\n'
            menu += '\t<div class="cat-index-img">\n'
            menu += '\t<div class="cat-index-img-wrapper">\n'
            menu += '\t<img src="' + rs.image.url + '" alt="" class="img-fluid">\n'
            menu += '\t</div>\n'
            menu += '\t</div>\n'
            menu += '\t</div>\n'
            menu += '\t<div class="face back">\n'
            menu += '\t<ul class="pt-4 w-100 p-4 back-card-border">\n'
            menu += categoryTree(int(rs.id),'')
            menu += '\t\t</ul>\n'
            menu += '\t</div>\n\n'
            menu += '\t</div>\n'
            menu += '\t</div>\n'
            menu += '\t</div>\n'
            menu += '\t</div>\n'  
            
    return menu


@register.filter
def product_spec(category):
    product_features = ProductFeatures.objects.filter(product__category=category)
    feature_and_values = defaultdict(list)
    for product_feature in product_features:
        if product_feature.value not in feature_and_values[(product_feature.feature.feature_name, product_feature.feature.feature_filter_name)]:
            feature_and_values[
                (product_feature.feature.feature_name, product_feature.feature.feature_filter_name)
            ].append(product_feature.value)
    print(feature_and_values)
    search_filter_body = """<div class="col-md-12"><center><strong>ФИЛЬТР</strong></center> <hr>{}</div>"""
    mid_res = ""

    
    for (feature_name, feature_filter_name), feature_values in feature_and_values.items():
        
        feature_name_html = f"""<p><b>{feature_name}</b></p>"""
        feature_values_res = ""
        for f_v in feature_values:
            mid_feature_values_res = \
                "<input type='checkbox' class='check' id='check-option-{feature_name}' name='{f_f_name}' value='{feature_name}' onchange='this.form.submit();'> {feature_name}</br>".format(
                    feature_name=f_v, f_f_name=feature_filter_name
                )
            feature_values_res += mid_feature_values_res
        feature_name_html += feature_values_res
        mid_res += feature_name_html + '<hr>'
    res = search_filter_body.format(mid_res)
    return mark_safe(res)