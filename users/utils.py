from .models import Profile, Skill
#extends filter
from django.db.models import Q
#for pagination importing paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginationProfiles(request, profiles, results):
    #pagination
    page = request.GET.get('page')

    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    leftIndex = (int(page) - 4)
    
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)
    return custom_range, profiles



def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'): #if we have anything to search
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query) #name__iexact=search_query if query matches perfectly #search by skill

    profiles = Profile.objects.distinct().filter( #distinct() otherwise duplicates appear
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
        ) #name__icontains so not case sensetive #& and | or

    return profiles, search_query
