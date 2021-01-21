from django import forms
from django.utils.translation import ugettext_lazy as _


class ApprovalForm(forms.Form):
    status = forms.ChoiceField(
        label=_('Approval Status'),
        choices=[
            ('reviewed', 'Reviewed'),
            ('rejected', 'Rejected')
        ])

    remarks = forms.CharField(
        label=_('Remarks'),
        required=False,
        widget=forms.Textarea,
    )

class feedbackForm(forms.Form):
    bad_scan = forms.CharField(
        label=_('Bad Scan'),
        required=True,
        widget=forms.Textarea,
    )
