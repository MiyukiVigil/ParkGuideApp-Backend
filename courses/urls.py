from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, CompleteModuleView, ModuleProgressViewSet, CourseProgressViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'progress', ModuleProgressViewSet, basename='progress')
router.register(r'course-progress', CourseProgressViewSet, basename='course-progress')

urlpatterns = [
    path('', include(router.urls)),
    path('complete-module/', CompleteModuleView.as_view(), name='complete-module'),
]