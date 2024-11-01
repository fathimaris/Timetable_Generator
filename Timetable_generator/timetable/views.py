import random
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from timetable.forms import course_form, subject_form, staff_form, CourseSelectionForm
from timetable.models import Course, Subject, Staff, Course



def Mainpage(request):
    return render(request,'Home.html')

def Homepage(request):
    return render(request,'Home.html')

def Courses(request):
    data = Course.objects.all()
    return render(request, 'Courses.html',{'data':data})
def create_course(request):
    form=course_form()
    if request.method=='POST':
        form=course_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Courses')
    return render(request,'create_course.html',{'form':form})



def update_course(request,id):
    data=Course.objects.get(id=id)
    form=course_form(instance=data)
    if request.method=='POST':
        form=course_form(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('Courses')
    return render(request,'update_course.html',{'form':form})

def delete_course(request,id):
    data=Course.objects.get(id=id)
    data.delete()
    return redirect('Courses')

def Subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'Subjects.html', {'data': subjects})

def create_subject(request):
    form=subject_form()
    if request.method=='POST':
        form=subject_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Subjects')
    courses = Course.objects.all()
    return render(request,'create_subject.html',{'form': form, 'courses': courses})

def update_subject(request,id):
    data=Subject.objects.get(id=id)
    form=subject_form(instance=data)
    if request.method=='POST':
        form=subject_form(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('Subjects')
    courses = Course.objects.all()
    return render(request,'update_subject.html',{'form': form, 'courses': courses})

def delete_subject(request,id):
    data=Subject.objects.get(id=id)
    data.delete()
    return redirect('Subjects')

def Staffs(request):
    staff_members = Staff.objects.prefetch_related('subjects').all()
    return render(request, 'Staff.html', {'staff_members': staff_members})

def create_staff(request):
    form=staff_form()
    if request.method=='POST':
        form=staff_form(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.save()
            form.save_m2m()
            return redirect('Staffs')
    subjects = Subject.objects.all()
    return render(request,'create_staff.html',{'form': form})




def update_staff(request, id):
    staff_member = get_object_or_404(Staff, id=id)
    form = staff_form(instance=staff_member)

    if request.method == 'POST':
        form = staff_form(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            return redirect('Staffs')

    return render(request, 'update_staff.html', {'form': form})


def delete_staff(request, id):
    staff_member = get_object_or_404(Staff, id=id)
    staff_member.delete()
    return redirect('Staffs')

def generate_timetable(request):
    timetable_data = {}
    form = CourseSelectionForm()

    if request.method == 'POST':
        if 'generate' in request.POST:
            selected_courses = request.POST.getlist('courses')
            staff_availability = {
                'Monday': [set() for _ in range(4)],
                'Tuesday': [set() for _ in range(4)],
                'Wednesday': [set() for _ in range(4)],
                'Thursday': [set() for _ in range(4)],
                'Friday': [set() for _ in range(4)],
            }

            for course_id in selected_courses:
                course = get_object_or_404(Course, id=course_id)
                subjects = course.subjects.all()

                timetable = {
                    'Monday': [None] * 4,
                    'Tuesday': [None] * 4,
                    'Wednesday': [None] * 4,
                    'Thursday': [None] * 4,
                    'Friday': [None] * 4,
                }

                for day in timetable.keys():
                    for period in range(4):
                        available_subjects = [
                            subject for subject in subjects
                            if not staff_availability[day][period].intersection(subject.staff.all())
                        ]
                        subject = random.choice(available_subjects) if available_subjects else None

                        if subject:
                            staff_member = random.choice(subject.staff.all())
                            timetable[day][period] = (subject, staff_member)
                            staff_availability[day][period].add(staff_member)
                        else:
                            timetable[day][period] = ('NIL', 'NIL')

                timetable_data[course.name] = timetable

        elif 'save_changes' in request.POST:

            for key, value in request.POST.items():
                if key.startswith('subject_staff_'):

                    parts = key.split('_')
                    course_name = parts[2]
                    day = parts[3]
                    period_index = int(parts[4])

                    subject_staff = value.split(' (')
                    if len(subject_staff) == 2:
                        subject_name = subject_staff[0]
                        staff_name = subject_staff[1].rstrip(')')


    return render(request, 'generate_timetable.html', {'form': form, 'timetable_data': timetable_data})
