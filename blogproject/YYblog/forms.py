from django import forms


class MessageForm(forms.Form):
    location=forms.CharField(label='居住地',max_length=100)
    job=forms.CharField(label='职业',max_length=100)
    eduction=forms.CharField(label='教育经历',max_length=100)
    head_photo=forms.ImageField(label='个人头像',max_length=200,required=False)


   
   
    