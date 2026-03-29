from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request,
    get_jwt_identity
)

# ---------------- TOKEN HELPERS ----------------
def set_auth_cookies(response, identity):
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=False,
        samesite="Lax"
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax"
    )

    return response


# ---------------- AUTH CORE ----------------
def get_current_user():
    """
    Try:
    1. Access token
    2. Refresh token (silent refresh)
    Returns:
        (user, refresh_needed)
    """

    # Try access token
    try:
        verify_jwt_in_request()
        return get_jwt_identity(), False
    except Exception:
        pass

    # Try refresh token
    try:
        verify_jwt_in_request(refresh=True)
        return get_jwt_identity(), True
    except Exception:
        return None, False

# ---------------- API HELPER ----------------

def api_auth_required():
    """
    Used for /api routes (JSON-based)
    """

    user, needs_refresh = get_current_user()

    if not user:
        return None, jsonify({"error": "auth_required"}), 401

    response = None
    if needs_refresh:
        response = make_response()
        response = set_auth_cookies(response, user)

    return user, response, None

