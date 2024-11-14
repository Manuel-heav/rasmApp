import django_filters
from django_filters import DateTimeFromToRangeFilter, ChoiceFilter, CharFilter, NumberFilter

from .models import BudgetedAP, ERABudget

Month = (
        ( "1", "ሐምሌ"),
        ( "2", "ነሃሴ"),
        ( "3", "መስከረም"),
        ( "4", "ጥቅምት"),
        ( "5", "ህዳር"),
        ( "6", "ታህሳስ"),
        ( "7", "ጥር"),
        ( "8", "የካቲት"),
        ( "9", "መጋቢት"),
        ( "10", "ሚያዚያ"),
        ( "11", "ግንቦት"),
        ( "12", "ሰኔ"),    
)

REMARK1 = (
    ('በጦርነቱ/በፀጥታ ችግር ምክንያት', 'በጦርነቱ/በፀጥታ ችግር ምክንያት'),('በኮንትራት የሚተዳደሩ ፕሮጀክቶች በመቋረጣቸው ምክንያት', 'በኮንትራት የሚተዳደሩ ፕሮጀክቶች በመቋረጣቸው ምክንያት'),('በግዢ ሂደት ላይ ያሉ ፕሮጀክቶች', 'በግዢ ሂደት ላይ ያሉ ፕሮጀክቶች'),('በግብአት እጥረት ምክንያት', 'በግብአት እጥረት ምክንያት'),('በመንገድ ወሰን ማስከበር ምክንያት', 'በመንገድ ወሰን ማስከበር ምክንያት'),('የተለያየ (Others)', 'የተለያየ (Others)')
    )


class ERABudgetFilter(django_filters.FilterSet):
    class Meta:
        model = ERABudget
        fields = {
            'bdistrict__districtname': ['icontains'],
            'bfinancer__financerName': ['icontains'],
            'bprojectname': ['icontains'],
            'bproject__project': ['icontains'],
            'bcontractor': ['icontains'],
            'bworktype__maintenancetype': ['icontains'],
            'bcontractorname': ['icontains'],
            'bconsultant': ['icontains'],
            'broadsegment': ['icontains'],
            'budgetamount': ['lt', 'gt'],
        }
