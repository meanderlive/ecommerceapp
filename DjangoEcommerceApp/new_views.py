from django.shortcuts import render,get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage
from .models import *
from django.contrib.auth import logout
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib import messages

def custom_logout_view(request):
    logout(request)
    return redirect('register')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    email_template_name = 'dev_html/password_reset_email.html'
    subject_template_name = 'dev_html/password_reset_subject.txt'
    template_name = 'dev_html/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'dev_html/password_reset_confirm.html'


def home_redirect(request):
    print("home_redirect called")
    if request.user.is_authenticated:
        print("User is authenticated")
        return redirect('jewellery-account')
    else:
        print("User is not authenticated")
        return redirect('register')

def register(request):
    insta = Instagram_image.objects.first()
    if request.user.is_authenticated:
        return redirect('jewellery-account')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(f'POST data: {request.POST}')
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Form is valid and user created successfully.")
            #return render(request,"dev_html/jewellery-store-admin-account.html")
            return redirect('jewellery-account')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'dev_html/demo-jewellery-register.html', {'form': form,"insta": insta})

def custom_login(request):
    insta = Instagram_image.objects.first()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('jewellery-account')
    else:
        form = AuthenticationForm()
    return render(request, 'dev_html/demo-jewellery-login.html', {'form': form, "insta": insta})

@login_required
def change_password(request):
    insta = Instagram_image.objects.first()
    if request.method == 'POST':
        form = CustomUserChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Keeps the user logged in after password change
            return redirect('jewellery-account')  # Redirect to a success page
    else:
        form = CustomUserChangePasswordForm(user=request.user)
    return render(request, 'dev_html/demo-jewellery-update.html', {'form': form, "insta": insta})

@login_required
def update_profile(request):
    insta = Instagram_image.objects.first()
    user = request.user

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('jewellery-account')  # Redirect to the profile page or any other page
    else:
        form = CustomUserUpdateForm(instance=user)

    return render(request, 'dev_html/demo-jewellery-all-update.html', {'form': form,"insta": insta})

@login_required
def update_password(request):
    insta = Instagram_image.objects.first()
    user = request.user

    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('jewellery-account')  # Redirect to the profile page or any other page
    else:
        form = PasswordUpdateForm(instance=user)

    return render(request, 'dev_html/demo-jewellery-password-update.html', {'form': form,"insta": insta})

@login_required
def insert_profile(request):
    insta = Instagram_image.objects.first()
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('jewellery-account')  # Redirect to the profile page or any other page
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'dev_html/demo-jewellery-profile.html', {'form': form,"insta": insta})


@login_required
def get_profile(request):
    insta = Instagram_image.objects.first()
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    con={'profile': user_profile , "insta": insta}
    return render(request, 'dev_html/demo-jewellery-profile-view.html', con)

@login_required
def update_profile(request):
    insta = Instagram_image.objects.first()
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_view')  # Redirect to the profile page or any other page
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'dev_html/demo-jewellery-profile-update.html', {'form': form,"insta": insta})

@login_required
def delete_profile(request):

    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
        messages.success(request, 'Profile deleted successfully.')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile does not exist.')

    return redirect('profile_view')  # Redirect to a suitable page after deletion



def jewellery_admin(request):
    return render(request,"dev_html/jewellery-store-admin-account.html")

@login_required
def jewellery_account(request):
    cat_home_data=Jewellery_store_cat.objects.first()
    mydata= Featured_products.objects.all()
    insta= Instagram_image.objects.first()
    slider_img= Slider_home.objects.first()
    con={
        "home_pro": mydata,
        "insta":insta,
        "slider_img":slider_img,
        "cat_home_data":cat_home_data
    }
    return render(request,"dev_html/demo-jewellery-store.html" , con)

def jewellery_store_shop(request):
    mydata = Featured_products.objects.all()
    pro_data = Featured_products.objects.all()[:3]
    pro_datax = Featured_products.objects.all()[4:7]
    insta = Instagram_image.objects.first()
    con = {
        "home_pro": mydata,
        "insta": insta,
        "pro_data":pro_data,
        "new":pro_datax

    }
    return render(request,"dev_html/demo-jewellery-store-shop.html",con)

