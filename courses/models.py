from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.JSONField()

    def __str__(self):
        return self.title.get('en', 'Untitled Course')

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.JSONField()
    content = models.JSONField(blank=True, null=True)
    quiz = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title.get('en', 'Untitled Module')

class ModuleProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'module') 

    def __str__(self):
        return f"{self.user} - {self.module}"


class CourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_modules = models.PositiveIntegerField(default=0)
    total_modules = models.PositiveIntegerField(default=0)
    progress = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} - {self.course} ({self.progress:.0%})"