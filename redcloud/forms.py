from django import forms
from django.contrib.auth.models import User
from .models import Post
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields =   ('text',)

"""<div class="comment">
        <p class= "content-section">
        Comment {{ forloop.counter }} by {{ comment.name }}
        {{ comment.created }}
        </p>
        {{ comment.body|linebreaks }}
      </div>"""
#<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">



