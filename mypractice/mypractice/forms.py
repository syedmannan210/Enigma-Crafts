from django import forms
class userForm(forms.Form): #forms is the module and Form is the class
    num1=forms.CharField(label="Value1", max_length=20, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    num2=forms.CharField(label="Value2")
