from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^signup$', views.signup, name="signup"),
    re_path(r"^signup/validate$", views.signup_validate, name="signup_validate"),
    re_path(r'^login$', views.c_login, name="login"),
    re_path(r'^login/send_otp$', views.send_otp, name="send_otp"),
    re_path(r"^login/validate$", views.login_validate, name="login_validate"),
    re_path(r'^search$', views.search, name="search"),
    re_path(r'^vehicle$', views.vehicle, name="vehicle"),
    re_path(r'^vehicle/validate$', views.vehicle_validate, name="vehicle_validate"),
    re_path(r"^trip/validate", views.trip_validate, name="trip_validate"),
    re_path(r"^trip/cancel", views.trip_cancel, name="trip_cancel"),
    re_path(r"^trip/pickup", views.trip_pickup, name="trip_pickup"),
    re_path(r"^trip/complete", views.trip_complete, name="trip_complete"),
    re_path(r'trip/(?P<trip_id>[0-9]+)', views.get_trip_details, name="get_trip_details"),
    re_path(r'^logout$', views.c_logout, name="logout"),
    re_path(r'^my_ride', views.my_ride, name="my_ride"),
    re_path(r'^find_ride', views.find_ride, name="find_ride"),
    re_path(r'^support', views.support, name="support"),
    re_path(r'^about', views.about, name="about"),
    re_path(r'^profile$', views.c_profile, name="profile"),
    re_path(r"^profile/validate", views.profile_validate, name="profile_validate"),
]
