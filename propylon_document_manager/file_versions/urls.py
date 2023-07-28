from django.urls import path
from propylon_document_manager.file_versions.views import upload_file, get_file_version, get_unique_files, get_file_versions

app_name = "file_versions"

urlpatterns = [
    path('upload-file/', view=upload_file, name='upload_file'),
    path('get-file-version/', view=get_file_version, name='get_file_version'),
    path("get-unique-files/", view=get_unique_files, name="get_unique_files"),
    path("get-file-versions/", view=get_file_versions, name="get_file_versions"),

]
