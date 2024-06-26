import json
import base64
import logging

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import select
from sqlalchemy import func

from db.database import get_session, AsyncSession
from db.models import *
from services.minio_service import MinioInstance
from urllib.request import urlopen
from starlette.responses import HTMLResponse


logger = logging.getLogger(__name__)
handler = logging.FileHandler("logs/router_log.log")
handler.setFormatter(logging.Formatter("%(levelname)s - %(asctime)s - %(lineno)s - %(message)s"))
logger.addHandler(handler)

router = APIRouter(prefix="/memes")

minio = MinioInstance("minio:9000",
                      "hBoAreTWrFZnuefmj5bH",
                      "D0LT1z9MJgf8HaRXMJmSiIvSD31cm4R8R33nCQN5")


@router.get("/", status_code=200)
async def get_all_memes_records(
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    per_page: int = 10,
):
    offset = (page - 1) * per_page
    memes_data = await session.exec(select(Memes).limit(per_page).offset(offset))
    memes = memes_data.all()
    total_count = await session.exec(select(func.count(Memes.id)))
    total_pages = (total_count.one() + per_page - 1) // per_page

    html_content = "<html><body>"
    for meme in memes:
        image_bytes = minio.get_by_name(bucket="tata", name=meme.name)
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        html_content += f'<img src="data:image/png;base64,{base64_image}" alt="{meme.name}" width="300"><br>'
    html_content += "</body></html>"

    return HTMLResponse(
        content=html_content,
        headers={
            "X-Total-Count": str(total_count),
            "X-Total-Pages": str(total_pages),
        },
    )


@router.post("/", status_code=200)
async def post_from_url(mem: Memes, session: AsyncSession=Depends(get_session)):
    try:
        data = urlopen(mem.url)

        result = minio.put_from_url(data, mem.name, "tata")
        logger.info(f"created {result.object_name} object; etag: {result.etag}, version-id: {result.version_id}")

        session.add(mem)
        await session.commit()
        return {"operation" : "success"}
    except Exception as e:
        logger.error(f"post_from_url method - error: {e}")
        raise HTTPException(status_code=404, detail=f"{e}")


@router.get("/{id}", responses = {200: {"content": {"image/png": {}}}}, response_class=Response)
async def get_mem_by_id(*, session: AsyncSession=Depends(get_session), id: int):
    meme = await session.get(Memes, id)
    if not meme:
        logger.info(f"get_mem_by_id - meme with id {id} not found")
        raise HTTPException(status_code=404, detail="Meme not found")
    image_bytes = minio.get_by_name(bucket="tata", name=meme.name)
    return Response(content=image_bytes, media_type="image/png")


@router.put("/{id}", status_code=200)
async def update_mem_by_id(*, session: AsyncSession=Depends(get_session), id: int, mem: Memes):
    existing_mem = await session.get(Memes, id)
    if not existing_mem:
        raise HTTPException(status_code=404, detail="Meme not found")
    if mem.url != existing_mem.url:
        existing_mem.url = mem.url
        minio.replace_by_name(bucket="tata", name=mem.name, url=mem.url)
    existing_mem.name = mem.name
    existing_mem.description = mem.description
    await session.commit()
    return {"operation" : "success"}


@router.delete("/{id}", status_code=200)
async def delete_mem_by_id(*, session: AsyncSession=Depends(get_session), id: int):
    meme = await session.get(Memes, id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    minio.remove_by_name(bucket="tata", name=meme.name)
    await session.delete(meme)
    await session.commit()
    return {"operation" : "success"}