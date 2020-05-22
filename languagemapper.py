from .cppmapper import convertercpp
from .cmapfunction import converterc
from .gomapper import convertergo
from .mapperpython import converterpython
file= open("intermediate.xml","r")
#Integrate with Django code as per how to access the language item from database @Aman
language='C' #Modify here


if(language=='C'):
    converterc()

if(language=='Python'):
    converterpython()

if(language=='CPP'):
    convertcpp()

if(language=='Go'):
    converterperl()

