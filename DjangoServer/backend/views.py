from django.shortcuts import render, redirect
import subprocess
from subprocess import Popen
from backend.models import Website, WebsiteList
from backend.functions import get_site_list, get_current_sites, find_average, process_go_line, get_tone_words_hashmap

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

            go_pipe.terminate()

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
    tone_words= get_tone_words_hashmap()
    master_list = WebsiteList.objects.first()
    sites = get_current_sites(master_list)
    site_list = get_site_list(sites)
    #key map holds urls as keys and scores as values
    score_map={}
    for site in sites:
        score_map[site.url] = 0
    # search for the term "key" in the list of sites
    # for each site's frequency of that term, multiply that frequency by tone_words[key]
    # and add the product to that site's score in score_map
    for key in tone_words:
        go_pipe = Popen(['./golang/main', key, site_list], stdout=subprocess.PIPE)
        go_pipe.wait()
        for line in go_pipe.stdout:
            line = line.decode("utf-8")
            results = line.split(',')
            url_searched = results[0]  # the
            url_searched = url_searched[1:-1]
            if Website.objects.filter(list=master_list, url=url_searched).exists():
                word_count = int(results[1])  # the frequency for that url
                weighted_word_count = word_count*tone_words[key]
                score_map[url_searched] += weighted_word_count
    #   round scores
    for site in sites:
        score_map[site.url] = round(score_map[site.url], 2)

    ordered_values = sorted(score_map.values())
    ordered_values.reverse()

    # get results in a zip array for displaying

    ordered_sites = list(sorted(score_map, key=score_map.__getitem__, reverse=True))
    results = zip(ordered_sites, ordered_values)
    return render(request, 'tone.html', {'map': score_map, 'results': results})


def delete_url_view(request, id):
    id_to_delete = int(id)
    site_to_delete = Website.objects.get(id=id_to_delete)
    site_to_delete.delete()
    return redirect('/')
