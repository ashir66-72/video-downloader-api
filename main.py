import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from yt_dlp import YoutubeDL

app = Flask(__name__)
CORS(app)  # Allows your frontend to securely fetch files

DOWNLOAD_DIR = "/tmp"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'best', 
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['default']}},
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
        return send_file(filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Koyeb passes the port dynamically via environment variables, defaulting to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
