import requests

# ─────────────────────────────
# STEP 1: Login
# ─────────────────────────────
login_response = requests.post(
    'http://127.0.0.1:8000/api/users/login/',
    json={
        'username': 'testuser',
        'password': 'Test@1234'
    }
)

token = login_response.json()['tokens']['access']
print(f"✅ Login successful")
print(f"Token: {token[:30]}...")

headers = {'Authorization': f'Bearer {token}'}

# ─────────────────────────────
# STEP 2: Upload Resume
# ─────────────────────────────
with open('/home/myusername/Downloads/Riya_Resume.pdf', 'rb') as f:
    upload_response = requests.patch(
        'http://127.0.0.1:8000/api/users/profile/',
        headers=headers,
        files={'resume': f}
    )

print(f"\n✅ Resume Upload Status: {upload_response.status_code}")
print(upload_response.json())

# ─────────────────────────────
# STEP 3: Parse Resume
# ─────────────────────────────

parse_response = requests.post(
    'http://127.0.0.1:8000/api/agents/resume/parse/',
    headers=headers
)

print(f"\n✅ Parse Status: {parse_response.status_code}")
print(f"Response text: {parse_response.text}")