from django.forms import ModelForm, Form
from django import forms
from presentation.models import FutureUser



class AddUserMailForm(ModelForm):
    class Meta:
        model = FutureUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(AddUserMailForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True


class ContactForm(Form):
	sender = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea(attrs={'class': 'class="input-group input-group--wrapper"'}))
	copy = forms.BooleanField(required = False)

