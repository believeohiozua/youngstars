from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import (
    Story,
    Mcq,
    Profile
)
# Landing Page On authenticztion (DASHBOARD)


@login_required
def Index(request):
    context = {
        'stories': Story.objects.filter(publish=True)
    }
    return render(request, 'index.html', context)


@login_required
def StoryPage(request):
    profile = Profile.objects.get(user=request.user)  # Get Current Profile
    title = request.POST.get('title')
    if title:
        request.session['title'] = Story.objects.get(title=title).title
        context = {'story': Story.objects.get(
            title=title).story}  # Get Story 1
        if not profile.assessed:
            return render(request, 'story.html', context)
    else:
        return HttpResponse("<h1 style='color:red; text-align: center'>You are Not Authorized to view this Page!</h1>")


@login_required
def Questions(request):
    context = {'questions': Mcq.objects.filter(
        story__title__contains=request.session.get('title'))}
    profile = Profile.objects.get(user=request.user)
    done = request.POST.get("done")
    flag = request.POST.get("flag")  # Check for Mal-practise
    if done and not profile.assessed:
        profile.total_points = int(done) * 10  # Total score
        profile.assessed = True
        if flag:
            profile.malpractise = True
        profile.save()
        return redirect("/")
    profile = Profile.objects.get(user=request.user)
    if not profile.assessed:
        return render(request, 'questions.html', context)
    else:
        return HttpResponse("<h1 style='color:red; text-align: center'>You are Not Authorized to view this Page!</h1>")
