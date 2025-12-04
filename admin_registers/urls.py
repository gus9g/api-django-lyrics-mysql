from django.urls import path 
from admin_registers import views 

urlpatterns = [
    path('', views.index, name='index'),

    path('genre', views.musicalGenre, name='genre'),
    path('genre/add', views.musicalGenreAdd, name='genre_add'),
    path('genre/alter', views.musicalGenreAlter, name='genre_alter'),
    path('genre/remove', views.musicalGenreRemove, name='genre_remove'),
    
    path('band', views.band, name='band'),
    path('band/add', views.bandAdd, name='band_add'),
    path('band/alter', views.bandAlter, name='band_alter'),
    path('band/remove', views.bandRemove, name='band_remove'),

    path('album', views.album, name='album'),
    path('album/add', views.albumAdd, name='album_add'),
    path('album/alter', views.albumAlter, name='album_alter'),
    path('album/remove', views.albumRemove, name='album_remove'),
    
    path('song', views.song, name='song'),
    path('song/add', views.songAdd, name='song_add'),
    path('song/alter', views.songAlter, name='song_alter'),
    path('song/remove', views.songRemove, name='song_remove'),
]
