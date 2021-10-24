from givers.models import Give,Vendor
from datetime import datetime,timedelta, tzinfo
from django.utils import timezone
from django.db.models import Q

#update update_picked from views
def update_picked():
    vend=Vendor.objects.filter(payment_status=False)
    give=Give.objects.filter(~Q(gift_status='received') & Q(date_requested__isnull=False))
    data = {
            'date_requested':None,
            'gift_recipient': '',
            'gift_status':'unpicked'}
    for obj in give:
        b=timezone.now()-obj.date_requested
        diff=int(b.days)
        if diff>=2 and obj.gift.payment_status==False:
            
            obj.date_requested= data['date_requested']
            obj.gift_recipient= data['gift_recipient']
            obj.gift_status=data['gift_status']
            obj.gift.ticket=''
            obj.gift.amount=None
            obj.gift.receiver_number=None
            obj.gift.delivery_address=None
            obj.gift.giver_contacted=False
            obj.gift.receiver_contacted=False
            obj.save()
    