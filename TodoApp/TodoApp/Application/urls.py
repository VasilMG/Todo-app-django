from django.conf import settings
from django.urls import path
from django.conf.urls.static import static


from TodoApp.Application.views import index_view, create_todo, edit_todo, delete_todo, download

urlpatterns = [
    path('', index_view, name='index'),
    path('crete-todo/', create_todo, name='create_todo'),
    path('edit/<int:pk>/', edit_todo, name= 'edit'),
    path('delete/<int:pk>/', delete_todo, name= 'delete'),
    path('download/', download, name= 'download'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
