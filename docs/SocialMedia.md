## Specs

Assignement: [github:secondbrain:social_media.md](https://github.com/SecondBrain-io/tech-interview/blob/master/developers/backend/social_media.md)

### Models

```python
class FollowModel:
    id: PK
    followed: FK(UserModel)
    followed_by: FK(UserModel)

class PostModel:
    id: PK
    content: str
    timestamp: int
    author: FK(UserModel)
```


### DTOS

```python
class PaginationParams:
    page: int
    page_size: int

class PaginationResponse:
    page: int
    page_size: int
    total: int
    total_pages: int

class Paginated[T]:
    pagination: PaginationResponse
    total_count: int
    results: list[T]

class UserSearch(PaginationParams):
    username_contains: str | None

class UserPublic:
    usename: str

class PostSearch(PaginationParams):
    whitelist: list[str] | None  # To be able to see someone else posts
    blacklist: list[str] | None  # To be able to skip yourself from your feed

class Post:
    # id for deletion, but requires "neutral" id to avoid system-info leak (e.g. not incremental)
    id: PK
    content: str
    datetime: tz-datetime
    authorName: str

class PostCreate:
    content: str
```

* `POST /posts`
    * payload: PostCreate
    * status_code: 201
    * response: Post

* `DELETE /posts/{post_id}`
    * status_code: 204

* `GET /users`
    * parameters: UserSearch
    * status_code: 200
    * response: Paginated[UserPublic]
        * order by asc username

* `GET /posts`
    * parameters: PostSearch
    * status_code: 200
    * response: Paginated[Post]
        * order by desc datetime

* `POST /users/follow/{username}`
    * status_code: 201
    * response: empty ?

* `DELETE /users/follow/{username}`
    * status_code: 204
