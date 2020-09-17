from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.views.generic import View
from django.http import JsonResponse
from docx_scripts.add_page_numbers import set_page_numbers
from docx_scripts.headings import get_headings
from django.conf import settings
import json
import urllib.parse


class Home(TemplateView):
    template_name = 'home.html'


class Upload(View):
    def post(self, request, *args, **kwargs):
        # obtain Post request and save it as a document in the media folder
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        file = fs.save(uploaded_file.name, uploaded_file)
        file_name = urllib.parse.unquote(fs.url(file)).split('/')[-1]

        # Get the path for the file and retrieve the headings
        media_root = settings.MEDIA_ROOT

        path = media_root + "\\" + file_name
        headings = get_headings(path, 'Heading 1')
        headings['file_name'] = file_name

        return JsonResponse(headings, safe=False)


class ProcessView(View):
    def post(self, request, *args, **kwargs):
        page_specifications = json.loads(request.body)
        numbered_file_path = set_page_numbers(page_specifications)

        return JsonResponse(numbered_file_path, safe=False)
