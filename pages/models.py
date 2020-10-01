from django.db import models


class WordDoc(models.Model):
    file_name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    doc_file = models.FileField(upload_to='unprocessed')

    def __str__(self):
        return f"Original file name: {self.file_name}, Saved file name: {self.doc_file}"

    def delete(self, *args, **kwargs):
        self.doc_file.delete()
        super().delete(*args, **kwargs)
