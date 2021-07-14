from django.shortcuts import render,redirect

from chairman.models import *
from .models import *
from random import *
from .utils import *

from django.http import JsonResponse #ajax


# Create your views here.
def index(request):
    try:
        if 'w_email' in request.session:
            uid=User.objects.get(email=request.session['w_email'])
            wid=Watchman.objects.get(user_id=uid)
            member_count=Member.objects.all().count()
            notice_count=Notice.objects.all().count()
            event_count=Event.objects.all().count()
            last3_member=Member.objects.all().order_by('-id')[:3]
            last_event=Event.objects.all().order_by('-id')[0]
            last_notice=Notice.objects.all().order_by('-id')[0]
            context={
                    'uid': uid,
                    'wid': wid,
                    'member_count':member_count,
                    'notice_count':notice_count,
                    'event_count':event_count,  
                    'last_event':last_event,
                    'last_notice':last_notice,
                    'last3_member':last3_member,

                        }
            return render(request,'watchman/index.html',{'context':context})
        else:
            return render(request,'chairman/c_login.html')
    except:
        return render(request,'chairman/c_login.html')

def register(request):
    if request.POST:
        fname=request.POST['fname']
        lname=request.POST['lname']
        contactNo=request.POST['contactNo']
        email=request.POST['email']

        uid=User.objects.create(email=email,role='Watchman')
        wid=Watchman.objects.create(fname=fname,lname=lname,contact_no=contactNo,user_id=uid)
        
        s_msg='Your Registration Request is sent to Chairman for approval'
        return render(request,'watchman/registration.html',{'s_msg':s_msg})
    else:
        return render(request,'watchman/registration.html')

def view_member(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        #mid=Member.objects.all().order_by('m_id__homeNo')
        mid=Member.objects.all()
        context={
            'mid':mid,
            'uid':uid,
            'wid':wid,
            }
        return render(request,'watchman/view-member.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def view_notice(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        noticeData=Notice.objects.all().order_by('-id')
        context={
            'noticeData':noticeData,
            'uid':uid,
            'wid':wid,
        }
        return render(request,'watchman/view-notice.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def view_event(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        eventData=Event.objects.all().order_by('-id')
        context={
            'eventData':eventData,
            'uid':uid,
            'wid':wid,
        }
        return render(request,'watchman/view-event.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def view_photo(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        photoData=Photo.objects.all().order_by('-id')
        context={
            'photoData':photoData,
            'uid':uid,
            'wid':wid,
        }
        return render(request,'watchman/view-photo.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def view_video(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        videoData=Video.objects.all().order_by('-id')
        context={
            'videoData':videoData,
            'uid':uid,
            'wid':wid,
        }
        return render(request,'watchman/view-video.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def profile(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        context={
                    'uid':uid,
                    'wid':wid,
                }
        if request.POST:
            fname=request.POST['fname']
            lname=request.POST['lname']
            address=request.POST['address']
            newPassword=request.POST['newPassword']
            contactNo=request.POST['contactNo']
            bloodgroup=request.POST['bloodgroup']

            if 'profilePic' in request.FILES:
                profilePic=request.FILES['profilePic']
                wid.profile_pic=profilePic
                wid.save()

            if newPassword:
                uid.password=newPassword
                uid.save()

            wid.fname=fname
            wid.lname=lname
            wid.address=address
            wid.contact_no=contactNo
            wid.bloodgroup=bloodgroup

            wid.save()
            return render(request,'watchman/profile.html',{'context':context})
        else:
            return render(request,'watchman/profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def add_visitor(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        if request.POST:
            fname=request.POST['fname']
            lname=request.POST['lname']
            contactNo=request.POST['contactNo']
            homeNo=request.POST['homeNo']
            visitorid=Visitor.objects.create(fname=fname,lname=lname,contact_no=contactNo,homeNo=homeNo)
            
            return redirect('w_view-visitor')      

        else:
            context={
                        'uid':uid,
                        'wid':wid,
                    }
            return render(request,'watchman/add-visitor.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def view_visitor(request):
    if 'w_email' in request.session:
        vid=Visitor.objects.all().order_by('-id')
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        context={
                    'uid':uid,
                    'wid':wid,
                    'vid':vid,
                }
        return render(request,'watchman/view-visitor.html',{'context':context}) 
    else:
        return render(request,'chairman/c_login.html')

def del_visitor(request):
    if 'w_email' in request.session:
        id=request.POST['id']
        vvid=Visitor.objects.get(id=id)
        vvid.delete()
        vid=list(Visitor.objects.values())
        context={
            'vid':vid, 
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')
 

def contact_list(request):
    if 'w_email' in request.session:
        uid=User.objects.get(email=request.session['w_email'])
        wid=Watchman.objects.get(user_id=uid)
        mid_contact=Member.objects.all().order_by('m_id__homeNo')
        wid_contact=Watchman.objects.all()
        context={
                'wid':wid,         #for sidebar
                'mid_contact':mid_contact,        
                'uid':uid,         #for sidebar
                'wid_contact':wid_contact,
            }
        return render(request,'watchman/contact-list.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

