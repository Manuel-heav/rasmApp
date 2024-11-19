from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.db.models.fields import BLANK_CHOICE_DASH
from django.contrib.admin import widgets

class DistrictForm(ModelForm):
    class Meta:
        model = District
        fields = ['districtname']


class RoadSegmentExtForm(forms.ModelForm):
    class Meta:
        model = RoadSegmentExt
        fields = '__all__' 

RoadSegmentRoadSegmentExtFormSet = inlineformset_factory(RoadSegment, RoadSegmentExt, form=RoadSegmentExtForm, extra=2)

class RoadConditionSurveyForm(forms.ModelForm):
    #disabled_fields = ['roadsegext', 'problem','qty']
    class Meta:
        model = RoadConditionSurvey
        exclude = ['actvty']
        labels = {
            'roadsegext':'Km Range',
            'problem':'Condition',
            'severity':'Severity',
            'extent':'Extent',
            'activity':'Activity',
            'qty':'Quantity',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roadsegext'].disabled = True
        self.fields['qty'].disabled = True
        self.fields['roadsegext'].widget.attrs['readonly'] = True
        self.fields['qty'].widget.attrs['readonly'] = True

RoadSegmentExtRoadConditionSurveyFormSet = inlineformset_factory(RoadSegmentExt, RoadConditionSurvey, form=RoadConditionSurveyForm, extra=2)




class ActionPlanForm(ModelForm):
    class Meta:
        model = ActionPlan
        fields = '__all__'


class BudgetedAPForm(forms.ModelForm):
    disabled_fields = ['erabudget']
    class Meta:
        model = BudgetedAP
        fields = ['erabudget','month','bapinBr','bapinKm']
    
        labels = {
            'bapinBr':'ፋይናንሺያል | Financial',
            'bapinKm':'ፊዚካል | Physical',
            'erabudget':'የፕሮጀክቱ ስም | Project Name',
            'month':'ወር | Month',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['erabudget'].widget.attrs.update({'style': 'width: 50%;'})
        self.fields['erabudget'].disabled = True
        #self.fields['erabudget'].widget.attrs.update({'class': 'form-control'})
        self.fields['month'].widget.attrs.update({'style': 'width: 50%;'})
        self.fields['bapinBr'].widget.attrs.update({'style': 'width: 50%;'})
        self.fields['bapinKm'].widget.attrs.update({'style': 'width: 50%;'})
        self.fields['remark'].widget.attrs.update({'cols': 30, 'rows': 1})
        self.fields['remark1'].widget.attrs.update({'style': 'width: 70%;'})
        self.fields['remark2'].widget.attrs.update({'cols': 30, 'rows': 1})


class APForm(forms.ModelForm):
    class Meta:
        model = APSummary
        fields = ['budgetedap','bapmonth','actionInBr','actionInKm','bremark1','bremark2']


class AccomplishmentForm(forms.ModelForm):
    disabled_fields = ['erabudget', 'budgetedap','bapmonth']
    class Meta:
        model = Accomplishment
        fields = ['id','budgetedap','bapmonth','actionInBr','actionInKm','securityproblem','duetocontracttermination','underprocurementprocess','resourceshortages','rightofwayissues','other']

        labels = {
            'actionInBr':'ክንውን በፋይናንሺያል | Financial Accomplishment',
            'actionInKm':'ክንውን በፊዚካል | Physical Accomplishment',
            'budgetedap':'የፕሮጀክቱ ስም | Project Name',
            'bapmonth':'ወር | Month',
            #'unit': 'መለኪያ | Unit',
            'securityproblem':'በፀጥታ ችግር ምክንያት',
            'duetocontracttermination':'በኮንትራት የሚተዳደሩ ፕሮጀክቶች በመቋረጣቸው ምክንያት',
            'underprocurementprocess':'በግዢ ሂደት ላይ ያሉ ፕሮጀክቶች',
            'resourceshortages':'በግብአት እጥረት ምክንያት',
            'rightofwayissues':'በመንገድ ወሰን ማስከበር ምክንያት',
            'other':'የተለያየ (Others)'
        }
        
        widgets = {
            #'actionInBr': forms.TextInput(attrs={'placeholder': 'ፋይናንሺያል'}),
            #'actionInKm': forms.TextInput(attrs={'placeholder': 'ፊዚካል'}),
            #'bremark2': forms.Textarea(
            #   attrs={'placeholder': 'ተጨማሪ አስተያየት እዚህ ይጻፉ'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['budgetedap'].widget.attrs['hidden'] = True
        #self.fields['erabudget'].widget.attrs['hidden'] = True
        #self.fields['erabudget'].widget.attrs.update({'style': 'width: 50%;'})
        self.fields['budgetedap'].widget.attrs.update({'style': 'width: 100%;'})
        self.fields['budgetedap'].disabled = True
        self.fields['budgetedap'].widget.attrs['readonly'] = True
        self.fields['bapmonth'].disabled = True
        #self.fields['erabudget'].widget.attrs.update({'class': 'form-control'})
        #self.fields['erabudget'].widget.attrs['readonly'] = True
        self.fields['actionInBr'].widget.attrs.update({'style': 'width: 80%;'})
        self.fields['actionInKm'].widget.attrs.update({'style': 'width: 80%;'})
        #self.fields['bremark1'].widget.attrs.update({'style': 'width: 100%;'})
        #self.fields['bremark2'].widget.attrs.update({'cols': 30, 'rows': 1})
        


class RMBudgetForm(ModelForm):
    class Meta:
        model = RMBudget
        fields = '__all__'

class BudgetedAPForm(forms.ModelForm):
    class Meta:
        model = BudgetedAP
        fields = '__all__'
        widgets = {
          'bremark2': forms.Textarea(attrs={'rows':1, 'cols':1}),
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']