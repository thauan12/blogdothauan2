from django.urls import path
# from .views import ListarPostsListView, IndexView, DetalhePostView, FormContatoView
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('listar/', views.ListarPostsListView.as_view(), name='listar_posts'),
    path('detalhe/<int:ano>/<int:mes>/<int:dia>/<slug:slug>',
         views.DetalhePostView.as_view(), name='detalhe_post'),
    path('enviarpost/<int:pk>/',
         views.FormContatoView.as_view(),
         name='enviar_post'),
    path('comentar/<int:pk>/', views.ComentarioCreateView.as_view(), name='comentar_post'),
    path('cadusuario/', views.CadUsuarioView.as_view(), name='cadusuario'),
    path('login/', views.LoginUsuarioView.as_view(), name='loginuser'),
    path('logout/', views.LogoutView.as_view(), name='logoutuser'),
]