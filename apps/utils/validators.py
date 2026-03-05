import environ
from io import BytesIO
from PIL import Image, UnidentifiedImageError, ImageOps
from PIL.Image import DecompressionBombError
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
import os, io, fitz

def validate_secure_image(f):
    ALLOWED_MIMES = ['PNG', 'JPEG']
    MAX_IMAGE_SIZE=5*1024*1024
    MAX_WIDTH = 2048
    MAX_HEIGHT = 2048
    MAX_PIXELS = 4_194_304
    #Taille
    if f.size > MAX_IMAGE_SIZE:
        raise ValidationError("Image trop volumineuse.")
    f.seek(0)
    try:
        Image.MAX_IMAGE_PIXELS = MAX_PIXELS
        with Image.open(f) as img:
            if img.format not in ALLOWED_MIMES:
                raise ValidationError("Format de fichier invalide.")
            if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
                raise ValidationError("Largeur ou hauteur trop grande.")
            if img.width * img.height > MAX_IMAGE_SIZE:
                raise ValidationError("Résolution tron grande.")
    except DecompressionBombError:
        raise ValidationError("Image potentiellement dangereuse (Decompression Bomb).")
    except UnidentifiedImageError:
        raise ValidationError("Le fichier n'a pas pu être identifié comme une image valide.")
    finally:
        f.seek(0)
    return f

def sanitize_image(f):
    #re-encode + exif delete
    with Image.open(f) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        out = BytesIO()
        img.save(out, format="WEBP", quality=85, method=6)
        out.seek(0)
        return ContentFile(out.read(), name=f.name.rsplit('.', 1)[0] + ".webp")

def validate_document_file(f):
    MAX_FILE_SIZE = 10 * 1024 * 1024  
    ALLOWED_EXTENSIONS = ["pdf", "xlsx", "ods", "docx", "odt", "png", "jpg", "jpeg"]
    OFFICE_EXTENSIONS = ["xlsx", "ods", "docx", "odt"]
    IMAGE_EXTENSIONS = ["png", "jpg", "jpeg"]
    #Extension/Nom & taille
    isPDF = False
    filename = os.path.basename(f.name.strip()) 
    ext = os.path.splitext(filename)[1][1:].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Extension non autorisée: .{ext}")
    if f.size > MAX_FILE_SIZE:
        raise ValidationError(f"Fichier trop volumineux (> {MAX_FILE_SIZE // (1024*1024)} MB)")
    #Type MIME
    f.seek(0)
    header = f.read(8)
    f.seek(0)
    if ext == "pdf":
        if not header.startswith(b"%PDF-"):
            raise ValidationError("Le fichier n'est pas un PDF valide.")
        isPDF = True
        f = sanitize_pdf(f)
    elif ext in OFFICE_EXTENSIONS:
        if not header.startswith(b"PK\x03\x04"):
            raise ValidationError(f"Le fichier {ext} n'est pas un fichier Office/LibreOffice valide.")
    elif ext in IMAGE_EXTENSIONS:
        if not (header[:2] == b"\xFF\xD8" or header[:8] == b"\x89PNG\r\n\x1a\n"):
            raise ValidationError(f"L'image {f.name} n'est pas valide.")
        f = validate_secure_image(f)
        f.seek(0)
        f = sanitize_image(f)
    else:
        raise ValidationError("Type de fichier non pris en charge.")
    return f


def sanitize_pdf(f):
    try:
        input_content = f.read()
        doc = fitz.open(stream=input_content, filetype="pdf")
        new_doc = fitz.open()
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_pdf = fitz.open()
            img_pdf.insert_page(0, width=pix.width, height=pix.height)
            img_pdf[0].insert_image(img_pdf[0].rect, stream=img_bytes.getvalue())
            new_doc.insert_pdf(img_pdf)
        sanitized_content = new_doc.write()
        sanitized_file = ContentFile(sanitized_content, name=f.name)
        return sanitized_file
    finally:
        if 'doc' in locals():
            doc.close()
        if 'new_doc' in locals():
            new_doc.close()
