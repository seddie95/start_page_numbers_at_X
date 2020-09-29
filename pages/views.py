from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect
from docx_scripts.add_page_numbers import set_page_numbers
from docx_scripts.headings import get_headings
from django.conf import settings
import json
import os
from .forms import FileForm
from .models import WordDoc


class Home(TemplateView):
    template_name = 'home.html'


class Upload(View):
    def get(self, request, *args, **kwargs):
        form = FileForm()

        return render(request, 'home.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save(commit=False)

            # Set the objects file name equal to the original filename
            doc.file_name = request.FILES['doc_file'].name
            doc.save()

            path = doc.doc_file.path

            headings = get_headings(path, 'Heading 1')
            headings['primary_key'] = doc.pk

            return render(request, 'process.html', {
                'headings': headings
            })


class ProcessView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve settings for page numbering
        pk = request.POST.get('pk')
        doc_obj = WordDoc.objects.get(pk=pk)

        page_specs = dict(request.POST.lists())
        page_specs['doc_obj'] = doc_obj

        path = set_page_numbers(page_specs)

        return render(request, 'download.html', {
            'path': path
        })


class DeleteView(View):
    def post(self, request, *args, **kwargs):
        pk = json.loads(request.body)
        doc_obj = WordDoc.objects.get(pk=pk)
        doc_obj.delete()

        return JsonResponse('Removed file from server ', safe=False)


class DeleteNumberedView(View):
    def post(self, request, *args, **kwargs):
        file_name = json.loads(request.body)
        media_root = settings.MEDIA_ROOT
        path = media_root + "\\" + file_name
        os.remove(path)

        return JsonResponse('Removed file from server ', safe=False)