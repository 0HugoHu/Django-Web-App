import json

from django.shortcuts import render
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from haystack.query import SearchQuerySet

from .util import otp_generator, send_otp_email, validate_otp, validate_password
from .models import User, City, Country, Countrylanguage


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def search(request):
    query = request.GET.get("query", "").strip()
    result = {"cities": [], "countries": [], "languages": []}

    if not query and len(query) < 3:
        return JsonResponse(result)

    city_pks = list(SearchQuerySet().autocomplete(i_city_name=query).values_list("pk", flat=True))
    country_pks = list(SearchQuerySet().autocomplete(i_country_name=query).values_list("pk", flat=True))
    language_pks = list(SearchQuerySet().autocomplete(i_language_name=query).values_list("pk", flat=True))

    result["cities"] = [City.objects.filter(pk=city_pk).values().first() for city_pk in city_pks]
    result["countries"] = [Country.objects.filter(pk=country_pk).values().first() for country_pk in country_pks]
    result["languages"] = [Countrylanguage.objects.filter(pk=language_pk).values().first() for language_pk in
                           language_pks]

    return render(request, "search_results.html", result)


def signup(request):
    return render(request, "signup.html")


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


@login_required
def get_country_details(request, country_name):
    country = Country.objects.get(name=country_name)
    result = {"country": country}

    return render(request, "country.html", result)


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
