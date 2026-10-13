from app.service import (
    create_link ,
    get_link_by_short_code ,
    increment_click_count ,
    is_link_expired,
    delete_link
    )

from app.database.models import Link
from datetime import datetime , timezone , timedelta

def test_create_link(session , test_user):
    url = "https://www.youtube.com/" 
    user = test_user

    link = create_link(url , user.user_id , session)

    assert link.original_url == url
    assert link.user.user_id == user.user_id
    assert isinstance(link.link_id , int)
    assert isinstance(link.short_code , str)
    assert link.short_code != ""

    saved_link = session.get(Link, link.link_id)
    assert saved_link is not None
    assert saved_link.original_url == link.original_url
    assert saved_link.user_id == user.user_id 

def test_get_link_by_short_code(session , test_link): 
    link = test_link
    short_code = link.short_code
    original_link = get_link_by_short_code(short_code , session)
    expected_url = "https://www.youtube.com/" 

    assert original_link is not None 
    assert original_link.original_url == expected_url
    assert original_link.short_code == short_code 
    assert original_link.link_id == link.link_id


def test_get_link_by_short_code_returns_none_when_missing(session):
    link = get_link_by_short_code("nonexistent_code", session)

    assert link is None

def test_increment_click_count(test_link , session): 
    old_count = test_link.click_count
    increment_click_count(test_link , session)

    session.refresh(test_link)

    assert test_link.click_count == old_count+1


def test_link_without_expiry_is_not_expired(test_link):
    test_link.expired_at = None

    assert is_link_expired(test_link) is False


def test_link_with_future_expiry_is_not_expired(test_link):
    now = datetime(2026, 10, 13, 12, 0, tzinfo=timezone.utc)
    test_link.expired_at = now + timedelta(hours=1)

    assert is_link_expired(test_link, now=now) is False


def test_link_with_past_expiry_is_expired(test_link):
    now = datetime(2026, 10, 13, 12, 0, tzinfo=timezone.utc)
    test_link.expired_at = now - timedelta(hours=1)

    assert is_link_expired(test_link, now=now) is True


def test_link_expiring_exactly_now_is_expired(test_link):
    now = datetime(2026, 10, 13, 12, 0, tzinfo=timezone.utc)
    test_link.expired_at = now

    assert is_link_expired(test_link, now=now) is True


def test_delete_link_removes_link_from_database(test_link, session):
    link_id = test_link.link_id

    delete_link(test_link, session)

    deleted_link = session.get(Link, link_id)

    assert deleted_link is None
