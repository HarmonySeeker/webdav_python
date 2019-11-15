"""
File serving all the functions of the WebDav web app.

TSU Task
"""

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper

import os

SOURCE_DIR = "./init_app/source_folder/"


def path_valid(path):
    """Check if path isn't pointing on smth outside the source folder."""
    return SOURCE_DIR[1:] in path


def create_abs_path(path, name):
    """Return an absolute path of given element in filesystem."""
    temp_str = os.path.abspath(os.path.join(SOURCE_DIR, path + name))
    return temp_str


def get_full_folder_contains():
    """Walk down the source folder and get names & links of all files, dirs."""
    resp_arr = []
    for root, dirs, files in os.walk(SOURCE_DIR, topdown=True):
        for name in files:
            full_name = '/'.join(os.path.join(root, name).split('/')[3:])
            resp_arr.append({"name": full_name, "type": "file"})
        for name in dirs:
            full_name = '/'.join(os.path.join(root, name + '/').split('/')[3:])
            resp_arr.append({"name": full_name, "type": "dir"})

    return(resp_arr)


def get_folder_contains(folder_name):
    """Get current folder's contents."""
#   resp_arr.append({"name": name, "type": "file", "url": fs.url(name)})
    resp_arr = []
    source_path = SOURCE_DIR + folder_name
    for name in os.listdir(source_path):
        if os.path.isfile(source_path + name):
            resp_arr.append({"name": name, "type": "file"})
        else:
            name += '/'
            resp_arr.append({"name": name, "type": "dir", "url": name})

    return(resp_arr)


def delete_file(request, path):
    cut_url = '/'.join(request.path.split('/')[3:])
    file_name = request.POST['delete_file']
    fpath = create_abs_path(path, file_name)
    if file_name != "":
        if path_valid(fpath) and os.path.isfile(fpath):
            os.remove(fpath)
            print("DELETED FILE: " + file_name)
            print("AT: " + cut_url)


def delete_folder(request, path):
    dir_name = request.POST['delete_dir']
    dpath = create_abs_path(path, dir_name)
    if dir_name != "":
        if path_valid(dpath) and len(os.listdir(dpath)) == 0:
            os.rmdir(dpath)
            print("DELETED DIR: " + dir_name)


def create_folder(request, path):
    new_dir = request.POST['create_folder']
    ndpath = create_abs_path(path, new_dir)
    if new_dir != "":
        if path_valid(ndpath) and not os.path.exists(ndpath):
            os.mkdir(ndpath)


def download_file(request, path):
    file_name = request.POST['download_file']
    dwpath = create_abs_path(path, file_name)

    wrapper = FileWrapper(open(dwpath, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + file_name
    return response

@api_view(['GET', 'POST'])
def source(request, path):
    """URL handler for list function of source folder."""
    if request.method == 'POST':
        if "delete_file" in request.POST:
            delete_file(request, path)

        elif "delete_dir" in request.POST:
            delete_folder(request, path)

        elif "create_folder" in request.POST:
            create_folder(request, path)

        elif "download_file" in request.POST:
            response = download_file(request, path)
            return response

    context = {}
    resp_arr = get_folder_contains(path)
    context['results'] = resp_arr
#   print(path)
#   print(resp_arr)
    return render(request, "ls.html", context)


@api_view(['GET'])
def full_source(request):
    """URL handler for list_all function of source folder."""
    resp_arr = get_full_folder_contains()
    context = {}
    context['results'] = resp_arr
    return render(request, "full_ls.html", context)


@api_view(['GET', 'POST'])
def file_upload(request, path):
    """File upload function."""
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        print(fs.url(name))
        print("New file: " + name)
    return render(request, 'upload.html', context)
