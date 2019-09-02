from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title", "url", "description")
        widgets = {
            "url": forms.HiddenInput,
        }
    # we have to check if the provided image is valid
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()  # obtain user submitted image extension.
        if extension not in valid_extensions:
            raise forms.ValidationError("The given url is not,\
                                        jpg, jpeg or png")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)  # obtain image
        image_url = self.cleaned_data['url']
        cd = self.cleaned_data
        image_name = "{}.{}".format(cd['title'], image_url.rsplit('.',1)[1].lower())

        # download image
        response = request.urlopen(image_url)
        image.image.save(image_name,
                        ContentFile(response.read()),
                        save=False)
        if commit:
            image.save()
        return image 

