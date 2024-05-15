from pydantic import BaseModel


class UserPostIn(BaseModel):  # we make classes for each resource we take in
    body: str  # use type hints to show what data type body should be


class UserPost(UserPostIn):
    id: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int  # identifies each comment uniquely


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
