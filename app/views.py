from fastapi import Request
from fastapi.responses import HTMLResponse
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from app import app, templates
from app.db import DB_URL, MODEL_MODULE
from app.models.data_models import Post, Post_Pydantic, PostIn_Pydantic


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    """Home page."""
    post = Post(title='Test', content='This is a test', published=True)
    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post}
    )


@app.post("/posts", response_model=Post_Pydantic)
async def create_post(post: PostIn_Pydantic):
    post_obj = await Post.create(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_tortoise_orm(post_obj)


@app.get(
    "/post/{post_id}", response_model=Post_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_post(post_id: int):
    return await Post_Pydantic.from_queryset_single(Post.get(id=post_id))

register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": [MODEL_MODULE]},
    generate_schemas=True,
    add_exception_handlers=True,
)
