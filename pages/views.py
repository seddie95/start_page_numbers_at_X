from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.conf import settings
import json
import os
from .forms import FileForm
from .models import WordDoc
from docx_scripts.add_page_numbers import set_page_numbers
from docx_scripts.headings import get_headings


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

            # Retrieve the headings for the newly saved file
            path = doc.doc_file.path

            # Retrieve only the Heading 1 headings
            headings = get_headings(path, 'Heading 1')
            request.session = {**headings, 'primary_key': doc.pk}
            headings['primary_key'] = doc.pk

            return render(request, 'process.html', {
                'headings': headings
            })


class ProcessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'process.html')

    def post(self, request, *args, **kwargs):
        # Retrieve settings for page numbering
        pk = request.POST.get('pk')
        doc_obj = WordDoc.objects.get(pk=pk)

        page_specs = dict(request.POST.lists())
        page_specs['doc_obj'] = doc_obj

        # Use the specifications to number the page accordingly
        path = set_page_numbers(page_specs)

        return render(request, 'download.html', {
            'path': path
        })


class DeleteView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the specific entry and delete it and associated files
        pk = json.loads(request.body)
        doc_obj = WordDoc.objects.get(pk=pk)
        doc_obj.delete()

        return JsonResponse('Removed file from server ', safe=False)
