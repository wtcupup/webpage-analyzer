"""
Helper functions to take all the logic out of the views that isn't important to understanding how 
the view works
"""

from backend.models import Website, WebsiteList


def get_site_list(sites):
    site_list = ''
    for site in sites:
        site_list += site.url + ','
    return site_list[:-1]  # get rid of trailing comma


def get_current_sites(master_list):
    sites = master_list.website_set.all()
    for site in sites:
        site.was_searched = False
    return sites


def find_average(sites):
    total = 0.0
    if len(sites) == 0:
        return 0
    for site in sites:
        total += site.count

    return round(total / len(sites), 2)


def process_go_line(line, master_list):
    line = line.decode("utf-8")
    results = line.split(',')
    url_searched = results[0]
    url_searched = url_searched[1:-1]
    if Website.objects.filter(list=master_list, url=url_searched).exists():
        current_site = Website.objects.get(list=master_list, url=url_searched)
        current_site.was_searched = True
        word_count = int(results[1])
        current_site.count = word_count
        current_site.save()


def get_tone_words_hashmap():
    tone_map = []
    return tone_map
