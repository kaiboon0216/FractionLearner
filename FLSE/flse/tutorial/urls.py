from django.urls import path
from . import views
from .views import TutorialDetailView,TutorialListView,TutorialUpdateView,TutorialCreateView,TutorialDeleteView,CommentDeleteView,CommentUpdateView,QcommentDeleteView,QcommentUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.home, name= 'tutorial-home'),
    path("tutorial/<int:pk>/", TutorialDetailView.as_view(), name='tutorial-detail'),
    path('tutorial/<int:pk>/delete/', TutorialDeleteView.as_view(),name='tutorial-delete'),
    path('addquestion/', views.addquestion,name='add-question'),
    path("search/", views.search),
    path("upload/notes/",views.upload,name='new-notes'),
    path("tutorial/", login_required(TutorialListView.as_view()), name="tutorial"),
    path('tutorial/<int:pk>/update/', TutorialUpdateView.as_view(),name='tutorial-update'),
    path("newquestion/", TutorialCreateView.as_view(), name='new-tutorial'),
    path("tutorial/<int:pk>/vote/", views.tutorial_like, name='vote_tutorial'),
    path("tutorial/<int:pk>/comment/", views.add_comment, name='comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(),name='comment-delete'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(),name='comment-update'),
    path("comment/<int:pk>/vote/", views.comment_like, name='vote'),
    path("comment/<int:pk>/qcomment/", views.add_qcomment, name='qcomment'),
    path('qcomment/<int:pk>/update/', QcommentUpdateView.as_view(),name='qcomment-update'),
    path('qcomment/<int:pk>/delete/', QcommentDeleteView.as_view(),name='qcomment-delete'),
    path("qcomment/<int:pk>/vote/", views.qcomment_like, name='qvote'),
    path("qcomment/<int:pk>/solution/", views.SolutionView, name='solution'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)