from database import models
from base62 import encode_base62 
from sqlmodel import select
from datetime import datetime , timezone

def create_link(Url : str  , session): 
    original_url = str(Url)

    link_obj = models.Link(
        original_url= original_url,
    )

    session.add(link_obj)
    session.flush()
    

    link_obj.short_code = encode_base62(link_obj.link_id)

    session.commit()
    session.refresh(link_obj)

    return link_obj    


def get_link_by_short_code(short_code : str , session): 
    link = session.exec(
        select(models.Link).where(
            models.Link.short_code == short_code
        )
    ).first()

    return link

def increment_click_count(link , session): 
    link.click_count += 1
    session.commit()

def is_link_expired(link): 
    if link.expired_at is None: 
        return False
    return link.expired_at <= datetime.now(timezone.utc)

def delete_link(link, session):
    session.delete(link)
    session.commit()

