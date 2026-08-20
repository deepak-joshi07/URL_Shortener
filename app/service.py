from app.database.models import Link
from app.base62 import encode_base62
from app.id_generation.snowflake import SnowflakeGenerator
from sqlmodel import select
from datetime import datetime, timezone


id_generator = SnowflakeGenerator(machine_id=1)


def create_link(url: str, session):
    original_url = str(url)

    link_id = id_generator.generate_id()
    short_code = encode_base62(link_id)

    link_obj = Link(
        original_url=original_url,
        link_id=link_id,
        short_code=short_code
    )

    session.add(link_obj)
    session.commit()
    session.refresh(link_obj)

    return link_obj


def get_link_by_short_code(short_code: str, session):
    link = session.exec(
        select(Link).where(
            Link.short_code == short_code
        )
    ).first()

    return link


def increment_click_count(link, session):
    link.click_count += 1
    session.commit()


def is_link_expired(link):
    if link.expired_at is None:
        return False

    return link.expired_at <= datetime.now(timezone.utc)


def delete_link(link, session):
    session.delete(link)
    session.commit()