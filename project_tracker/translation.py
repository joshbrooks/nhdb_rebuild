from modeltranslation.translator import register, TranslationOptions
from .models import Tag, Project, Organization

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Project)
class ProjectTranslation(TranslationOptions):
    fields = ('name', 'description')


@register(Organization)
class OrganizationTranslation(TranslationOptions):
    fields = ('description',)