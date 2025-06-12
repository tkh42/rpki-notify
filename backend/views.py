# myapp/views.py
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import RegistrationForm


def index(request):
    inconsistencies = [] 
    errors = []
    reachability_statuses = []

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False # User is not verified until email confirmation
            user.verification_token = str(uuid.uuid4()) # Generate a unique token
            user.save()

            # Send verification email
            verification_link = request.build_absolute_uri(
                reverse('verify_email', args=[user.verification_token])
            )
            send_mail(
                'Verify your email for System Status Dashboard',
                f'Please click the following link to verify your email: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect('registration_success') # Redirect to a success page
    else:
        form = RegistrationForm()

    context = {
        'inconsistencies': inconsistencies,
        'errors': errors,
        'reachability_statuses': reachability_statuses,
        'form': form,  # Include the registration form in the context
    }

    return render(request, 'index.html', context)


def verify_email(request, token):
    try:
        user = RegisteredUser.objects.get(verification_token=token, is_verified=False)
        user.is_verified = True
        user.verification_token = None # Clear the token after verification
        user.save()
        return render(request, 'verification_success.html') # Create this template
    except RegisteredUser.DoesNotExist:
        return render(request, 'verification_failed.html') # Create this template


def registration_success(request):
    return render(request, 'registration_success.html') # Create this template
