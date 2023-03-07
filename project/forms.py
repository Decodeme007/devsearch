from django.forms import ModelForm
from .models import Project, Review
# for adding style to field
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__' takes all attributes and make them form fields
        fields = ['title', 'featured_image', 'description',
                  'demo_link', 'source_link',]
        # modify field tag adding check box
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add title'})
        # self.fields['description'].widget.attrs.update({'class':'input','placeholder':'Add title'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place Your Vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
