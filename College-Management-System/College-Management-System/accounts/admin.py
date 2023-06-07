from django.contrib import admin
from .models import Student_profiles
admin.site.register(Student_profiles)
from .models import StudentRating
admin.site.register(StudentRating)
from .models import ManagerProfile
admin.site.register(ManagerProfile)
from .models import UploadedFile
admin.site.register(UploadedFile)