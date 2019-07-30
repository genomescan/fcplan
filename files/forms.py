from django import forms


class UploadFileForm(forms.Form):
    file_field = forms.FileField(label='Click or drop files here',
                                 widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                        'class': 'btn btn-default'}))


class ContactForm(forms.Form):
    your_name = forms.CharField(label='Your name',
                                max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                              'style': 'max-width: 370px'}))
    your_email = forms.EmailField(label='Your e-mail address',
                                  max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                                'style': 'max-width: 370px'}))
    your_message = forms.CharField(label='Your question',
                                   max_length=1000,
                                   widget=forms.Textarea(attrs={'class': 'form-control form-control-lg',
                                                                'style': 'max-width: 370px; height: 250px'}))


