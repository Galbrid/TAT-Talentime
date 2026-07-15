from rest_framework import serializers
from .models import Category, Status, Course, Enrolled


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at', 'updated_at')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name')


class CourseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Course
        fields = (
            'id', 'name', 'slug', 'course_code', 'description', 'category', 'category_name',
            'level', 'duration', 'eligibility', 'price', 'instructor', 'syllabus',
            'curriculum', 'highlights', 'status', 'batch_timings', 'placement_details',
            'certification', 'created_at', 'updated_at'
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'


class EnrolledSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_details = CourseSerializer(source='course', read_only=True)
    status = serializers.SlugRelatedField(slug_field='name', queryset=Status.objects.all())
    
    class Meta:
        model = Enrolled
        fields = ('id', 'student', 'student_name', 'student_email', 'course', 'course_name', 'course_details', 'status', 'enrolled_date', 'updated_at')


class EnrolledCreateSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field='name', queryset=Status.objects.all(), required=False)

    class Meta:
        model = Enrolled
        fields = ('student', 'course', 'status')
