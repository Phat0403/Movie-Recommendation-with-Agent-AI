import React from "react";
import { useAuth } from "../hooks/useAuth";
// 1. Import thêm useMutation và useQueryClient
import { useQuery, useQueries, useMutation, useQueryClient } from "@tanstack/react-query";
// 2. Import hàm API để xóa
import { fetchMyList, removeFromMyList } from "../hooks/myListApi";
import Card from "../components/Card";
import { useNavigate } from "react-router-dom";
const fetchMovieDetails = async (movieId) => {
  const response = await fetch(`http://localhost:8000/api/movie/${movieId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch movie details for ID: ${movieId}`);
  }
  return response.json();
};

const MyListPage = () => {
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  // 3. Lấy queryClient instance
  const queryClient = useQueryClient();

  // Query để lấy danh sách ID phim
  const {
    data: myListData = [],
    isLoading: isLoadingMyList,
    error: myListError,
  } = useQuery({
    queryKey: ["my-list", currentUser?.token],
    queryFn: () => fetchMyList(currentUser?.token),
    enabled: !!currentUser?.token,
  });

  // Dùng useQueries để lấy chi tiết từng phim
  const movieDetailsQueries = useQueries({
    queries: (myListData || []).map((movieId) => ({
      queryKey: ["movie", movieId],
      queryFn: () => fetchMovieDetails(movieId),
      enabled: !!myListData && myListData.length > 0,
    })),
  });

  // 4. Thiết lập mutation để xử lý việc xóa phim
  const removeMovieMutation = useMutation({
    mutationFn: removeFromMyList, // Hàm sẽ được gọi khi mutate()
    onSuccess: () => {
      // 5. Khi xóa thành công, vô hiệu hóa query "my-list".
      // Điều này sẽ khiến TanStack Query tự động gọi lại API `fetchMyList`,
      // cập nhật lại `myListData` và UI sẽ được render lại với danh sách mới.
      console.log("Movie removed! Invalidating my-list query...");
      queryClient.invalidateQueries({ queryKey: ["my-list", currentUser?.token] });
    },
    onError: (error) => {
      // (Tùy chọn) Xử lý lỗi, ví dụ hiển thị thông báo
      console.error("Failed to remove movie:", error);
      alert(error.message || "Could not remove the movie. Please try again.");
    }
  });

  // 6. Tạo hàm xử lý để gọi mutation
  const handleRemoveMovie = (movieId) => {
    if (!currentUser?.token) return;
    removeMovieMutation.mutate({ movieId, token: currentUser.token });
  };
  
  // Trạng thái loading và error
  const isLoading = isLoadingMyList || movieDetailsQueries.some((query) => query.isLoading);
  
  if (isLoading) return <div>Loading...</div>;
  if (myListError) return <div>Error: {myListError.message}</div>;

  const moviesList = movieDetailsQueries
    .filter((query) => query.isSuccess)
    .map((query) => query.data);
  if (!currentUser){
    navigate("/login");
  return null; // Trả về null nếu chưa đăng nhập
  }
  return (
    <div className='py-16'>
      <div className='container mx-auto'>
        <h3 className='capitalize text-lg lg:text-xl font-semibold my-3'>My List</h3>
        
        {moviesList.length > 0 ? (
          <div className='grid grid-cols-[repeat(auto-fit,260px)] gap-6 justify-center lg:justify-start'>
            {moviesList.map((movie, index) => {
              // 7. Xác định xem phim này có đang trong quá trình xóa hay không
              const isRemoving = 
                removeMovieMutation.isPending && 
                removeMovieMutation.variables?.movieId === movie[0].tconst;

              return (
                <Card 
                  key={movie[0].tconst || index} 
                  data={movie[0]} 
                  index={index} 
                  trending={false} 
                  // 8. Truyền hàm xử lý và trạng thái xóa xuống component Card
                  onRemove={handleRemoveMovie}
                  isRemoving={isRemoving}
                />
              );
            })}
          </div>
        ) : (
          <p>Your list is empty.</p>
        )}
      </div>
    </div>
  );
};

export default MyListPage;