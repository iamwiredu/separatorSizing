from django import forms
from .models import VerticalSeparatorDesign

class VerticalSeparatorDesignForm(forms.ModelForm):
    class Meta:
        model = VerticalSeparatorDesign
        fields = [
            'name',
            'Wg', 'Wl', 'Pg', 'Pl', 'Ug', 'dp',
            'velocity_factor', 'holdup_time', 'surge_factor',
            'pressure', 'mist_eliminator_ring',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'Wg': forms.NumberInput(attrs={'class': 'form-control'}),
            'Wl': forms.NumberInput(attrs={'class': 'form-control'}),
            'Pg': forms.NumberInput(attrs={'class': 'form-control'}),
            'Pl': forms.NumberInput(attrs={'class': 'form-control'}),
            'Ug': forms.NumberInput(attrs={'class': 'form-control'}),
            'dp': forms.NumberInput(attrs={'class': 'form-control'}),
            'velocity_factor': forms.NumberInput(attrs={'class': 'form-control'}),
            'holdup_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'surge_factor': forms.NumberInput(attrs={'class': 'form-control'}),
            'pressure': forms.NumberInput(attrs={'class': 'form-control'}),
            'mist_eliminator_ring': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        help_texts = {
            'velocity_factor': 'Use between 0.5 and 1.0 depending on design conservatism',
            'dp': 'In feet (ft)',
            'Ug': 'In centipoise (cP)',
        }
