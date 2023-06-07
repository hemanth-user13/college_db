import pdb

from django.shortcuts import render, redirect
from .models import UploadedFile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm
from .models import *
from  teachers.models import *
from django.db.models import Avg
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import StudentRating
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_login(request):
    forms = UserLoginForm()
    if request.method == "POST":
        forms = UserLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data["username"]
            print(username,"**********")
            password = forms.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid User or Password")
                return redirect("login")

    context = {
        "forms": forms
    }
    return render(request, "accounts/login.html", context)

def user_logout(request):
    logout(request)
    return redirect("login")

def Student_login(request):
    if request.method=="POST":
        import pdb;pdb.set_trace()
        username = request.POST.get("username")
        print (username,"*******************")
    return render(request, "accounts/Student_profile.html")
def student_signup(request):
    return render(request,'accounts/student_signup.html')

from django.shortcuts import render
from .models import StudentRating, ManagerProfile

def manager_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        manager_profile = ManagerProfile.objects.filter(username=username).first()

        if manager_profile and manager_profile.password == password:
            # Calculate average rating for each teacher
            data = (
                StudentRating.objects.values('teacher')
                .annotate(avg_rating=Avg('rating'))
                .order_by('teacher')
            )
            # Pass the data to the template for rendering
            context = {'data': data}
            return render(request, 'accounts/managerhome.html', context)
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'accounts/manager_login.html', {'error_message': error_message})
    else:
        return render(request, 'accounts/manager_login.html')

def manager_view(request):
    return render(request,'accounts/manager_rating_view.html')
def Stu_data(request):
    #if request.method == 'POST':
        # firstname = request.POST.get('firstname')
        # lastname = request.POST.get('lastname')
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # instance = Student_profiles.objects.create(firstname=firstname, lastname=lastname,username=username,password=password)
        # return redirect('../student_login/')
    # else:
    #     return render(request, 'student_signup.html')
    if request.method == 'POST':
        username = request.POST.get('username')

        # Check if the username already exists in the model
        if Student_profiles.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
            return render(request, 'accounts/student_signup.html', {'error_message': error_message})
        else:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            username = request.POST.get('username')
            password = request.POST.get('password')
            Student_profiles.objects.create(firstname=firstname,lastname=lastname,username=username,password=password)
            return render(request, 'accounts/Student_profile.html')

def stu_rating(request):
    print("calling")

    if request.method == 'POST':
        teacher = request.POST.get('teacher')
        rating = request.POST.get('rating')
        stid = int([i for i in request.META.get('HTTP_REFERER').split("/") if i][-1])
        uname = Student_profiles.objects.get(id=stid).username
        print(uname)

        # Check if the user has already rated the teacher
        student_rating = StudentRating.objects.filter(username=uname, teacher=teacher).first()
        if student_rating:
            # If the rating already exists, update it
            student_rating.rating = rating
            student_rating.save()
            return HttpResponse("Your rating has been updated.")

        StudentRating.objects.create(teacher=teacher, rating=rating, username=uname)
        return redirect('../../accounts/teacherrating/{0}'.format(stid))
    else:
        return render(request, 'teachers/teachers_info.html')
#def student_rating(request):
    #ratings = StudentRating.objects.all()
    #return render(request, 'accounts/manager_rating_view.html', {'ratings': ratings})


def login_val(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print (username,"***********%%%%%%%%%%%%%%%%%")
        # Check if the user exists in the model

        #import pdb;pdb.set_trace()
        try:
            user = Student_profiles.objects.get(username=username)
        except Student_profiles.DoesNotExist:
            return render(request, 'Student_profile.html', {'error': 'Invalid username or password'})

        # Verify the password
        if user.password != password:
            return render(request, 'accounts/Student_profile.html', {'error': 'Invalid username or password'})

        # If the username and password match, redirect to another webpage
        return redirect('../../accounts/teacherrating/{0}'.format(user.id))#student_submit_rating
    else:
        return render(request, 'Student_profile.html')

def teach_rating(request,pk):
    st = Student_profiles.objects.get(id=pk)
    print (st.username)
    #import pdb;pdb.set_trace()
    teachers = TeacherInfo.objects.all()
    teachers = [i.name for i in teachers]
    print (teachers,type(teachers))


    return render(request, "teachers/teachers_info.html",{"data":teachers})


def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        # Check if the username exists
        user = User.objects.filter(username=username).first()
        if user is None:
            messages.error(request, 'No user found with this username')
            return redirect('/forgetpassword/')

        # Generate password reset token
        token_generator = default_token_generator
        token = token_generator.make_token(user)

        # Build password reset URL
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        password_reset_url = f"{current_site.domain}/resetpassword/{uid}/{token}/"

        # Send password reset email
        email_subject = 'Reset Your Password'
        email_body = render_to_string('accounts/reset_password_email.html', {
            'user': user,
            'reset_url': password_reset_url
        })
        email = EmailMessage(email_subject, email_body, to=[user.email])
        email.send()

        messages.success(request, 'Password reset instructions sent to your email')
        return redirect('/login/')

    return render(request, 'accounts/forget.html')

def managerhome(request):
    return render(request,"")


def show_teachers_rating(request):
    teachers = StudentRating.objects.values_list('teacher', flat=True).distinct()
    if request.method == "POST":
        option = request.POST.get("visualization")
        print (option,"f;hlewiuygiegyeiyeiy")
        if option == 'tabularform':
            data = (
                StudentRating.objects.values('teacher')
                .annotate(avg_rating=Avg('rating'))
                .order_by('teacher')
            )
            teacher_ratings = {entry['teacher']: entry['avg_rating'] for entry in data}

            average_ratings = [teacher_ratings[teacher] for teacher in teachers]
            print(average_ratings)
            # Pass the data to the template for rendering
            context = {'data': data,'teachers': teachers}

            return render(request, 'accounts/manager_rating_view.html',context)  # Render tabular.html template
        elif option == 'charts':
            teachers = StudentRating.objects.values_list('teacher', flat=True).distinct()
            data = (
                StudentRating.objects.values('teacher')
                .annotate(avg_rating=Avg('rating'))
                .order_by('teacher')
            )
            teacher_ratings = {entry['teacher']: entry['avg_rating'] for entry in data}

            average_ratings = [teacher_ratings[teacher] for teacher in teachers]
            charttype = "pieChart"
            teachers = teachers
            ratings = average_ratings
            print(teachers, average_ratings)
            context = {
                'charttype': charttype,
                'teachers': teachers,
                'average_ratings': average_ratings,
            }
            return render(request, 'accounts/charts.html',context)


def individual_rating(request, teacher):
    ratings = StudentRating.objects.filter(teacher=teacher)
    context = {
        'teacher': teacher,
        'ratings': ratings
    }
    return render(request, 'accounts/individual_rating.html', context)

def piechart(request):
    teachers = StudentRating.objects.values_list('teacher', flat=True).distinct()
    data = (
        StudentRating.objects.values('teacher')
        .annotate(avg_rating=Avg('rating'))
        .order_by('teacher')
    )
    teacher_ratings = {entry['teacher']: entry['avg_rating'] for entry in data}

    average_ratings = [teacher_ratings[teacher] for teacher in teachers]
    charttype = "pieChart"
    teachers = teachers
    ratings = average_ratings
    print(teachers, average_ratings)
    context = {
        'charttype': charttype,
        'teachers': teachers,
        'average_ratings': average_ratings,
    }
    return render(request, "charts.html", context)



def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        uploaded_file = UploadedFile(file=file)
        uploaded_file.save()
        return render(request, 'teachers/teachers_info.html')
    return render(request, '')

