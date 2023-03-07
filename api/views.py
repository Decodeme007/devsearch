# take any py data and convert to json
# from django.http import JsonResponse
# rest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
#
from rest_framework.response import Response
#
from .serializers import ProjectSerializer
from project.models import Project, Review, Tag


@api_view(['GET'])
def getRouters(request):

    routes = [
        # turn into javascript
        {'GET': '/api/projects'},  # return list of project objects
        {'GET': '/api/projects/id'},  # return single project
        {'POST': '/api/projects/id/vote'},

        # get token built in routes
        # json web token have expiretion time like 5 mins
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},  # for stayed login
    ]

    # safe= False turn any kind of data in json(javascript object notation)
    # return JsonResponse(routes, safe=False)
    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # restriction like login required
def getProjects(request):
    # print('USER', request.user)
    projects = Project.objects.all()
    # takes project and convert in json
    # for single object to convert or not many=T
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # takes project and convert in json
    # for single object to convert or not many=T
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


# modify project vote
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile  # request - coming from token not session
    data = request.data  # rest framework

    # print('DATA', data)
    review, created = Review.objects.get_or_create(  # if user exist it get if not it creates
        owner=user,
        project=project,

    )

    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response('Tag was deleted!')


# @api_view(['DELETE'])
# def removeTag(request):
#     tagId = request.data['tag']
#     projectId = request.data['project']

#     project = Project.objects.get(id=projectId)
#     tag = Tag.objects.get(id=tagId)

#     project.tags.remove(tag)

#     return Response('Tag was deleted!')