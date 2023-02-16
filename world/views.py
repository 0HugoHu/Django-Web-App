import json

from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.db.models import Q
import random
from .util import otp_generator, send_otp_email, validate_otp, validate_password
from .models import User, Trip, Vehicle


@login_required
def home(request):
    return render(request, "home.html")


@login_required
@csrf_exempt
def search(request):
    peer = ""
    if request.GET["joinShared"] == "true":
        peer = "available"

    current_time = datetime.now()
    pickup_hour = int(request.GET["estimatePickUpTime"].split(':')[0])
    pickup_min = int(request.GET["estimatePickUpTime"].split(':')[1])
    updated_time = current_time + timedelta(
        minutes=(60 * pickup_hour + pickup_min - 60 * current_time.hour - current_time.minute))

    trip_model = Trip(
        begin=request.GET["departure"],
        destination=request.GET["destination"],
        passenger=request.GET["email"],
        vehicle_type=request.GET["choice"],
        estimate_pickup_time=updated_time,
        estimate_fee=request.GET["estimateFee"],
        peer=peer,
    )
    trip_model.save(force_insert=True)
    result = {"success": True, "message": "Trip Requested!"}
    return JsonResponse(result)


def signup(request):
    return render(request, "signup.html")


@login_required
@csrf_exempt
def my_ride(request):
    result = {"ongoing": Trip.objects.filter(
        (Q(status='Request') | Q(status='Order Taking') | Q(status='In Progress')) & (
                Q(passenger=request.user.email) | Q(driver=request.user.email))),
        "completed": Trip.objects.filter(
            Q(status='Completed') & (Q(passenger=request.user.email) | Q(driver=request.user.email))),
        "cancelled": Trip.objects.filter(
            Q(status='Cancelled') & (Q(passenger=request.user.email) | Q(driver=request.user.email)))}

    return render(request, "my_ride.html", result)


@login_required
@csrf_exempt
def find_ride(request):
    return render(request, "my_ride.html")


@login_required
@csrf_exempt
def support(request):
    return render(request, "support.html")


@login_required
@csrf_exempt
def about(request):
    return render(request, "about.html")

@csrf_exempt
def vehicle(request):
    return render(request, "about.html")


@csrf_exempt
def vehicle_validate(request):
    return render(request, "about.html")


@csrf_exempt
def signup_validate(request):
    body = json.loads(request.body)
    email = body.get("email", "")
    first_name = body.get("first_name", "")
    last_name = body.get("last_name", "")
    username = body.get("username", "")
    gender = body.get("gender", "FEMALE")
    password = body.get("password", "")
    confirm_password = body.get("confirm_password", "")
    phone_number = body.get("phone_number", "")
    is_driver = body.get("is_driver", False)
    driver_license = body.get("driver_license", "")
    plate_number = body.get("plate_number", "")

    if not first_name:
        result = {"success": False, "message": "First name must be entered!"}
        return JsonResponse(result)

    if not last_name:
        result = {"success": False, "message": "Last name must be entered!"}
        return JsonResponse(result)

    if not username:
        result = {"success": False, "message": "User name must be entered!"}
        return JsonResponse(result)

    if not password:
        result = {"success": False, "message": "Password cannot be Null!"}
        return JsonResponse(result)

    if password != confirm_password:
        result = {"success": False, "message": "Two Passwords are not Equal!"}
        return JsonResponse(result)

    if not email:
        result = {"success": False, "message": "Email must be entered!"}
        return JsonResponse(result)

    if not phone_number:
        result = {"success": False, "message": "Phone number must be entered!"}
        return JsonResponse(result)

    if is_driver and (not driver_license):
        result = {"success": False, "message": "To register as a driver, your driver license ID must be entered!"}
        return JsonResponse(result)

    if is_driver and (not plate_number):
        result = {"success": False, "message": "To register as a driver, your vehicle plate number must be entered!"}
        return JsonResponse(result)

    user_group = "PASSENGER"
    if is_driver:
        user_group = "DRIVER"

    try:
        User.objects.create(email=email,
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                            password=password,
                            user_group=user_group,
                            driver_license=driver_license,
                            plate_number=plate_number,
                            phone_number=phone_number,
                            gender=gender
                            )
    except IntegrityError:
        result = {"success": False, "message": "User already exists! Try with a different email!"}
        return JsonResponse(result)

    if user_group == "DRIVER":
        vehicle_model = Vehicle(plate_number=plate_number)
        vehicle_model.save(force_insert=True)

    otp = otp_generator()
    otp_status = send_otp_email(email, otp)

    if not otp_status:
        result = {"success": False, "message": "Incorrect email!"}
        return JsonResponse(result)

    request.session["auth_otp"] = otp
    request.session["auth_email"] = email
    # cache.set('{0}_auth_otp'.format(request.session.session_key), otp, 120)
    # cache.set('{0}_auth_email'.format(request.session.session_key), email, 120)
    result = {"success": True, "message": "Verification code has sent to email!"}
    return JsonResponse(result)


def c_login(request):
    return render(request, "login.html")


