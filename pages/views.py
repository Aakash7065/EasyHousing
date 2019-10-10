from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from listings.choice import bedroom_choices, price_choices, state_choices


# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-listing_date').filter(is_publised=True)[:3]
    state_choices1 = sorted(state_choices)
    context = {
        'listings': listings,
        'price_choice': price_choices,
        'bedroom_choice': bedroom_choices,
        'state_choice': state_choices
    }
    return render(request, 'pages/index.html', context)


def about(request):
    realtors = Realtor.objects.order_by('hire_date')
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }
    return render(request, 'pages/about.html', context)
