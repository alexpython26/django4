from django import template
import women.views as views
from women.models import Category, TagPost

#отображение рубрик


register = template.Library()


# #простой тэг simple_tag
# @register.simple_tag()
# def get_categories():
#     return views.cats_db


#читает все рублири
@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


#тэг для шаблонов
@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}

