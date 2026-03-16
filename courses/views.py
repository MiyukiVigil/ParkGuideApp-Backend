# courses/views.py
from rest_framework import viewsets, permissions, status
from .models import Course, Module
from .serializers import CourseSerializer, ModuleSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ModuleProgress, CourseProgress
from .serializers import ModuleProgressSerializer, CourseProgressSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]  # requires token

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class ModuleProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ModuleProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompleteModuleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        module_id = request.data.get('module_id')

        try:
            module = Module.objects.select_related('course').get(id=module_id)
        except Module.DoesNotExist:
            return Response({'detail': 'Invalid module_id'}, status=status.HTTP_400_BAD_REQUEST)

        progress, created = ModuleProgress.objects.get_or_create(
            user=request.user,
            module=module,
            defaults={'completed': True}
        )

        if not created and not progress.completed:
            progress.completed = True
            progress.save(update_fields=['completed'])

        course = module.course
        total_modules = course.modules.count()
        completed_modules = ModuleProgress.objects.filter(
            user=request.user,
            module__course=course,
            completed=True,
        ).count()
        ratio = (completed_modules / total_modules) if total_modules else 0

        CourseProgress.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={
                'completed_modules': completed_modules,
                'total_modules': total_modules,
                'progress': ratio,
                'completed': total_modules > 0 and completed_modules >= total_modules,
            }
        )

        return Response({'status': 'completed', 'created': created})