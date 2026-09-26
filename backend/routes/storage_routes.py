"""
Storage Routes (Cloud Storage Simulation)
==========================================
Handles file upload, download, listing, and deletion.
Simulates cloud object storage using local filesystem.

In production, replace with Firebase Storage, AWS S3, or GCS.

Endpoints:
    POST   /api/storage/upload    - Upload a file
    GET    /api/storage/files     - List user's files
    GET    /api/storage/files/<id>/download - Download a file
    DELETE /api/storage/files/<id> - Delete a file

Cloud Computing Concepts Demonstrated:
- Cloud Object Storage: Storing unstructured data (files/images)
- User-scoped Storage: Each user has isolated file storage
- Difference: Cloud DB (structured) vs Object Storage (files)
"""

import os
import json
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from models.database import get_db
from utils.auth_helpers import token_required, generate_file_id

storage_bp = Blueprint('storage', __name__)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'json', 'csv'}


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_user_upload_dir(user_id):
    """
    Get user-specific upload directory.
    Simulates cloud storage bucket/folder per user.
    """
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], user_id)
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


@storage_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(user_id):
    """
    Upload a file to cloud storage (simulated).
    
    Files are stored in user-specific directories to simulate
    cloud storage bucket organization.
    
    Request: multipart/form-data with 'file' field
    
    Returns:
        201: File uploaded successfully
        400: No file or invalid format
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({
            'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    # Generate unique filename
    file_id = generate_file_id()
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'bin'
    stored_filename = f"{file_id}.{extension}"

    # Save to user-specific directory
    user_dir = get_user_upload_dir(user_id)
    storage_path = os.path.join(user_dir, stored_filename)
    file.save(storage_path)

    # Get file size
    file_size = os.path.getsize(storage_path)

    # Save metadata to database
    db = get_db()
    db.execute(
        '''INSERT INTO user_files 
           (file_id, user_id, filename, original_filename, storage_path, file_size, file_type)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (file_id, user_id, stored_filename, original_filename, storage_path, file_size, extension)
    )
    db.commit()
    db.close()

    return jsonify({
        'message': 'File uploaded successfully',
        'file': {
            'file_id': file_id,
            'original_filename': original_filename,
            'file_size': file_size,
            'file_type': extension
        }
    }), 201


@storage_bp.route('/files', methods=['GET'])
@token_required
def list_files(user_id):
    """
    List all files uploaded by the authenticated user.
    Only returns the user's own files (data isolation).
    """
    db = get_db()
    files = db.execute(
        '''SELECT file_id, original_filename, file_size, file_type, uploaded_at
           FROM user_files WHERE user_id = ? ORDER BY uploaded_at DESC''',
        (user_id,)
    ).fetchall()
    db.close()

    file_list = []
    for f in files:
        file_list.append({
            'file_id': f['file_id'],
            'filename': f['original_filename'],
            'file_size': f['file_size'],
            'file_type': f['file_type'],
            'uploaded_at': f['uploaded_at']
        })

    return jsonify({'files': file_list, 'count': len(file_list)}), 200


@storage_bp.route('/files/<file_id>/download', methods=['GET'])
@token_required
def download_file(user_id, file_id):
    """
    Download a file from cloud storage (simulated).
    Only the file owner can download it (authorization).
    """
    db = get_db()
    file_record = db.execute(
        '''SELECT * FROM user_files WHERE file_id = ? AND user_id = ?''',
        (file_id, user_id)
    ).fetchone()
    db.close()

    if not file_record:
        return jsonify({'error': 'File not found'}), 404

    if not os.path.exists(file_record['storage_path']):
        return jsonify({'error': 'File not found on storage'}), 404

    return send_file(
        file_record['storage_path'],
        download_name=file_record['original_filename'],
        as_attachment=True
    )


@storage_bp.route('/files/<file_id>', methods=['DELETE'])
@token_required
def delete_file(user_id, file_id):
    """
    Delete a file from cloud storage (simulated).
    Removes both the file from storage and its metadata from the database.
    """
    db = get_db()

    file_record = db.execute(
        '''SELECT * FROM user_files WHERE file_id = ? AND user_id = ?''',
        (file_id, user_id)
    ).fetchone()

    if not file_record:
        db.close()
        return jsonify({'error': 'File not found'}), 404

    # Delete file from storage
    if os.path.exists(file_record['storage_path']):
        os.remove(file_record['storage_path'])

    # Delete metadata from database
    db.execute('DELETE FROM user_files WHERE file_id = ?', (file_id,))
    db.commit()
    db.close()

    return jsonify({'message': 'File deleted successfully'}), 200
