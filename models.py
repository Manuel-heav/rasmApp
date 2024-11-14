from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
from django_pandas.managers import DataFrameManager

# Create your models here.

REGION_CHOICES = (
    ('አማራ', 'አማራ'),('አፋር', 'አፋር'),('ቤኒሻንጉል-ጉሙዝ', 'ቤኒሻንጉል-ጉሙዝ'),('ድሬዳዋ', 'ድሬዳዋ'),('ጋምቤላ', 'ጋምቤላ'),('ሀረሪ', 'ሀረሪ'),('ኦሮሚያ', 'ኦሮሚያ'),('ደቡብ ኢትዮጵያ', 'ደቡብ ኢትዮጵያ'),('ሶማሊ', 'ሶማሊ'),('ደቡብ ምዕራብ ኢትዮጵያ', 'ደቡብ ምዕራብ ኢትዮጵያ'),('ትግራይ', 'ትግራይ'),('ሲዳማ', 'ሲዳማ'),('ማዕከላዊ ኢትዮጵያ', 'ማዕከላዊ ኢትዮጵያ'),('በኔትወርክ ውስጥ በሚገኙ ክልሎች', 'በኔትወርክ ውስጥ በሚገኙ ክልሎች'),('በኔትወርኩ ስር በሚገኙ  መንገዶች', 'በኔትወርኩ ስር በሚገኙ  መንገዶች'),('ድሬደዋና የተለያዩ ክልሎች', 'ድሬደዋና የተለያዩ ክልሎች'),('በሁሉም', 'በሁሉም')
    )

REMARK1_CHOICES = (
    ('በጦርነቱ/በፀጥታ ችግር ምክንያት', 'በጦርነቱ/በፀጥታ ችግር ምክንያት'),('በኮንትራት የሚተዳደሩ ፕሮጀክቶች በመቋረጣቸው ምክንያት', 'በኮንትራት የሚተዳደሩ ፕሮጀክቶች በመቋረጣቸው ምክንያት'),('በግዢ ሂደት ላይ ያሉ ፕሮጀክቶች', 'በግዢ ሂደት ላይ ያሉ ፕሮጀክቶች'),('በግብአት እጥረት ምክንያት', 'በግብአት እጥረት ምክንያት'),('በመንገድ ወሰን ማስከበር ምክንያት', 'በመንገድ ወሰን ማስከበር ምክንያት'),('የተለያየ (Others)', 'የተለያየ (Others)')
    )

FORTHEMONTH_CHOICES = (
    ('መስከረም', 'መስከረም'),('ጥቅምት', 'ጥቅምት'),('ህዳር', 'ህዳር'),('ታህሳስ', 'ታህሳስ'),('ጥር', 'ጥር'),('የካቲት', 'የካቲት'),('መጋቢት', 'መጋቢት'),('ሚያዚያ', 'ሚያዚያ'),('ግንቦት', 'ግንቦት'),('ሰኔ', 'ሰኔ'),('ሐምሌ', 'ሐምሌ'),('ነሃሴ', 'ነሃሴ')
    )


class District(models.Model):
    districtno = models.CharField(max_length=10, default=None, blank=True, null=True)
    districtname = models.CharField(max_length=30)
    remark = models.CharField(max_length=50, default=None, blank=True, null=True)
    modifiedon = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'DistrictTb'
        ordering = ['districtno']
    
    def __str__(self):
        return self.districtname
    
    def get_absolute_url(self):
        return reverse('district_edit', kwargs={'pk': self.pk})

