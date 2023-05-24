import os
import shutil
from zipfile import ZipFile
from django.shortcuts import render
from django.conf import settings
import ast
from django.urls import path, include


def extract_app_name(zip_file_path):
    with ZipFile(zip_file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('apps.py'):
                app_name = os.path.dirname(file_name).replace('/', '.')  # Convert folder path to Python module path
                print(app_name)
                with zip_ref.open(file_name) as apps_file:
                    apps_content = apps_file.read().decode('utf-8')
                    module = ast.parse(apps_content)
                    class_def = next(node for node in module.body if isinstance(node, ast.ClassDef))
                    app_name = next(node.value.s for node in ast.walk(class_def) if isinstance(node, ast.Assign) and node.targets[0].id == 'name')
                    return app_name
    return None


# def update_root_urls(app_name):
#     with open(os.path.join(settings.BASE_DIR, 'myproject', 'urls.py'), 'a') as urls_file:
#         urls_file.write(f"from {app_name}.urls import *\n")
def update_root_urls(app_name):
    urls_path = os.path.join(settings.BASE_DIR, 'myproject', 'urls.py')
    with open(urls_path, 'r') as urls_file:
        lines = urls_file.readlines()

    include_line = f"    path('', include('{app_name}.urls')),\n"
    urlpatterns_index = None
    for i, line in enumerate(lines):
        if line.startswith('urlpatterns = ['):
            urlpatterns_index = i + 1
            break

    if urlpatterns_index is not None:
        lines.insert(urlpatterns_index, include_line)

    with open(urls_path, 'w') as urls_file:
        urls_file.write(''.join(lines))

def update_installed_apps(app_name):
    settings_path = os.path.join(settings.BASE_DIR, 'myproject', 'settings.py')
    with open(settings_path, 'r') as settings_file:
        lines = settings_file.readlines()

    # app_config_line = f"    '{app_name}.apps.{app_name.capitalize()}Config',\n"
    app_config_line = f"    '{app_name}',\n"

    installed_apps_index = None
    for i, line in enumerate(lines):
        if line.startswith('INSTALLED_APPS'):
            installed_apps_index = i + 1
            break

    if installed_apps_index is not None:
        lines.insert(installed_apps_index, app_config_line)

    with open(settings_path, 'w') as settings_file:
        settings_file.write(''.join(lines))


def upload(request):
    if request.method == 'POST' and request.FILES['zip_file']:
        zip_file = request.FILES['zip_file']
        
        # Save the uploaded ZIP file
        with open(os.path.join(settings.MEDIA_ROOT, zip_file.name), 'wb') as f:
            for chunk in zip_file.chunks():
                f.write(chunk)
        
        # Extract the ZIP file to the root folder
        extract_path = settings.BASE_DIR
        with ZipFile(os.path.join(settings.MEDIA_ROOT, zip_file.name), 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # Get the extracted app name
        extracted_app_name = extract_app_name(os.path.join(settings.MEDIA_ROOT, zip_file.name))
        
        # Update root URLs
        update_root_urls(extracted_app_name)
        
        # Update installed apps
        update_installed_apps(extracted_app_name)
        
        return render(request, 'success.html',)
    
    return render(request, 'upload.html')
