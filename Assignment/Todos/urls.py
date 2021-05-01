from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('customer_login/',views.clogin,name="clogin"),
    path('moderator_login/',views.mlogin,name="mlogin"),
    path('customer_todos',views.cTodos,name="ctodos"),
    path('add_todo/',views.addTodo,name="addTodo"),
    path('moderator_todos',views.mTodos,name='mtodos'),
    path('logout/',views.logout1,name="logout"),
    path('todos/<str:id>',views.todos.as_view(),name="todos"),
    path('mark_complete/<int:id>',views.markComplete,name="markComplete")
]
