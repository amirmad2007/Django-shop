from django import forms
from .models import Message
# class ContactUsForm(forms.Form):
#     name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Your Name' , 'class': 'form-control'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email','class': 'form-control'}))
#     subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Subject','class': 'form-control'}))
#     message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message','class': 'form-control'}))

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','text']
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder': 'email'
            }),
            'subject': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'subject'
            }),
            'text':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder': 'message'
      
            }),
          
        }