@login_required
def jewellery_store_categories(request):
    insta = Instagram_image.objects.first()
    catee= Categories_images.objects.first()
    con={
        "insta": insta,
        "x":catee
    }
    return render(request,"dev_html/demo-jewellery-store-categories.html",con)

@login_required
def jewellery_store_blog(request):
    insta = Instagram_image.objects.first()
    blog_d = Blog_c.objects.all()
    con = {
        "insta": insta,
        "blog": blog_d
    }
    return render(request,"dev_html/demo-jewellery-store-blog.html",con)

@login_required
def jewellery_store_contact(request):
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
    }
    return render(request,"dev_html/demo-jewellery-store-contact.html",con)

@login_required
def jewellery_store_wishlist(request):
    mydata = Featured_products.objects.all()
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
        "mydata":mydata
    }
    return render(request,"dev_html/demo-jewellery-store-wishlist.html",con)

@login_required
def jewellery_store_about(request):
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
    }
    return render(request,"dev_html/demo-jewellery-store-about.html",con)

@login_required
def jewellery_store_faq(request):
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
    }
    return render(request,"dev_html/demo-jewellery-store-faq.html",con)

@login_required
def jewellery_store_account(request):
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
    }
    return render(request,"dev_html/demo-jewellery-store-account.html",con)

@login_required
def jewellery_store_cart(request):
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
    }
    return render(request,"dev_html/demo-jewellery-store-cart.html",con)

@login_required
def jewellery_store_checkout(request):
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
    }
    return render(request,"dev_html/demo-jewellery-store-checkout.html",con)

@login_required
def jewellery_store_single_product(request):
    insta = Instagram_image.objects.first()
    con = {
        "insta": insta,
    }
    return render(request,"dev_html/demo-jewellery-store-single-product.html",con)


def contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        comment = request.POST.get('comment')
        print(name)
        # Create and save the contact message
        set=ContactMessage(name=name, email=email, phone=phone, comment=comment)
        print(set.name)
        set.save()
        print('successfull')


        return redirect('jewellery-account')
        print()

    return render(request, "dev_html/demo-jewellery-store-contact.html")

# admin dashboard
@login_required(login_url="/admin")
def jewellery_store_image_cat(request):
    return render(request,"jewellery_admin/jewellery_form_1.html")

def table(request):
    return render(request,"jewellery_admin/table.html")

@login_required(login_url="/admin")
def jewellery_td_store_image_cat(request):
    all_cat = Jewellery_store_cat.objects.all()
    return render(request,"jewellery_admin/jewellery_td_store_cat.html" ,{"cat_data":all_cat})


def upload_images(request):
    if request.method == 'POST' and request.FILES:
        earrings_image = request.FILES.get('earrings_image')
        rings_image = request.FILES.get('rings_image')
        bracelet_image = request.FILES.get('bracelet_image')
        necklace_image = request.FILES.get('necklace_image')

        jewellery_store_cat = Jewellery_store_cat(
            earrings_image=earrings_image,
            rings_image=rings_image,
            bracelet_image=bracelet_image,
            necklace_image=necklace_image
        )
        jewellery_store_cat.save()
        print("successful working")

        return redirect('jewellery-td-store-cat-images')
        #return HttpResponse('sucessful')

    return render(request, 'jewellery_admin/jewellery_form_1.html')


def update_jewellery_store_cat(request, pk):
    jewellery_store_cat = get_object_or_404(Jewellery_store_cat, pk=pk)

    if request.method == 'POST' and request.FILES:
        if 'earrings_image' in request.FILES:
            jewellery_store_cat.earrings_image = request.FILES['earrings_image']
        if 'rings_image' in request.FILES:
            jewellery_store_cat.rings_image = request.FILES['rings_image']
        if 'bracelet_image' in request.FILES:
            jewellery_store_cat.bracelet_image = request.FILES['bracelet_image']
        if 'necklace_image' in request.FILES:
            jewellery_store_cat.necklace_image = request.FILES['necklace_image']

        jewellery_store_cat.save()

        return redirect('jewellery-td-store-cat-images')

    return render(request, 'jewellery_admin/update_jewellery_store_cat.html', {'jewellery_store_cat': jewellery_store_cat})


