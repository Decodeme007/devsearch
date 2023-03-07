from rest_framework import serializers
from project.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)  # overriding owner
    tags = TagSerializer(many=True)  # want multiple tags many=True

    reviews = serializers.SerializerMethodField()  # adding attribute review

    class Meta:
        model = Project
        fields = '__all__'

    # must start with get_methodName #self refer to serializer class #obj project
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
