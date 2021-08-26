from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("cards/", login_required(views.CardListView.as_view()), name="cards"),
    path("cards/<slug:pk>", login_required(views.CardDetailView.as_view()), name="card"),
    path("cards/<int:id>/edit", views.update_view, name="card_edit"),
    path("cards/purchase/<int:purchase_id>", views.purchase_info, name="purchase_info"),    
    path("generate/", views.generate, name="generate"),
    path("generate/ready", views.generate, name="ready"),
    path("generate/send_to_db", views.generate, name="send_to_db"),
    path("accounts/", include("django.contrib.auth.urls")),

]
