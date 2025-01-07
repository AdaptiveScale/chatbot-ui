import os
import re
from typing import Union

from flask_uploads import UploadSet, IMAGES, DOCUMENTS
from werkzeug.datastructures import FileStorage


EXTENDED_IMAGES = tuple(IMAGES) + ('.ico',)


class CustomUploadSet(UploadSet):
    def file_allowed(self, storage, basename):
        if basename.lower().endswith('.txt'):
            return True
        return super().file_allowed(storage, basename)


class FileHelper:
    def __init__(self):
        self.IMAGE_SET = CustomUploadSet('images', EXTENDED_IMAGES)
        self.DOCUMENT_SET = CustomUploadSet('documents', DOCUMENTS)

    def get_image_set(self):
        return self.IMAGE_SET

    def get_document_set(self):
        return self.DOCUMENT_SET

    def upload_image(self, image: FileStorage, folder: str):
        path = self.get_image_path(filename=image.filename, folder=folder)
        uploaded_image = self.save_image(image=image, folder=folder)

        new_filename = uploaded_image.split('/')[-1]
        path = path.replace(image.filename, new_filename)
        return path

    def upload_document(self, document: FileStorage, folder: str):
        path = self.get_document_path(filename=document.filename, folder=folder)
        uploaded_document = self.save_document(document=document, folder=folder)

        new_filename = uploaded_document.split('/')[-1]
        path = path.replace(document.filename, new_filename)
        return path

    def save_image(self, image: FileStorage, folder: str = None, name: str = None) -> str:
        return self.IMAGE_SET.save(image, folder, name)

    def save_document(self, document: FileStorage, folder: str = None, name: str = None) -> str:
        return self.DOCUMENT_SET.save(document, folder, name)

    def get_image_path(self, filename: str = None, folder: str = None) -> str:
        return self.IMAGE_SET.path(filename, folder)

    def get_document_path(self, filename: str = None, folder: str = None) -> str:
        return self.DOCUMENT_SET.path(filename, folder)

    def find_image_any_format(self, filename: str, folder: str) -> Union[str, None]:
        for _format in IMAGES:
            image = f"{filename}.{_format}"
            image_path = self.IMAGE_SET.path(filename=image, folder=folder)
            if os.path.isfile(image_path):
                return image_path
        return None

    def find_document_any_format(self, filename: str, folder: str) -> Union[str, None]:
        for _format in DOCUMENTS:
            document = f"{filename}.{_format}"
            document_path = self.DOCUMENT_SET.path(filename=document, folder=folder)
            if os.path.isfile(document_path):
                return document_path
        return None

    @classmethod
    def _retrieve_filename(cls, file: Union[str, FileStorage]) -> str:
        if isinstance(file, FileStorage):
            return file.filename
        return file

    @classmethod
    def is_image_filename_safe(cls, file: Union[str, FileStorage]) -> bool:
        filename = cls._retrieve_filename(file)
        allowed_format = "|".join(IMAGES)
        regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
        return re.match(regex, filename) is not None

    @classmethod
    def is_document_filename_safe(cls, file: Union[str, FileStorage]) -> bool:
        filename = cls._retrieve_filename(file)
        allowed_format = "|".join(DOCUMENTS)
        regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
        return re.match(regex, filename) is not None

    @classmethod
    def get_basename(cls, file: Union[str, FileStorage]) -> str:
        filename = cls._retrieve_filename(file)
        return os.path.split(filename)[1]

    @classmethod
    def get_extension(cls, file: Union[str, FileStorage]) -> str:
        filename = cls._retrieve_filename(file)
        return os.path.splitext(filename)[1]

    @staticmethod
    def delete_file(path: str) -> bool:
        """
        Delete the file given its path.

        Parameters:
            path (str): Path to the file to be deleted.

        Returns:
            bool: True if the file was deleted successfully, False otherwise.
        """
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting file {path}. Reason: {e}")
            return False

    @staticmethod
    def delete_dir(path: str) -> bool:
        """
        Delete the directory given its path.

        Parameters:
            path (str): Path to the directory to be deleted.

        Returns:
            bool: True if the direcotory was deleted successfully, False otherwise.
        """
        try:
            if os.path.exists(path):
                files = os.listdir(path)
                if len(files) > 0:
                    for file in files:
                        os.remove(os.path.join(path, file))
                os.rmdir(path)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting file {path}. Reason: {e}")
            return False
