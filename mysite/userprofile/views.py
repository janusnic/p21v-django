from django.shortcuts import get_object_or_404, render
from .forms import RegistrationForm, UserProfileForm, EditProfileForm

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from .models import UserProfile

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both RegistrationForm and UserProfileForm.
        user_form = RegistrationForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = RegistrationForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'userprofile/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the email and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the email/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
            # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('%s'%(reverse('userprofile:profile')))
                # return HttpResponseRedirect('/blog/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your User account is disabled.")
        else:
       # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        # return render(request, 'blog/login.html', {})
        # return render(request, 'blog/index.html', {})
        return render(request, 'blog/index.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/blog/')

@login_required
def profile_view(request):
    user = request.user
    
    context = {
        'first_name':user.first_name, 'last_name':user.last_name
    }
    return render(request, 'userprofile/profile.html', context)

@login_required
def edit_profile(request):

    user = request.user
    
    form = EditProfileForm(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name})
    #profileform = UserProfileForm(instance=UserProfile.objects.get(user=user))

    user_profile = request.user.profile
    if request.method == 'POST':
        profileform = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid() and profileform.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            profileform.save()
            return HttpResponseRedirect('%s'%(reverse('userprofile:profile')))
    else:
        profileform = UserProfileForm(instance=user_profile)
    
    context = {
        "edit_form": form, "profileform":profileform
    }

    return render(request, "userprofile/edit_profile.html", context)