from django.shortcuts import render, HttpResponse

# Create your views here.
# function based view
def home(request):

    name = "Traker"
    args = {'name': name}
    return render(request, 'account/home.html', args)

def login(request):

    return render(request, 'account/login.html')

def startTimer(request):
    # TODO named tuple?
    self.new_interval = Interval(course=course_id, start_time=time.time())  # some data structure for interval

def endTimer(request):
    self.new_interval.end_time = time.time()
    # TODO send to sql
    self.new_interval = None