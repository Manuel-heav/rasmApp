# Generated by Django 5.0.7 on 2024-07-13 11:04

import django.db.models.deletion
import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forTheMonth', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('መስከረም', 'መስከረም'), ('ጥቅምት', 'ጥቅምት'), ('ህዳር', 'ህዳር'), ('ታህሳስ', 'ታህሳስ'), ('ጥር', 'ጥር'), ('የካቲት', 'የካቲት'), ('መጋቢት', 'መጋቢት'), ('ሚያዚያ', 'ሚያዚያ'), ('ግንቦት', 'ግንቦት'), ('ሰኔ', 'ሰኔ'), ('ሐምሌ', 'ሐምሌ'), ('ነሐሴ', 'ነሐሴ')], default=None, max_length=53, null=True)),
                ('actionPlanInBr', models.FloatField(blank=True, default=None, null=True)),
                ('actionPlanInKm', models.FloatField(blank=True, default=None, null=True)),
                ('remark', models.TextField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'actionplanTb',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultantN', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'db_table': 'consultantTb',
            },
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractor', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'db_table': 'contractorTb',
            },
        ),
        migrations.CreateModel(
            name='Designstandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designstandardname', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'DesignStandardTb',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('districtno', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('districtname', models.CharField(max_length=30)),
                ('remark', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('modifiedon', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'DistrictTb',
                'ordering': ['districtno'],
            },
        ),
        migrations.CreateModel(
            name='Financer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financerName', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
            options={
                'db_table': 'financerTb',
            },
        ),
        migrations.CreateModel(
            name='MaintenanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenancetype', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'db_table': 'maintenancetypesTb',
            },
        ),
        migrations.CreateModel(
            name='Majorsurfacetype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('majorsurfacetypename', models.CharField(max_length=30)),
                ('currentmarketunitprice', models.FloatField(blank=True, default=None, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'MajorSurfaceTypeTb',
            },
        ),
        migrations.CreateModel(
            name='PavedStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paved', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
            options={
                'db_table': 'pavedStatusTb',
            },
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'db_table': 'projecttypeTb',
            },
        ),
        migrations.CreateModel(
            name='Regionalgovernment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regionalgovernmentname', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'RegionalGovernmentTb',
            },
        ),
        migrations.CreateModel(
            name='RFCClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfccl', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
            options={
                'db_table': 'rfcclassTb',
            },
        ),
        migrations.CreateModel(
            name='RFCId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfc', models.CharField(blank=True, default=None, max_length=20, null=True)),
            ],
            options={
                'db_table': 'rfcIdTb',
            },
        ),
        migrations.CreateModel(
            name='Roadclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roadclassname', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'RoadClassTb',
            },
        ),
        migrations.CreateModel(
            name='Roadconditionindex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roadconditionindexname', models.CharField(max_length=255)),
                ('value', models.FloatField()),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'RoadConditionIndexTb',
            },
        ),
        migrations.CreateModel(
            name='RoadType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roadT', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
            options={
                'db_table': 'roadtypeTb',
            },
        ),
        migrations.CreateModel(
            name='Achieve',
            fields=[
                ('actionplan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rasmApp.actionplan')),
                ('actionInBr', models.FloatField(blank=True, default=None, null=True)),
                ('actionInKm', models.FloatField(blank=True, default=None, null=True)),
                ('remark', models.TextField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'achieveTb',
                'ordering': ['actionplan'],
            },
        ),
        migrations.CreateModel(
            name='ContractorName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractorName', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('contractorType', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.contractor')),
            ],
            options={
                'db_table': 'contractorNameTb',
            },
        ),
        migrations.CreateModel(
            name='RMBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('regions', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('አማራ', 'አማራ'), ('አፋር', 'አፋር'), ('ቤኒሻንጉል-ጉሙዝ', 'ቤኒሻንጉል-ጉሙዝ'), ('ድሬዳዋ', 'ድሬዳዋ'), ('ጋምቤላ', 'ጋምቤላ'), ('ሀረሪ', 'ሀረሪ'), ('ኦሮሚያ', 'ኦሮሚያ'), ('ደቡብ ኢትዮጵያ', 'ደቡብ ኢትዮጵያ'), ('ሶማሊ', 'ሶማሊ'), ('ደቡብ ምዕራብ ኢትዮጵያ', 'ደቡብ ምዕራብ ኢትዮጵያ'), ('ትግራይ', 'ትግራይ'), ('ሲዳማ', 'ሲዳማ')], default=None, max_length=75, null=True)),
                ('approvedBudgetAmt', models.FloatField(blank=True, default=None, null=True)),
                ('budgetYear', models.IntegerField(blank=True, default=None, null=True)),
                ('consultant', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.consultant')),
                ('contractorN', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.contractorname')),
                ('contractorT', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.contractor')),
                ('district', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.district')),
                ('financer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.financer')),
                ('maintenancetypes', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.maintenancetype')),
                ('project', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.projecttype')),
            ],
            options={
                'db_table': 'rmbudgetTb',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='actionplan',
            name='rmbudget',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.rmbudget'),
        ),
        migrations.CreateModel(
            name='Roadsurfacetype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roadsurfacetypename', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('asphaltgravel', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('majorsurfacetypename', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.majorsurfacetype')),
            ],
            options={
                'db_table': 'RoadSurfaceTypeTb',
            },
        ),
        migrations.CreateModel(
            name='BudgetExt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lenToBeMaintained', models.FloatField(blank=True, default=None, null=True)),
                ('budget', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.rmbudget')),
                ('roadT', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.roadtype')),
            ],
            options={
                'db_table': 'budgetExtTb',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionno', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('sectionname', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('modifiedon', models.DateTimeField(blank=True, default=None, null=True)),
                ('districtname', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.district')),
            ],
            options={
                'db_table': 'SectionTb',
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('segmentno', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('roadid', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('revisedroadid', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('segmentname', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('length', models.FloatField(blank=True, default=None, null=True)),
                ('asphaltlength', models.FloatField(blank=True, default=None, null=True)),
                ('gravellength', models.FloatField(blank=True, default=None, null=True)),
                ('width', models.FloatField(blank=True, default=None, null=True)),
                ('constructionyear', models.IntegerField(blank=True, default=None, null=True)),
                ('constructioncost', models.FloatField(blank=True, default=None, null=True)),
                ('averagedailytraffic', models.IntegerField(blank=True, default=None, null=True)),
                ('regions', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('አማራ', 'አማራ'), ('አፋር', 'አፋር'), ('ቤኒሻንጉል-ጉሙዝ', 'ቤኒሻንጉል-ጉሙዝ'), ('ድሬዳዋ', 'ድሬዳዋ'), ('ጋምቤላ', 'ጋምቤላ'), ('ሀረሪ', 'ሀረሪ'), ('ኦሮሚያ', 'ኦሮሚያ'), ('ደቡብ ኢትዮጵያ', 'ደቡብ ኢትዮጵያ'), ('ሶማሊ', 'ሶማሊ'), ('ደቡብ ምዕራብ ኢትዮጵያ', 'ደቡብ ምዕራብ ኢትዮጵያ'), ('ትግራይ', 'ትግራይ'), ('ሲዳማ', 'ሲዳማ')], default=None, max_length=75, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('modifiedon', models.DateTimeField(blank=True, default=None, null=True)),
                ('designstandardname', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.designstandard')),
                ('roadclassname', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.roadclass')),
                ('roadsurfacetypename', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.roadsurfacetype')),
                ('sectionname', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.section')),
            ],
            options={
                'db_table': 'SegmentTb',
                'ordering': ['segmentno'],
            },
        ),
        migrations.CreateModel(
            name='RoadConditionSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surveyDate', models.DateField(blank=True, default=None, null=True)),
                ('inspector', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('area', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('startKm', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('kmCount', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('range', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('severity', models.IntegerField(blank=True, default=None, null=True)),
                ('extent', models.IntegerField(blank=True, default=None, null=True)),
                ('roadSide', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('problem', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('solution', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('district', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.district')),
                ('segmentNo', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.segment')),
            ],
            options={
                'db_table': 'RoadConditionSurveyTb',
            },
        ),
        migrations.CreateModel(
            name='Roadcondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.FloatField(blank=True, default=None, null=True)),
                ('remark', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('roadcondindexname', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.roadconditionindex')),
                ('segmentn', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.segment')),
            ],
            options={
                'db_table': 'RoadConditionTb',
            },
        ),
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rlength', models.FloatField(blank=True, default=None, null=True)),
                ('rfc', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('regions', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('አማራ', 'አማራ'), ('አፋር', 'አፋር'), ('ቤኒሻንጉል-ጉሙዝ', 'ቤኒሻንጉል-ጉሙዝ'), ('ድሬዳዋ', 'ድሬዳዋ'), ('ጋምቤላ', 'ጋምቤላ'), ('ሀረሪ', 'ሀረሪ'), ('ኦሮሚያ', 'ኦሮሚያ'), ('ደቡብ ኢትዮጵያ', 'ደቡብ ኢትዮጵያ'), ('ሶማሊ', 'ሶማሊ'), ('ደቡብ ምዕራብ ኢትዮጵያ', 'ደቡብ ምዕራብ ኢትዮጵያ'), ('ትግራይ', 'ትግራይ'), ('ሲዳማ', 'ሲዳማ')], default=None, max_length=75, null=True)),
                ('startX', models.FloatField(blank=True, default=None, null=True)),
                ('endX', models.FloatField(blank=True, default=None, null=True)),
                ('startY', models.FloatField(blank=True, default=None, null=True)),
                ('endY', models.FloatField(blank=True, default=None, null=True)),
                ('maintainedKm', models.FloatField(blank=True, default=None, null=True)),
                ('maintenanceCost', models.FloatField(blank=True, default=None, null=True)),
                ('designstandardname', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.designstandard')),
                ('district', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.district')),
                ('pavedst', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.pavedstatus')),
                ('roadclassname', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.roadclass')),
                ('roadsurfacetypename', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.roadsurfacetype')),
                ('roadT', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.roadtype')),
                ('section', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.section')),
                ('segmentName', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.segment')),
            ],
            options={
                'db_table': 'roadTb',
            },
        ),
        migrations.AddField(
            model_name='rmbudget',
            name='segment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rasmApp.segment'),
        ),
    ]