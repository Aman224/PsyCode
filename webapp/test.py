from webapp.models import Content

print(Content.objects.last().inputData)