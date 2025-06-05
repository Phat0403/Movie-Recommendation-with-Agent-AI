import pytest
from unittest.mock import MagicMock
from services.comment import CommentService
from models.comment import Comment
from datetime import datetime

@pytest.fixture
def comment_service():
    db = MagicMock()
    service = CommentService(db)
    return service

def test_create_comment(comment_service):
    comment_service.comment_controller.create = MagicMock()
    result = comment_service.create("tt123", "john_doe", "Nice movie!")
    assert isinstance(result, Comment)
    assert result.username == "john_doe"
    assert result.comment == "Nice movie!"

def test_get_comment_success(comment_service):
    mock_comment = Comment(id=1, movie_id="tt123", username="john_doe", comment="Great!", comment_time=datetime.now())
    comment_service.comment_controller.get = MagicMock(return_value=mock_comment)

    result = comment_service.get(1)
    assert result.id == 1
    assert result.username == "john_doe"

def test_get_comment_fail(comment_service):
    comment_service.comment_controller.get = MagicMock(side_effect=Exception("DB error"))

    result = comment_service.get(999)
    assert result is None

def test_get_comments_by_movie_id(comment_service):
    mock_comments = [
        Comment(movie_id="tt123", username="alice", comment="Good"),
        Comment(movie_id="tt123", username="bob", comment="Bad"),
    ]
    comment_service.comment_controller.get_comments_by_movie_id = MagicMock(return_value=mock_comments)

    result = comment_service.get_comments_by_movie_id("tt123")
    assert result["status"] == 200
    assert len(result["comments"]) == 2

def test_get_comments_by_username(comment_service):
    mock_comments = [
        Comment(movie_id="tt123", username="alice", comment="Good"),
        Comment(movie_id="tt456", username="alice", comment="Awesome"),
    ]
    comment_service.comment_controller.get_comments_by_username = MagicMock(return_value=mock_comments)

    result = comment_service.get_comments_by_username("alice")
    assert result["status"] == 200
    assert len(result["comments"]) == 2

def test_get_comments_by_username_not_found(comment_service):
    comment_service.comment_controller.get_comments_by_username = MagicMock(return_value=[])

    result = comment_service.get_comments_by_username("unknown_user")
    assert result["status"] == 200
    assert result["comments"] == []

def test_update_comment(comment_service):
    mock_comment = Comment(id=1, movie_id="tt123", username="user", comment="Old comment", comment_time=datetime.now())
    comment_service.comment_controller.get = MagicMock(return_value=mock_comment)
    comment_service.comment_controller.update = MagicMock()

    updated = comment_service.update(1, "Updated comment")
    assert updated.comment == "Old comment"  # content doesn't change in memory, controller handles persistence

def test_update_comment_fail(comment_service):
    comment_service.comment_controller.get = MagicMock(return_value=None)

    with pytest.raises(ValueError) as exc:
        comment_service.update(999, "Won't update")
    assert "not found" in str(exc.value)

def test_delete_comment_success(comment_service):
    mock_comment = Comment(id=1, movie_id="tt123", username="user", comment="bye", comment_time=datetime.now())
    comment_service.comment_controller.get = MagicMock(return_value=mock_comment)
    comment_service.comment_controller.delete = MagicMock()

    result = comment_service.delete(1)
    assert result["status"] == 200

def test_delete_comment_not_found(comment_service):
    comment_service.comment_controller.get = MagicMock(return_value=None)

    result = comment_service.delete(999)
    assert result["status"] == 404

def test_delete_comment_error(comment_service):
    comment_service.comment_controller.get = MagicMock(return_value=Comment(id=1))
    comment_service.comment_controller.delete = MagicMock(side_effect=Exception("delete error"))

    result = comment_service.delete(1)
    assert result["status"] == 400
