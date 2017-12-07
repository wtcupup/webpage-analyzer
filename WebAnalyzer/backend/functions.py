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
    tone_words_map = {}
    tone_words_map['good'] = 0.5
    tone_words_map['better'] = 0.3
    tone_words_map['best'] = 0.9
    tone_words_map['excellent'] =0.8
    tone_words_map['nice'] = 0.5
    tone_words_map['positive'] = 0.5
    tone_words_map['cool'] = 0.4
    tone_words_map['terrific'] = 0.8
    tone_words_map['fantastic'] = 0.8
    tone_words_map['perfect'] = 1
    tone_words_map['awesome'] = 0.8
    tone_words_map['bad'] = -0.5
    tone_words_map['worse'] = -0.4
    tone_words_map['worst'] = -0.9
    tone_words_map['terrible'] = -0.8
    tone_words_map['horrible'] = -0.8
    tone_words_map['ugly'] = -0.4
    tone_words_map['negative'] = -0.5
    tone_words_map['evil'] = -0.9
    tone_words_map['disgrace'] = -0.8
    tone_words_map['disappoint'] = -0.4
    tone_words_map['trouble'] = -0.3
    return tone_words_map

