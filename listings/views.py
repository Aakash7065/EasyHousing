from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import Paginator
from .choice import state_choices, bedroom_choices, price_choices


def index(request):
    listings = Listing.objects.order_by('-listing_date').filter(is_publised=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listing = paginator.get_page(page)
    context = {'listings': paged_listing}
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    print("request")
    print(request.GET)
    listing_query = Listing.objects.order_by('-listing_date').filter(is_publised=True)

    if "keywords" in request.GET:
        keywords = request.GET["keywords"]
        print(keywords)
        if keywords:
            listing_query = listing_query.filter(description__icontains=keywords)

    if "city" in request.GET:
        city = request.GET["city"]
        if city:
            listing_query = listing_query.filter(city__iexact=city)

    if "state" in request.GET:
        state = request.GET["state"]
        if state:
            listing_query = listing_query.filter(state__iexact=state)

    if "bedrooms" in request.GET:
        bedroom = request.GET["bedrooms"]
        if bedroom:
            listing_query = listing_query.filter(bedroom__lte=bedroom)

    if "price" in request.GET:
        price = request.GET["price"]
        if price:
            listing_query = listing_query.filter(price__lte=price)

    context = {
        'price_choice': price_choices,
        'bedroom_choice': bedroom_choices,
        'state_choice': state_choices,
        'listings': listing_query,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
