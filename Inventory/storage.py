from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client
from django.conf import settings
import os

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = settings.SUPABASE_BUCKET

    def _save(self, name, content):
        content = content.read()
        file_path = os.path.join(self.bucket, name)
        self.supabase.storage.from_(self.bucket).upload(file_path, content)
        return name

    def _open(self, name, mode='rb'):
        file_path = os.path.join(self.bucket, name)
        response = self.supabase.storage.from_(self.bucket).download(file_path)
        return ContentFile(response)

    def delete(self, name):
        file_path = os.path.join(self.bucket, name)
        self.supabase.storage.from_(self.bucket).remove([file_path])

    def exists(self, name):
        file_path = os.path.join(self.bucket, name)
        try:
            self.supabase.storage.from_(self.bucket).download(file_path)
            return True
        except:
            return False

    def url(self, name):
        file_path = os.path.join(self.bucket, name)
        return self.supabase.storage.from_(self.bucket).get_public_url(file_path)