class Section(models.Model):
    sectionno = models.CharField(max_length=10, default=None, blank=True, null=True)
    sectionname = models.CharField(max_length=50, default=None, blank=True, null=True)
    districtname = models.ForeignKey(District, on_delete = models.CASCADE, default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    modifiedon = models.DateTimeField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'SectionTb'
    
    def __str__(self):
        return str(self.sectionname) if self.sectionname else ''

    def get_absolute_url(self):
        return reverse('section_edit', kwargs={'pk': self.pk})

class Roadclass(models.Model):
    roadclassname = models.CharField(max_length=50, default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    class Meta:
        db_table = 'RoadClassTb'

    def __str__(self):
        return self.roadclassname

    def get_absolute_url(self):
        return reverse('roadclass_edit', kwargs={'pk': self.pk})


class Majorsurfacetype(models.Model):
    majorsurfacetypename = models.CharField(max_length=30)
    currentmarketunitprice = models.FloatField(default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    class Meta:
        db_table = 'MajorSurfaceTypeTb'

    def __str__(self):
        return self.majorsurfacetypename

    def get_absolute_url(self):
        return reverse('majorsurfacetype_edit', kwargs={'pk': self.pk})


class Roadsurfacetype(models.Model):
    roadsurfacetypename = models.CharField(max_length=30, default=None, blank=True, null=True)
    majorsurfacetypename = models.ForeignKey(Majorsurfacetype, on_delete = models.CASCADE, default=None, blank=True, null=True)
    asphaltgravel = models.CharField(max_length=30, default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    class Meta:
        db_table = 'RoadSurfaceTypeTb'

    def __str__(self):
        return self.roadsurfacetypename

    def get_absolute_url(self):
        return reverse('roadsurfacetype_edit', kwargs={'pk': self.pk})


class Regionalgovernment(models.Model):
    regionalgovernmentname = models.CharField(max_length=30, default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    class Meta:
        db_table = 'RegionalGovernmentTb'

    def __str__(self):
        return self.regionalgovernmentname

    def get_absolute_url(self):
        return reverse('regionalgovernment_edit', kwargs={'pk': self.pk})


class Designstandard(models.Model):
    designstandardname = models.CharField(max_length=30, default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    class Meta:
        db_table = 'DesignStandardTb'

    def __str__(self):
        return self.designstandardname

    def get_absolute_url(self):
        return reverse('designstandard_edit', kwargs={'pk': self.pk})


class Segment(models.Model):
    segmentno = models.CharField(max_length=10, default=None, blank=True, null=True)
    roadid = models.CharField(max_length=20, default=None, blank=True, null=True)
    revisedroadid = models.CharField(max_length=20, default=None, blank=True, null=True)
    segmentname = models.CharField(max_length=50, default=None, blank=True, null=True)
    sectionname = models.ForeignKey(Section, on_delete = models.CASCADE, default=None, blank=True, null=True)
    length = models.FloatField(default=None, blank=True, null=True)
    asphaltlength = models.FloatField(default=None, blank=True, null=True)
    gravellength = models.FloatField(default=None, blank=True, null=True)
    width = models.FloatField(default=None, blank=True, null=True)
    constructionyear = models.IntegerField(default=None, blank=True, null=True)
    constructioncost = models.FloatField(default=None, blank=True, null=True)
    roadclassname = models.ForeignKey(Roadclass, on_delete = models.CASCADE, default=None, blank=True, null=True)
    roadsurfacetypename = models.ForeignKey(Roadsurfacetype, on_delete = models.CASCADE, default=None, blank=True, null=True)
    averagedailytraffic = models.IntegerField(default=None, blank=True, null=True)
    regions = MultiSelectField(choices = REGION_CHOICES, default=None, blank=True, null=True)
    designstandardname = models.ForeignKey(Designstandard, on_delete = models.CASCADE, default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    modifiedon = models.DateTimeField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'SegmentTb'
        ordering = ['segmentno']
    
    def __str__(self):
        return str(self.segmentname) if self.segmentname else ''

    def get_absolute_url(self):
        return reverse('segment_edit', kwargs={'pk': self.pk})


class Roadconditionindex(models.Model):
    roadconditionindexname = models.CharField(max_length=255)
    value = models.FloatField()
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    class Meta:
        db_table = 'RoadConditionIndexTb'

    def __str__(self):
        return self.roadconditionindexname

    def get_absolute_url(self):
        return reverse('roadconditionindex_edit', kwargs={'pk': self.pk})


class Roadcondition(models.Model):
    segmentn = models.ForeignKey(Segment, on_delete = models.CASCADE, default=None, blank=True, null=True)
    roadcondindexname = models.ForeignKey(Roadconditionindex, on_delete = models.CASCADE, default=None, blank=True, null=True)
    year = models.FloatField(default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    class Meta:
        db_table = 'RoadConditionTb'

    def __str__(self):
        return self.segmentn

    def get_absolute_url(self):
        return reverse('roadcondition_edit', kwargs={'pk': self.pk})


class Financer(models.Model):
    def __str__(self):
        return self.financerName
    financerName = models.CharField(max_length=50, default=None, blank=True, null=True)
    class Meta:
        db_table = "financerTb"

    def __str__(self):
        return self.financerName

    def get_absolute_url(self):
        return reverse('financer_edit', kwargs={'pk': self.pk})

class ProjectType(models.Model):
    project = models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table = "projecttypeTb"

    def __str__(self):
        return self.project

    def get_absolute_url(self):
        return reverse('projecttype_edit', kwargs={'pk': self.pk})


class MaintenanceType(models.Model):
    maintenancetype = models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table = "maintenancetypesTb"

    def __str__(self):
        return self.maintenancetype

    def get_absolute_url(self):
        return reverse('maintenancetype_edit', kwargs={'pk': self.pk})


class Contractor(models.Model):
    contractor = models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table = "contractorTb"

    def __str__(self):
        return self.contractor

    def get_absolute_url(self):
        return reverse('contractor_edit', kwargs={'pk': self.pk})


class ContractorName(models.Model):
    contractorType = models.ForeignKey(Contractor, on_delete = models.CASCADE, default=None, blank=True, null=True)
    contractorName = models.CharField(max_length=200, default=None, blank=True, null=True)
    class Meta:
        db_table = "contractorNameTb"

    def __str__(self):
        return self.contractorName

    def get_absolute_url(self):
        return reverse('contractorname_edit', kwargs={'pk': self.pk})


class Consultant(models.Model):
    consultantN = models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table = "consultantTb"

    def __str__(self):
        return self.consultantN

    def get_absolute_url(self):
        return reverse('consultant_edit', kwargs={'pk': self.pk})


class RoadType(models.Model):
    roadT = models.CharField(max_length=50, default=None, blank=True, null=True)
    class Meta:
        db_table = "roadtypeTb"

    def __str__(self):
        return self.roadT

    def get_absolute_url(self):
        return reverse('roadtype_edit', kwargs={'pk': self.pk})


class RFCId(models.Model):
    rfc = models.CharField(max_length=20, default=None, blank=True, null=True)
    class Meta:
        db_table = "rfcIdTb"

    def __str__(self):
        return self.rfc

    def get_absolute_url(self):
        return reverse('rfcId_edit', kwargs={'pk': self.pk})


class RFCClass(models.Model):
    rfccl = models.CharField(max_length=50, default=None, blank=True, null=True)
    class Meta:
        db_table = "rfcclassTb"
        ordering = ['id']

    def __str__(self):
        return self.rfccl

    def get_absolute_url(self):
        return reverse('rfcclass_edit', kwargs={'pk': self.pk})


class PavedStatus(models.Model):
    paved = models.CharField(max_length=50, default=None, blank=True, null=True)
    class Meta:
        db_table = "pavedStatusTb"

    def __str__(self):
        return self.paved

    def get_absolute_url(self):
        return reverse('pavedStatus_edit', kwargs={'pk': self.pk})


class Road(models.Model):
    district = models.ForeignKey(District, on_delete = models.CASCADE, default=None, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete = models.CASCADE, default=None, blank=True, null=True)
    segmentName = models.ForeignKey(Segment, on_delete = models.CASCADE, default=None, blank=True, null=True)
    roadT = models.ForeignKey(RoadType, on_delete = models.CASCADE, default=None, blank=True, null=True)
    rlength = models.FloatField(default=None, blank=True, null=True)
    rfc = models.CharField(max_length=20, default=None, blank=True, null=True)
    roadsurfacetypename = models.ForeignKey(Roadsurfacetype, on_delete = models.CASCADE, default=None, blank=True, null=True)
    roadclassname = models.ForeignKey(Roadclass, on_delete = models.CASCADE, default=None, blank=True, null=True)
    designstandardname = models.ForeignKey(Designstandard, on_delete = models.CASCADE, default=None, blank=True, null=True)
    regions = MultiSelectField(choices = REGION_CHOICES, default=None, blank=True, null=True)
    startX = models.FloatField(default=None, blank=True, null=True)
    endX = models.FloatField(default=None, blank=True, null=True)
    startY = models.FloatField(default=None, blank=True, null=True)
    endY = models.FloatField(default=None, blank=True, null=True)
    maintainedKm = models.FloatField(default=None, blank=True, null=True)
    maintenanceCost = models.FloatField(default=None, blank=True, null=True)
    pavedst = models.ForeignKey(PavedStatus, on_delete = models.CASCADE, default=None, blank=True, null=True)
    class Meta:
        db_table = "roadTb"

    def __str__(self):
        return str(self.segmentName) if self.segmentName else ''


    def get_absolute_url(self):
        return reverse('road_edit', kwargs={'pk': self.pk})


class RoadSegment(models.Model):
    district = models.ForeignKey(District, on_delete = models.CASCADE, db_column="districtname")
    sectionname = models.ForeignKey(Section, on_delete = models.CASCADE, default=None, blank=True, null=True)
    roadname = models.CharField(max_length=100)
    asphaltlength = models.FloatField(blank=True, null=True)
    gravellength = models.FloatField(blank=True, null=True)
    totall = models.FloatField(editable=False)
    rfc_id = models.CharField(max_length=20, default=None, blank=True, null=True)
    surfacetype = models.ForeignKey(Roadsurfacetype, on_delete = models.CASCADE, default=None, blank=True, null=True)
    rfcclass = models.ForeignKey(RFCClass, on_delete = models.CASCADE, default=None, blank=True, null=True)
    designstd = models.ForeignKey(Designstandard, on_delete = models.CASCADE, default=None, blank=True, null=True)
    remark = models.CharField(max_length=255, default=None, blank=True, null=True)
    modifiedon = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'RoadSegmentTb'
        ordering = ['id']
    
    def save(self, *args, **kwargs):
        self.totall = self.asphaltlength + self.gravellength
        super(RoadSegment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.roadname) if self.roadname else ''




class RMProblem(models.Model):
    problem = models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table = 'ProblemTb'
        ordering = ['id']

    def __str__(self):
        return self.problem

class Activity(models.Model):
    activitycode = models.CharField(max_length=10, blank=True)
    activity = models.CharField(max_length=200, default=None, blank=True, null=True)
    unit = models.CharField(max_length=20, default=None, blank=True, null=True)
    urate = models.FloatField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'ActivityTb'
        ordering = ['id']

    def __str__(self):
        return self.activitycode

class RoadSegmentExt(models.Model):
    roadsegment = models.ForeignKey(RoadSegment,  default=None, on_delete = models.PROTECT)
    inspector = models.CharField(max_length=50, default=None, blank=True, null=True)
    fromlen = models.IntegerField()
    tolen = models.IntegerField()
    class Meta:
        db_table = 'RoadSegmentExtTb'
        ordering = ['id']

    def __str__(self):
        return f"{self.fromlen} - {self.tolen}"




class RoadConditionSurvey(models.Model):
    #surveydate = models.DateTimeField(auto_now=True)
    roadsegext = models.ForeignKey(RoadSegmentExt,  default=None, on_delete = models.CASCADE)
    #startkm = models.CharField(max_length=50, default=None, blank=True, null=True)
    #kmcount = models.CharField(max_length=10, default=None, blank=True, null=True) # 1, 2, ...
    problem = models.ForeignKey(RMProblem, default=None, blank=True, null=True, on_delete = models.CASCADE)
    #problemtxt = models.CharField(max_length=100, default=None, blank=True, null=True)
    severity = models.IntegerField(default=0, blank=True, null=True)
    extent = models.IntegerField(default=0, blank=True, null=True)
    actvty = models.CharField(max_length=200, blank=True, null=True) 
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE, default=None, blank=True, null=True)
    qty = models.FloatField(default=0, blank=True, null=True)
    class Meta:
        db_table = 'RoadConditionSurveyTb'
        ordering = ['id']

    def __str__(self):
        return self.segmentNo
    def save(self, *args, **kwargs):
        if self.problem.id == 1 or self.problem.id == 26:
            if self.severity == 1 and self.extent == 1:
                self.qty = '5'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '16'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '30'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '16'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '48'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '94'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '38'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '110'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '220'
            else:
                self.qty = '0'
        elif self.problem.id == 2 or self.problem.id == 25:
            if self.extent == 1:
                self.qty = '0.05'
            elif self.extent == 2:
                self.qty = '0.15'
            elif self.extent == 3:
                self.qty = '0.35'
            else:
                self.qty = '0'
        elif self.problem.id == 3 or self.problem.id == 24:
            if self.severity == 1 and self.extent == 1:
                self.qty = '12'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '38'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '60'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '50'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '150'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '350'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '100'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '300'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '700'
            else:
                self.qty = '0'
        elif self.problem.id == 4 or self.problem.id == 23:
            if self.severity == 1 and self.extent == 1:
                self.qty = '0.05'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '0.15'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '0.35'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '11'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '33'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '75'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '22'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '66'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '150'
            else:
                self.qty = '0'
        elif self.problem.id == 5 or self.problem.id == 22:
            if self.severity == 1 and self.extent == 1:
                self.qty = '0.05'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '0.15'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '0.35'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '11'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '33'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '75'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '22'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '66'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '150'
            else:
                self.qty = '0'
        elif self.problem.id == 6 or self.problem.id == 21:
            if self.severity == 1 and self.extent == 1:
                self.qty = '185'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '555'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '1295'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '275'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '740'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '1554'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '370'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '925'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '1850'
            else:
                self.qty = '0'
        elif self.problem.id == 7 or self.problem.id == 20:
            if self.severity == 1 and self.extent == 1:
                self.qty = '3.5'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '10.5'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '24.5'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '4.5'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '13'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '31.5'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '6'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '18'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '42'
            else:
                self.qty = '0'
        elif self.problem.id == 8 or self.problem.id == 19:
            if self.severity == 1 and self.extent == 1:
                self.qty = '0.25'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '0.75'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '1.75'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '0.75'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '2.25'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '5.25'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '2'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '6'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '14'
            else:
                self.qty = '0'
        elif self.problem.id == 11 or self.problem.id == 12:
            if self.severity == 1 and self.extent == 1:
                self.qty = '100'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '300'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '700'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '100'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '300'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '700'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '100'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '300'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '700'
            else:
                self.qty = '0'
        elif self.problem.id == 14:
            if self.severity == 1 and self.extent == 1:
                self.qty = '0.5'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '5'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '15'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '0.5'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '0.5'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '1.5'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '0.5'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '15'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '4.5'
            else:
                self.qty = '0'
        elif self.problem.id == 15:
            if self.severity == 1 and self.extent == 1:
                self.qty = '100'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '300'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '700'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '100'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '300'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '700'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '100'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '300'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '700'
            else:
                self.qty = '0'
        elif self.problem.id == 16:
            if self.severity == 1 and self.extent == 1:
                self.qty = '1'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '1'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '1'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '5'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '5'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '5'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '10'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '10'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '10'
            else:
                self.qty = '0'
        elif self.problem.id == 18:
            if self.severity == 1 and self.extent == 1:
                self.qty = '650'
            elif self.severity == 1 and self.extent == 2:
                self.qty = '650'
            elif self.severity == 1 and self.extent == 3:
                self.qty = '650'
            elif self.severity == 2 and self.extent == 1:
                self.qty = '650'
            elif self.severity == 2 and self.extent == 2:
                self.qty = '650'
            elif self.severity == 2 and self.extent == 3:
                self.qty = '650'
            elif self.severity == 3 and self.extent == 1:
                self.qty = '650'
            elif self.severity == 3 and self.extent == 2:
                self.qty = '650'
            elif self.severity == 3 and self.extent == 3:
                self.qty = '1300'
            else:
                self.qty = '0'
        else:
            self.qty = '0'
        super(RoadConditionSurvey, self).save(*args, **kwargs)
        
    
    def get_absolute_url(self):
        
        return reverse('roadconditionsurvey_edit', kwargs={'pk': self.pk})



class RMBudget(models.Model):
    district = models.ForeignKey(District, on_delete = models.CASCADE, default=None, blank=True, null=True)
    financer = models.ForeignKey(Financer, on_delete = models.CASCADE, default=None, blank=True, null=True)
    project = models.ForeignKey(ProjectType, on_delete = models.CASCADE, default=None, blank=True, null=True)
    projectName = models.CharField(max_length=100, default=None, blank=True, null=True)
    maintenancetypes = models.CharField(max_length=200, default=None, blank=True, null=True)
    regions = MultiSelectField(choices = REGION_CHOICES, default=None, blank=True, null=True)
    contractorT = models.ForeignKey(Contractor, on_delete = models.CASCADE, default=None, blank=True, null=True)
    contractorN = models.CharField(max_length=200, default=None, blank=True, null=True)
    consultant = models.CharField(max_length=200, default=None, blank=True, null=True)
    segment = models.CharField(max_length=200, default=None, blank=True, null=True)
    approvedBudgetAmt = models.FloatField(default=None, blank=True, null=True)
    budgetYear = models.IntegerField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'rmbudgetTb'
        ordering = ['id']
    
    def __str__(self):
        return str(self.projectName) if self.projectName else ''
    
    def get_absolute_url(self):
        return reverse('rmbudget_edit', kwargs={'pk': self.pk})

class BudgetExt(models.Model):
    budget = models.ForeignKey(RMBudget, on_delete = models.CASCADE, default=None, blank=True, null=True)
    roadT = models.ForeignKey(RoadType, on_delete = models.CASCADE, default=None, blank=True, null=True)
    lenToBeMaintained = models.FloatField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'budgetExtTb'
        ordering = ['id']
    
    def __str__(self):
        return str(self.budget) if self.budget else ''
    
    def get_absolute_url(self):
        return reverse('budgetext_edit', kwargs={'pk': self.pk})


class ActionPlan(models.Model):
    budgetext = models.ForeignKey(BudgetExt, on_delete = models.CASCADE, default=None, blank=True, null=True)
    forTheMonth = models.CharField(max_length=20, blank=True, null=True, choices=FORTHEMONTH_CHOICES)
    actionPlanInBr = models.FloatField(default=None, blank=True, null=True)
    actionPlanInKm = models.FloatField(default=None, blank=True, null=True)
    remark = models.TextField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'actionplanTb'
        ordering = ['id']

    def __str__(self):
        return str(self.budgetext) if self.budgetext else ''
    
    def get_absolute_url(self):
        return reverse('ap_edit', kwargs={'pk': self.pk})

class Achieve(models.Model):
    actionplan = models.OneToOneField(ActionPlan, on_delete=models.CASCADE, primary_key=True)
    actionInBr = models.FloatField(default=None, blank=True, null=True)
    actionInKm = models.FloatField(default=None, blank=True, null=True)
    remark = models.TextField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'achieveTb'
        ordering = ['actionplan']

    def __str__(self):
        return str(self.actionplan) if self.actionplan else ''
    
    @property
    def kmcomparison(self):
        kmcomp = self.actionplan.actionPlanInKm - self.actionInKm
        return kmcomp
    
    def get_absolute_url(self):
        return reverse('achieve_edit', kwargs={'pk': self.pk})


class ERABudget(models.Model):
    bdistrict = models.ForeignKey(District, on_delete = models.CASCADE, default=None, blank=True, null=True)
    bfinancer = models.ForeignKey(Financer, on_delete = models.CASCADE, default=None, blank=True, null=True)
    bzone = models.CharField(max_length=100, default=None, blank=True, null=True)
    bproject = models.ForeignKey(ProjectType, on_delete = models.CASCADE, default=None, blank=True, null=True)
    bprojectname = models.CharField(max_length=200, default=None, blank=True, null=True)
    bworktype = models.ForeignKey(MaintenanceType, on_delete = models.CASCADE, default=None, blank=True, null=True)
    bregion = models.CharField(max_length=100, default=None, blank=True, null=True)
    bcontractor = models.CharField(max_length=100, default=None, blank=True, null=True)
    bcontractorname = models.CharField(max_length=200, default=None, blank=True, null=True)
    bconsultant = models.CharField(max_length=200, default=None, blank=True, null=True)
    broadsegment = models.CharField(max_length=200, default=None, blank=True, null=True)    
    byear = models.CharField(max_length=20, default=None, blank=True, null=True) 
    budgetamount = models.FloatField(default=None, blank=True, null=True)
    basphalt = models.FloatField(null=True)
    bgravel = models.FloatField(null=True)
    budgetAmt = models.FloatField(null=True)
    remark = models.TextField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'erabudgetTb'
        ordering = ['id']
    def __str__(self):
        return self.bprojectname

    objects = DataFrameManager()



class BudgetedAP(models.Model):
        
    class Month(models.TextChoices):
        JUL = "1", "ሐምሌ"
        AUG = "2", "ነሃሴ"
        SEP = "3", "መስከረም"
        OCT = "4", "ጥቅምት"
        NOV = "5", "ህዳር"
        DEC = "6", "ታህሳስ"
        JAN = "7", "ጥር"
        FEB = "8", "የካቲት"
        MAR = "9", "መጋቢት"
        APR = "10", "ሚያዚያ"
        MAY = "11", "ግንቦት"
        JUN = "12", "ሰኔ"    
    
    erabudget = models.ForeignKey(ERABudget, on_delete = models.CASCADE, default=None, blank=True, null=True)
    bapmonth = models.CharField(max_length=20, blank=True, null=True, choices=FORTHEMONTH_CHOICES)
    month = models.CharField(
        max_length=2,
        choices=Month.choices,
        default=Month.JUL
    )    
    bapinBr = models.FloatField(default=None, blank=True, null=True)
    bapinKm = models.FloatField(default=None, blank=True, null=True)
    #remark = models.TextField(default=None, blank=True, null=True)
    financialacomp = models.FloatField(default=None, blank=True, null=True)
    physicalacomp = models.FloatField(default=None, blank=True, null=True)
    remark1 = models.CharField(max_length=100, blank=True, null=True, choices=REMARK1_CHOICES)
    remark2 = models.TextField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'budgetedAPTb'
    def __str__(self):
        return str(self.erabudget) if self.erabudget else ''


class APSummary(models.Model):
    budgetedap = models.OneToOneField(BudgetedAP, on_delete=models.CASCADE, primary_key=True)
    bapmonth = models.CharField(max_length=20, blank=True, null=True, choices=FORTHEMONTH_CHOICES)
    actionInBr = models.FloatField(default=None, blank=True, null=True)
    actionInKm = models.FloatField(default=None, blank=True, null=True)
    bremark1 = models.CharField(max_length=100, blank=True, null=True, choices=REMARK1_CHOICES)
    bremark2 = models.TextField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'apsummaryTb'
        ordering = ['budgetedap']

    def __str__(self):
        return str(self.budgetedap) if self.budgetedap else ''

class Accomplishment(models.Model):
    UNITS = (
            ('Km', 'Km'),
            ('%', '%'),
            ('pcs', 'pcs'),
        )    
    erabudget = models.ForeignKey(ERABudget, on_delete = models.CASCADE, default=None, blank=True, null=True)
    budgetedap = models.OneToOneField(BudgetedAP, on_delete=models.CASCADE, default=None)
    bapmonth = models.CharField(max_length=20, blank=True, null=True, choices=FORTHEMONTH_CHOICES)
    actionInBr = models.FloatField(default='', blank=True, null=True)
    actionInKm = models.FloatField(default='', blank=True, null=True)
    unit = models.CharField(max_length=10, default='', blank=True, null=True, choices=UNITS)
    bremark1 = models.CharField(max_length=100, blank=True, null=True, choices=REMARK1_CHOICES)
    bremark2 = models.TextField(default='', blank=True, null=True)
    securityproblem = models.CharField(max_length=240, default='', blank=True, null=True)
    duetocontracttermination = models.CharField(max_length=240, default='', blank=True, null=True)
    underprocurementprocess = models.CharField(max_length=240, default='', blank=True, null=True)
    resourceshortages = models.CharField(max_length=240, default='', blank=True, null=True)
    rightofwayissues = models.CharField(max_length=240, default='', blank=True, null=True)
    other = models.CharField(max_length=240, default='', blank=True, null=True)
    class Meta:
        db_table = 'accomplishmentTb'
        ordering = ['erabudget']

    def __str__(self):
        return str(self.erabudget) if self.erabudget else ''


class BudgetPerRoadType(models.Model):
    bdistrict = models.CharField(max_length=20, default=None, blank=True, null=True)
    bfinancer = models.CharField(max_length=20, default=None, blank=True, null=True)
    bzone = models.CharField(max_length=20, default=None, blank=True, null=True)
    bproject = models.CharField(max_length=20, default=None, blank=True, null=True)
    bprojectname = models.CharField(max_length=20, default=None, blank=True, null=True)
    broadsegment = models.CharField(max_length=20, default=None, blank=True, null=True)
    byear = models.DateField(auto_now=False, auto_now_add=False)
    Asphalt = models.FloatField(default=None, blank=True, null=True)
    Gravel = models.FloatField(default=None, blank=True, null=True)
    remark = models.TextField(default=None, blank=True, null=True)
    class Meta:
        db_table = 'budgetperroadtypeTb'
        ordering = ['bdistrict']
