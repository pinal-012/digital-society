from django.shortcuts import render,redirect
from .models import *
from random import *
from .utils import *

from django.http import JsonResponse #ajax

# Create your views here.
def index(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        member_count=Member.objects.all().count()
        notice_count=Notice.objects.all().count()
        event_count=Event.objects.all().count()
        last3_member=Member.objects.all().order_by('-id')[:3]
        last_event=Event.objects.all().order_by('-id')[0]
        last_notice=Notice.objects.all().order_by('-id')[0]
        context={
                    'uid': uid,
                    'cid': cid, 
                    'member_count':member_count,
                    'notice_count':notice_count,
                    'event_count':event_count,  
                    'last_event':last_event,
                    'last_notice':last_notice,
                    'last3_member':last3_member,
                }
        return render(request,'chairman/index.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  #c_login.html is login page for all applications i.e. chairman,watchman,member      

def login_page(request):
    return render(request,'chairman/c_login.html')  

def check_email(request):
    role = request.POST['role']
    email= request.POST['email']

    print("-------------role",role)
    print(email)
    
    try:
        uid=User.objects.filter(email=email)
        print("uid-----------",uid)
        print("uid.role",uid[0].role)
        if uid is not None:
            print("------------uid in")
            print(role)
            print(uid[0].role)
            if uid[0].role == role :
                msg=""
            else:
                msg="You are not a ",role   
        else:                            #control never goes to else part
            msg="email does not exist"
    except:
        if email=="":
            msg="please enter your Email"
        else:
            msg="email does not exist"   
    context={
        "msg":msg,
        "email":email,
    }
    return JsonResponse({"context":context})   

def login_evaluate(request):
    try:
        u_email=request.POST['email']
        u_password=request.POST['password'] 
        role=request.POST['role']

        uid=User.objects.get(email=u_email)     

        if role.capitalize()=="Chairman":    #no need to use capitalize     
            if uid.password == u_password:  
                cid=Chairman.objects.get(user_id=uid)
                request.session['c_email']=uid.email    
                return redirect('c_index')
            else:
                e_msg="Invalid Password.Please Try Again!"
                return render(request,"chairman/c_login.html",{'e_msg':e_msg})  
                
        elif role.capitalize()=="Member":
            if uid.password == u_password:  
                mid=Member.objects.get(user_id=uid) 
                request.session['m_email']=uid.email    
                return redirect('index')
            else:
                e_msg="Invalid Password.Please Try Again!"
                return render(request,"chairman/c_login.html",{'e_msg':e_msg})   #c_login.html is login page for all applications i.e. chairman,watchman,member      

        elif role.capitalize()=="Watchman":
            if uid.password == u_password:  
                wid=Watchman.objects.get(user_id=uid)
                request.session['w_email']=uid.email    
                return redirect('w_index')
            else:
                e_msg="Invalid Password.Please Try Again!"
                return render(request,"chairman/c_login.html",{'e_msg':e_msg})
        
        else:
            e_msg="Select a valid role"           
            return render(request,"chairman/c_login.html",{'e_msg':e_msg})
    except Exception as e:
        print('--------------------------',e)
        e_msg="Email does not exists!"
        return render(request,'chairman/c_login.html',{'e_msg':e_msg})

def logout(request):
    if 'c_email' in request.session:
        del request.session['c_email']
        return render(request,'chairman/c_login.html')
    elif 'm_email' in request.session:
        del request.session['m_email']
        return render(request,'chairman/c_login.html')
    elif 'w_email' in request.session:
        del request.session['w_email']
        return render(request,'chairman/c_login.html')
    else:
        return render(request,'chairman/c_login.html')

def forgot_password(request):
    return render(request,'chairman/forgot_password.html')

def send_otp(request):
    try:
        email=request.POST['email']
        generate_otp=randint(1111,9999)
        uid=User.objects.get(email=email)
        print('uid--------------------',uid.role)

        if uid:
            uid.otp=generate_otp
            uid.save()                   #otp updation in database
            if uid.role=='Chairman':
                cid=Chairman.objects.get(user_id=uid)
                sendOtpMail('OTP for Foreget Password','email_otp',uid.email,{'otp':generate_otp, 'cid':cid})
                return render(request,'chairman/reset_password.html',{'email':email})
            elif uid.role=='Member':
                mid=Member.objects.get(user_id=uid) 
                sendOtpMail('OTP for Foreget Password','email_otp',uid.email,{'otp':generate_otp, 'mid':mid})
                return render(request,'chairman/reset_password.html',{'email':email})
            elif uid.role=='Watchman':
                wid=Watchman.objects.get(user_id=uid)
                sendOtpMail('OTP for Foreget Password','email_otp',uid.email,{'otp':generate_otp, 'wid':wid})
                return render(request,'chairman/reset_password.html',{'email':email})
        else:
            e_msg="Email dosen't exists!"
            return render(request,'chairman/forgot_password.html',{'e_msg':e_msg})

    except Exception as e:
        print('--------------------------',e)
        e_msg="Email dosen't exists!!"
        return render(request,'chairman/forgot_password.html',{'e_msg':e_msg})

def reset_password(request):
    try:
        email=request.POST['email']
        otp=request.POST['otp']
        newPassword=request.POST['newPassword']
        confirmPassword=request.POST['confirmPassword']

        uid=User.objects.get(email=email)
        if uid:
            if str(uid.otp)==otp:
                if newPassword==confirmPassword:
                    uid.password=newPassword
                    uid.save()
                    s_msg='Successfully Reset Password!'
                    return render(request,'chairman/c_login.html',{'s_msg':s_msg})
                else:
                    e_msg='New-Password must be same as Confirm-Password'
                    return render(request,'chairman/reset_password.html',{'e_msg':e_msg,'email':email})
            else:
                e_msg='Incorrect OTP'
                return render(request,'chairman/reset_password.html',{'e_msg':e_msg, 'email':email})
        else:
            e_msg='Incorrect Email'
            return render(request,'chairman/forgot_password.html',{'e_msg':e_msg})
    except Exception as e:
        e_msg='Incorrect Email'
        print('----------------------',e)
        return render(request,'chairman/forgot_password.html',{'e_msg':e_msg})

def add_notice(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        if request.POST:
            title=request.POST['title']
            desc=request.POST['desc']
            nid=Notice.objects.create(title=title,description=desc)    #Table of Notice is created in Database,title is stored in title field and desc is stored in description field. 
            return redirect('c_view-notice')                            #repeated data doesn't occur at the time page refresh using redirect
        else:
            context={
                    'uid':uid,
                    'cid':cid,
                }
            return render(request,'chairman/add-notice.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  
    
def view_notice(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        noticeData=Notice.objects.all().order_by('-id')
        context={
            'uid':uid,
            'cid':cid,
            'noticeData':noticeData
        }
        return render(request,'chairman/view-notice.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def del_notice(request):
    if 'c_email' in request.session:
        id=request.POST['id']
        nid=Notice.objects.get(id=id)
        nid.delete()

        noticeData=list(Notice.objects.values())
        context={
            'noticeData':noticeData,
        }

        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')  

def profile(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        context={
            'uid':uid,
            'cid':cid,
        }
       
        return render(request,'chairman/profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def profile_update(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)

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
            cid.profile_pic=profilePic
            cid.save()

        if newPassword:
            uid.password=newPassword
            uid.save()

        mid=MemberDetail.objects.get(homeNo=homeNo)
        cid.fname=fname
        cid.lname=lname
        
        mid.address=address
        mid.contactNo=contactNo
        mid.family_member_detail=familyMemberDetail
        mid.job_profession=jobProfession
        mid.job_address=jobAddress
        mid.vehicle_type=vehicleType
        mid.vehicle_no=vehicleNumber
        mid.bloodgroup=bloodgroup

        cid.save()
        mid.save()

        context={
                'uid':uid,
                'cid':cid,
                'mid':mid
            }

        return render(request,'chairman/profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def add_event(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        
        if request.POST:
            e_title=request.POST['e_title']
            e_desc=request.POST['e_desc']
            e_date=request.POST['e_date']
            e_fromTime=request.POST['e_fromTime']
            e_toTime=request.POST['e_toTime']
            eid=Event.objects.create(e_title=e_title,e_description=e_desc,e_date=e_date,e_fromTime=e_fromTime,e_toTime=e_toTime,e_postedBy=cid.fname)

            if 'eventPic' in request.FILES:
                event_pic=request.FILES['eventPic']
                eid.event_pic=event_pic
                eid.save()

            return redirect('c_view-event')
        else:
            context={
                    'uid':uid,
                    'cid':cid,
                }
            return render(request,'chairman/add-event.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')   

def view_event(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        eventData=Event.objects.all().order_by('-id')  
        context={
            'uid':uid,
            'cid':cid,
            'eventData':eventData,
        }
        return render(request,'chairman/view-event.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')   

def del_event(request):
    if 'c_email' in request.session:
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
    
def view_complaint(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        complaintData=Complaint.objects.all().order_by('-id')
        context={
            'uid':uid,
            'cid':cid,
            'complaintData':complaintData,
        }
        return render(request,'chairman/view-complaint.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def del_complaint(request):
    if 'c_email' in request.session:
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

def view_suggestion(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        suggestionData=Suggestion.objects.all().order_by('-id')
        context={
            'uid':uid,
            'cid':cid,
            'suggestionData':suggestionData,
        }
        return render(request,'chairman/view-suggestion.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def del_suggestion(request):
    if 'c_email' in request.session:
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

def add_photo(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        if request.POST:
            photoName=request.POST['photoName']
            photo=request.FILES['photo']
            pid=Photo.objects.create(photoName=photoName,photo=photo,postedBy='Chairman-'+cid.fname+' '+cid.lname)
            return redirect('c_view-photo')
        else:
            context={
                'uid':uid,
                'cid':cid,
            }
            return render(request,'chairman/add-photo.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def view_photo(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        photoData=Photo.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'photoData':photoData,
        }
        return render(request,'chairman/view-photo.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def del_photo(request):
    if 'c_email' in request.session:
        id=request.POST['id']
        pid=Photo.objects.get(id=id)
        pid.delete()
        photoData=list(Photo.objects.values())
        context={
            'photoData':photoData,
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')  

def add_video(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        if request.POST:
            videoName=request.POST['videoName']
            video=request.FILES['video']
            vid=Video.objects.create(videoName=videoName,video=video,postedBy='Chairman-'+cid.fname+' '+cid.lname)
            return redirect('c_view-video')
        else:
            context={
                'uid':uid,
                'cid':cid,
            }
            return render(request,'chairman/add-video.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def view_video(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        videoData=Video.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'videoData':videoData,
        }
        return render(request,'chairman/view-video.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def del_video(request):
    if 'c_email' in request.session:
        id=request.POST['id']
        vid=Video.objects.get(id=id)
        vid.delete()
        videoData=list(Video.objects.values())
        context={
            'videoData':videoData,
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')

def add_member(request):#
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
       
        if request.POST:
            fname=request.POST['fname']
            lname=request.POST['lname']
            homeNo=request.POST['homeNo']
            contactNo=request.POST['contactNo']
            vehicleType=request.POST['vehicleType']
            vehicleNumber=request.POST['vehicleNumber']
            familyMemberDetail=request.POST['familyMemberDetail']
            bloodgroup=request.POST['bloodgroup']
            email=request.POST['email']
            jobProfession=request.POST['jobProfession']
            jobAddress=request.POST['jobAddress']
            address=request.POST['address']

            password=fname[:3]+str(randint(111,999))

            #if email != request.session['c_email']:
            #else:
            #   pass
            user_id=User.objects.create(email=email,password=password,role='Member')
            memberDetail_id=MemberDetail.objects.create(homeNo=homeNo,contactNo=contactNo,vehicle_type=vehicleType,vehicle_no=vehicleNumber,family_member_detail=familyMemberDetail,bloodgroup=bloodgroup,address=address,job_profession=jobProfession,job_address=jobAddress)
            member_id=Member.objects.create(fname=fname,lname=lname,m_id=memberDetail_id,user_id=user_id)
            
            mid=Member.objects.all()    #we can access data of Member model as well as Member-datails model by creating only one object as foreign key is given in Member Table
            
            context={
                'uid':uid,
                'cid':cid,
                'mid':mid,  
            }
    
            sendPasswordMail('Password to login','email_password',email,{'password':password, 'mid':mid})
            print('-----------------------------',email)
            return render(request,'chairman/view-member.html',{'context':context})
        else:
            context={
                    'uid':uid,
                    'cid':cid,
                }
        return render(request,'chairman/add-member.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')

def view_member_profile(request,pk): #   #primary key accepted
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        mid=Member.objects.get(id=pk)      #get pk to id
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
        }
       
        return render(request,'chairman/view-member-profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def view_member(request):#
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        mid=Member.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
        }
        return render(request,'chairman/view-member.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')   

def del_member(request):
    if 'c_email' in request.session:
        id=request.POST['id']
        memberid=Member.objects.get(id=id)
        memberid.delete()
        memberid.user_id.delete()
        memberid.m_id.delete()
        mid=list(Member.objects.values())
        context={
            'mid':mid,
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html')  

def update_member_profile(request):#
    if 'c_email' in request.session:
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
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

        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        md_mid=MemberDetail.objects.get(homeNo=homeNo)
        mid=Member.objects.get(m_id=md_mid)

        if 'profilePic' in request.FILES:
            profilePic=request.FILES['profilePic']
            mid.profile_pic=profilePic
            mid.save()

        if newPassword:
            mid.user_id.password=newPassword
            mid.save()

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

        mid.save()
        md_mid.save()

        context={
                'uid':uid,
                'md_mid':md_mid,
                'mid':mid,
                'cid':cid,
            }

        return render(request,'chairman/view-member-profile.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html')  

def watchman_list(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        wid_all=Watchman.objects.all().order_by('-id')         #order according to -id i.e. reverse data
    
        context={
            'uid':uid,
            'cid':cid,
            'wid_all':wid_all, 
        }
        return render(request,'chairman/watchman-list.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def watchman_approval(request,pk): #primary key accepted
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        wid=Watchman.objects.get(id=pk)      #get pk to id
        password=str(randint(1111,9999))+wid.fname[:3]

        if wid.is_verified==False:
            wid.is_verified=True
            wid.save()
            print('--------------------',wid.user_id.password)
            wid.user_id.password=password
            wid.user_id.save()
            sendPasswordMail('Login Password','email_watchman_password',wid.user_id.email,{'password':password, 'wid':wid})

        elif wid.is_verified==True:
            wid.is_verified=False
            wid.save()

        wid_all=Watchman.objects.all().order_by('-id')
        context={
            'uid':uid,
            'cid':cid,
            'wid':wid,
            'wid_all':wid_all,     
        }
        return render(request,'chairman/watchman-list.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def del_watchman(request):
    if 'c_email' in request.session:
        id=request.POST['id']
        wid=Watchman.objects.get(id=id)
        wid.delete()
        wid.user_id.delete()
        wid_all=list(Watchman.objects.values())
        context={
            'wid_all':wid_all, 
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html') 

def view_visitor(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        visitorData=Visitor.objects.all().order_by('-id')
        context={
                'visitorData':visitorData,
                'cid':cid,         #for sidebar
                'uid':uid,         #for sidebar
            }
        return render(request,'chairman/view-visitor.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def contact_list(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        mid=Member.objects.all().order_by('m_id__homeNo')
        wid=Watchman.objects.all()
        context={
                'mid':mid,
                'cid':cid,         #for sidebar
                'uid':uid,         #for sidebar
                'wid':wid,
            }
        return render(request,'chairman/contact-list.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def add_maintenance(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        mid=Member.objects.all().order_by('m_id__homeNo')
    
        if request.POST:
            homeNo=request.POST['homeNo']
            fromMonth=request.POST['fromMonth']
            toMonth=request.POST['toMonth']
            amount=request.POST['amount']
            dueDate=request.POST['dueDate']
            if homeNo != "All":
                maintenance_id=Maintenance.objects.create(homeNo=homeNo,fromMonth=fromMonth,toMonth=toMonth,amount=amount,dueDate=dueDate)
                
            else:
                for i in mid:
                    maintenance_id=Maintenance.objects.create(homeNo=i.m_id.homeNo,fromMonth=fromMonth,toMonth=toMonth,amount=amount,dueDate=dueDate)

            return redirect('c_view-maintenance')       
            #maintenanceData=Maintenance.objects.all().order_by('homeNo')
            #context={
            #    'cid':cid,         #for sidebar
            #    'uid':uid,         #for sidebar
            #    'maintenanceData':maintenanceData,
            #    }
            #return render(request,'chairman/view-maintenance.html',{'context':context})
        else:
            context={
                    'mid':mid,
                    'cid':cid,         #for sidebar
                    'uid':uid,         #for sidebar
                }
            return render(request,'chairman/add-maintenance.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def view_maintenance(request):
    if 'c_email' in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        cid=Chairman.objects.get(user_id=uid)
        maintenanceData=Maintenance.objects.all().order_by('homeNo')
        context={
                'cid':cid,         #for sidebar
                'uid':uid,         #for sidebar
                'maintenanceData':maintenanceData  
            }
        
        return render(request,'chairman/view-maintenance.html',{'context':context})
    else:
        return render(request,'chairman/c_login.html') 

def del_maintenance(request):
    if 'c_email' in request.session:
        id=request.POST['id']
        mid=Maintenance.objects.get(id=id)
        mid.delete()
        maintenanceData=list(Maintenance.objects.values())
        context={
            'maintenanceData':maintenanceData, 
        }
        return JsonResponse({"context":context})
    else:
        return render(request,'chairman/c_login.html') 



















































































