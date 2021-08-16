from django import forms

from car_hub.cars.models import CommentModel, CarModel

from django.utils.safestring import mark_safe


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    class Meta:
        model = CommentModel
        fields = 'comment'


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ('brand', 'description', 'year', 'image', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_fields()

    def _init_bootstrap_fields(self):
        for (_, field) in self.fields.items():
            if _ == 'price':
                field.widget.attrs['placeholder'] = mark_safe('&euro;')
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form-control'