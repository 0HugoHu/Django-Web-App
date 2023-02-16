import string
import random

from django.core.mail import EmailMessage


def otp_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_otp_email(email, otp):
    try:
        message = "Welcome!\n\nYour verification code is %s\n\nUse this code to complete email verification.\n\nBest,\nHugo Ride Registration Team" % (
            otp)
        email = EmailMessage('Hugo Ride: Verification Code', message, to=[email])
        email.send()
    except Exception:
        return False

    return True


def send_confirmation_email(email, driver):
    try:
        message = "Hi!\n\nYour ride has been confirmed by a driver: %s\n\nEnjoy your safe and convenient ride!\n\nBest,\nHugo Ride Registration Team" % (
            driver)
        email = EmailMessage('Hugo Ride: Trip Confirmed', message, to=[email])
        email.send()
    except Exception:
        return False

    return True


def validate_otp(otp, sent_otp, email, sent_email):
    if not sent_otp or not sent_email:
        result = {"success": False, "message": "Session has expired! Please request again!"}
        return result

    if not email or not otp:
        result = {"success": False, "message": "Your email has not been registered!"}
        return result

    if otp != sent_otp:
        result = {"success": False, "message": "Your verification code is wrong!"}
        return result

    if email != sent_email:
        result = {"success": False, "message": "Your email has not been registered!"}
        return result

    result = {"success": True, "message": "Verified"}
    return result


def validate_password(email, password, entered_password):
    if not email:
        result = {"success": False, "message": "Email required!"}
        return result

    if not entered_password:
        result = {"success": False, "message": "OTP or Password required!"}
        return result

    if password != entered_password:
        result = {"success": False, "message": "Wrong Password!"}
        return result

    result = {"success": True, "message": "Verified"}
    return result
