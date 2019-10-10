from .models import Contacts
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings

def contacts(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        # has user already contacted
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contacts.objects.filter(listing_id=listing_id, user_id=user_id).exists()
            if has_contacted:
                messages.error(request, "already contacted")
                return redirect('/listings/' + listing_id)

        contact = Contacts(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message,
                           user_id=user_id)
        contact.save()
        send_mail('Property Listing Inquiry',
                  f'There has been inquiry for {listing} . Signin to admin pannel for more Info',
                  settings.EMAIL_HOST,
                  ['aakash7065@gmail.com',f'{listing.realtor.email}'],
                  False
                  )
        messages.success(request, "your request has been saved successfully, we will contact you soon")
        return redirect('/listings/' + listing_id)
