from user_service_v2.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)