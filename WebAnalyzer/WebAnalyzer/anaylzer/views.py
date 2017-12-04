from django.shortcuts import render
import subprocess, os
from subprocess import Popen, run

# Create your views here.


def main_view(request):
    outputs = []
    if request.method == 'POST':
        search_word = request.POST['search_word']
        p = Popen(['./webpage-analyzer/main', str(search_word), 'http://www.wikipedia.org/'], stdout=subprocess.PIPE)
        p.wait()
        for line in p.stdout:
            outputs.append(line)
    return render(request, 'index.html', {'outputs': outputs})


'''
Code Fragments

run(['./webpage-analyzer/main', input_file_path, str(search_word)],
            shell=True, stdout=subprocess.PIPE)
            
p = Popen(['./webpage-analyzer/webpage-analyzer', input_file_path, str(search_word)], stdout=subprocess.PIPE)
        p.wait()

input_file_path = os.path.join('./webpage-analyzer', 'inputURLS.txt')
file = os.path.isfile(input_file_path)

output = subprocess.check_output(['./webpage-analyzer/webpage-analyzer',
                                          str(input_file_path), str(search_word)], shell=True)
'''