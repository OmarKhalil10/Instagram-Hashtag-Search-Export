from flask import Flask, redirect, request, render_template, jsonify
import requests
import os

def create_app(test_config=None):
    # Create and configure the app
    template_dir = os.path.abspath('templates')

    # Initialize the app
    app = Flask(__name__, template_folder=template_dir)

    # Load default config from settings.py
    app.config.from_pyfile('settings.py')

    # Configure Facebook OAuth
    app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
    app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")

    # Your Facebook app details
    app.config["redirect_url"] = 'https://127.0.0.1:8080/oauth/facebook/authorized'
    auth_url = 'https://www.facebook.com/v18.0/dialog/oauth'
    token_url = 'https://graph.facebook.com/v18.0/oauth/access_token'
    graph_url = 'https://graph.facebook.com/v18.0/'

    # Your Instagram account details and access token
    client_id = app.config["CLIENT_ID"]
    client_secret = app.config["CLIENT_SECRET"]
    redirect_url = app.config["redirect_url"]
    instagram_account_id = 'ADD_YOUR_INSTAGRAM_ACCOUNT_ID_HERE'
    access_token = 'ADD_ACCESS_TOKEN_HERE'

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/oauth/facebook/authorized', methods=['GET'])
    def authorized():
        global long_lived_access_token  # Add this line
        if 'code' in request.args:
            # Step 1: Get the short-lived access token
            code = request.args.get('code', '')
            short_lived_token = get_short_lived_token(code)

            # Step 2: Exchange short-lived token for a long-lived token
            long_lived_access_token = exchange_for_long_lived_token(short_lived_token)

            return f'Long-lived Access Token: {long_lived_access_token}'

        return 'Authorization failed. Please try again.'

    @app.route('/')
    def index():
        return render_template('pages/index.html')

    @app.route('/get_url', methods=['POST'])
    def get_url():
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_url,
            'scope': 'pages_show_list,instagram_basic,instagram_manage_comments,instagram_manage_insights,pages_read_engagement'
        }
        auth_redirect_url = f"{auth_url}?{'&'.join(f'{key}={val}' for key, val in params.items())}"
        return redirect(auth_redirect_url)

    def get_short_lived_token(code):
        params = {
            'client_id': client_id,
            'client_secret': client_secret,  # Corrected variable name
            'code': code,
            'redirect_uri': redirect_url
        }
        response = requests.get(url=token_url, params=params, verify=True)
        response_json = response.json()
        short_lived_token = response_json.get('access_token', '')
        return short_lived_token

    def exchange_for_long_lived_token(short_lived_token):
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': client_id,
            'client_secret': client_secret,  # Corrected variable name
            'fb_exchange_token': short_lived_token
        }
        response = requests.get(url=token_url, params=params, verify=True)
        response_json = response.json()
        long_lived_token = response_json.get('access_token', '')
        return long_lived_token

    @app.route('/get_hashtag_id', methods=['GET'])
    def route_get_hashtag_id():
        hashtag = request.args.get('hashtag')
        hashtag_id = get_hashtag_id(hashtag=hashtag, instagram_account_id=instagram_account_id, access_token=access_token)
        return jsonify({'hashtag_id': hashtag_id})

    @app.route('/get_data_of_hashtag', methods=['GET'])
    def route_get_data_of_hashtag():
        hashtag_id = request.args.get('hashtag_id')  # Provide the actual hashtag_id
        hashtag_data = get_data_of_hashtag(hashtag_id=hashtag_id, access_token=access_token)
        return jsonify({'hashtag_data': hashtag_data})

    @app.route('/get_top_media', methods=['GET'])
    def route_get_top_media():
        hashtag_id = request.args.get('hashtag_id')  # Provide the actual hashtag_id
        top_media_data = get_top_media(hashtag_id=hashtag_id, access_token=access_token, instagram_account_id=instagram_account_id)
        return jsonify({'top_media_data': top_media_data})

    @app.route('/get_recent_media', methods=['GET'])
    def route_get_recent_media():
        hashtag_id = request.args.get('hashtag_id')  # Provide the actual hashtag_id
        recent_media_data = get_recent_media(hashtag_id=hashtag_id, access_token=access_token, instagram_account_id=instagram_account_id)
        return jsonify({'recent_media_data': recent_media_data})

    @app.route('/get_recent_searched_hashtag', methods=['GET'])
    def route_get_recent_searched_hashtag():
        searched_hashtags = get_recent_searched_hashtag(instagram_account_id=instagram_account_id, access_token=access_token)
        return jsonify({'searched_hashtags': searched_hashtags})

    # Hashtag search functions based on the article
    def get_hashtag_id(hashtag='', instagram_account_id='', access_token=''):
        url = graph_url + 'ig_hashtag_search'
        params = {'user_id': instagram_account_id, 'q': hashtag, 'access_token': access_token}
        response = requests.get(url, params=params)
        
        try:
            response_json = response.json()
            hashtag_id = response_json['data'][0]['id']
            return hashtag_id
        except (KeyError, IndexError):
            # Handle the cases where 'data' or 'id' keys are not present in the response
            return None

    def get_data_of_hashtag(hashtag_id='', access_token=''):
        url = graph_url + hashtag_id
        params = {'access_token': access_token, 'fields': 'id,name'}
        response = requests.get(url, params=params)
        response_json = response.json()
        return response_json

    def get_top_media(hashtag_id='', access_token='', instagram_account_id=''):
        url = graph_url + hashtag_id + '/top_media'
        params = {'access_token': access_token, 'user_id': instagram_account_id, 'fields': 'caption,like_count,permalink'}
        response = requests.get(url, params=params)
        response_json = response.json()
        return response_json

    def get_recent_media(hashtag_id='', access_token='', instagram_account_id=''):
        url = graph_url + hashtag_id + '/recent_media'
        params = {'access_token': access_token, 'user_id': instagram_account_id, 'fields': 'caption,like_count,permalink'}
        response = requests.get(url, params=params)
        response_json = response.json()
        return response_json

    def get_recent_searched_hashtag(instagram_account_id='', access_token=''):
        url = graph_url + instagram_account_id + '/recently_searched_hashtags'
        params = {'access_token': access_token, 'limit': 30}
        response = requests.get(url, params=params)
        response_json = response.json()
        return response_json

    @app.errorhandler(404)
    def not_found(error):
        return render_template('pages/errors/404.html',data={
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template('pages/errors/405.html', data={
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessed(error):
        return render_template('pages/errors/422.html',data={
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def unauthorized(error):
        return render_template('pages/errors/500.html',data={
            'success': False,
            'error': 500,
            'message': 'Unauthorized'
        }), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080, ssl_context=('server.crt', 'server.key'))