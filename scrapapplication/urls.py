"""
URL configuration for scrapapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scrapapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegistrationView.as_view(),name='sign-up'),
    path('',views.SignInView.as_view(),name='sign-in'),
    path('logout/',views.SignOutView.as_view(),name='sign-out'),
    path('home/',views.HomeView.as_view(),name='home'),
    path('profiles/<int:pk>/change',views.ProfileUpdateView.as_view(),name='update-profile'),
    path('profiles/<int:pk>',views.ProfileDetailsView.as_view(),name='profile-det'),
    path('scrap/',views.ScrapAddView.as_view(),name='scrap-add'),
    path('scrap/<int:pk>/change',views.ScrapUpdateView.as_view(),name='scrap-update'),
    path('scrap/<int:pk>',views.ScrapDetailView.as_view(),name='scrap-detail'),
    path('wishlist/<int:scrap_id>/',views.WishlistView.as_view(),name='wishlist_toggle'),
    path('wishlist/', views.WishlistProductsView.as_view(), name='wishlist_products'),
    path('scrap/<int:scrap_id>/bids/add/',views.BidsAddView.as_view(),name='bids'),
    path('bids/',views.BidsListView.as_view(),name='bidslist'),
    path('bids/<int:pk>/remove',views.BidsDeleteView.as_view(),name='bid-delete'),
    path('scrap/<int:pk>/remove',views.ScrapDeleteView.as_view(),name='scrap-remove'),
    path('bids/<int:pk>',views.BidRequestView.as_view(),name='bid-request'),
    path('wishlist/delete/<int:pk>',views.WishlistDeleteView.as_view(),name='wishlist-delete')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
