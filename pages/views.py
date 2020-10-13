from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
import json
from .forms import FileForm
from .models import WordDoc
from docx_scripts.add_page_numbers import set_page_numbers
from docx_scripts.headings import get_headings


class UploadView(View):
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

            if bool(headings):
                request.session = {**headings, 'primary_key': doc.pk}
                headings['primary_key'] = doc.pk

                return render(request, 'process.html', {
                    'headings': headings
                })
            else:
                # Delete file, pass message and form to homepage
                context = 0
                form = FileForm()
                doc.delete()
                return render(request, 'home.html', {
                    'context': context, 'form': form
                })


class ProcessView(View):
    def get(self, request, *args, **kwargs):
        """Return users to homepage if they
        refresh the page or navigate to /process """

        form = FileForm()

        return render(request, 'home.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        # Retrieve settings for page numbering
        pk = request.POST.get('pk')
        doc_obj = WordDoc.objects.get(pk=pk)

        page_specs = dict(request.POST.lists())
        page_specs['doc_obj'] = doc_obj

        # Use the specifications to number the page accordingly
        path = set_page_numbers(page_specs)
        file_name = path.split('/')[1]

        if path != 1:
            return render(request, 'download.html', {
                'path': path, 'file_name': file_name
            })

        else:
            # Return form and message if file could not be numbered
            form = FileForm()
            return render(request, 'home.html', {
                 'form': form
            })


class DeleteView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the specific entry and delete it and associated files
        pk = json.loads(request.body)
        doc_obj = WordDoc.objects.get(pk=pk)
        doc_obj.delete()

        return JsonResponse('Removed file from server ', safe=False)


def error_404_view(request, exception):
    return render(request, "404.html")


def error_500_view(request):
    return render(request, "500.html")
