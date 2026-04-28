from io import BytesIO
from typing import BinaryIO, Iterable

from pypdf import PdfReader, PdfWriter


def merge_from_fileobjs(file_objs: Iterable[BinaryIO]) -> bytes:
    """Merge PDFs from an iterable of file-like objects and return bytes.

    Each file-like object should be seeked to the start.
    """
    writer = PdfWriter()

    for f in file_objs:
        try:
            f.seek(0)
        except Exception:
            pass
        reader = PdfReader(f)
        for page in reader.pages:
            writer.add_page(page)

    out = BytesIO()
    writer.write(out)
    out.seek(0)
    return out.read()
