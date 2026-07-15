#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tat_backend.settings')
django.setup()

from course.models import Category, Course, Status

# Create Status entries
for status_name in ['pending', 'active', 'denied']:
    Status.objects.get_or_create(name=status_name)
    print(f"Status: {status_name}")

# Create Categories
categories = [
    'Healthcare BPO',
    'Software Development',
    'Business Management',
    'Digital Marketing'
]

cat_objs = {}
for cat_name in categories:
    cat, created = Category.objects.get_or_create(name=cat_name)
    cat_objs[cat_name] = cat
    print(f"{'✓' if created else '·'} Category: {cat_name}")

# Create Sample Courses
courses_data = [
    {
        'name': 'Certified Professional Coder (CPC)',
        'course_code': 'MED-101',
        'description': 'Comprehensive medical coding training in ICD-10-CM, CPT, and HCPCS coding systems.',
        'category': 'Healthcare BPO',
        'level': 'Advanced',
        'duration': '12 weeks',
        'eligibility': 'Life Sciences graduates, Medical graduates',
        'price': 18500,
        'instructor': 'Dr. Sarah Johnson',
        'syllabus': 'Advanced ICD-10-CM Guidelines, CPT Coding, HCPCS Modifiers, Complex Procedures',
        'curriculum': 'Module 1: Coding Foundations | Module 2: Advanced Systems | Module 3: Compliance',
        'highlights': ['Real Chart Reviews', 'Industry Expert Training', '100% Placement Support', 'Exam Preparation'],
        'status': 'published',
        'batch_timings': 'Mon-Wed-Fri 6PM-8PM IST',
        'placement_details': 'Direct hiring runs with top healthcare BPO companies',
        'certification': 'CPC Certification'
    },
    {
        'name': 'Python for Web Development',
        'course_code': 'DEV-201',
        'description': 'Learn Python, Django, and modern web development practices from industry experts.',
        'category': 'Software Development',
        'level': 'Intermediate',
        'duration': '8 weeks',
        'eligibility': 'Basic programming knowledge required',
        'price': 12000,
        'instructor': 'Rajesh Kumar',
        'syllabus': 'Python Basics, Django Framework, REST APIs, Database Design',
        'curriculum': 'Module 1: Python Essentials | Module 2: Django Deep Dive | Module 3: Deployment',
        'highlights': ['Live Projects', 'Code Review Sessions', 'Git Workflow Training', 'Career Mentoring'],
        'status': 'published',
        'batch_timings': 'Tue-Thu-Sat 7PM-9PM IST',
        'placement_details': 'Referral program with tech startups and enterprises',
        'certification': 'Full Stack Developer Certificate'
    },
    {
        'name': 'Business Analytics Essentials',
        'course_code': 'BIZ-301',
        'description': 'Master data analysis, business intelligence, and decision-making with analytics tools.',
        'category': 'Business Management',
        'level': 'Beginner',
        'duration': '6 weeks',
        'eligibility': 'Any graduate',
        'price': 9500,
        'instructor': 'Priya Sharma',
        'syllabus': 'Excel Advanced, Power BI, Data Visualization, Statistical Analysis',
        'curriculum': 'Module 1: Data Fundamentals | Module 2: BI Tools | Module 3: Case Studies',
        'highlights': ['Hands-on Projects', 'Industry Data Sets', 'Tool Certification', 'Job Ready Training'],
        'status': 'published',
        'batch_timings': 'Mon-Wed-Fri 5PM-6:30PM IST',
        'placement_details': 'Analytics roles in finance and consulting firms',
        'certification': 'Business Analytics Professional'
    },
]

for course_data in courses_data:
    cat = cat_objs[course_data.pop('category')]
    course, created = Course.objects.get_or_create(
        course_code=course_data['course_code'],
        defaults={**course_data, 'category': cat}
    )
    status = '✓' if created else '·'
    print(f"{status} Course: {course.name} (₹{course.price})")

print("\n✅ Sample data seeding complete!")
