from django.shortcuts import render, redirect
import subprocess
from subprocess import Popen
from backend.models import Website, WebsiteList
from backend.functions import get_site_list, get_current_sites, find_average, process_go_line

# Create your views here.


def main_view(request):
    master_list = WebsiteList.objects.first()
    sites = get_current_sites(master_list)
    average = 0
    was_search = False

    if request.method == 'POST':

        search_word = request.POST.get('search_word', False)
        url_to_add = request.POST.get('new_url', False)

        if search_word:
            was_search = True
            site_list = get_site_list(sites)
            go_pipe = Popen(['./golang/main', str(search_word), site_list], stdout=subprocess.PIPE)
            go_pipe.wait()

            for line in go_pipe.stdout:
                process_go_line(line, master_list)

        elif url_to_add:

            if not Website.objects.filter(list=master_list, url=url_to_add).exists():
                new_website = Website(list=master_list, url=url_to_add)
                new_website.save()

        sites = master_list.website_set.all()
        sites = sites.order_by('count')
        sites = sites.reverse()
        average = find_average(sites)
    return render(request, 'index.html', {'sites': sites, 'average': average, 'was_search': was_search})


def tone_view(request):

    return render(request, 'tone.html', context=None)


def delete_url_view(request, id):
    id_to_delete = int(id)
    site_to_delete = Website.objects.get(id=id_to_delete)
    site_to_delete.delete()
    return redirect('/')
