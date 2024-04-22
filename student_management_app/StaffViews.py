import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from student_management_app.models import Subjects, SessionYearModel, Students


def staff_home(request):
    return render(request, "staff_template/staff_home_template.html")


def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_take_attendance.html",{"subjects":subjects, "session_years":session_years})
@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)
    list_data = []

    for student in students:
        data_small = {"id": student.admin.id, "name": student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
