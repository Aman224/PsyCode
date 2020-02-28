from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Content
from .forms import InputForm
import subprocess
import sys
import os
# from webapp.transmogrify import transmogrify

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

            f = open("input.ini",'w')
            f.write(data)
            f.close()

            os.system("python ./webapp/transmogrify.py")

        # pdata = transmogrify()

        # Content.objects.filter(inputData = data).update(outputData=pdata)
        f = open('Phase1.intXML', 'r')
        data = f.read()
        f.close()

        context = {'form': form, 'object': data}

        return render(request, self.template_name, context)
