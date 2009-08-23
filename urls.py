from django.conf.urls.defaults import *
from shop.models import Product

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'home/index.html'}),
)

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^products/$', 'object_list', {'queryset': Product.get_ordered_by_price(), 'template_name': 'product/list.html'})
)


urlpatterns += patterns('project.shop.views',
    (r'^create-product/$', 'create_product'),
    (r'^add-product/$', 'add_product'),
    (r'^edit-product/(?P<product_id>\d+)$', 'edit_product'),
    (r'^update-product/(?P<product_id>\d+)$', 'update_product'),
    (r'^delete-product/(?P<product_id>\d+)$', 'delete_product'),
 
    (r'^card/$', 'card'),
    (r'^add-to-card/(?P<product_id>\d+)$', 'add_to_card'),
    
    (r'^register/$', 'register'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout')
)
