from django.urls import path
from films import views
from films.constants import LIST_CREATE, RETRIEVE_UPDATE_DESTROY

urlpatterns = [
    path('', views.MovieListCreateAPIView.as_view()),  # GET->list, POST->create
    path('<int:id>/', views.movie_detail_api_view),  # GET->item, PUT->update, DELETE->destroy
    path('directors/', views.DirectorListCreateAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view()),
    path('genres/', views.GenreViewSet.as_view(LIST_CREATE)),
    path('genres/<int:id>/', views.GenreViewSet.as_view(RETRIEVE_UPDATE_DESTROY))
]
