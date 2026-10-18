
from fastapi.testclient import TestClient
from sqlmodel import select

from app.main import app
from app.database.models import Link
from app.auth_service import create_access_token


client = TestClient(app)


def test_create_short_link(test_user, session , override_get_session):
        token = create_access_token(
            {"sub": str(test_user.user_id)}
        )

        original_url = "https://example.com/new-test-page"

        response = client.post(
            "/api/links",
            json={"original_url": original_url},
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["original_url"] == original_url
        assert data["short_code"]
        assert data["short_url"]
        assert data["click_count"] == 0

        created_link = session.exec(
            select(Link).where(
                Link.short_code == data["short_code"]
            )
        ).first()

        assert created_link is not None
        assert created_link.original_url == original_url
        assert created_link.user_id == test_user.user_id



def test_redirect_to_original_url(test_link , session , override_get_session):
        response = client.get(
                f"/{test_link.short_code}",
                follow_redirects=False,
        )

        assert response.status_code == 307
        assert response.headers["location"] == test_link.original_url


def test_delete_link_by_short_code(test_user ,test_link ,session , override_get_session):
        short_code = test_link.short_code

        token = create_access_token(
            {"sub": str(test_user.user_id)}
        )  

        response = client.delete(
                f"/api/links/{short_code}",
                headers={"Authorization": f"Bearer {token}"},
        )    

        assert response.status_code == 200
        assert response.json()  == {
                "message": "Short link deleted successfully"
        }
         
        


