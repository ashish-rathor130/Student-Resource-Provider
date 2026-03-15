from django.shortcuts import render, redirect
from .models import CustomUser
from .utils import generate_otp, verify_otp
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login,logout
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from resources.models import CourseModel,SemesterModel,Notes,Subject,Unit
from django.db.models import Subquery
from .forms import CourseForm,SubjectForm,SemesterForm,UnitForm,NotesForm

def home(request):
    courses = CourseModel.objects.all()
    semesters = SemesterModel.objects.all()
    notes = Notes.objects.all()
    subjects = Subject.objects.all()
    units = Unit.objects.all()
    
    resources = {
        "courses":courses,
        'semesters':semesters,
        'notes':notes,
        'subjects':subjects,
        'units':units
    }
    
    return render(request, 'home.html',resources)

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
       
        try:
            user = CustomUser.objects.create_user(username = username,email=email, password=password)
            otp = generate_otp()
            user.email_otp = otp
            user.save()
            send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp}',
                settings.DEFAULT_USER_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, "Registration successful! An OTP has been sent to your email.")
            return redirect('verify_otp', user_id=user.id)
        except Exception as e:
            messages.error(request,f"This email is already exists!")
            return redirect('register')

    return render(request, 'auth/register.html')

def verify_user_otp(request, user_id):
   user = CustomUser.objects.get(id=user_id)
   if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        if verify_otp(entered_otp, user.email_otp):
            user.is_email_verified = True
            user.email_otp = None
            user.save()
            messages.success(request, "Email verified successfully! You can now log in.")
            return redirect('login')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP','user_id': user.id})
   return render(request, 'auth/verify_otp.html', {'user_id': user.id})


def resend_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    # Optional: throttle resends (e.g., allow only after 60 seconds)
    if hasattr(user, "otp_last_sent") and user.otp_last_sent:
        if timezone.now() - user.otp_last_sent < timedelta(seconds=60):
            messages.error(request, "Please wait before requesting another OTP.")
            return redirect('verify_otp', user_id=user.id)

    # Generate new OTP
    otp = generate_otp()
    user.email_otp = otp
    user.otp_last_sent = timezone.now()  # add this field in your model
    user.save()

    # Send OTP via email
    send_mail(
        'Your OTP Code',
        f'Your new OTP is: {otp}',
        settings.DEFAULT_USER_EMAIL,
        [user.email],
        fail_silently=False,
    )
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_otp', user_id=user.id)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                if user.is_email_verified:
                    print(login(request, user))
                    messages.success(request, "Login successful!")
                    return redirect('home')
                else:
                    messages.error(request, "Please verify your email before logging in.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid credentials.")
                return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('login')

    return render(request, 'auth/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def reset_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            print(user)
            # Generate a temporary password
            temp_password = get_random_string(length=8)
            user.set_password(temp_password)
            user.save()

            # Send email with new password
            subject = "Password Reset Request"
            message = f"Hello {user.username},\n\nYour temporary password is: {temp_password}\nPlease log in and change it immediately."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            # Success message
            messages.success(request, "A temporary password has been sent to your registered email.")
            return redirect("login")

        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email address.")
            return redirect("reset_password")

    return render(request, "auth/reset_password.html")

@login_required
def change_password_view(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        # Check old password
        if not user.check_password(old_password):
            messages.error(request, "Your old password is incorrect.")
            return redirect("change_password")

        # Check new password match
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect("change_password")

        # Update password
        user.set_password(new_password)
        user.save()

        messages.success(request, "Your password has been changed successfully. Please log in again.")
        return redirect("login")

    return render(request, "auth/change_password.html")


@login_required
def profile(request,user_id):
    user = CustomUser.objects.get(pk = user_id)
    return render(request,'profile.html',{'user':user})

def about_us(request):
    return render(request,"about.html")
    
def notes(request,sem_id):
    semester = SemesterModel.objects.get(semester_id = sem_id)
    subs = semester.subjects.values()
    units = Unit.objects.all()
    
    resources = {
        'semester':semester,
        'subjects':semester.subjects.values(),
        'units':[{units.filter(subject_id=id.get('subject_id'))} for id in subs]
    }
    return render(request,"notes/note.html",resources)

def all_units(request,sub_id):
    subject = Subject.objects.get(subject_id=sub_id)
    units = Unit.objects.filter(subject = sub_id)
    resources = {
        'units':units,
        'semester':subject.semester,
        'subject':subject,
    }
    return render(request,"notes/units.html",resources)


def upload_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        data = CourseModel.objects.all()
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user  # attach logged-in user
            try:
                is_exists = data.get(course_name = course.course_name)
                if is_exists:
                    messages.warning(request, "Course is already uploaded!")       
            except Exception as e:
                course.save()
                messages.success(request, "Course uploaded successfully!")
                return redirect('home')
    else:
        form = CourseForm()
    return render(request, "uploads/upload_course.html", {"form": form})


def upload_semester(request):
    if request.method == "POST":
        form = SemesterForm(request.POST)
        semesters = SemesterModel.objects.all()
        if form.is_valid():
            form.save()
            messages.success(request, "Semester uploaded successfully!")
            return redirect('upload_semester')  # reload page or redirect elsewhere
        else:
            messages.error(request, "There was an error uploading the semester.")
    else:
        form = SemesterForm()
    return render(request, "uploads/upload_semester.html", {"form": form})

def upload_subject(request,sem_id):
    semester = SemesterModel.objects.get(semester_id = sem_id)
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.semester = semester
            sub.save()
            messages.success(request, "Subject uploaded successfully!")
            return redirect('home')  # reload page or redirect elsewhere
        else:
            messages.error(request, "There was an error uploading the subject.")
    else:
        form = SubjectForm()
    return render(request, "uploads/upload_subject.html", {"form": form,'semester':semester})

def upload_unit(request,sub_id):
    try:
        subject = Subject.objects.get(subject_id= sub_id)
    except:
        subject = ""
        
    print(subject.subject_name)
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.subject = subject
            unit.save()
            messages.success(request, "Unit uploaded successfully!")
            return redirect('upload_unit')  # reload page or redirect elsewhere
        else:
            messages.error(request, "There was an error uploading the unit.")
    else:
        form = UnitForm()
    return render(request, "uploads/upload_unit.html", {"form": form,'subject':subject})

def upload_note(request):
    if request.method == "POST":
        form = NotesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Note uploaded successfully!")
            return redirect('upload_note')  # reload page or redirect elsewhere
        else:
            messages.error(request, "There was an error uploading your note.")
    else:
        form = NotesForm()
    return render(request, "uploads/upload_note.html", {"form": form})

def papers(request):
    return render(request,"papers/sem1.html")