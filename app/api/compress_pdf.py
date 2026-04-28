from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
import tempfile
import os

from pdf2image import convert_from_path, exceptions as pdf_exceptions
from PIL import Image

router = APIRouter()


@router.post("/compress")
async def compress_pdf_endpoint(
	file: UploadFile = File(...),
	quality: int = Form(50),
	start_page: Optional[int] = Form(None),
	end_page: Optional[int] = Form(None),
	preview: bool = Form(False),
):
	"""Compress an uploaded PDF.

	- `start_page` and `end_page` are optional 1-based page indexes to limit the range.
	- If `preview` is true, the endpoint returns JSON with `size_bytes` instead of the PDF.
	"""
	if not file.filename or not file.content_type or "pdf" not in file.content_type:
		raise HTTPException(status_code=400, detail="A PDF file is required")

	tmp_in = None
	try:
		tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
		content = await file.read()
		tmp_in.write(content)
		tmp_in.flush()
		tmp_in.close()

		# Prepare convert args
		convert_kwargs = {}
		if start_page is not None:
			convert_kwargs["first_page"] = int(start_page)
		if end_page is not None:
			convert_kwargs["last_page"] = int(end_page)

		try:
			images = convert_from_path(tmp_in.name, **convert_kwargs)
		except pdf_exceptions.PDFInfoNotInstalledError:
			raise HTTPException(status_code=500, detail="Poppler is not installed or not found in PATH. Install poppler (poppler-utils) and ensure it's available.")
		except pdf_exceptions.PDFPageCountError:
			raise HTTPException(status_code=500, detail="Unable to get page count. Is poppler installed and in PATH?")

		if not images:
			raise HTTPException(status_code=500, detail="Failed to read PDF pages")

		out_io = BytesIO()
		jpg_pages = []
		for img in images:
			img = img.convert("RGB")
			buf = BytesIO()
			img.save(buf, format="JPEG", quality=max(10, min(95, int(quality))))
			buf.seek(0)
			jpg = Image.open(buf)
			jpg_pages.append(jpg.copy())
			buf.close()

		jpg_pages[0].save(out_io, format="PDF", save_all=True, append_images=jpg_pages[1:])
		out_io.seek(0)

		size_bytes = out_io.getbuffer().nbytes

		if preview:
			return JSONResponse({"size_bytes": size_bytes})

		headers = {"Content-Disposition": "attachment; filename=compressed.pdf", "Content-Length": str(size_bytes)}
		return StreamingResponse(out_io, media_type="application/pdf", headers=headers)

	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		if tmp_in is not None:
			try:
				os.unlink(tmp_in.name)
			except Exception:
				pass

