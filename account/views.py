from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
from actions.utils import create_action
from actions.models import Action

@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile') \
    .prefetch_related('target')[:10]

    return render(request,
                'account/dashboard.html',
                {'section':'dashboard',
                'actions':actions})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()  # save new user to the database.
            # create profile for new user
            Profile.objects.create(user=new_user)
            create_action(request.user, 'has created an account')
            return render(request,
                        'account/register_done.html',
                        {'new_user':new_user})
    else:
        form = UserRegistrationForm()
    return render(request,
                'account/register.html',
                {'form':form})

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,
                                                files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Error updating your profile.')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                'account/edit.html',
                {'user_form':user_form,
                'profile_form':profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)  # retrieve all active users
    return render(request,
            'account/user/list.html',
            {'users':users,
            'section':'people'})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request,
            'account/user/detail.html',
            {'user':user,
            'section':'people'})

@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status":"ok"})
        except:
            return JsonResponse({"status":"ko"})
    return JsonResponse({"status":"ko"})
        
