"""
Helper functions to take all the logic out of the views that isn't important to understanding how 
the view works
"""


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

    return total / len(sites)