from django.shortcuts import render_to_response
import json
import urllib.request
api_key = "&api_key=wuH4hRXxyQgUVH9NBEPbd4RARpKyMMIg7wXq9dC5"

fields = """&_fields=id,school.name,latest.admissions.act_scores.midpoint.cumulative,latest.admissions.admission_rate.overall,latest.completion.completion_rate_4yr_150nt,school.city,latest.cost.tuition.in_state,latest.student.size,latest.admissions.sat_scores.midpoint.math,latest.admissions.sat_scores.midpoint.critical_reading,latest.admissions.admission_rate.overall,latest.admissions.sat_scores.average.overall,latest.student.enrollment.all"""

def home(request):
    if request.GET.get('school.name'): #Check if there are tags
        print(fields)
        schoolname = request.GET.get('school.name')
        schoolstate = request.GET.get('school.state')
        usermath = request.GET.get('satmath')
        userreading = request.GET.get('satreading')
        youract = request.GET.get('act')

        completedurl = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.name=" + schoolname + "&school.state=" + schoolstate + fields + api_key
        print(completedurl)
        response = urllib.request.urlopen(completedurl)
        parsedjson = json.loads(response.read().decode())
        criticalreading = parsedjson['results'][0]['latest.admissions.sat_scores.midpoint.critical_reading']
        math = parsedjson['results'][0]['latest.admissions.sat_scores.midpoint.math']
        combinedtheirsat = int(criticalreading) + int(math)
        combinedyoursat = int(usermath) + int(userreading)
        population = parsedjson['results'][0]['latest.student.enrollment.all']
        schoolcity = parsedjson['results'][0]['school.city']
        schoolnamerefiner = parsedjson['results'][0]['school.name']
        tuition = parsedjson['results'][0]['latest.cost.tuition.in_state']
        graduationrate = parsedjson['results'][0]['latest.completion.completion_rate_4yr_150nt']*100
        admissionrate = parsedjson['results'][0]['latest.admissions.admission_rate.overall']*100
        theiract = parsedjson['results'][0]['latest.admissions.act_scores.midpoint.cumulative']
        return render_to_response(template_name="home.html", context={
            "mathsat": math, "state": schoolstate, "criticalreading": criticalreading, "usermath": usermath, "userreading": userreading, "combinedsat": combinedtheirsat, "combinedyoursat": combinedyoursat,
            "studentsize": population, "city": schoolcity, "name": schoolnamerefiner, "tuition": tuition, "graduationrate": graduationrate, "admissionrate": admissionrate, "theiract": theiract, "youract": youract
        })
    else:
        return render_to_response(template_name="home.html")

