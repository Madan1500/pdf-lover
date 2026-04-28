from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from ..services.pdf_utils import merge_from_fileobjs
from io import BytesIO

router = APIRouter()


@router.post("/merge")
async def merge_pdfs(files: List[UploadFile] = File(...)):
	"""Accept multiple uploaded PDF files and return a merged PDF.

	No authentication is applied.
	"""
	if not files or len(files) < 1:
		raise HTTPException(status_code=400, detail="At least one PDF file is required")

	MAX_FILES = 20
	if len(files) > MAX_FILES:
		raise HTTPException(status_code=400, detail=f"Maximum {MAX_FILES} files allowed")

	file_objs = []
	for f in files:
		# basic content-type check
		content_type = f.content_type or ""
		if not ("pdf" in content_type or content_type == "application/octet-stream"):
			raise HTTPException(status_code=400, detail=f"File {f.filename} is not a PDF")
		# ensure file pointer at start
		try:
			await f.seek(0)
		except Exception:
			pass
		file_objs.append(f.file)

	try:
		merged_bytes = merge_from_fileobjs(file_objs)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to merge PDFs: {e}")

	result = BytesIO(merged_bytes)
	result.seek(0)

	headers = {
		"Content-Disposition": "attachment; filename=merged.pdf"
	}

	return StreamingResponse(result, media_type="application/pdf", headers=headers)
