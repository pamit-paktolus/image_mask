from flask import Flask, request, jsonify
import os
from mask_ids_v2 import mask_maker_v2
import csv
from utils_v2 import decrypt_v4
app = Flask(__name__)
API_KEY = 'YOUR_SECURE_API_KEY'


@app.route('/mask_maker_v2', methods=['POST'])
def apply_mask_to_folder():
    # auth_header = request.headers.get('Authorization')
    # if not auth_header or not auth_header.startswith('Bearer '):
    #     return jsonify({'error': 'Missing or invalid API key'}), 401

    # api_key = auth_header.split()[1]  # Extract API key from header
    # if api_key != API_KEY:
    #     return jsonify({'error': 'Unauthorized'}), 403
    if 'images' not in request.files:
        return jsonify({'error': 'No images found'}), 400

    images_folder = request.files.getlist('images')

    images_paths = []
    
    for idx, image_file in enumerate(images_folder):
        # image_file = image_file.rstrip()
        IMAGE_PATH = os.path.join("images", image_file.filename)
        images_paths.append(IMAGE_PATH)

    masked_images_paths = []
    

    for image_path in images_paths:
        masked_image = mask_maker_v2(image_path)
        # masked_image_path = f'masked_{image_path}'
        masked_images_paths.append({image_path:masked_image})

    # Specify the CSV file path
    csv_file = 'data.csv'

    # Open CSV file for writing
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header (optional for single dictionary)
        writer.writerow(['Key', 'Value'])

        # Write data rows
        for i in masked_images_paths:
            writer.writerow(i.items())

    print(f'CSV file "{csv_file}" has been created successfully.')
    # for image_path in images_paths:
    #     os.remove(image_path)

    return jsonify({'masked_images_paths': masked_images_paths}), 200


@app.route('/decrypt', methods=['POST'])
def decrypt_image():
    # auth_header = request.headers.get('Authorization')
    # if not auth_header or not auth_header.startswith('Bearer '):
    #     return jsonify({'error': 'Missing or invalid API key'}), 401

    # api_key = auth_header.split()[1]  # Extract API key from header
    # if api_key != API_KEY:
    #     return jsonify({'error': 'Unauthorized'}), 403
    if 'images' not in request.files:
        return jsonify({'error': 'No images found'}), 400

    images_folder = request.files.getlist('images')
    images_paths = []

    for idx, image_file in enumerate(images_folder):
        IMAGE_PATH = os.path.join("encrypted", image_file.filename)
        images_paths.append(IMAGE_PATH)

    masked_images_paths = []

    for image_path in images_paths:
        if image_path.split('.')[-1] == 'enc':
            path = decrypt_v4(image_path)
    return jsonify({'decrypted_images_paths': path}), 200


@app.route('/mask_maker_v3', methods=['POST'])
def apply_mask_to_folder_filename_only():
    # auth_header = request.headers.get('Authorization')
    # if not auth_header or not auth_header.startswith('Bearer '):
    #     return jsonify({'error': 'Missing or invalid API key'}), 401

    # api_key = auth_header.split()[1]  # Extract API key from header
    # if api_key != API_KEY:
    #     return jsonify({'error': 'Unauthorized'}), 403

    if 'images' not in request.files:
        return jsonify({'error': 'No images found'}), 400

    images_folder = request.files.getlist('images')

    images_paths = []

    f = open( images_folder[0].filename, "r")
    for idx, image_file in enumerate(f.readlines()):
        image_file = image_file.rstrip()
        IMAGE_PATH = os.path.join("images", image_file)
        images_paths.append(IMAGE_PATH)

    masked_images_paths = []
    

    for image_path in images_paths:
        masked_image = mask_maker_v2(image_path)

        masked_images_paths.append({image_path:masked_image})

    # Specify the CSV file path
    csv_file = 'data.csv'

    # Open CSV file for writing
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header (optional for single dictionary)
        writer.writerow(['Key', 'Value'])

        # Write data rows
        for i in masked_images_paths:
            writer.writerow(i.items())

    print(f'CSV file "{csv_file}" has been created successfully.')
    # for image_path in images_paths:
    #     os.remove(image_path)

    return jsonify({'masked_images_paths': masked_images_paths}), 200

if __name__ == '__main__':
    app.run(debug=True)
