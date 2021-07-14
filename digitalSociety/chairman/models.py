from django.db import models
import math
from django.utils import timezone


# Create your models here.
class User(models.Model):
    email=models.EmailField(unique=True,null=True)
    password=models.CharField(max_length=20)
    otp=models.IntegerField(default=20)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    role=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.email

class MemberDetail(models.Model):        #new
    homeNo=models.CharField(max_length=30)
    address=models.CharField(max_length=200)
    job_profession=models.CharField(max_length=30)
    job_address=models.CharField(max_length=200)
    vehicle_type=models.CharField(max_length=20)
    vehicle_no=models.CharField(max_length=20)
    bloodgroup=models.CharField(max_length=20)
    family_member_detail=models.CharField(max_length=20)
    contactNo=models.CharField(max_length=20)

    def __str__(self):
        return self.homeNo

class Chairman(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    m_id=models.ForeignKey(MemberDetail, on_delete=models.CASCADE,null=True)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    profile_pic=models.FileField(upload_to='img/',blank=True,default='c_profilePic.jpg')

    def __str__(self):
        return self.fname

class Member(models.Model):         #new
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    m_id=models.ForeignKey(MemberDetail, on_delete=models.CASCADE, null=True)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    profile_pic=models.FileField(upload_to='img/',blank=True,default='member_default_pic.jpg')

    def __str__(self):
        return self.fname

class Notice(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.title

    def whenPublished(self):
        now = timezone.now()
        diff= now - self.created_at
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1 or seconds == 0:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

class Event(models.Model):
    e_title=models.CharField(max_length=50)
    e_description=models.CharField(max_length=500)
    e_date=models.CharField(max_length=50,blank=False)
    e_fromTime=models.CharField(max_length=50,blank=False)
    e_toTime=models.CharField(max_length=50,blank=False)
    e_created_at=models.DateTimeField(auto_now_add=True,blank=False)
    e_updated_at=models.DateTimeField(auto_now=True,blank=False)
    e_postedBy=models.CharField(max_length=50,null=True)
    event_pic=models.FileField(upload_to='img/',blank=True,default='eventpic_default.jpg')
    def __str__(self):
        return self.e_title

    
    def whenPublished(self):
        now = timezone.now()
        diff= now - self.e_created_at
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1 or seconds == 0:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

class Watchman(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    fname=models.CharField(max_length=30,blank=True)
    lname=models.CharField(max_length=30,blank=True)
    contact_no=models.CharField(max_length=30,blank=True)
    is_verified=models.BooleanField(default=False)
    profile_pic=models.FileField(upload_to='img/',blank=True,default='watchman_default_pic.png')
    address=models.CharField(max_length=150,blank=True)
    bloodgroup=models.CharField(max_length=10,blank=True)

    def __str__(self):
        return self.fname

class Visitor(models.Model):
    fname=models.CharField(max_length=30,blank=True)
    lname=models.CharField(max_length=30,blank=True)
    contact_no=models.CharField(max_length=30,blank=True)
    homeNo=models.CharField(max_length=30)
    date=models.DateField(auto_now_add=True)
    inTime=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.fname
    
class Complaint(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    postedBy=models.CharField(max_length=50,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.title

    def whenPublished(self):
        now = timezone.now()
        diff= now - self.created_at
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1 or seconds == 0:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

class Suggestion(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    postedBy=models.CharField(max_length=50,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.title

    def whenPublished(self):
        now = timezone.now()
        diff= now - self.created_at
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1 or seconds == 0:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

class Photo(models.Model):
    photoName=models.CharField(max_length=50)
    photo=models.FileField(upload_to='img/',blank=False)
    postedBy=models.CharField(max_length=50,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)
    
    def __str__(self):
        return self.photoName
    
    def whenPublished(self):
        now = timezone.now()
        diff= now - self.created_at
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1 or seconds == 0:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

class Video(models.Model):
    videoName=models.CharField(max_length=50)
    video=models.FileField(upload_to='video/',blank=False)
    postedBy=models.CharField(max_length=50,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)
    
    def __str__(self):
        return self.videoName
    
    def whenPublished(self):
        now = timezone.now()
        diff= now - self.created_at
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1 or seconds == 0:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

class Maintenance(models.Model):
    #mem_id=models.ForeignKey(Member, on_delete=models.CASCADE,null=True)
    homeNo=models.CharField(max_length=20,default='XXX')
    fromMonth=models.CharField(max_length=20,default="--")
    toMonth=models.CharField(max_length=20,default="--")
    amount=models.IntegerField(default=0)
    dueDate=models.DateField(default="--")
    status=models.CharField(max_length=20,default='Pending')

    def __str__(self):
        return self.homeNo

class Transaction(models.Model):
    maintenance_id=models.ForeignKey(Maintenance, on_delete=models.CASCADE,null=True)##
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.maintenance_id.homeNo
    
