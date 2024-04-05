from import_export import resources
from publicuser.models import CustomerReg

class UploadResource(resources.ModelResource):
    class Meta:
        model=CustomerReg