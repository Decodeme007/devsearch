from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
# block view for user (decorator)
from django.contrib.auth.decorators import login_required
# utils for search
from .utils import searchProjects, paginationProjects
# flash message
from django.contrib import messages


# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginationProjects(request, projects, 6)

    context = {'projects': projects, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'project/project.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        # update project vote count
        projectObj.getVoteCount

        messages.success(request, 'Your review is successfully added')
        return redirect('project', pk=projectObj.id)

    return render(request, 'project/single-project.html', {'project': projectObj, 'form': form})


@login_required(login_url="login")  # shows only after login
def createProject(request):
    profile = request.user.profile  # so project get associated to profile
    form = ProjectForm()
    if request.method == 'POST':
        # request.FILES for sending files too
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():  # is_valid() checks it's not suspicious
            project = form.save(commit=False)  # create the object
            project.owner = profile  # one to many
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')  # here we can just pass url names

    context = {'form': form}
    return render(request, "project/project_form.html", context)


@login_required(login_url="login")  # shows only after login
def updateProject(request, pk):
    profile = request.user.profile  # so only login authorised user can update
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)  # prefilled form

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():  # is_valid() checks it's not suspicious
            project = form.save()  # create the object
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')  # here we can just pass url names

    context = {'form': form, 'project':project}
    return render(request, "project/project_form.html", context)


@login_required(login_url="login")  # shows only after login
def deleteProject(request, pk):
    profile = request.user.profile  # so only login authorised user can delete
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'delete_template.html', context)
