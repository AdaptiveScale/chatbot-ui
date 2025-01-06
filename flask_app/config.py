import os


class Config:
    UPLOADED_IMAGES_DEST = os.path.join("static", "images")
    UPLOADED_DOCUMENTS_DEST = os.path.join("static", "documents")
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
