# dashboard/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from register.models import Profile
from super.models import Child

# This decorator ensures only logged-in users can see this page.
@login_required
def dashboard_view(request):
    # Get the profile and children for the currently logged-in user.
    # We use request.user to get the user object.
    profile = get_object_or_404(Profile, user=request.user)
    children = Child.objects.filter(parent=request.user)

    context = {
        'user': request.user,
        'profile': profile,
        'children': children,
    }
    return render(request, 'dashboard/dashboard.html', context)