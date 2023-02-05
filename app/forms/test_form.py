from django import forms


class TestForm(forms.Form):
    char_field = forms.CharField(max_length=100)
    text_field = forms.CharField(widget=forms.Textarea)
    hidden = forms.CharField(widget=forms.HiddenInput, initial="hidden")
    email_field = forms.EmailField()
    url_field = forms.URLField()
    integer_field = forms.IntegerField()
    float_field = forms.FloatField()
    decimal_field = forms.DecimalField(max_digits=5, decimal_places=2)
    date_field = forms.DateField()
    time_field = forms.TimeField()
    datetime_field = forms.DateTimeField()
    boolean_field = forms.BooleanField()
    choice_field = forms.ChoiceField(choices=[(1, "Option 1"), (2, "Option 2"), (3, "Option 3")])
    multiple_choice_field = forms.MultipleChoiceField(choices=[(1, "Option 1"), (2, "Option 2"), (3, "Option 3")])
    # file_field = forms.FileField()
    # image_field = forms.ImageField()
