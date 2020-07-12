"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.db.models import Q
from django.shortcuts import render

from ratelimit.decorators import ratelimit
from mhttc.apps.main.models import Project
from itertools import chain

from mhttc.settings import VIEW_RATE_LIMIT as rl_rate, VIEW_RATE_LIMIT_BLOCK as rl_block

from django.shortcuts import render

# Custom 404/500 views


def handler404(request, exception):
    response = render(request, "base/404.html", {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, "base/500.html", {})
    response.status_code = 500
    return response


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def index_view(request):
    return render(request, "main/index.html")


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def about_view(request):
    return render(request, "main/about.html")


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def terms_view(request):
    return render(request, "terms/usage_agreement_fullwidth.html")


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def contact_view(request):
    return render(request, "main/contact.html")


# Search


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def search_view(request, query=None):
    """search projects. This is available to anyone with a login    
    """
    context = {"submit_result": "anything"}

    # First go, see if the user added a query variable as a GET request
    if query is None:
        query = request.GET.get("q")

    # Empty query should return all parts ("")
    if query is not None:
        results = run_query(query)
        context["results"] = results

    return render(request, "search/search.html", context)


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def run_search(request):
    """The driver to show results for a parts search.
    """
    if request.method == "POST":
        q = request.POST.get("q")
    else:
        q = request.GET.get("q")

    if q is not None:
        results = run_query(q)
        context = {"results": results, "submit_result": "anything"}
        return render(request, "search/result.html", context)


# Search Function ##############################################################


def run_query(q, available=False):
    """search across projects and centers.
    """
    # If the user adds hashtag, remove
    if q.startswith("#"):
        q = q.replace("#", "", 1)

    # Allow support for future kinds of searches
    searches = {"projects": projects_query}
    query_types = searches.keys()

    results = []
    for query_type in query_types:
        if query_type in searches:
            results = list(chain(results, searches[query_type](q)))
    return results


def projects_query(q):
    """specific search for distributions
    """
    return Project.objects.filter(
        Q(name__icontains=q)
        | Q(center__name__icontains=q)
        | Q(description__icontains=q)
    ).distinct()
