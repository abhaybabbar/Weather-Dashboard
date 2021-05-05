from django import forms
from .models import City

class CityForm(forms.ModelForm):
    # we have used forms.Form over here, they represent django form
    #forms.ModelForm creates model form, meta class is necessary for it, in model form we do not need to use .save() method
    class Meta:
        model = City
        fields = ('city_name',)
        #in turple, if we have only one value we have to use ',' otherwise it will take it as a value
        widgets = {
            'city_name': forms.TextInput(attrs={'class':'form-control my-3 input-city w-75 mx-auto', 'placeholder': 'Enter City Name..', 'autocomplete': 'off'})
        }
        #in django form, we write widget in each field
        #in ModelForm we write widget of all the fields together, and therefore the name widgets