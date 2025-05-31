// src/components/CommentSection.jsx
import React, { useState } from 'react';
import moment from 'moment';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchCommentsByMovieId,
  createComment,
  deleteCommentAPI,
  updateCommentAPI,
} from '../hooks/commentApi'; // Adjust path as needed

// Query key factory
const commentsKeys = {
  all: ['comments'],
  list: (movieId) => [...commentsKeys.all, 'list', movieId],
  detail: (id) => [...commentsKeys.all, 'detail', id],
};


const CommentSection = ({ movieId, currentUser }) => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [newCommentText, setNewCommentText] = useState('');
  const [editingComment, setEditingComment] = useState(null); // { id: number, text: string }
  const [submissionError, setSubmissionError] = useState(null); // For mutation errors

  // Fetching comments
  const {
    data: comments = [], // Default to empty array
    isLoading: isLoadingComments,
    error: fetchError,
  } = useQuery({
    queryKey: commentsKeys.list(movieId),
    queryFn: () => fetchCommentsByMovieId(movieId),
    enabled: !!movieId, // Only run query if movieId is available
  });

  // Mutation for creating a comment
  const createCommentMutation = useMutation({
    mutationFn: createComment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: commentsKeys.list(movieId) });
      setNewCommentText('');
      setSubmissionError(null);
    },
    onError: (error) => {
      setSubmissionError(error.message);
    }
  });

  // Mutation for deleting a comment
  const deleteCommentMutation = useMutation({
    mutationFn: deleteCommentAPI,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: commentsKeys.list(movieId) });
      setSubmissionError(null);
    },
    onError: (error) => {
      setSubmissionError(error.message);
    }
  });

  // Mutation for updating a comment
  const updateCommentMutation = useMutation({
    mutationFn: updateCommentAPI,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: commentsKeys.list(movieId) });
      setEditingComment(null);
      setSubmissionError(null);
    },
    onError: (error) => {
      setSubmissionError(error.message);
    }
  });


  const handleCommentSubmit = (e) => {
    e.preventDefault();
    if (!newCommentText.trim() || !currentUser) return;
    setSubmissionError(null);
    createCommentMutation.mutate({
      movieId,
      commentText: newCommentText,
      token: currentUser.token,
    });
    console.log('token', currentUser.token);
  };

  const handleDeleteComment = (commentId) => {
    if (!currentUser || !window.confirm("Are you sure you want to delete this comment?")) return;
    setSubmissionError(null);
    deleteCommentMutation.mutate({ commentId, token: currentUser.token });
  };

  const handleStartEdit = (comment) => {
    setEditingComment({ id: comment.id, text: comment.comment_text });
    setSubmissionError(null);
  };

  const handleCancelEdit = () => {
    setEditingComment(null);
  };

  const handleSaveEdit = (e) => {
    e.preventDefault();
    console.log('editingComment', editingComment);
    if (!editingComment || !editingComment?.text.trim() || !currentUser) return;
    setSubmissionError(null);
    updateCommentMutation.mutate({
      commentId: editingComment.id,
      commentText: editingComment.text,
      token: currentUser.token,
    });
  };

  const isMutating = createCommentMutation.isPending || deleteCommentMutation.isPending || updateCommentMutation.isPending;

  if (isLoadingComments) return <p className="text-gray-400">Loading comments...</p>;

  // Combined error display
  const displayError = fetchError?.message || submissionError;

  return (
    <div className="mt-10 py-8 border-t border-gray-700">
      <h3 className="text-2xl font-semibold text-white mb-6">Comments ({comments.length})</h3>

      {displayError && <p className="text-red-500 bg-red-100 border border-red-500 p-3 rounded mb-4">Error: {displayError}</p>}

      

      {comments.length > 0 ? (
        <ul className="space-y-6">
          {comments.map((comment) => (
            <li key={comment.id} className="p-4 bg-gray-800 rounded-lg shadow">
              {editingComment && editingComment.id === comment.id ? (
                <form onSubmit={handleSaveEdit}>
                  <textarea
                    className="w-full p-2 bg-gray-700 border border-gray-600 rounded text-white"
                    rows="3"
                    value={editingComment.text}
                    onChange={(e) => setEditingComment({...editingComment, text: e.target.value})}
                    disabled={isMutating}
                  />
                  <div className="mt-2 space-x-2">
                    <button type="submit" disabled={isMutating || !editingComment.text?.trim()} className="py-1 px-3 bg-green-600 hover:bg-green-700 text-white text-sm rounded disabled:bg-gray-500">
                      {updateCommentMutation.isPending && updateCommentMutation.variables?.commentId === comment.id ? 'Saving...' : 'Save'}
                    </button>
                    <button type="button" onClick={handleCancelEdit} disabled={isMutating} className="py-1 px-3 bg-gray-600 hover:bg-gray-500 text-white text-sm rounded">
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <>
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold text-orange-500">{comment.username}</p>
                      <p>{comment.comment}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {moment(comment.comment_time).format('MMMM Do YYYY, h:mm a')}
                        {comment.updated_at && comment.updated_at !== comment.created_at &&
                          <span className="italic"> (edited {moment(comment.updated_at).fromNow()})</span>
                        }
                      </p>
                    </div>
                    {currentUser && (currentUser.username === comment.username || currentUser.isAdmin) && (
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleStartEdit(comment)}
                          className="text-blue-400 hover:text-blue-300 text-sm"
                          disabled={isMutating}
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteComment(comment.id)}
                          className="text-red-400 hover:text-red-300 text-sm"
                          disabled={isMutating || (deleteCommentMutation.isPending && deleteCommentMutation.variables?.commentId === comment.id)}
                        >
                           {deleteCommentMutation.isPending && deleteCommentMutation.variables?.commentId === comment.id ? 'Deleting...' : 'Delete'}
                        </button>
                      </div>
                    )}
                  </div>
                  <p className="mt-3 text-gray-300 whitespace-pre-wrap">{comment.comment_text}</p>
                </>
              )}
            </li>
          ))}
        </ul>
      ) : (
        !isLoadingComments && !fetchError && <p className="text-gray-500">No comments yet. Be the first to comment!</p>
      )}
      {currentUser ? (
        <form onSubmit={handleCommentSubmit} className="mt-8">
          <textarea
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded text-white placeholder-gray-500 focus:ring-orange-500 focus:border-orange-500"
            rows="4"
            placeholder="Write your comment..."
            value={newCommentText}
            onChange={(e) => setNewCommentText(e.target.value)}
            disabled={isMutating}
          />
          <button
            type="submit"
            disabled={!newCommentText.trim() || isMutating}
            className="mt-3 py-2 px-6 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded disabled:bg-gray-600 disabled:cursor-not-allowed cursor-pointer"
          >
            {createCommentMutation.isPending ? 'Submitting...' : 'Post Comment'}
          </button>
        </form>
      ) : (
        <div className="mt-8 p-4 bg-gray-800 border border-gray-700 rounded text-center">
          <p className="text-gray-400">
            You need to be logged in to post a comment.
          </p>
          <button
            onClick={() => navigate('/login')} // Assuming you have a /login route
            className="mt-2 py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded"
          >
            Login
          </button>
        </div>
      )}
    </div>
  );
};

export default CommentSection;