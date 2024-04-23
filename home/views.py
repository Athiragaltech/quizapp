from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from .forms import CourseForm
from django.shortcuts import render, get_object_or_404
from .models import Course
from django.core.paginator import Paginator
from .forms import QuizForm
from .forms import QuizQuestionForm
from .forms import QuizChoiceForm
from .models import QuizQuestion
from .models import Quiz, QuizQuestion
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from .models import QuizQuestion, QuizChoice
from django.http import HttpResponse
from .models import QuizChoice


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Send email notification
                send_login_email(user)
                if user.is_superuser:
                    return redirect('admin_index')  # Redirect to admin_index if user is superuser
                else:
                    return redirect('index')  # Redirect to index if user is not superuser
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def index(request):
    courses = Course.objects.all()
    return render(request, 'index.html', {'courses': courses})

def send_login_email(user):
    subject = 'Welcome to our platform!'
    message = render_to_string('welcome.html', {'user': user})  # Render the welcome email template
    from_email = 'athiranass@gmail.com'  # Change this to your email
    to_email = [user.email]  # Assuming user has an email field
    email = EmailMessage(subject, message, from_email, to_email)
    email.content_subtype = "html"  # Ensure that the email content type is HTML
    email.send()
def admin_index(request):
    # Your admin index view logic here
    return render(request, 'admin_index.html')
def custom_logout(request):
  
    return redirect('index')
def courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_index')  
    else:
        form = CourseForm()
    return render(request, 'courses.html', {'form': form})

def course_view(request):
   
    courses = Course.objects.all()
    return render(request, 'course_view.html', {'courses': courses})
 

def delete(request,id):
    dlt=Course.objects.get(id=id)
    dlt.delete()
    return redirect('admin_index') 
def edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    data = {
        "data": course
    }
    return render(request, 'edit.html', data)


def update(request, id):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course_price = request.POST.get('course_price')
        course_offer_price = request.POST.get('course_offer_price')
        course_description = request.POST.get('course_description')
        course_type = request.POST.get('course_type')
        course_status = request.POST.get('course_status')
        
        # Fetch the Course object from the database
        edit = Course.objects.get(id=id)
        
        # Check if a new image file was uploaded and update the thumbnail accordingly
        if 'img' in request.FILES:
            edit.thumbnail = request.FILES['img']
        
        # Update other fields of the Course object
        edit.course_name = course_name
        edit.course_price = course_price
        edit.course_offer_price = course_offer_price
        edit.course_description = course_description
        edit.course_type = course_type
        edit.course_status = course_status
               
        # Save the updated Course object
        edit.save()
        
        # Redirect to a specific URL after updating (e.g., admin index)
        return redirect('admin_index')
    
    # If the request method is not POST, render the same page
    return render(request, 'edit.html')

def course_userside(request):
    # Retrieve all courses
    all_courses = Course.objects.all()
    
    # Paginate the courses with 10 courses per page
    paginator = Paginator(all_courses, 10)
    
    # Get the page number from the request's query parameters
    page_number = request.GET.get('page')
    
    # Get the courses for the requested page
    courses = paginator.get_page(page_number)
    
    # Render the template with paginated courses
    return render(request, 'course_userside.html', {'courses': courses})  
def logout(request):
      return render(request, 'courses/index.html')
  

def viewmore(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        'course': course
    }
    return render(request, 'view_more1.html', context)
def viewmore1(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        'course': course
    }
    return render(request, 'view_more2.html', context)
def viewmore2(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        'course': course
    }
    return render(request, 'view_more2.html', context)



def admin_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return redirect('admin_index')  # Redirect to quiz detail page
    else:
        form = QuizForm()
    return render(request, 'admin_quiz.html', {'form': form})

def create_quizq(request):
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_index')  # Redirect to the view showing list of quiz questions
    else:
        form = QuizQuestionForm()
    return render(request, 'create_quizq.html', {'form': form})

def create_quiz_choice(request):
    if request.method == 'POST':
        form = QuizChoiceForm(request.POST)
        if form.is_valid():
            # Associate the QuizChoice with the selected QuizQuestion
            question_id = request.POST.get('question')  # Get the selected QuizQuestion ID from the form
            question = QuizQuestion.objects.get(pk=question_id)  # Retrieve the QuizQuestion object using the ID
            form.instance.question = question  # Associate the QuizChoice with the selected QuizQuestion
            form.save()
            return redirect('admin_index')  # Redirect to the view showing list of quiz choices
    else:
        form = QuizChoiceForm()
    return render(request, 'create_quiz_choice.html', {'form': form})


    
def quiz(request):
    # Filter questions based on the selected quiz title (in this case, 'ASP questions')
    questions = QuizQuestion.objects.filter(quiz__quiz_title='ASP question').prefetch_related('choices')

    return render(request, 'quizz.html', {'questions': questions})


def quiz1(request):
    # Filter questions based on the selected quiz title (in this case, 'Django questions')
    questions = QuizQuestion.objects.filter(quiz__quiz_title='ASP question').prefetch_related('choices')
    
    if request.method == 'POST':
        total_score = 0
        for question_id, choice_id in request.POST.items():
            if question_id.startswith('question'):
                # Extract numeric part of the question_id
                question_number = question_id.replace('question_', '')
                # Ensure it's a valid integer
                try:
                    question_id = int(question_number)
                except ValueError:
                    # Handle the case where question_id is not a valid integer
                    return HttpResponse("Invalid question ID")
                
                selected_choice = QuizChoice.objects.get(pk=int(choice_id))
                if selected_choice.is_correct:
                    total_score += selected_choice.question.points
        
        return render(request, 'quizz.html', {'questions': questions, 'Score': total_score})
    
    else:
        return render(request,"quizz.html",{"questions":questions})

    
   
def quiz2(request):
    # Filter questions based on the selected quiz title (in this case, 'PHP')
    questions = QuizQuestion.objects.filter(quiz__quiz_title='Php questions').prefetch_related('choices')

    return render(request, 'quizz.html', {'questions': questions})


def grade_quiz(request):
    if request.method == 'POST':
        total_score = 0
        for question_id, choice_id in request.POST.items():
            if question_id.startswith('question'):
                # Extract numeric part of the question_id
                question_number = question_id.replace('question_', '')
                # Ensure it's a valid integer
                try:
                    question_id = int(question_number)
                except ValueError:
                    # Handle the case where question_id is not a valid integer
                    return HttpResponse("Invalid question ID")
                
                selected_choice = QuizChoice.objects.get(pk=int(choice_id))
                if selected_choice.is_correct:
                    total_score += selected_choice.question.points
        
                return render(request, 'quizz.html', {'Score': total_score})
    else:
        return HttpResponse("Method not allowed")



