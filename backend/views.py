# myapp/views.py
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RegistrationForm
from .models import Report, RegisteredUser, RelyingParty
from django.db.models import Prefetch


def index(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # In a real app, configure email settings in settings.py and uncomment this.
            # verification_link = request.build_absolute_uri(
            #     reverse('verify_email', args=[user.verification_token])
            # )
            # send_mail(
            #     'Verify your email for RPKI-Notify',
            #     f'Please click the following link to verify your email: {verification_link}',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [user.email],
            #     fail_silently=False,
            # )
            
            # On successful registration, redirect to a success page.
            return redirect('registration_success')

    # Use select_related and prefetch_related to optimize database queries, reducing page load time.
    latest_report = Report.objects.order_by('-time_stamp').prefetch_related(
        Prefetch('relying_parties', queryset=RelyingParty.objects.prefetch_related('rp_logs', 'errors')),
        'inconsistencies',
        'aggregated_errors',
        'repositories',
        'ghostbusters',
        'differences'
    ).first()

    context = {
        'form': form,
        'latest_report': latest_report,
    }

    if latest_report:
        # Prepare context data for the template
        rp_logs_initial = {}
        for rp in latest_report.relying_parties.all():
            rp_logs_initial[rp.name] = [log.log_entry for log in rp.rp_logs.all()[:50]]
        
        common_errors = latest_report.aggregated_errors.order_by('-count')[:10]

        context.update({
            'inconsistencies': latest_report.inconsistencies.all(),
            'error_messages': common_errors,
            'repositories': latest_report.repositories.all(),
            'rp_names': list(latest_report.relying_parties.all().values_list("name", flat=True)),
            'vrps_per_rp': list(latest_report.relying_parties.all().values_list("num_vrps", flat=True)),
            'rp_logs_initial': rp_logs_initial,
            'rp_logs_counts': {rp.name: rp.rp_logs.count() for rp in latest_report.relying_parties.all()},
            'ghostbusters_count': latest_report.ghostbusters.count(),
            'num_repos': latest_report.repositories.count(),
            'differences': latest_report.differences.all(),
            'relying_parties': latest_report.relying_parties.all(),
            'reachable_repos_count': latest_report.repositories.filter(reachable=True).count(),
            'unreachable_repos_count': latest_report.repositories.filter(reachable=False).count(),
        })
    
    return render(request, 'index.html', context)


def get_all_rp_logs(request, rp_name):
    """API endpoint to fetch all logs for a given relying party."""
    latest_report = Report.objects.order_by('-time_stamp').first()
    if latest_report:
        try:
            # Find the relying party in the latest report
            rp = latest_report.relying_parties.get(name=rp_name)
            logs = list(rp.rp_logs.all().values_list('log_entry', flat=True))
            return JsonResponse({'logs': logs})
        except RelyingParty.DoesNotExist:
            return JsonResponse({'logs': []}, status=404)
    return JsonResponse({'logs': []}, status=404)


def verify_email(request, token):
    """Handle email verification link."""
    user = get_object_or_404(RegisteredUser, verification_token=token)
    if not user.is_verified:
        user.is_verified = True
        user.save()
    return render(request, 'verification_success.html')


def registration_success(request):
    """Show a success message after user registration."""
    return render(request, 'registration_success.html')