def delete_jewellery_store_cat(request,pk):
    msg=Jewellery_store_cat.objects.get(pk=pk)
    msg.delete()
    return redirect('jewellery-td-store-cat-images')

@login_required(login_url="/admin")
def featured_product_upload(request):
    if request.method == 'POST' and request.FILES:
        featured_product_image = request.FILES.get('featured_product_image')
        featured_product_title = request.POST.get('featured_product_title')
        featured_product_price = request.POST.get('featured_product_price')


        jewellery_store_featured = Featured_products(
            featured_product_image=featured_product_image,
            featured_product_title=featured_product_title,
            featured_product_price=featured_product_price,

        )
        jewellery_store_featured.save()
        print("successful working")

        return redirect('jewellery-store-td-featured-products')
        #return HttpResponse('sucessful')

    return render(request, 'jewellery_admin/jewellery-store-featured-products.html')

@login_required(login_url="/admin")
def jewellery_td_featured_product(request):
    all_cat = Featured_products.objects.all()
    return render(request,"jewellery_admin/jewellary-store-td-featured-product.html" ,{"cat_data":all_cat})


def update_jewellery_store_featured_product(request, pk):
    print("Call to update_jewellery_store_featured_product")
    featured_product = get_object_or_404(Featured_products, pk=pk)

    if request.method == 'POST':
        print("Processing POST request")
        if 'featured_product_image' in request.FILES:
            print(f"Received featured_product_image: {request.FILES['featured_product_image']}")
            featured_product.featured_product_image = request.FILES['featured_product_image']
        if 'featured_product_title' in request.POST:
            print(f"Received featured_product_title: {request.POST['featured_product_title']}")
            featured_product.featured_product_title = request.POST['featured_product_title']
        if 'featured_product_price' in request.POST:
            print(f"Received featured_product_price: {request.POST['featured_product_price']}")
            featured_product.featured_product_price = request.POST['featured_product_price']

        try:
            with transaction.atomic():
                featured_product.save()
                print("Saved featured_product successfully")
        except Exception as e:
            print(f"Error saving featured_product: {e}")
            return render(request, 'jewellery_admin/jewellery-store-up-featured-product.html', {
                'featured_product': featured_product,
                'error_message': f"An error occurred while saving: {e}"
            })

        return redirect('jewellery-store-td-featured-products')  # Adjust to your actual redirect URL

    return render(request, 'jewellery_admin/jewellery-store-up-featured-product.html',{'jewellery_store_cat': featured_product})



def delete_jewellery_featured_product(request,pk):
    msg=Featured_products.objects.get(pk=pk)
    msg.delete()
    return redirect('jewellery-store-td-featured-products')

@login_required(login_url="/admin")
def insta_images(request):
    if request.method == 'POST' and request.FILES:
        instagram_img1 = request.FILES.get('instagram_img1')
        instagram_img2 = request.FILES.get('instagram_img2')
        instagram_img3 = request.FILES.get('instagram_img3')
        instagram_img4 = request.FILES.get('instagram_img4')
        instagram_img5 = request.FILES.get('instagram_img5')
        instagram_img6 = request.FILES.get('instagram_img6')

        jewellery_store_cat = Instagram_image(
            instagram_img1=instagram_img1,
            instagram_img2=instagram_img2,
            instagram_img3=instagram_img3,
            instagram_img4=instagram_img4,
            instagram_img5=instagram_img5,
            instagram_img6=instagram_img6
        )
        jewellery_store_cat.save()
        print("successful working")

        return redirect('jewellery-td-store-instagram')
        #return HttpResponse('sucessful')

    return render(request, 'jewellery_admin/jewellery-store-instagram.html')