@csrf_exempt
def send_otp(request):
    '''
    When you will click on 'Send Otp" button on front end then ajax call will be hit and
    that lead to call this function
    '''
    body = json.loads(request.body)
    email = body.get("email", "")

    otp = otp_generator()
    otp_status = send_otp_email(email, otp)
    if not otp_status:
        result = {"success": False, "message": "incorrect email"}
        return JsonResponse(result)

    request.session["auth_otp"] = otp
    request.session["auth_email"] = email
    # cache.set('{0}_auth_otp'.format(request.session.session_key), otp, 120)
    # cache.set('{0}_auth_email'.format(request.session.session_key), email, 120)

    result = {"successs": True, "message": "otp sent"}
    return JsonResponse(result)


@csrf_exempt
def login_validate(request):
    body = json.loads(request.body)
    sent_otp = request.session.get("auth_otp", "")
    sent_email = request.session.get("auth_email", "")

    email = body.get("email", "")
    otp = body.get("otp", "")

    try:
        user = User.objects.get(email=email)
        password = user.password
    except ObjectDoesNotExist:
        result = {"success": False, "message": "This email has not been registered!"}
        return JsonResponse(result)

    result = validate_otp(otp, sent_otp, email, sent_email)

    if not result["success"]:
        password_result = validate_password(email, password, otp)
        if not password_result["success"]:
            return JsonResponse(password_result)

    login(request, user)
    result = {"success": True, "message": "Login Succeeds!"}
    return JsonResponse(result)


@login_required
def c_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")


@login_required
def c_profile(request):
    return render(request, "profile.html")


@csrf_exempt
def get_trip_details(request, trip_id):
    if not trip_id:
        trip_id = 1
    try:
        trip = Trip.objects.get(id=int(trip_id))
    except ObjectDoesNotExist:
        trip = {}

    result = {"trip": trip}

    return render(request, "trip.html", result)


@csrf_exempt
def trip_validate(request):
    body = json.loads(request.body)
    departure = body.get("departure", "")
    destination = body.get("destination", "")
    vehicle_type = body.get("vehicle_type", "")
    trip_id = body.get("id", "")

    try:
        if departure:
            Trip.objects.filter(id=trip_id).update(
                departure=departure,
            )

        if destination:
            Trip.objects.filter(id=trip_id).update(
                destination=destination,
            )

        Trip.objects.filter(id=trip_id).update(
            vehicle_type=vehicle_type,
        )

    except ObjectDoesNotExist:
        result = {"success": False, "message": "Unknown error happens! Please try again!"}
        return JsonResponse(result)

    result = {"success": True, "message": "trip Updated!"}
    return JsonResponse(result)


@login_required
@csrf_exempt
def trip_cancel(request):
    body = json.loads(request.body)
    trip_id = body.get("id", "")
    Trip.objects.filter(id=trip_id).update(
        status='Cancelled',
    )
    result = {"success": True, "message": "Picked-up Passenger!"}
    return JsonResponse(result)


@login_required
@csrf_exempt
def trip_pickup(request):
    body = json.loads(request.body)
    pickup_time = body.get("pickup_time", "")
    trip_id = body.get("id", "")
    Trip.objects.filter(id=trip_id).update(
        pickup_time=pickup_time,
    )
    result = {"success": True, "message": "Picked-up Passenger!"}
    return JsonResponse(result)


@login_required
@csrf_exempt
def trip_complete(request):
    body = json.loads(request.body)
    arrive_time = body.get("arrive_time", "")
    trip_id = body.get("id", "")
    Trip.objects.filter(id=trip_id).update(
        arrive_time=arrive_time,
        actual_fee=Trip.objects.get(id=trip_id).estimate_fee + round(random.random() * 10 - 5, 2)
    )
    result = {"success": True, "message": "Completed Trip!"}
    return JsonResponse(result)


@csrf_exempt
def profile_validate(request):
    body = json.loads(request.body)
    email = body.get("email", "")
    username = body.get("username", "")
    gender = body.get("gender", "")
    password = body.get("password", "")
    phone_number = body.get("phone_number", "")
    is_driver = body.get("is_driver", False)
    driver_license = body.get("driver_license", "")
    plate_number = body.get("plate_number", "")

    if is_driver and (not driver_license):
        result = {"success": False, "message": "To register as a driver, your driver license ID must be entered!"}
        return JsonResponse(result)

    if is_driver and (not plate_number):
        result = {"success": False, "message": "To register as a driver, your vehicle plate number must be entered!"}
        return JsonResponse(result)

    try:
        if username:
            User.objects.filter(email=email).update(
                username=username,
            )

        if password:
            User.objects.filter(email=email).update(
                password=password,
            )

        if gender:
            User.objects.filter(email=email).update(
                gender=gender,
            )

        if phone_number:
            User.objects.filter(email=email).update(
                phone_number=phone_number,
            )

        if is_driver:
            User.objects.filter(email=email).update(
                driver_license=driver_license,
                car_number=plate_number,
                user_group="DRIVER",
            )

        if not is_driver and driver_license:
            User.objects.filter(email=email).update(
                driver_license=driver_license,
            )

        if not is_driver and plate_number:
            User.objects.filter(email=email).update(
                plate_number=plate_number,
            )

    except ObjectDoesNotExist:
        result = {"success": False, "message": "Unknown error happens! Please try again!"}
        return JsonResponse(result)

    result = {"success": True, "message": "Profile Updated!"}
    return JsonResponse(result)
