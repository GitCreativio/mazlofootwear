"""
Module: careers/models.py

This module defines the data models for the careers section of the application and
implements cache invalidation for job listings when jobs are created, updated, or deleted.

Models:
    Job: Represents an open position with relevant details.
    Application: Captures candidate applications for specific job openings.

Signal Handlers:
    invalidate_jobs_cache: Clears the cached list of all jobs on save/delete events.
"""
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django_redis import get_redis_connection

class Job(models.Model):
    """
    Represents a job opening within the organization.

    Fields:
        JOB_TYPES (list of tuple): Available employment types.
        title (CharField): The title of the job position.
        job_type (CharField): The employment type (Full-time, Part-time, Remote).
        location (CharField): The location where the job is based.
        description (TextField): Detailed description of the role.
        requirements (TextField): Newline-separated list of job requirements.
    """
    JOB_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote'),
    ]
    title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(help_text="Enter each requirement on a new line")

    def __str__(self):
        """
        Return the job title as its string representation.
        """
        return self.title

class Application(models.Model):
    """
    Represents a candidate's application for a specific job opening.

    Fields:
        job (ForeignKey): The Job instance this application is for.
        full_name (CharField): Applicant's full name.
        email (EmailField): Applicant's email address.
        phone_number (CharField): Optional contact number.
        resume (FileField): Uploaded resume file.
        cover_letter (TextField): Optional cover letter content.
        submission_date (DateTimeField): Timestamp of application submission.
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)    
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string combining the applicant's name and job title.
        """
        return f"{self.full_name} - {self.job.title}"

# @receiver([post_save, post_delete], sender=Job)
# def invalidate_jobs_cache(sender, instance, **kwargs):
#     """
#     Signal handler to clear the cache of all jobs when a Job is saved or deleted.

#     Clears the 'all_jobs' cache key to ensure that job listings remain up-to-date.

#     Args:
#         sender (Model): The model class sending the signal (Job).
#         instance (Job): The instance being saved or deleted.
#         **kwargs: Additional signal keyword arguments.
#     """
#     cache.delete('all_jobs')
