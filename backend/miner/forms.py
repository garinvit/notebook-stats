from django import forms
from .models import Miner


class MinerForm(forms.ModelForm):

    class Meta:
        model = Miner
        fields = '__all__'