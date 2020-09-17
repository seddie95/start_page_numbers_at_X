from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.views.generic import View
from django.http import JsonResponse
from docx_scripts.headings import get_headings
from django.conf import settings
import json


class Home(TemplateView):
    template_name = 'home.html'


class Upload(View):
    def post(self, request, *args, **kwargs):
        # obtain Post request and save it as a document in the media folder
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)

        # Get the path for the file and retrieve the headings
        media_url = settings.MEDIA_ROOT
        path = media_url + "\\" + uploaded_file.name
        headings = get_headings(path, 'Heading 1')

        return JsonResponse(headings, safe=False)


class ProcessView(View):
    def post(self, request, *args, **kwargs):
        page_specifications = json.loads(request.body)




        return None
