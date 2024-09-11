from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Company, Job

class JobListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_company = Company.objects.create(name='Test Company', description='Test Description', website='http://test.com')
        number_of_jobs = 13
        for job_num in range(number_of_jobs):
            Job.objects.create(title=f'Job {job_num}', company=test_company, description='Test job description', requirements='Test requirements', salary=50000, location='Test Location')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['jobs']), 10)

class JobModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name='Test Company', description='Test Description', website='http://test.com')
        Job.objects.create(title='Test Job', company=Company.objects.get(id=1), description='Test job description', requirements='Test requirements', salary=50000, location='Test Location')

    def test_title_max_length(self):
        job = Job.objects.get(id=1)
        max_length = job._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_title(self):
        job = Job.objects.get(id=1)
        expected_object_name = f'{job.title}'
        self.assertEqual(str(job), expected_object_name)
# Create your tests here.
