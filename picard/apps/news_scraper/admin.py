from django.contrib import admin
from .models import Source,Article,Company

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'url', 'category' , 'language','status')
    ordering = ('title',)
    # search_fields = ['user__username', 'user__email',
    #                  'user__first_name', 'user__last_name', 'time']
    # list_filter = ('action_type', 'created_at',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'company', 'published_at','status')
    # search_fields = ['user__username', 'user__email',
    #                  'user__first_name', 'user__last_name', 'time']
    # list_filter = ('action_type', 'created_at',)
    pass

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'query','all_sources','status')

    def all_sources(self, obj):
        return ", ".join([p.title for p in obj.sources.all()])
    # search_fields = ['user__username', 'user__email',
    #                  'user__first_name', 'user__last_name', 'time']
    # list_filter = ('action_type', 'created_at',)