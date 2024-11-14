from import_export import resources
from .models import ERABudget

class ERABudgetResource(resources.ModelResource):
    class Meta:
        model = ERABudget