def update_jewellery_insta(request, pk):
    jewellery_store_cat = get_object_or_404(Instagram_image, pk=pk)

    if request.method == 'POST' and request.FILES:
        if 'instagram_img1' in request.FILES:
            jewellery_store_cat.instagram_img1 = request.FILES['instagram_img1']
        if 'instagram_img2' in request.FILES:
            jewellery_store_cat.instagram_img2 = request.FILES['instagram_img2']
        if 'instagram_img3' in request.FILES:
            jewellery_store_cat.instagram_img3 = request.FILES['instagram_img3']
        if 'instagram_img4' in request.FILES:
            jewellery_store_cat.instagram_img4 = request.FILES['instagram_img4']
        if 'instagram_img5' in request.FILES:
            jewellery_store_cat.instagram_img5 = request.FILES['instagram_img5']
        if 'instagram_img6' in request.FILES:
            jewellery_store_cat.instagram_img6 = request.FILES['instagram_img6']

        jewellery_store_cat.save()

        return redirect('jewellery-td-store-instagram')

    return render(request, 'jewellery_admin/jewellery-store-up-instagram.html', {'jewellery_store_cat': jewellery_store_cat})

def delete_jewellery_insta(request,pk):
    msg=Instagram_image.objects.get(pk=pk)
    msg.delete()
    return redirect('jewellery-td-store-instagram')

#@login_required
def jewellery_td_insta(request):
    all_cat = Instagram_image.objects.all()
    return render(request,"jewellery_admin/jewellery-store-td-instagram.html" ,{"cat_data":all_cat})

@login_required(login_url="/admin")
def categories_upload(request):
    if request.method == 'POST' and request.FILES:
        earrings_image = request.FILES.get('earrings_image')
        rings_image = request.FILES.get('rings_image')
        bracelet_image = request.FILES.get('bracelet_image')
        necklace_image = request.FILES.get('necklace_image')
        Bangles_image = request.FILES.get('Bangles_image')
        Pendants_image = request.FILES.get('Pendants_image')
        Chain_image = request.FILES.get('Chain_image')

        jewellery_store_cat = Categories_images(
            earrings_image=earrings_image,
            rings_image=rings_image,
            bracelet_image=bracelet_image,
            necklace_image=necklace_image,
            Bangles_image=Bangles_image,
            Pendants_image=Pendants_image,
            Chain_image=Chain_image

        )

        jewellery_store_cat.save()
        print("successful working")

        return redirect('jewellery-td-store-categories')
        #return HttpResponse('sucessful')

    return render(request, 'jewellery_admin/jewellery-store-categories.html')


def jewellery_td_categories(request):
    all_cat = Categories_images.objects.all()
    return render(request,"jewellery_admin/jewellery-store-td-categories.html" ,{"cat_data":all_cat})

def update_jewellery_categories(request, pk):
    jewellery_store_cat = get_object_or_404(Categories_images, pk=pk)

    if request.method == 'POST' and request.FILES:
        if 'earrings_image' in request.FILES:
            jewellery_store_cat.earrings_image = request.FILES['earrings_image']
        if 'rings_image' in request.FILES:
            jewellery_store_cat.rings_image = request.FILES['rings_image']
        if 'bracelet_image' in request.FILES:
            jewellery_store_cat.bracelet_image = request.FILES['bracelet_image']
        if 'necklace_image' in request.FILES:
            jewellery_store_cat.necklace_image = request.FILES['necklace_image']
        if 'Bangles_image' in request.FILES:
            jewellery_store_cat.Bangles_image = request.FILES['Bangles_image']
        if 'Pendants_image' in request.FILES:
            jewellery_store_cat.Pendants_image = request.FILES['Pendants_image']
        if 'Chain_image' in request.FILES:
            jewellery_store_cat.Chain_image = request.FILES['Chain_image']

        jewellery_store_cat.save()

        return redirect('jewellery-td-store-categories')

    return render(request, 'jewellery_admin/update_jewellery_categories.html', {'jewellery_store_cat': jewellery_store_cat})


def delete_jewellery_categories(request,pk):
    msg=Categories_images.objects.get(pk=pk)
    msg.delete()
    return redirect('jewellery-td-store-instagram')

@login_required(login_url="/admin")
def blog_upload(request):
    if request.method == 'POST' and request.FILES:
        image = request.FILES.get('image')
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')

        jewellery_store_featured = Blog_c(
            image=image,
            title=title,
            description=description,
            author=author
        )
        jewellery_store_featured.save()
        print("successful working")

        return redirect('jewellery-store-td-blog')
        #return HttpResponse('sucessful')

    return render(request, 'jewellery_admin/jewellery-store-blog.html')


