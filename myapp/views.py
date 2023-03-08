from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import myapp.models 
import requests
import json
from requests.exceptions import MissingSchema
# Create your views here.
def index(request):
    logout(request)
    if "tasks" not in request.session:
        request.session['tasks'] = []
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return HttpResponseRedirect(reverse('index'))
def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)
        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        # Otherwise, return login page again with new context
        else:
            return render(request, "myapp/login.html", {
                "message": "Invalid Credentials"
            })
        
    return render(request, "myapp/login.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first_name = request.POST["f_name"]
        last_name = request.POST["l_name"]
        if User.objects.create_user(username, email, password, first_name, last_name):
         return HttpResponseRedirect(reverse("login"))
        else:
            #exception to be handled
            return HttpResponse('user already existed')


    return render(request, "myapp/signup.html")


def home(request):
    return render(request, "myapp/home.html") 
def contest(request):
    return render(request, "myapp/contest.html") 
def quiz(request):
    return render(request, "myapp/quiz.html") 
def questions(request, lang):
    return render(request, "myapp/"+lang+".html")

def profile(request):
    return render(request, "myapp/profile.html")
def logout_view(request):
    logout(request)
    return render(request, "myapp/login.html", {
                "message": "Logged Out Successful"
            })

def problem(request, problem_id):
    problem = myapp.models.Problem.objects.get(id=problem_id)
    return render(request, "myapp/problem.html",{
        "problem":problem
    })
CODE_EVALUATION_URL = u'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'
CLIENT_SECRET = '88836b92d51b182929912d4f63b015a4f5928d2a'
callback = 'http://127.0.0.1:8000/myapp/code/1'
def code(request, problem_id):
    if request.method == 'POST':
        user_code = request.POST["code"]
        lang = request.POST["lang"]
        input = myapp.models.Problem.objects.get(id=problem_id).testin
        actual_output = myapp.models.Problem.objects.get(id=problem_id).testout.split('\r')
        output = ''
        u_output = ''
        status = ''
        data = {
                'source':user_code,
                'lang':lang,
                'time_limit': 5,
                'memory_limit': 246323,
                'input':input,
                'callback' : callback,
                'id': "client-001"
            }
        headers = {"client-secret":CLIENT_SECRET}
        resp1 = requests.post(CODE_EVALUATION_URL, json=data, headers=headers)
        dict1 = json.loads(resp1.text)
        status_update_url = dict1['status_update_url']
        resp2 = requests.get(status_update_url, headers=headers)
        dict2 = json.loads(resp2.text)
        while(dict2['result']['compile_status'] == None): #and dict2['result']['compile_status'] == 'OK'):
            resp2 = requests.get(status_update_url, headers=headers)
            dict2 = json.loads(resp2.text)
        if dict2['result']['compile_status'] != 'OK' :
            output = dict2['result']['compile_status']
        else:
            while(dict2['result']['run_status']['output'] == None): #and dict2['result']['compile_status'] == 'OK'):
                resp2 = requests.get(status_update_url, headers=headers)
                dict2 = json.loads(resp2.text)
            resp3 = requests.get(dict2['result']['run_status']['output'], headers={'content-type':'text/plain'})
            output = resp3.text
            u_output = resp3.text.split('\n')
            u_output.pop()#To eliminate the empty character
            actual_output = [i.replace('\n','') for i in actual_output]
            status = 'some of the test cases failed'
            # status evalution
            if dict2['result']['run_status']['status'] != 'AC':
                output = '{} Error Occured'.format(dict2['result']['run_status']['status'])
            elif len(actual_output) == len(u_output) and actual_output == u_output: #test case checking
                status = 'success'
        return render(request, 'myapp/code.html',{
            'actual_output':actual_output, 'user_output' : output,'problem_id':problem_id,'status': status
        } )
    return render(request,"myapp/code.html",{
        "problem_id":problem_id
    }) 


