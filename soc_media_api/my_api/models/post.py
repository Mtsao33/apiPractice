from pydantic import BaseModel


class UserPostIn(BaseModel):  # we make classes for each resource we take in
    body: str  # use type hints to show what data type body should be


class UserPost(UserPostIn):
    id: int
    user_id: int

    class Config:
        orm_mode = True # return_value["body"] or return_value.body (second works with sqlchemy rows)


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int  # identifies each comment uniquely
    user_id: int 
    
    class Config:
        orm_mode = True 


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
