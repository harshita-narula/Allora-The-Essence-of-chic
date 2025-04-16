from django import forms

class MobileNumberForm(forms.Form):
    mobile_number = forms.CharField(max_length=15)

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
