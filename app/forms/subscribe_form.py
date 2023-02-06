from django import forms


class LocationSubscribeForm(forms.Form):
    choices = [
        (1, "세종"),
        (2, "서울"),
    ]
    checkbox_field = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=choices,
    )
