from app.config.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token
)

payload = {
    "user_id": 1,
    "email": "admin@retailpulse.com",
    "role": "Super Admin"
}

# Generate Access Token
access_token = create_access_token(payload)

# Generate Refresh Token
refresh_token = create_refresh_token(payload)

print("=" * 60)
print("ACCESS TOKEN")
print("=" * 60)
print(access_token)

print("\n")

print("=" * 60)
print("REFRESH TOKEN")
print("=" * 60)
print(refresh_token)

print("\n")

print("=" * 60)
print("DECODED ACCESS TOKEN")
print("=" * 60)
print(decode_token(access_token))