import json

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
)
from webauthn.helpers import options_to_json
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
    RegistrationCredential,
    AuthenticationCredential,
)

from .models import UserPasskey


TOKEN_COOKIE_NAME = getattr(settings, "PASSKEY_TOKEN_COOKIE_NAME", "auth_token")


def parse_registration_credential(data):
    raw = json.dumps(data)
    if hasattr(RegistrationCredential, "model_validate_json"):
        return RegistrationCredential.model_validate_json(raw)
    return RegistrationCredential.parse_raw(raw)


def parse_authentication_credential(data):
    raw = json.dumps(data)
    if hasattr(AuthenticationCredential, "model_validate_json"):
        return AuthenticationCredential.model_validate_json(raw)
    return AuthenticationCredential.parse_raw(raw)


def set_token_cookie(response, token_key: str):
    response.set_cookie(
        TOKEN_COOKIE_NAME,
        token_key,
        httponly=True,
        secure=True,
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 30,
    )
    return response
 
 
 
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def passkey_register_options(request):
    user = request.user

    exclude_credentials = [
        PublicKeyCredentialDescriptor(id=bytes(passkey.credential_id))
        for passkey in UserPasskey.objects.filter(user=user)
    ]

    options = generate_registration_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        rp_name=settings.WEBAUTHN_RP_NAME,
        user_id=str(user.pk).encode("utf-8"),
        user_name=getattr(user, "email", None) or user.get_username(),
        user_display_name=user.get_username(),
        exclude_credentials=exclude_credentials,
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.REQUIRED,
            user_verification=UserVerificationRequirement.REQUIRED,
        ),
    )

    request.session["passkey_registration_challenge"] = options.challenge.hex()

    return Response(json.loads(options_to_json(options)))
 


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def passkey_register_verify(request):
    challenge_hex = request.session.get("passkey_registration_challenge")

    if not challenge_hex:
        return Response(
            {"detail": "Registration challenge fehlt."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    credential = parse_registration_credential(request.data)

    try:
        verification = verify_registration_response(
            credential=credential,
            expected_challenge=bytes.fromhex(challenge_hex),
            expected_origin=settings.WEBAUTHN_ORIGIN,
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            require_user_verification=True,
        )
    except Exception as exc:
        return Response(
            {"verified": False, "detail": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    UserPasskey.objects.create(
        user=request.user,
        name=request.data.get("name", "Passkey"),
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
        device_type=str(getattr(verification, "credential_device_type", "")),
        backed_up=bool(getattr(verification, "credential_backed_up", False)),
        transports=request.data.get("response", {}).get("transports", []),
    )

    request.session.pop("passkey_registration_challenge", None)

    return Response({"verified": True})
 
 
 

# 3. Login ohne E-Mail: Options

# Hier kein User, keine E-Mail, keine allow_credentials.

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def passkey_login_options(request):
    options = generate_authentication_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        user_verification=UserVerificationRequirement.REQUIRED,
    )

    request.session["passkey_login_challenge"] = options.challenge.hex()

    return Response(json.loads(options_to_json(options)))

# Das ist der entscheidende Unterschied zum alten Code.

# Vorher:

# allow_credentials = [...]

# Jetzt:

# # keine allow_credentials

# Dadurch kann der Browser auch einen Passkey von einem anderen Gerät anbieten, z. B. per QR-Code/Smartphone, wenn Browser und Gerät das unterstützen.

# 4. Login ohne E-Mail: Verify + DRF Token Cookie setzen
import base64


def base64url_to_bytes(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def passkey_login_verify(request):
    challenge_hex = request.session.get("passkey_login_challenge")

    if not challenge_hex:
        return Response(
            {"detail": "Login challenge fehlt."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    raw_id = request.data.get("rawId")

    if not raw_id:
        return Response(
            {"detail": "rawId fehlt."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        credential_id = base64url_to_bytes(raw_id)
    except Exception:
        return Response(
            {"detail": "rawId ist ungültig."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        passkey = UserPasskey.objects.select_related("user").get(
            credential_id=credential_id
        )
    except UserPasskey.DoesNotExist:
        return Response(
            {"detail": "Unbekannter Passkey."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    credential = parse_authentication_credential(request.data)

    try:
        verification = verify_authentication_response(
            credential=credential,
            expected_challenge=bytes.fromhex(challenge_hex),
            expected_origin=settings.WEBAUTHN_ORIGIN,
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            credential_public_key=bytes(passkey.public_key),
            credential_current_sign_count=passkey.sign_count,
            require_user_verification=True,
        )
    except Exception as exc:
        return Response(
            {"verified": False, "detail": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    passkey.sign_count = verification.new_sign_count
    passkey.last_used_at = timezone.now()
    passkey.save(update_fields=["sign_count", "last_used_at"])

    token, _ = Token.objects.get_or_create(user=passkey.user)

    request.session.pop("passkey_login_challenge", None)

    response = Response(
        {
            "verified": True,
            "user_id": passkey.user.pk,
        }
    )

    set_token_cookie(response, token.key)

    return response