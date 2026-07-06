"""
Kosh Ticketing - Upload Routes
Handles file uploads for event images
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid

uploads_bp = Blueprint('uploads', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@uploads_bp.route('/image', methods=['POST'])
def upload_image():
    """Upload event image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)

        if size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Max 5MB'}), 400

        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{ext}"

        # In production, upload to S3/Cloudinary
        # For now, return mock URL
        mock_url = f"/uploads/{filename}"

        return jsonify({
            'message': 'Upload successful',
            'url': mock_url,
            'filename': filename
        }), 200

    except Exception as e:
        return jsonify({'error': 'Upload failed', 'details': str(e)}), 500
