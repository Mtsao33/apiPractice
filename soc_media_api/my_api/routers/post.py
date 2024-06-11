from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Depends
from my_api.database import comment_table, post_table, database

from my_api.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

from my_api.models.user import User
from my_api.security import get_current_user, oauth2_scheme

# models are used to validate data
router = APIRouter()  # basically app, but can be integrated into existing app


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id) # .c = column
    return await database.fetch_one(query) # returns first value from query (alt: fetch_all)


@router.post(
    "/post", response_model=UserPost, status_code=201
)  # status code 200 for getting resources, so change posting resources to 201
async def create_post(
    post: UserPostIn,
    current_user: Annotated[User, Depends(get_current_user)]
):  # FastAPI checks body of post request at specified endpoint. if body exists, is str, constructs UserPostIn object.
    
    
    data = {**post.model_dump(), "user_id": current_user.id} # same function as deprecated .dict() function
    query = post_table.insert().values(data) # dictionary keys match with columns of database
    last_record_id = await database.execute(query) # insertion query - returns id of inserted value - execute is for any nonselect func 
    return {**data, "id": last_record_id} 

@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn, current_user: Annotated[User, Depends(get_current_user)]):
    
    post = await find_post(comment.post_id)  # check if post exists, find_post is async
    if not post:
        raise HTTPException(
            status_code=404, detail="Post not found"
        )  # 404 means not found, avoids creating comment with null data
    data = {**comment.model_dump(), "user_id": current_user.id}
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id} # returns the body, id


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(
    post_id: int,
):  # post_id from url passed into this function
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query) 


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }  # why await? We make sure we finish get_comments_on_post first before finishing executing the rest of this line


# for each router, we construct an instance of the specified response_model and return it
