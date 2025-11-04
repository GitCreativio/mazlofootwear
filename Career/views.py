from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from .models import Job, Application

"""
Module: careers/views.py

This module defines view functions for the careers section of the site, handling:
- Displaying available job listings (with caching).
- Processing job application submissions via POST requests.
"""

def careers(request):
    """
    Handle displaying job listings and processing application submissions.

    GET requests:
        - Retrieve cached list of Job objects under 'all_jobs' key (24h expiration).
        - Render the 'careers.html' template with the jobs context.

    POST requests:
        - Extract application form fields (job_id, full_name, email, phone_number,
          cover_letter, resume file) from request.
        - Validate the job exists; create and save an Application instance.
        - Add a success or error message and redirect back to the careers page.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: Rendered careers page or redirect after form submission.
    """
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number', '')
        cover_letter = request.POST.get('cover_letter', '')
        resume = request.FILES.get('resume')

        try:
            job = Job.objects.get(id=job_id)
            application = Application(
                job=job,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                resume=resume,
                cover_letter=cover_letter
            )
            application.save()
            messages.success(request, 'Application submitted successfully!')
        except Job.DoesNotExist:
            messages.error(request, 'Invalid job selected.')
        return redirect('careers')
    
    # Cache jobs for 24 hours (86400 seconds)
    jobs = cache.get_or_set(
        'all_jobs',
        lambda: list(Job.objects.all()),
        60 * 60 * 24
    )

    return render(request, 'careers.html', {'jobs': jobs})
