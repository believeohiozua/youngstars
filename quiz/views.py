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
    return render(request, 'index.html')

# Story Page


@login_required
def StoryPage(request):
    profile = Profile.objects.get(user=request.user)  # Get Current Profile
    story = {'story': Story.objects.get(pk=1).story}  # Get Story 1
    if not profile.assessed:
        return render(request, 'story.html', story)
    else:
        return HttpResponse("<h1 style='color:red; text-align: center'>You are Not Eligible to view this Page Again</h1>")


@login_required
def Questions(request):
    questions = {'questions': Mcq.objects.all(), }
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
        return render(request, 'questions.html', questions)
    else:
        return HttpResponse("<h1 style='color:red; text-align: center'>You are Not Eligible to view this Page Again</h1>")
