from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Status, Course, Enrolled
from .serializers import (
    CategorySerializer, StatusSerializer, CourseSerializer,
    CourseDetailSerializer, EnrolledSerializer, EnrolledCreateSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAdminUser]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(status='published')
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        """Get all courses including drafts (admin only)."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        courses = Course.objects.all()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)


class EnrolledViewSet(viewsets.ModelViewSet):
    serializer_class = EnrolledSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return enrollments for current user."""
        return Enrolled.objects.filter(student=self.request.user)

    def create(self, request, *args, **kwargs):
        """Enroll in a course."""
        serializer = EnrolledCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if already enrolled
        course_id = serializer.validated_data['course'].id
        if Enrolled.objects.filter(student=request.user, course_id=course_id).exists():
            return Response(
                {'error': 'Already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save(student=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """Get my enrolled courses."""
        enrollments = self.get_queryset()
        serializer = EnrolledSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending enrollments."""
        enrollments = self.get_queryset().filter(status__name='pending')
        serializer = EnrolledSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active enrollments."""
        enrollments = self.get_queryset().filter(status__name='active')
        serializer = EnrolledSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def denied(self, request):
        """Get denied enrollments."""
        enrollments = self.get_queryset().filter(status__name='denied')
        serializer = EnrolledSerializer(enrollments, many=True)
        return Response(serializer.data)
