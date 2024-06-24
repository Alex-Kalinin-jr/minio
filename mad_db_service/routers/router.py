import json
import base64

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import select
from sqlalchemy.orm import joinedload

from db.database import get_session, AsyncSession
from db.models import *
from services.minio_service import MinioInstance
from urllib.request import urlopen
from starlette.responses import HTMLResponse

router = APIRouter(prefix="/memes")

minio = MinioInstance("minio:9000",
                      "hBoAreTWrFZnuefmj5bH",
                      "D0LT1z9MJgf8HaRXMJmSiIvSD31cm4R8R33nCQN5")


@router.get("/", status_code=200)
async def get_all_memes_records(session: AsyncSession=Depends(get_session)):
    memes_data = await session.exec(select(Memes))
    memes = memes_data.all()
    html_content = "<html><body>"
    for meme in memes:
        image_bytes = minio.get_by_name(bucket="tata", name=meme.name)
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        html_content += f'<img src="data:image/png;base64,{base64_image}" alt="{meme.name}" width="300"><br>'
    html_content += "</body></html>"

    return HTMLResponse(content=html_content)


@router.post("/", status_code=200)
async def post_from_url(mem: Memes, session: AsyncSession=Depends(get_session)):
    try:
        data = urlopen(mem.url)

        result = minio.put_from_url(data, mem.name, "tata")
        print(f"created {result.object_name} object; etag: {result.etag}, version-id: {result.version_id}")

        session.add(mem)
        await session.commit()
        return {"operation" : "success"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")


@router.get("/{id}", responses = {200: {"content": {"image/png": {}}}}, response_class=Response)
async def get_mem_by_id(*, session: AsyncSession=Depends(get_session), id: int):
    meme = await session.get(Memes, id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    image_bytes = minio.get_by_name(bucket="tata", name=meme.name)
    return Response(content=image_bytes, media_type="image/png")



# @router.get("/categories", status_code=200, response_model=List[Categories])
# async def get_categories(*, session: AsyncSession=Depends(get_session)):
#     categories = await session.exec(select(Categories).distinct())

#     if not categories:
#         raise HTTPException(status_code=404, detail="Answers not found")

#     return categories.all()


# @router.get("/category/{category}", status_code=200, response_model=Categories)
# async def get_category_by_name(*, session: AsyncSession=Depends(get_session), category: str):
#     category = await session.exec(select(Categories).where(Categories.name == category).distinct())

#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return category.one()


# @router.get("/category_data/{category}", status_code=200, response_model=List[Positions])
# async def get_positions_by_category(*, session: AsyncSession=Depends(get_session), category: str):
#     positions = await session.exec(
#         select(Positions)
#         .join(Positions.category)
#         .where(Categories.name == category)
#     )

#     if not positions:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return positions.all()


# @router.get("/position/{pos}", status_code=200, response_model=Positions)
# async def get_position_by_name(*, session: AsyncSession=Depends(get_session), pos: str):
#     result = await session.exec(select(Positions).where(Positions.position == pos))

#     if not result:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return result.one()


# @router.get("/position_data/{pos}", status_code=200, response_model=List[Links])
# async def get_positions_by_category(*, session: AsyncSession=Depends(get_session), pos: str):
#     links = await session.exec(
#         select(Links)
#         .join(Links.position)
#         .where(Positions.position == pos)
#     )

#     if not links:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return links.all()



# @router.get("/category_by_id/{category}", status_code=200, response_model=Categories)
# async def get_category_by_id(*, session: AsyncSession=Depends(get_session), category: str):
#     category = await session.exec(
#         select(Categories).where(Categories.id == int(category))
#     )

#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return category.one()