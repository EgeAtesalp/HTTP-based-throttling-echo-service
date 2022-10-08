import uvicorn



def main():
    config = uvicorn.Config("app.app:app", port=8000, log_level="info", reload = True)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()