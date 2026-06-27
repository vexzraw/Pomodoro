from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Carga las variables desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Lee la clave de las variables de entorno
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.route('/api/search')
def search_youtube():
    query = request.args.get('q', '')
    if not query or not YOUTUBE_API_KEY:
        return jsonify({"error": "Falta API Key o Query"}), 400

    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        req = youtube.search().list(
            q=query, 
            part='snippet', 
            type='video', 
            maxResults=10, 
            videoCategoryId=10
        )
        res = req.execute()
        
        videos = []
        for v in res.get('items', []):
            videos.append({
                'id': v['id']['videoId'],
                'title': v['snippet']['title'],
                'artist': v['snippet']['channelTitle']
            })
        return jsonify(videos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
