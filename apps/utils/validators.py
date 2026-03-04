import environ
from io import BytesIO
from PIL import Image, UnidentifiedImageError, ImageOps
from PIL.Image import DecompressionBombError
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

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