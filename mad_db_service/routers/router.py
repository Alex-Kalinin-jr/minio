import json

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.orm import joinedload

from db.database import get_session, AsyncSession
from db.models import *
from services.minio_service import MinioInstance

router = APIRouter(prefix="/memes")

minio = MinioInstance("minio:9000",
                      "cIMgklpimVsquh6gYVo2",
                      "02HyWGyuwCRGH8KA2JuTN4yL2bPhSJIvHvQ5zWPN")


@router.get("/", status_code=200)
async def get_all_memes_records(session: AsyncSession=Depends(get_session)):
    memes_data = await session.exec(select(Memes))
    memes = memes_data.all()
    return memes


@router.post("/", status_code=200)
async def response_mock(mem: Memes, session: AsyncSession=Depends(get_session)):
    session.add(mem)
    await session.commit()
    minio.mock(mem.url, mem.name, "tata")
    return {"hello" : "world"}


@router.get("/{id}")
async def get_mem_by_id(*, session: AsyncSession=Depends(get_session), id: int):
    meme = await session.get(Memes, id)

    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")

    return meme


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