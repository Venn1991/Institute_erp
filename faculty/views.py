from django.shortcuts import render, HttpResponse, redirect
from accounts.models import Faculty, ClassCourse, Attendance, Marks
from .forms import Classcourseform
from django.http import HttpResponseRedirect
from django.db import connection
import json
from django.contrib.auth.decorators import login_required

# Create your views here.

studentid= ""
year= 0
sem= 0
attendance_visited=0
marks_visited=0

@login_required
def faculty_home(request):

    current_user = request.user
    current_faculty = Faculty.objects.get(facultyid=current_user.id)

    # return render(request,"student_home.html")
    return render(request, "faculty_home.html", {"current_faculty": current_faculty})


@login_required
def faculty_course(request):
    current_user = request.user
    current_faculty = Faculty.objects.get(facultyid=current_user.id)

    if request.method == "POST":
        form = Classcourseform(request.POST)
        if form.is_valid():
            year = form.cleaned_data["ac_year"]
            sem = form.cleaned_data["semester"]

            result = (
                ClassCourse.objects.filter(facultyid=current_user.id)
                .values("courseid")
                .distinct()
            )

            args = {
                "form": form,
                "year": year,
                "sem": sem,
                "result": result,
                "current_faculty": current_faculty,
            }

            return render(request, "faculty_course.html", args)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Classcourseform()
        return render(
            request,
            "faculty_course.html",
            {"form": form, "current_faculty": current_faculty},
        )


@login_required
def faculty_attendance(request):
    current_user = request.user
    current_faculty = Faculty.objects.get(facultyid=current_user.id)

    global studentid,year,sem,attendance_visited

    if request.method == "POST" and attendance_visited==0:

        attendance_visited=1

        studentid=json.loads(request.POST['studentid'])
        year=json.loads(request.POST['year'])
        sem=json.loads(request.POST['semester'])

        return HttpResponse("Successfully Sent !")
    # if a GET (or any other method) we'll create a blank form
    elif request.method=='GET' and attendance_visited==1:

        cursor = connection.cursor()
        cursor.execute(
            "call view_students_attendance_by_faculty(%s,%s,%s,%s);",
            [studentid, current_user.id, year, sem],
        )
        result = cursor.fetchall()
        args = {
            "result": result,
            'studentid':studentid,
            "current_faculty": current_faculty,
        }
        attendance_visited=0
        return render(request,"faculty_attendance.html",args)

    else:
        return redirect('/faculty/all_attendance')




@login_required
def faculty_attendance_update(request):

    data = request.POST["updates"]
    python_data = json.loads(data)

    print(python_data)
    if python_data is not None:
        print("Data received")

        for key, value in python_data.items():
            attendance_obj = Attendance.objects.get(attendanceid=key)
            attendance_obj.attended = value
            attendance_obj.save()

    return HttpResponse("Successfully Updated!")


@login_required
def faculty_all_attendance(request):
    current_user = request.user
    current_faculty = Faculty.objects.get(facultyid=current_user.id)

    if request.method == "POST":
        form = Classcourseform(request.POST)
        if form.is_valid():
            year = form.cleaned_data["ac_year"]
            sem = form.cleaned_data["semester"]

            cursor = connection.cursor()
            cursor.execute(
                "call view_all_students_attendance_by_faculty(%s,%s,%s);",
                [current_user.id, year, sem],
            )
            result = cursor.fetchall()

            args = {"form": form, "result": result, "current_faculty": current_faculty,'ac_year':year,'semester':sem}

            return render(request, "faculty_all_attendance.html", args)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Classcourseform()
        return render(
            request,"faculty_all_attendance.html",{"form": form, "current_faculty": current_faculty})


@login_required
def faculty_marks(request):

    current_user = request.user
    current_faculty = Faculty.objects.get(facultyid=current_user.id)

    global studentid,year,sem,marks_visited

    if request.method == "POST" and marks_visited==0:
        marks_visited=1

        studentid=json.loads(request.POST['studentid'])
        year=json.loads(request.POST['year'])
        sem=json.loads(request.POST['semester'])

        return HttpResponse("Successfully Sent !")

    elif request.method=="GET" and marks_visited==1:
            cursor = connection.cursor()
            cursor.execute(
                "call view_students_marks_by_faculty(%s,%s,%s,%s);",
                [studentid, current_user.id, year, sem],
            )
            result = cursor.fetchall()

            args = {
                "studentid": studentid,
                "current_faculty": current_faculty,
                "result": result,
            }

            return render(request, "faculty_marks.html", args)

    else:
        return redirect('/faculty/all_marks')


@login_required
def faculty_marks_update(request):

    data = request.POST.get("updates")
    python_data = json.loads(data)

    print(python_data)
    if python_data is not None:
        print("Data received")

        for key, value in python_data.items():
            marks_obj = Marks.objects.get(marksid=key)
            marks_obj.obtained = value
            marks_obj.save()

    return HttpResponse("Successfully Updated!")


@login_required
def faculty_all_marks(request):
    current_user = request.user
    current_faculty = Faculty.objects.get(facultyid=current_user.id)

    if request.method == "POST":
        form = Classcourseform(request.POST)
        if form.is_valid():
            year = form.cleaned_data["ac_year"]
            sem = form.cleaned_data["semester"]

            cursor = connection.cursor()
            cursor.execute(
                "call view_all_students_marks_by_faculty(%s,%s,%s);",
                [current_user.id, year, sem],
            )
            result = cursor.fetchall()

            args = {"form": form, "result": result, "current_faculty": current_faculty,"year":year,"sem":sem}

            return render(request, "faculty_all_marks.html", args)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Classcourseform()
        return render(
            request,
            "faculty_all_marks.html",
            {"form": form, "current_faculty": current_faculty},
        )


@login_required
def faculty_all_marks_update(request):

    data = request.POST.get("updates")
    python_data = json.loads(data)

    print(python_data)
    if python_data is not None:
        print("Data received")

        for key, value in python_data.items():
            marks_obj = Marks.objects.get(marksid=key)
            marks_obj.obtained = value
            marks_obj.save()

    return HttpResponse("Successfully Updated!")


@login_required
def faculty_timetable(request):

    current_user = request.user
    current_faculty = Faculty.objects.get(facultyid=current_user.id)

    cursor = connection.cursor()
    cursor.execute(
        "call view_timetable_faculty(%s);", [current_user.id]
    )
    result = cursor.fetchall()

    args = { "result": result, "current_faculty": current_faculty}

    return render(request, "faculty_timetable.html", args)