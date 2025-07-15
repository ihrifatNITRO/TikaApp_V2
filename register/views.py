from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .forms import RegistrationForm
from .models import Profile
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            id_card = form.cleaned_data['id_card']
            phone_number = form.cleaned_data['phone_number']

            # Check for duplicates
            if User.objects.filter(username=email).exists():
                messages.error(request, 'This email address is already in use.')
            elif Profile.objects.filter(id_card=id_card).exists():
                messages.error(request, 'This ID Card number is already registered.')
            elif Profile.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'This phone number is already in use.')
            else:
                # --- This block now ONLY runs if everything is unique ---
                full_name = form.cleaned_data['full_name']
                password = form.cleaned_data['password']

                user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name)
                user.is_active = False
                user.save()

                Profile.objects.create(user=user, id_card=id_card, phone_number=phone_number)

                # --- The email logic is now safely inside the else block ---
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('register/verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(mail_subject, message, 'from@your-domain.com', [email])
                
                return redirect('verification_sent')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'register/register.html', context)


# This new view handles the actual verification when the user clicks the link
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('verification_success')
    else:
        return redirect('verification_failed')

# These are simple views to show message pages
def verification_sent_view(request):
    return render(request, 'register/verification_sent.html')

def verification_success_view(request):
    return render(request, 'register/verification_success.html')

def verification_failed_view(request):
    return render(request, 'register/verification_failed.html')