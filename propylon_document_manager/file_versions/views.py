from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from propylon_document_manager.file_versions.models import FileVersion 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def upload_file(request):
    if request.method == 'POST':
        file_name = request.data.get("file_name", "")
        file_url = request.data.get("file_url", "")
        if file_name and file_url:
            user = request.user
            version_number = 0 
            max_version = FileVersion.objects.filter(user=user, file_name=file_name).order_by('-version_number').first()
            if max_version:
                version_number = max_version.version_number + 1
            FileVersion.objects.create(file_name=file_name, version_number=version_number, file_url=file_url, user=user)
            return JsonResponse({'message': 'File version created successfully!'}, status=201)
        else:
            return JsonResponse({'error': 'File name and file URL are required.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_file_version(request):
    if request.method == 'GET':
        file_name = request.query_params.get("file_name", "")
        revision = request.query_params.get("revision", None)
        user = request.user

        if file_name:
            if revision is None:
                # If no specific version is provided, get the latest version
                latest_version = FileVersion.objects.filter(user=user, file_name=file_name).order_by('-version_number').first()
                if latest_version:
                    return JsonResponse({
                        'file_name': latest_version.file_name,
                        'version_number': latest_version.version_number,
                        'file_url': latest_version.file_url,
                    }, status=200)
                else:
                    return JsonResponse({'error': 'File not found.'}, status=404)
            else:
                try:
                    version_number = int(revision)
                    specific_version = FileVersion.objects.get(user=user, file_name=file_name, version_number=version_number)
                    return JsonResponse({
                        'file_name': specific_version.file_name,
                        'version_number': specific_version.version_number,
                        'file_url': specific_version.file_url,
                    }, status=200)
                except FileVersion.DoesNotExist:
                    # If the specific version is not found, get the latest version
                    latest_version = FileVersion.objects.filter(user=user, file_name=file_name).order_by('-version_number').first()
                    if latest_version:
                        return JsonResponse({
                            'file_name': latest_version.file_name,
                            'version_number': latest_version.version_number,
                            'file_url': latest_version.file_url,
                        }, status=200)
                    else:
                        return JsonResponse({'error': 'File not found.'}, status=404)
                except ValueError:
                    return JsonResponse({'error': 'Invalid revision number.'}, status=400)
        else:
            return JsonResponse({'error': 'File name is required.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_unique_files(request):
    if request.method == 'GET':
        user = request.user
        unique_files = FileVersion.objects.filter(user=user).values('file_name').distinct()
        file_names = [file['file_name'] for file in unique_files]
        return JsonResponse({'unique_files': file_names}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_file_versions(request):
    if request.method == 'GET':
        file_name = request.query_params.get("file_name", "")
        if file_name:
            user = request.user
            file_versions = FileVersion.objects.filter(user=user, file_name=file_name).values('version_number')
            versions = [version['version_number'] for version in file_versions]
            return JsonResponse({'file_name': file_name, 'versions': versions}, status=200)
        else:
            return JsonResponse({'error': 'File name is required.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)