from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Content
from .forms import InputForm

class HomeView(TemplateView):

    template_name = 'webapp/home.html' 

    def get(self, request):
        form = InputForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        
        form = InputForm(request.POST)
        
        if form.is_valid():
            form.save()
            data = form.cleaned_data['inputData']
            form = InputForm(request.POST)
            
        context = {'form': form, 'object': data}

        return render(request, self.template_name, context)
