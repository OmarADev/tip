from django.urls import path
from . import views

urlpatterns = [
    # Authentication Routes
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Homepage: List all itineraries
    path('', views.home, name='home'),

    # Itinerary Detail: View details of a specific itinerary
    path('itinerary/<int:pk>/', views.itinerary_detail, name='itinerary_detail'),

    # Create Itinerary: Form to create a new itinerary
    path('itinerary/create/', views.create_itinerary, name='create_itinerary'),

    # Edit Itinerary: Form to edit an existing itinerary
    path('itinerary/<int:pk>/edit/', views.edit_itinerary, name='edit_itinerary'),

    # Delete Itinerary: Confirm and delete an itinerary
    path('itinerary/<int:pk>/delete/', views.delete_itinerary, name='delete_itinerary'),

    # Share Itinerary: Generate a shareable link for an itinerary
    path('itinerary/<int:pk>/share/', views.share_itinerary, name='share_itinerary'),
]
