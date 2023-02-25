from typing import Optional, List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post], )
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int =10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip)\
        .all()

    results_list = []
    for i in range(len(results)):
        results[i][0].owner
        results_list.append(results[i][0].__dict__)
        results_list[i]["owner"] = results_list[i]["owner"].__dict__
        results_list[i]["votes"] =  results[i][1]


    print(results_list)
    # for i in range(len(post)):
    #     post[i].owner
    #     post[i] = post[i].__dict__
    #     post[i]["owner"] = post[i]["owner"].__dict__
        #post.__dict__["owner"] = post.__dict__["owner"].__dict__t__

    return results_list


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s,%s,%s) RETURNING *""",
    #                # %s - sanitaze for SQL injection
    #                (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    post.owner
    post.__dict__["owner"] = post.__dict__["owner"].__dict__
    return new_post.__dict__


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    #

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == id).first()



    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post[0].owner
    result = post[0].__dict__
    result["owner"] = result["owner"].__dict__
    result["votes"] = post[1]

    print(result)
    # post.owner
    # post.__dict__["owner"] = post.__dict__["owner"].__dict__
    return  result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists ")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorize to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def change_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    new_post = post_query.first()

    if new_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists ")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    post.owner
    post.__dict__["owner"] = post.__dict__["owner"].__dict__
    return post_query.first().__dict__
