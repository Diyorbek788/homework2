from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404

from .forms import UserForm
from app_users.forms import StudentForm
from app_users.models import Hobby, Student
from django.shortcuts import render




User = get_user_model()


def home_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    full_name = request.user.get_full_name()
    context = {
        "full_name": full_name,
    }

    return render(request, 'app_main/home.html', context)


def teachers(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')

    teachers_list = User.objects.all()

    context = {
        'teachers': teachers_list
    }

    return render(request, 'app_main/teachers.html', context)


def teacher_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            if request.POST.get('password1') == request.POST.get('password2'):
                user = form.save(commit=False)
                user.set_password(request.POST.get('password1'))
                user.save()
                return redirect('teachers')

    form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'app_main/teacher_form.html', context)


def teacher_detail(request, id):
    teacher = get_object_or_404(User, id=id)
    context = {
        'teacher': teacher
    }
    return render(request, 'app_main/teacher.html', context)


def teacher_update(request, id):
    teacher = get_object_or_404(User, id=id)

    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.username = request.POST.get('username')
        teacher.email = request.POST.get('email')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password2:
            if password1 == password2:
                teacher.set_password(password2)

        teacher.save()
        return redirect('teachers')

    context = {
        'teacher': teacher
    }
    return render(request, 'app_main/teacher_form.html', context)


def teacher_delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('teachers')


def students_list(request, id):
    teacher = get_object_or_404(User, id=id)
    students = teacher.student_set.all()

    context = {
        'students': students,
        'teacher': teacher,
    }
    return render(request, 'app_main/students.html', context)


def student_create(request, teacher_id):
    if request.method == 'POST':
        teacher = get_object_or_404(User, id=teacher_id)
        form = StudentForm(request.POST)
        
        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = teacher
            student.save()
            
            hobbies_list = request.POST.getlist('hobbies')  # Multiple hobbies are sent as a list
            for hobby_id in hobbies_list:
                hobby = get_object_or_404(Hobby, id=hobby_id)
                student.hobbies.add(hobby)  # Add each selected hobby to the student

            return redirect('teacher_students', id=teacher_id)
    else:
        form = StudentForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'app_main/new_student.html', context)

def filtered_students(request):
    if request.method == 'POST':
        hobby_id = request.POST.get('hobby_id')  
        hobby = get_object_or_404(Hobby, id=hobby_id)
        filtered_students = Student.objects.filter(hobbies=hobby)
    else:
        filtered_students = Student.objects.all()  

    context = {
        'filtered_students': filtered_students
    }

    return render(request, 'filtered_students.html', context)