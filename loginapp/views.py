from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.shortcuts import redirect, render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, "loginapp/index.html")

def login_page(request):
    return render(request, "loginapp/login.html")

def login_user(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return render(request, "loginapp/product.html")
    else:
        return render(request, "loginapp/login.html", {'data': 'failed'})
def generate_new_captcha():
    """
    Generates a new CAPTCHA key and image URL for the registration form.
    """
    captcha_key = CaptchaStore.generate_key()  # Generate a new CAPTCHA key
    captcha_image = captcha_image_url(captcha_key)  # Get the image URL for the CAPTCHA
    return {'key': captcha_key, 'image': captcha_image}   
def register_page(request):
    context = generate_new_captcha()
    return render(request, 'loginapp/register.html', context)


def register_user(request):
   if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        captcha_key = request.POST.get('captcha_1')
        captcha_response = request.POST.get('captcha_0')

        # Validate CAPTCHA
        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            if captcha.response == captcha_response:
                # CAPTCHA is valid
                if User.objects.filter(username=username).exists():
                    return render(request, 'loginapp/register.html', {
                        'error': 'Username already exists.',
                        'captcha': generate_new_captcha()
                    })
                elif User.objects.filter(email=email).exists():
                    return render(request, 'loginapp/register.html', {
                        'error': 'Email already exists.',
                        'captcha': {'key': captcha_key, 'image': captcha_image_url(captcha_key)}
                    })
                else:
                    # Create user
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect('login_page')
            else:
                # CAPTCHA is invalid
                return render(request, 'loginapp/register.html', {
                    'error': 'Invalid CAPTCHA. Please try again.',
                    'captcha': {'key': captcha_key, 'image': captcha_image_url(captcha_key)}
                })
        except CaptchaStore.DoesNotExist:
            return render(request, 'loginapp/register.html', {'error': 'Invalid CAPTCHA session. Please try again.'})