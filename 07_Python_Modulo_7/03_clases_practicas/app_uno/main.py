from jose import jwt
from datetime import datetime, timedelta, timezone
import secrets

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

def main():
    data = {
        "sub":"usuario123",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    print("\nToken JWT generado:\n")
    print(token + "\n")

if __name__ == "__main__":
    main()
    
