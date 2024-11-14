from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from rasmApp.models import *

@admin.register(ERABudget)
class ERABudgetAdmin(ImportExportModelAdmin):
    pass


# Register your models here.
admin.site.register(District)#, DistrictAdmin)
admin.site.register(Section)#, SectionAdmin)
admin.site.register(Roadclass)
admin.site.register(Majorsurfacetype)
admin.site.register(Roadsurfacetype)
admin.site.register(Regionalgovernment)
admin.site.register(Designstandard)
admin.site.register(Segment)#, SegmentAdmin)
admin.site.register(Roadcondition)
admin.site.register(Roadconditionindex)
admin.site.register(Financer)
admin.site.register(ProjectType)
admin.site.register(MaintenanceType)
admin.site.register(Contractor)
admin.site.register(ContractorName)
admin.site.register(Consultant)
admin.site.register(RoadType)
admin.site.register(RFCId)
admin.site.register(RFCClass)
admin.site.register(PavedStatus)
admin.site.register(Road)
admin.site.register(RMBudget)#, RMBudgetAdmin)
admin.site.register(BudgetExt)
admin.site.register(ActionPlan)
admin.site.register(Achieve)#, AchieveAdmin)
#admin.site.register(ERABudget)#, ERABudgetAdmin)
admin.site.register(BudgetedAP)
admin.site.register(Accomplishment)
admin.site.register(RoadSegment)
admin.site.register(Activity)
admin.site.register(RMProblem)
admin.site.register(RoadSegmentExt)
admin.site.register(RoadConditionSurvey)