@login_required(login_url="/admin")
def jewellery_td_blog(request):
    all_cat = Blog_c.objects.all()
    return render(request,"jewellery_admin/jewellery-store-td-blog.html" ,{"cat_data":all_cat})


def delete_jewellery_blog(request,pk):
    msg=Blog_c.objects.get(pk=pk)
    msg.delete()
    return redirect('jewellery-store-td-blog')


def update_jewellery_store_blog(request, pk):
    print("Call to update_jewellery_store_featured_product")
    featured_product = get_object_or_404(Blog_c, pk=pk)

    if request.method == 'POST':
        print("Processing POST request")
        if 'image' in request.FILES:
            featured_product.image = request.FILES['image']
        if 'title' in request.POST:
            featured_product.title = request.POST['title']
        if 'description' in request.POST:
            featured_product.description = request.POST['description']
        if 'author' in request.POST:
            featured_product.author = request.POST['author']

        try:
            with transaction.atomic():
                featured_product.save()
                print("Saved featured_product successfully")
        except Exception as e:
            print(f"Error saving featured_product: {e}")
            return render(request, 'jewellery_admin/jewellery-store-up-featured-product.html', {
                'featured_product': featured_product,
                'error_message': f"An error occurred while saving: {e}"
            })

        return redirect('jewellery-store-td-blog')

    return render(request, 'jewellery_admin/jewellery-store-up-blog.html',{'jewellery_store_cat': featured_product})


def slider_home(request):
    if request.method == 'POST' and request.FILES:
        slider_img_left1 = request.FILES.get('slider_img_left1')
        slider_img_right1 = request.FILES.get('slider_img_right1')
        slider_img_left2 = request.FILES.get('slider_img_left2')
        slider_img_right2 = request.FILES.get('slider_img_right2')
        slider_img_left3 = request.FILES.get('slider_img_left3')
        slider_img_right3 = request.FILES.get('slider_img_right3')
        jewellery_store_cat = Slider_home(
            slider_img_left1=slider_img_left1,
            slider_img_right1=slider_img_right1,
            slider_img_left2=slider_img_left2,
            slider_img_right2=slider_img_right2,
            slider_img_left3=slider_img_left3,
            slider_img_right3=slider_img_right3,
        )

        jewellery_store_cat.save()
        print("successful working")

        return redirect('jewellery-td-store-slider-home')
        #return HttpResponse('sucessful')

    return render(request, 'jewellery_admin/jewellery-store-slider-home.html')


def jewellery_td_slider(request):
    all_cat = Slider_home.objects.all()
    return render(request,"jewellery_admin/jewellery-store-td-slider-home.html" ,{"cat_data":all_cat})

def delete_jewellery_slider_home(request,pk):
    msg=Slider_home.objects.get(pk=pk)
    msg.delete()
    return redirect('jewellery-td-store-slider-home')


def update_jewellery_slider_home(request, pk):
    jewellery_store_cat = get_object_or_404(Slider_home, pk=pk)

    if request.method == 'POST' and request.FILES:
        if 'slider_img_left1' in request.FILES:
            jewellery_store_cat.slider_img_left1 = request.FILES['slider_img_left1']
        if 'slider_img_right1' in request.FILES:
            jewellery_store_cat.slider_img_right1 = request.FILES['slider_img_right1']
        if 'slider_img_left2' in request.FILES:
            jewellery_store_cat.slider_img_left2 = request.FILES['slider_img_left2']
        if 'slider_img_right2' in request.FILES:
            jewellery_store_cat.slider_img_right2 = request.FILES['slider_img_right2']
        if 'slider_img_left3' in request.FILES:
            jewellery_store_cat.slider_img_left1 = request.FILES['slider_img_left3']
        if 'slider_img_right3' in request.FILES:
            jewellery_store_cat.slider_img_right3 = request.FILES['slider_img_right3']


        jewellery_store_cat.save()

        return redirect('jewellery-td-store-slider-home')

    return render(request, 'jewellery_admin/update_jewellery_slider_home.html', {'jewellery_store_cat': jewellery_store_cat})
