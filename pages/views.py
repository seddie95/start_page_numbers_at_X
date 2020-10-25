from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
import json
from .forms import FileForm
from .models import WordDoc
from docx_scripts.add_page_numbers import set_page_numbers
from docx_scripts.headings import get_headings
from django.contrib import messages


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = FileForm()

        return render(request, 'home.html', {
            'form': form
        })


class ProcessView(View):
    def get(self, request, *args, **kwargs):
        """Return users to homepage if they
        refresh the page or navigate to /process """
        return redirect('home')

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
                # Delete file and redirect to homepage with message
                doc.delete()
                messages.error(request, 'No Headings Found!')
                return redirect('home')


class DownloadView(View):
    def get(self, request, *args, **kwargs):
        """Return users to homepage if they
        refresh the page or navigate to /process """
        return redirect('home')

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
            messages.error(request, 'File could not be numbered!')
            return redirect('home')


class DeleteView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the specific entry and delete it and associated files
        pk = json.loads(request.body)
        doc_obj = WordDoc.objects.get(pk=pk)
        doc_obj.delete()

        return JsonResponse('Removed file from server ', safe=False)


class FileDeleted(View):
    def get(self, request, *args, **kwargs):
        """Return users to homepage
         after two minutes as file will be deleted. """
        messages.error(request, 'File was Deleted!')
        return redirect('home')


class HelpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'help.html')


def error_404_view(request, exception):
    return render(request, "404.html")


def error_500_view(request):
    return render(request, "500.html")
