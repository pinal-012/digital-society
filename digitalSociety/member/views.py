from django.shortcuts import render,redirect
from chairman.models import *
from random import *           #password generation
from .utils import *           #send email

from django.conf import settings   #paytm
from .paytm import generate_checksum, verify_checksum #paytm
from django.views.decorators.csrf import csrf_exempt  #paytm

from django.http import JsonResponse #ajax


# Create your views here.
def index(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid) 
        member_count=Member.objects.all().count()
        notice_count=Notice.objects.all().count()
        event_count=Event.objects.all().count()
        last3_member=Member.objects.all().order_by('-id')[:3]
        last_event=Event.objects.all().order_by('-id')[0]
        last_notice=Notice.objects.all().order_by('-id')[0]
        context={
                    'uid': uid,
                    'mid': mid,
                    'member_count':member_count,
                    'notice_count':notice_count,
                    'event_count':event_count,  
                    'last_event':last_event,
                    'last_notice':last_notice,
                    'last3_member':last3_member,
                }
        return render(request,'member/index.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')         

def view_notice(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        noticeData=Notice.objects.all()
        context={
            'uid':uid,
            'mid':mid,
            'noticeData':noticeData
        }
        return render(request,'member/view-notice.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def add_event(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)

        if request.POST:
            e_title=request.POST['e_title']
            e_desc=request.POST['e_desc']
            e_date=request.POST['e_date']
            e_fromTime=request.POST['e_fromTime']
            e_toTime=request.POST['e_toTime']
            
            eid=Event.objects.create(e_title=e_title,e_description=e_desc,e_date=e_date,e_fromTime=e_fromTime,e_toTime=e_toTime,e_postedBy=mid.fname+' '+mid.lname)
            
            if 'eventPic' in request.FILES:
                event_pic=request.FILES['eventPic']
                eid.event_pic=event_pic
                eid.save()
            
            return redirect('view-your-event')
        else:
            context={
                'uid':uid,
                'mid':mid,
                }
            return render(request,'member/add-event.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def view_event(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        eventData=Event.objects.all().order_by('-id') 
        context={
            'uid':uid,
            'mid':mid,
            'eventData':eventData,
        }
        return render(request,'member/view-event.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def view_your_event(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        eventData=Event.objects.all().filter(e_postedBy=mid.fname+' '+mid.lname).order_by('-id') 
        context={
            'uid':uid,
            'mid':mid,
            'eventData':eventData,
        }
        return render(request,'member/view-your-event.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 


def del_event(request):
    if 'm_email' in request.session:
        id=request.POST['id']
        eid=Event.objects.get(id=id)
        eid.delete()
        eventData=list(Event.objects.values())
        context={
            'eventData':eventData,
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')  

def profile(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        
        context={
            'uid':uid,
            'mid':mid,
        }
       
        return render(request,'member/profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def profile_update(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)

        fname=request.POST['fname']
        lname=request.POST['lname']
        address=request.POST['address']
        newPassword=request.POST['newPassword']
        contactNo=request.POST['contactNo']
        familyMemberDetail=request.POST['familyMemberDetail']
        jobProfession=request.POST['jobProfession']
        jobAddress=request.POST['jobAddress']
        vehicleType=request.POST['vehicleType']
        vehicleNumber=request.POST['vehicleNumber']
        bloodgroup=request.POST['bloodgroup']
        homeNo=request.POST['homeNo']          #to get mid homeNo is needed

        if 'profilePic' in request.FILES:
            profilePic=request.FILES['profilePic']
            mid.profile_pic=profilePic
            mid.save()

        if newPassword:
            uid.password=newPassword
            uid.save()
        
        md_mid=MemberDetail.objects.get(homeNo=homeNo)
        mid.fname=fname
        mid.lname=lname
        
        md_mid.address=address
        md_mid.contactNo=contactNo
        md_mid.family_member_detail=familyMemberDetail
        md_mid.job_profession=jobProfession
        md_mid.job_address=jobAddress
        md_mid.vehicle_type=vehicleType
        md_mid.vehicle_no=vehicleNumber
        md_mid.bloodgroup=bloodgroup

        uid.save()
        md_mid.save()
        mid.save()

        context={
                'uid':uid,
                'mid':mid,
            }

        return render(request,'member/profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def add_complaint(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
         
        if request.POST:
            title=request.POST['title']
            description=request.POST['desc']
            complaint_id=Complaint.objects.create(title=title,description=description,postedBy=mid.fname+''+mid.lname)
            return redirect('view-complaint') 
        else:
            context={
                'uid':uid,
                'mid':mid,
                }
        return render(request,'member/add-complaint.html',{'context':context}) 
    else:
        return render(request,'chairman/c_login.html') 

def view_complaint(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        complaintData=Complaint.objects.all().filter(postedBy=mid.fname+''+mid.lname).order_by('-id')
        context={
            'complaintData':complaintData,
            'uid':uid,
            'mid':mid,
        }
        return render(request,'member/view-complaint.html',{'context':context}) 
    else:
        return render(request,'chairman/c_login.html') 

def del_complaint(request):
    if 'm_email' in request.session:
        id=request.POST['id']
        cid=Complaint.objects.get(id=id)
        cid.delete()
        complaintData=list(Complaint.objects.values())
        context={
            'complaintData':complaintData,
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')

def add_suggestion(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        if request.POST:
            title=request.POST['title']
            description=request.POST['desc']
            suggestion_id=Suggestion.objects.create(title=title,description=description,postedBy=mid.fname+' '+mid.lname)      
            return redirect('view-suggestion')
        else:
            context={
                'uid':uid,
                'mid':mid,
            }
            return render(request,'member/add-suggestion.html',{'context':context}) 
    else:
        return render(request,'chairman/c_login.html') 

def view_suggestion(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        suggestionData=Suggestion.objects.all().filter(postedBy=mid.fname+' '+mid.lname).order_by('-id')
        context={
            'suggestionData':suggestionData,
            'uid':uid,
            'mid':mid,
        }
        return render(request,'member/view-suggestion.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def del_suggestion(request):
    if 'm_email' in request.session:
        id=request.POST['id']
        sid=Suggestion.objects.get(id=id)
        sid.delete()
        suggestionData=list(Suggestion.objects.values())
        context={
            'suggestionData':suggestionData,
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')


def view_member(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        mid_all=Member.objects.all()
        context={
            'mid_all':mid_all,
            'mid':mid,         #for sidebar
            'uid':uid,         #for sidebar
        }
        return render(request,'member/view-member.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def view_member_profile(request,pk):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        mid_pk=Member.objects.get(id=pk)      #get pk to id
        context={
            'uid':uid,
            'mid_pk':mid_pk,
            'mid':mid,
        }
       
        return render(request,'member/view-member-profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def view_photo(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        photoData=Photo.objects.all()
        context={
                'photoData':photoData,
                'mid':mid,         #for sidebar
                'uid':uid,         #for sidebar
            }
        return render(request,'member/view-photo.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def view_video(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        videoData=Video.objects.all()
        context={
                'videoData':videoData,
                'mid':mid,         #for sidebar
                'uid':uid,         #for sidebar
            }
        return render(request,'member/view-video.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def view_visitor(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        visitorData=Visitor.objects.filter(homeNo=mid.m_id.homeNo)
        context={
                'visitorData':visitorData,
                'mid':mid,         #for sidebar
                'uid':uid,         #for sidebar
            }
        return render(request,'member/view-visitor.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def contact_list(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        mid_contact=Member.objects.all().order_by('m_id__homeNo')
        wid=Watchman.objects.all()
        context={
                'mid':mid,         #for sidebar
                'mid_contact':mid_contact,        
                'uid':uid,         #for sidebar
                'wid':wid,
            }
        return render(request,'member/contact-list.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def maintenance_bill(request):
    if 'm_email' in request.session:
        uid=User.objects.get(email=request.session['m_email'])
        mid=Member.objects.get(user_id=uid)
        maintenanceData=Maintenance.objects.filter(homeNo=mid.m_id)
        context={
                'mid':mid,         #for sidebar       
                'uid':uid,         #for sidebar
                'maintenanceData':maintenanceData,
            }
        return render(request,'member/maintenance-bill.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def initiate_payment(request,pk):
    if 'm_email' in request.session:
        #if request.method == "GET":
        #   return render(request, 'member/maintenance-bill.html')
        try:
            global paymentid
            uid=User.objects.get(email=request.session['m_email'])
            maintenance=Maintenance.objects.get(id=pk)
            amount = maintenance.amount
            paymentid=pk
            
            print('-----------------',uid.email)
            print('-----------------',amount)
            print('-----------------',paymentid)
                
        except:
            return render(request, 'member/maintenance-bill.html', context={'error': 'Wrong Accound Details or amount'})

        transaction = Transaction.objects.create(made_by=uid, amount=amount,maintenance_id=maintenance)  ##
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            #('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/member/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'member/redirect.html', context=paytm_params)
    else:
        return render(request,'chairman/c_login.html') 

@csrf_exempt
def callback(request):
    
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        print('----------------------------------------------status',received_data['STATUS'])
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            if received_data['STATUS'] ==  ['TXN_SUCCESS']:
                maintenance=Maintenance.objects.get(id=paymentid)
                maintenance.status='Paid'
                maintenance.save()
               # t_id=Transaction.objects.get(order_id=received_data['ORDERID'])
                #uid=User.objects.get(email=request.session['m_email'])
                #print('-----------------',t_id.made_by)
                context={'received_data':received_data}
                print('-----------------------',received_data)
                
                #sendPaymentMail('Paytm Payment','email_callback',t_id.made_by,{'maintenance':maintenance,'txnid':received_data['TXNID'],'orderid':received_data['ORDERID'],'txnamount':received_data['TXNAMOUNT']})

        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'member/callback.html', context=received_data)
        return render(request, 'member/callback.html', context=received_data)



#zmdi-zmdi-walk      visitor
#



