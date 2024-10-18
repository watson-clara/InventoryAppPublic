from app import create_app
import os


app = create_app()

if __name__ == '__main__':
    print(app.url_map)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)