from django.shortcuts import render,redirect,HttpResponse
from ecommerceapp.models import Contact,Products,Orders,OrderUpdate
from django.contrib import messages
from math import ceil
# Create your views here.
def index(request):
    allprods=[]
    catprods = Products.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Products.objects.filter(category=cat)
        n=len(prod)
        nSlides=n // 4 +ceil(n/4) - (n //4 )
        allprods.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allprods}
    return render(request,"index.html",params)

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        desc=request.POST['desc']
        pnumber=request.POST['pnumber']
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,'we will get you soon')
    

    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/login')
    if request.method=="POST":

        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
         

        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
        
        id = Order.order_id
        oid=str(id)
        oid=str(id)
        param_dict = {

            'MID': 'add ur merchant id',
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict}) 

    return render(request, 'checkout.html')