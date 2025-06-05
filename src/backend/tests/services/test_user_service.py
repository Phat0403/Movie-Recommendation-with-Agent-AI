import pytest
from unittest.mock import MagicMock
from services.user import UserService
from models.favorite import Favorite
from models.comment import Comment

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def user_service(mock_db_session):
    return UserService(db=mock_db_session)

def test_add_favorite_movie_success(user_service, mock_db_session):
    mock_db_session.query().filter().first.return_value = None  # No existing favorite
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    result = user_service.add_favorite_movie("john", "movie123")
    assert result is True
    mock_db_session.add.assert_called()

def test_add_favorite_movie_already_exists(user_service, mock_db_session):
    mock_db_session.query().filter().first.return_value = Favorite(username="john", movie_id="movie123")

    with pytest.raises(ValueError, match="Movie is already in favorites"):
        user_service.add_favorite_movie("john", "movie123")

def test_add_favorite_movie_failure(user_service, mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    mock_db_session.add.side_effect = Exception("DB error")
    mock_db_session.rollback.return_value = None

    result = user_service.add_favorite_movie("john", "movie123")
    assert result is False
    mock_db_session.rollback.assert_called()

def test_remove_favorite_movie_success(user_service, mock_db_session):
    mock_fav = MagicMock()
    mock_db_session.query().filter().first.return_value = mock_fav

    result = user_service.remove_favorite_movie("john", "movie123")
    assert result is True
    mock_db_session.delete.assert_called_with(mock_fav)
    mock_db_session.commit.assert_called()

def test_remove_favorite_movie_not_found(user_service, mock_db_session):
    mock_db_session.query().filter().first.return_value = None

    with pytest.raises(ValueError, match="Favorite movie not found"):
        user_service.remove_favorite_movie("john", "movie123")

def test_remove_favorite_movie_exception(user_service, mock_db_session):
    mock_fav = MagicMock()
    mock_db_session.query().filter().first.return_value = mock_fav
    mock_db_session.commit.side_effect = Exception("DB failure")
    mock_db_session.rollback.return_value = None

    with pytest.raises(ValueError, match="Error removing favorite movie:"):
        user_service.remove_favorite_movie("john", "movie123")
    mock_db_session.rollback.assert_called()

def test_get_favorite_movies_success(user_service, mock_db_session):
    mock_db_session.query().filter().all.return_value = [
        Favorite(username="john", movie_id="m1"),
        Favorite(username="john", movie_id="m2"),
    ]

    result = user_service.get_favorite_movies("john")
    assert result == ["m1", "m2"]

def test_get_favorite_movies_failure(user_service, mock_db_session):
    mock_db_session.query().filter().all.side_effect = Exception("DB error")

    result = user_service.get_favorite_movies("john")
    assert result == []

def test_get_user_info(user_service):
    user_service.get_favorite_movies = MagicMock(return_value=["m1", "m2"])

    mock_comment1 = MagicMock(spec=Comment)
    mock_comment1.movie_id = "m1"
    mock_comment1.comment = "Nice!"

    mock_comment2 = MagicMock(spec=Comment)
    mock_comment2.movie_id = "m2"
    mock_comment2.comment = "Awesome!"

    user_service.comment_controller.get_comments_by_username = MagicMock(return_value=[mock_comment1, mock_comment2])

    result = user_service.get_user_info("john")
    assert result == {
        "username": "john",
        "favorite_movies": ["m1", "m2"],
        "comments": [{"m1": "Nice!"}, {"m2": "Awesome!"}],
    }
