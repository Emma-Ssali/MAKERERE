from django import forms


class GeneratePayslipForm(forms.Form):
    employee_id = forms.IntegerField(label='Employee ID')


class EmailPayslipForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
    subject = forms.CharField(label='Subject', max_length=100)
    body = forms.CharField(label='Body', widget=forms.Textarea)
    attachment = forms.FileField(label='Attachment', required=False)