import sys

import pymongo
from fastapi import FastAPI
from fastapi.security import OAuth2Bearer

version = f"{sys.version_info.major}.{sys.version_info.minor}"

oauth2_scheme = OAuth2Bearer(tokenUrl="https://YOUR_AUTH0_DOMAIN/oauth/token")

app = FastAPI()

AUTH0_DOMAIN = "YOUR_AUTH0_DOMAIN"
API_AUDIENCE = "YOUR_API_IDENTIFIER"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            algorithms=["RS256"],
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
        user_id = payload["sub"]
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id


@app.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user)):
    return {"message": f"Hello, {user_id}!"}


@app.get("/")
async def hello():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}


@app.get("/run")
def run_block():
    """Run a given block in a container and return the result"""
    import os
    from uuid import uuid4

    import docker

    block = request.get_json()

    client = docker.from_env()

    _uuid = str(uuid4())
    try:
        with open("/tmp/" + _uuid, "w") as pfile:
            pfile.write(block["block"]["code"] + "\n\n")
            pfile.write(block["call"] + "\n")
            print(block["block"]["code"] + "\n\n")
            print(block["call"] + "\n")

        result = client.containers.run(
            block["block"]["containerimage"],
            auto_remove=False,
            volumes={"/tmp": {"bind": "/tmp/", "mode": "rw"}},
            entrypoint="",
            command="python /tmp/" + _uuid,
        )
        result = result.decode("utf-8").strip()
        return result
    finally:
        os.remove("/tmp/" + _uuid)
