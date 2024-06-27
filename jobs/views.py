# from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Job, Company
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .forms import ApplicationForm
from .models import Application

def job_list(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__name__icontains=query)
        ).order_by('-created_at')
    else:
        jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'query': query})

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

def company_detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_jobs = company.job_set.all().order_by('-created_at')
    return render(request, 'jobs/company_detail.html', {
        'company': company,
        'company_jobs': company_jobs
    })

@login_required
def submit_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company  # Assuming the user has an associated company
            job.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm()
    return render(request, 'jobs/submit_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def employer_dashboard(request):
    company = request.user.company  # Assuming the user has an associated company
    jobs = Job.objects.filter(company=company).order_by('-created_at')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})
# Create your views here.
