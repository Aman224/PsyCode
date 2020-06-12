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
            language = form.cleaned_data['language']

            form = InputForm(request.POST)

            f = open("input.ini",'w')
            f.write(data)
            f.write("\n")
            f.close()



        # pdata = transmogrify()

        # Content.objects.filter(inputData = data).update(outputData=pdata)
        
        # Language module for python
        if(language == 'python'):
            # Transmography
            os.system("python ./webapp/Stag1JsonImplementation.py")
            os.system("python ./webapp/StateMachineMethod.py > Final.xml")

            # Language
            os.system("python ./webapp/mapperpython.py")

        # Language module for C
        elif(language == 'c'):
            # Transmogrify
            os.system("python ./webapp/CLexer.py")
            os.system("python ./webapp/CMapStateMachine.py > Final.xml")

            # Language
            os.system("python ./webapp/cmapper.py")


        # Language module for Cpp
        elif(language == 'c++'):
            # Transmogrify
            os.system("python ./webapp/CLexer.py")
            os.system("python ./webapp/CMapStateMachine.py > Final.xml")

            # Language
            os.system("python ./webapp/cppmapper.py")

        # Read output
        f = open('final_output.txt', 'r')
        data = f.read()
        f.close()

        os.system("> final_output.txt")

        context = {'form': form, 'object': data}

        return render(request, self.template_name, context)
