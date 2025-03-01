from django import forms

class VideoUploadForm(forms.Form):
    video = forms.FileField(label='Upload your video')
    language = forms.ChoiceField(choices=[
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('hi', 'Hindi'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('mr', 'Marathi'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('ru', 'Russian'),
        ('ja', 'Japanese'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('ar', 'Arabic'),
        ('bn', 'Bengali'),
        ('pa', 'Punjabi'),
        ('gu', 'Gujarati')
        # Add more language options as needed
    ], label='Select target language')
