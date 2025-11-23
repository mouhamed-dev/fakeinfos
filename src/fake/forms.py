from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class SelectForm(forms.Form):

    # --- PAYS ---
    pays = CountryField().formfield(
        initial='SN',
        widget=CountrySelectWidget(
            attrs={
                'name':'pays', 'id':"pays", 'class':"input-focus w-full text-gray-700 transition-all duration-300 ease-in-out p-2 rounded-xl border border-gray-300 focus:border-primary focus:ring-primary"
            }
        )
    )

    # --- GENRE ---
    genre = forms.ChoiceField(
        choices=[
            ('Homme', 'Masculin'),
            ('Femme', 'Féminin'),
        ],
        widget=forms.Select(
            attrs={
                "id": "genre",
                "name": "genre",
                'class':"input-focus w-full text-gray-700 transition-all duration-300 ease-in-out p-2 rounded-xl border border-gray-300 focus:border-primary focus:ring-primary"
            }
        )
    )
