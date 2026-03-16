from django.contrib import admin
from .models import Course, Module, ModuleProgress, CourseProgress

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('title', 'content', 'quiz')
    readonly_fields = ()
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_en')  # Show course ID and English title
    search_fields = ('title',)
    inlines = [ModuleInline]

    def title_en(self, obj):
        return obj.title.get('en', 'Untitled')
    title_en.short_description = "Title (EN)"

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title_en')
    list_filter = ('course',)
    search_fields = ('title',)

    def title_en(self, obj):
        return obj.title.get('en', 'Untitled')
    title_en.short_description = "Title (EN)"


@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'module', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at', 'module__course')
    search_fields = ('user__email', 'user__username', 'module__title')
    autocomplete_fields = ('user', 'module')
    ordering = ('-completed_at',)


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'completed_modules', 'total_modules', 'progress', 'completed', 'updated_at')
    list_filter = ('completed', 'updated_at', 'course')
    search_fields = ('user__email', 'user__username', 'course__title')
    autocomplete_fields = ('user', 'course')
    ordering = ('-updated_at',)