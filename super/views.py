# super/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ChildForm, SuperuserLoginForm, Child
from register.models import Profile
from django.db.models import Q 
from .models import Child


def superuser_login_view(request):
    if request.method == 'POST':
        form = SuperuserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            print(f"\n--- Attempting to find user with email: {username} ---")

            try:
                # 1. Try to find the user directly by their username/email
                user = User.objects.get(username=username)
                print("--- SUCCESS: Found a user with that email. ---")

                # 2. Manually check if the provided password is correct for that user
                is_password_correct = user.check_password(password)
                print(f"--- Checking password... Is it correct? {is_password_correct} ---")

                if is_password_correct:
                    # 3. Check if the user is a superuser
                    print(f"--- Checking status... Is superuser? {user.is_superuser} ---")
                    if user.is_superuser:
                        print("--- SUCCESS: All checks passed. Logging in. ---")
                        # Manually log in the user since all checks passed
                        login(request, user)
                        return redirect('super_dashboard')
                    else:
                        messages.error(request, "This account does not have admin privileges.")
                else:
                    messages.error(request, "Invalid password provided.")

            except User.DoesNotExist:
                print("--- FAILED: No user found with that email address. ---")
                messages.error(request, "No account found with that email address.")
        else:
            messages.error(request, "The form had errors.")
    else:
        form = SuperuserLoginForm()
        
    return render(request, 'super/super_login.html', {'form': form})



# This decorator ensures only superusers can access this view
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def superuser_dashboard_view(request):
    search_query = request.GET.get('q', '')
    user_list = User.objects.filter(is_superuser=False).select_related('profile')

    if search_query:
        # Prepare to search by email (which is text)
        email_query = Q(email__icontains=search_query)
        
        # Prepare a placeholder for the phone number query
        phone_query = Q() 

        # Try to convert the search term to a number.
        # If it works, we'll search the phone number field for an exact match.
        try:
            phone_number_query = int(search_query)
            phone_query = Q(profile__phone_number=phone_number_query)
        except ValueError:
            # If the search term is not a number, we'll just ignore it for the phone search.
            pass

        # Combine the email and phone queries with an "OR"
        user_list = user_list.filter(email_query | phone_query).distinct()

    context = {
        'users': user_list,
        'search_query': search_query,
    }
    return render(request, 'super/super_dashboard.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def user_profile_view(request, user_id):
    user_to_view = get_object_or_404(User, pk=user_id)
    profile_to_view = get_object_or_404(Profile, user=user_to_view)
    
    # Get all children related to this user
    children_qs = Child.objects.filter(parent=user_to_view)
    
    # --- NEW LOGIC ---
    # Create a list that will hold each child along with their pre-filled update form
    children_with_forms = []
    for child in children_qs:
        children_with_forms.append({
            'child_data': child,
            'update_form': ChildForm(instance=child)
        })
    # --- END OF NEW LOGIC ---

    # This is for the blank "Add Child" modal
    add_child_form = ChildForm() 

    context = {
        'user_to_view': user_to_view,
        'profile': profile_to_view,
        # Pass the new, combined list to the template
        'children_with_forms': children_with_forms,
        # This is still needed for the 'Add' modal
        'add_child_form': add_child_form, 
    }
    return render(request, 'super/user_profile.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def add_child_view(request, user_id):
    parent = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = parent
            child.save()
            messages.success(request, f"Successfully added child for {parent.email}.")
        else:
            # This will flash a message if the form is invalid
            messages.error(request, "Failed to add child. Please check the data provided.")

    return redirect('user_profile', user_id=user_id)



# This new view will handle the logic for updating a child's info
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def update_child_view(request, child_id):
    # Get the specific child object we want to update
    child = get_object_or_404(Child, pk=child_id)
    # Get the parent's ID to redirect back to the correct profile page
    parent_user_id = child.parent.id

    if request.method == 'POST':
        # Pass the specific 'child' instance to the form to pre-fill it with existing data
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save() # Save the changes to the existing child object
            messages.success(request, f"Successfully updated details for {child.child_name}.")
        else:
            messages.error(request, "Failed to update child. Please check the data provided.")
    
    return redirect('user_profile', user_id=parent_user_id)



# Add this new view to handle the deletion
@user_passes_test(lambda u: u.is_superuser, login_url='super_login')
def delete_user_view(request, user_id):
    # We only allow deletion via POST request for security
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, pk=user_id)
        # We store the email to show in the success message after deletion
        email = user_to_delete.email
        # This one command deletes the user.
        # Because of 'on_delete=models.CASCADE' in our Child model,
        # all children related to this user will be automatically deleted too.
        user_to_delete.delete()
        messages.success(request, f"Successfully deleted user {email} and all their records.")
    
    # Redirect back to the admin dashboard in all cases
    return redirect('super_dashboard')