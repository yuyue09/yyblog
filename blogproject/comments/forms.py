from django import forms

class CommentForm(forms.Form):
    text=forms.CharField(label='评论', max_length=200)

      

       