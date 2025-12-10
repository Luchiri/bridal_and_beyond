from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.auth_landing, name='auth_landing'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('create_board/', views.create_board, name='create_board'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/', views.view_board, name='view_board'),
    path('rename-board/<int:board_id>/', views.rename_board, name='rename_board'),
    path('delete-board/<int:board_id>/', views.delete_board, name='delete_board'),
    path('profile/', views.profile, name='profile'),
    path('home', views.home, name='home'),
    path("save-image/", views.save_image, name="save_image"),
    path('vendors/', views.vendors, name='vendors'),
    path('inspiration/', views.inspiration_view, name='inspiration'),
    path('color-palettes/', views.color_palettes, name='color_palettes'),
    path('blog-tips/', views.blog_tips, name='blog_tips'),
    path("bride/", views.bride_view, name="bride"),
    path("groom/", views.groom_view, name="groom"),
    path("honor/", views.honor, name="honor"),
    path("maid/", views.maid, name="maid"),
    path("men/", views.men, name="men"),
    path("girls/", views.girls, name="girls"),
    path("boys/", views.boys, name="boys"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
