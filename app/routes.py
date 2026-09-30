from fastapi import FastAPI , HTTPException , Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Session


from database.db import get_session
from app.service import (
    create_link ,
      get_link_by_short_code , 
      increment_click_count ,
        is_link_expired , delete_link )

from app.schemas import LinkCreate ,LinkResponse 
from app.auth_service import get_current_user
from app.database.models import User



app = FastAPI()

@app.post("/links", response_model=LinkResponse)
def create_short_link(
    data: LinkCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        created_link = create_link(
            url=data.original_url,
            user_id =current_user.user_id,
            session=session
        )

        return LinkResponse(
            short_code=created_link.short_code,
            short_url=f"http://localhost:8000/{created_link.short_code}",
            original_url=created_link.original_url,
            click_count=created_link.click_count,
            created_at=created_link.created_at,
            expires_at=created_link.expired_at
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.get('/{short_code}')
def redirect_to_original_url(
    short_code : str , 
    session : Session = Depends(get_session)
    ):
    link =  get_link_by_short_code(short_code, session)

    if link is None:
        raise HTTPException(
            status_code=404,
            detail= "Short link not found"
        )

    if is_link_expired(link):
        raise HTTPException(
            status_code=410,
            detail='Short link expired'
        )

    increment_click_count(
        link , 
        session
    )

    return RedirectResponse(
        url= link.original_url,
        status_code= 307
    )
@app.delete('/links/{short_code}')
def delete_link_by_shortcode(
        short_code : str,
        current_user: User = Depends(get_current_user),
        session : Session = Depends(get_session)
):
    link = get_link_by_short_code(
        short_code,
        session
    )

    if link is None: 
        raise HTTPException(
            status_code= 404, 
            detail="Short link not found"
        )
    
    if link.user_id == current_user.user_id:
        delete_link(
            link ,  
            session = session
        )

        return {
            "message": "Short link deleted successfully"
        }
    else:
        raise  HTTPException(
            status_code=404,
            detail= "Short link not found"
        )


