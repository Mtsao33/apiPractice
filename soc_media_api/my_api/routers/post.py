from fastapi import APIRouter, HTTPException

from my_api.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

# models are used to validate data
router = APIRouter()  # basically app, but can be integrated into existing app


post_table = {}  # database
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post(
    "/post", response_model=UserPost, status_code=201
)  # status code 200 for getting resources, so change posting resources to 201
async def create_post(
    post: UserPostIn,
):  # FastAPI checks body of post request at specified endpoint. if body exists, is str, constructs UserPostIn object.
    data = post.model_dump()  # same function as deprecated .dict() function
    last_record_id = len(post_table)
    new_post = {
        **data,
        "id": last_record_id,
    }  # creates new dictionary using key value pairs in data(thanks to **data), but with new "id" field
    post_table[last_record_id] = new_post
    return new_post  # returns the body, id


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)  # check if post exists
    if not post:
        raise HTTPException(
            status_code=404, detail="Post not found"
        )  # 404 means not found, avoids creating comment with null data
    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = {
        **data,
        "id": last_record_id,
    }  # creates new dictionary using key value pairs in data(thanks to **data), but with new "id" field
    comment_table[last_record_id] = new_comment
    return new_comment  # returns the body, id


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(
    post_id: int,
):  # post_id from url passed into this function
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }  # why await? We make sure we finish get_comments_on_post first before finishing executing the rest of this line


# for each router, we construct an instance of the specified response_model and return it
