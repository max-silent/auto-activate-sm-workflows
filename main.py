import logging

from config import settings
from fastapi import FastAPI


logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--openapi-file")
    args = parser.parse_args()
    if args.openapi_file:
        from fastapi.testclient import TestClient

        client = TestClient(app)
        r = client.get("/openapi.json")
        if r.status_code == 200:
            try:
                with open(args.openapi_file, "w") as f:
                    f.write(r.text)
            except Exception as e:
                logger.exception(f"Exception {e} writing file {args.openapi_file}")
        else:
            logger.error("Could not retrive openapi file from FastAPI app")
    else:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=5000)