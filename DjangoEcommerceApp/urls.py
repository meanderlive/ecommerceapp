#from DjangoEcommerceApp import new_views
from django.urls import path,re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

#from DjangoEcommerce import settings
from django.conf import settings
from django.contrib.auth.views import LogoutView
from .new_views import *
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    # admin login
    # register
    #path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('password_reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('', home_redirect, name='home'),
    path('', register, name='register'),
    path('custom_login', custom_login, name='custom_login'),
    path('forget-password', update_password, name='forget-password'),
    path('change-password/', change_password, name='change_password'),
    path('all-password/', update_profile, name='update_profile'),
    path('insert-profile/', insert_profile, name='insert-profile'),
    path('logout/', LogoutView.as_view(next_page='register'), name='logout'),
    #  user profile update
    path('profile/', get_profile, name='profile_view'),

    # URL pattern for updating the user profile
    path('profile/update/', update_profile, name='profile_update'),

    # URL pattern for deleting the user profile
    path('profile/delete/', delete_profile, name='profile_delete'),

    # end ===========
    path('admin_login_process',adminLoginProcess,name="admin_login_process"),
    path('admin/', adminLogin,name="admin_login"),
    path('admin_logout_process',adminLogoutProcess,name="admin_logout_process"),
    path('x-account', jewellery_account,name="jewellery-account"),
    path('store-shop', jewellery_store_shop,name="jewellery-store-shop"),
    path('cat', jewellery_store_categories,name="jewellery-store-categories"),
    path('xxblog', jewellery_store_blog,name="jewellery-store-blog"),
    path('contact', jewellery_store_contact,name="jewellery-store-contact"),
    path('contact_form', contact_form,name="contact_form"),
    path('wishlist', jewellery_store_wishlist,name="jewellery-store-wishlist"),
    path('about', jewellery_store_about,name="jewellery-store-about"),
    path('faq', jewellery_store_faq,name="jewellery-store-faq"),
    path('account', jewellery_store_account,name="jewellery-store-account"),
    path('cart', jewellery_store_cart,name="jewellery-store-cart"),
    path('checkout', jewellery_store_checkout,name="jewellery-store-checkout"),
    path('product', jewellery_store_single_product,name="jewellery-store-single-product"),

    # jewellery admin
    path('upload/', upload_images, name='upload_images'),
    path('xxcat', jewellery_store_image_cat, name='jewellery-store-cat-images'),
    path('cat-images', jewellery_td_store_image_cat, name='jewellery-td-store-cat-images'),
    path('store_cat/<int:pk>', update_jewellery_store_cat, name='update_jewellery_store_cat'),
    path('store_del/<int:pk>', delete_jewellery_store_cat, name='delete_jewellery_store_cat'),
    path('featured', featured_product_upload, name='jewellery-store-featured-products'),
    path('featured-table', jewellery_td_featured_product, name='jewellery-store-td-featured-products'),
    path('featured-up/<int:pk>', update_jewellery_store_featured_product, name='jewellery_store_up_featured_products'),
    path('featured-del/<int:pk>', delete_jewellery_featured_product, name='jewellery-store-del-featured-products'),
    path('table', table, name='table'),
    path('jewellery_admin', jewellery_admin, name='jewellery_admin'),

    path('insta', insta_images, name='jewellery-store-insta'),
    path('insta-td', jewellery_td_insta, name='jewellery-td-store-instagram'),
    path('insta-up/<int:pk>', update_jewellery_insta, name='update_jewellery_insta'),
    path('insta-del/<int:pk>', delete_jewellery_insta, name='delete_jewellery_insta'),
    path('category', categories_upload, name='jewellery-store-categories-x'),
    path('mm-categories-td', jewellery_td_categories, name='jewellery-td-store-categories'),
    path('categories-up/<int:pk>', update_jewellery_categories, name='update_jewellery_categories'),
    path('catt-del/<int:pk>', delete_jewellery_categories, name='delete_jewellery_categories'),
    path('blog_upload', blog_upload, name='jewellery-store-blog-x'),
    path('cc-bblog-td', jewellery_td_blog, name='jewellery-store-td-blog'),
    path('del/<int:pk>', delete_jewellery_blog, name='jewellery-store-del-blog'),
    path('blog-up/<int:pk>', update_jewellery_store_blog, name='update_jewellery_blog'),
    path('slider-home', slider_home, name='jewellery-store-slider'),
    path('slider-td', jewellery_td_slider, name='jewellery-td-store-slider-home'),
    path('slider-home-del/<int:pk>', delete_jewellery_slider_home, name='jewellery-store-del-slider-home'),
    path('slider-up/<int:pk>', update_jewellery_slider_home, name='update_jewellery_slider'),
    re_path(r'^.*/$', TemplateView.as_view(template_name='dev_html/404.html'), name='catchall-404'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)