from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from courses.models import Course
from history.forms import DateRangeForm
from timer.models import TimeInterval


@login_required
def index(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            request.session.__setitem__('start_date', form.cleaned_data['start_date'])
            request.session.__setitem__('end_date', form.cleaned_data['end_date'])
            return display_history(request)
        else:
            return render(request, 'history/index.html', {'date_form': form})
    else:
        return render(request, 'history/index.html', {'date_form': DateRangeForm()})


@login_required
def display_history(request):
    """Display work done in the given time period in comparison with user-defined time goals."""
    # We have to process the dates, which were converted to strings when entered into session
    start_date, end_date = request.session.__getitem__('start_date'), request.session.__getitem__('end_date')
    if start_date is None or end_date is None:  # ensure we can't access the page without having defined a date range
        return redirect('/history')
    start_date, end_date = timezone.datetime.strptime(start_date, '%m-%d-%Y'), \
                           timezone.datetime.strptime(end_date, '%m-%d-%Y')
    start_date = start_date.replace(tzinfo=timezone.get_current_timezone())
    end_date = end_date.replace(tzinfo=timezone.get_current_timezone())

    # Don't include a course that wasn't active for any of the given date range
    tallies = dict.fromkeys(Course.objects.filter(Q(user=request.user), Q(creation_time__lte=end_date),
                                                  Q(deactivation_time__isnull=True) | Q(deactivation_time__gte=start_date)), 0)
    for course in tallies.keys():  # multiply by how many weeks passed while course existed and was activated
        start, end = max(start_date, course.creation_time), \
                     end_date if course.activated else min(end_date, course.deactivation_time)
        course.total_target_hours = course.hours * (end - start).total_seconds() / 604800.0  # convert to weeks

    for interval in TimeInterval.objects.filter(course__user=request.user, start_time__gte=start_date,
                                                end_time__lte=end_date):
        tallies[interval.course] += (interval.end_time - interval.start_time).total_seconds() / 3600  # convert to hours

    return render(request, 'history/display.html', {'tallies': sorted(tallies.items(), key=lambda x: x[0].name),
                                                    'start_date': start_date, 'end_date': end_date})