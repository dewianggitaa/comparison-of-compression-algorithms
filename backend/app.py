from flask import Flask, jsonify, request, send_from_directory
import os
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import pywt
from PIL import Image
from pydub import AudioSegment
import scipy.fftpack as sf

app = Flask(__name__)

# ---------------------------------------------------- IMAGE --------------------------------------------------

UPLOAD_FOLDER = 'static/uploads/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_AUDIO = 'static/uploads/audio'
app.config['UPLOAD_AUDIO'] = UPLOAD_AUDIO

BEFORE_COMPRESS = 'static/image/before'
app.config['BEFORE_COMPRESS'] = BEFORE_COMPRESS

AFTER_DCT_COMPRESS = 'static/image/after/dct'
app.config['AFTER_DCT_COMPRESS'] = AFTER_DCT_COMPRESS

AFTER_AUDIO_DCT = 'static/audio/dct'
app.config['AFTER_AUDIO_DCT'] = AFTER_AUDIO_DCT

AFTER_DWT_COMPRESS = 'static/image/after/dwt'
app.config['AFTER_DWT_COMPRESS'] = AFTER_DWT_COMPRESS

AFTER_AUDIO_DWT = 'static/audio/dwt'
app.config['AFTER_AUDIO_DWT'] = AFTER_AUDIO_DWT

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

AUDIO_EXTENSION = 'mp3'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in AUDIO_EXTENSION

def selectQMatrix(qName):
    Q10 = np.array([[80,60,50,80,120,200,255,255],
                [55,60,70,95,130,255,255,255],
                [70,65,80,120,200,255,255,255],
                [70,85,110,145,255,255,255,255],
                [90,110,185,255,255,255,255,255],
                [120,175,255,255,255,255,255,255],
                [245,255,255,255,255,255,255,255],
                [255,255,255,255,255,255,255,255]])

    Q50 = np.array([[16,11,10,16,24,40,51,61],
                [12,12,14,19,26,58,60,55],
                [14,13,16,24,40,57,69,56],
                [14,17,22,29,51,87,80,62],
                [18,22,37,56,68,109,103,77],
                [24,35,55,64,81,104,113,92],
                [49,64,78,87,103,121,120,101],
                [72,92,95,98,112,100,130,99]])

    Q90 = np.array([[3,2,2,3,5,8,10,12],
                    [2,2,3,4,5,12,12,11],
                    [3,3,3,5,8,11,14,11],
                    [3,3,4,6,10,17,16,12],
                    [4,4,7,11,14,22,21,15],
                    [5,7,11,13,16,12,23,18],
                    [10,13,16,17,21,24,24,21],
                    [14,18,19,20,22,20,20,20]])
    if qName == "Q10":
        return Q10
    elif qName == "Q50":
        return Q50
    elif qName == "Q90":
        return Q90
    else:
        return np.ones((8,8))

@app.route('/compress-image', methods=['POST'])
def compress_dct():
    if 'files[]' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files[]')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(temp_path)

            # Read and convert the image to grayscale
            image = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                return jsonify({"error": "Could not read the image file"}), 400

            # Save the grayscale image to BEFORE_COMPRESS
            before_file_path = os.path.join(app.config['BEFORE_COMPRESS'], filename)
            cv2.imwrite(before_file_path, image)

            ########## kompresi DCT ##########
            height, width = image.shape
            block = 8

            # Dividing the image into 8x8 blocks
            sliced = []
            for i in range(0, height, block):
                for j in range(0, width, block):
                    slice_ = image[i:i+block, j:j+block] - 128
                    sliced.append(slice_)

            # Applying DCT and quantization
            DCToutput = [cv2.dct(np.float32(block)) for block in sliced]
            selectedQMatrix = selectQMatrix("Q90")
            for ndct in DCToutput:
                for i in range(block):
                    for j in range(block):
                        ndct[i, j] = np.around(ndct[i, j] / selectedQMatrix[i, j])

            # Applying inverse DCT
            invList = [cv2.idct(part) for part in DCToutput]

            # Reconstruct the compressed image
            row_blocks = width // block
            compressed_image = np.vstack([
                np.hstack(invList[i * row_blocks:(i + 1) * row_blocks]) 
                for i in range(len(invList) // row_blocks)
            ])

            compressed_image = np.clip(compressed_image + 128, 0, 255)
            compressed_image = compressed_image.astype(np.uint8)

            compressed_filename = 'dct_compressed_' + filename
            compressed_file_path = os.path.join(app.config['AFTER_DCT_COMPRESS'], compressed_filename)
            cv2.imwrite(compressed_file_path, compressed_image)


            ########## DWT KOMPRESI ##########

            # Read image using PIL
            image_pil = Image.open(before_file_path)
            A = np.array(image_pil)
            coeffs = pywt.wavedec2(A, 'haar', level=4)
            C = coeffs[0]
            Coeff_sort = np.sort(np.abs(C).ravel())

            keep = 0.9
            thresh = Coeff_sort[int((1 - keep) * len(Coeff_sort))]
            C_filter = C * (np.abs(C) > thresh)

            Areacon = pywt.waverec2([C_filter] + coeffs[1:], 'haar')

            compressed_dwt_image = Image.fromarray(Areacon.astype(np.uint8))
            compressed_dwt_name = 'dwt_compressed_' + filename
            compressed_dwt_path = os.path.join(app.config['AFTER_DWT_COMPRESS'], compressed_dwt_name)
            compressed_dwt_image.save(compressed_dwt_path)

            # Return URLs of the compressed images
            return jsonify({
                "dct_image_url": f"/static/image/after/dct/{compressed_filename}",
                "dwt_image_url": f"/static/image/after/dwt/{compressed_dwt_name}"
            })

    return jsonify({"error": "No valid files processed"}), 400

@app.route('/static/image/after/dct/<filename>')
def serve_dct_image(filename):
    return send_from_directory(app.config['AFTER_DCT_COMPRESS'], filename)

@app.route('/static/image/after/dwt/<filename>')
def serve_dwt_image(filename):
    return send_from_directory(app.config['AFTER_DWT_COMPRESS'], filename)


# --------------------------------------------- AUDIO -------------------------------------------
def read_audio(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        audio_data = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate

        if audio.channels == 2:
            audio_data = audio_data.reshape((-1, 2))

        return sample_rate, audio_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None, None
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")
        return None, None

def dct_compression(audio_data, compression_ratio):
    if len(audio_data.shape) == 1:
        audio_dct = sf.dct(audio_data.astype(float), norm='ortho')
    else:
        audio_dct = np.apply_along_axis(sf.dct, axis=0, arr=audio_data.astype(float), norm='ortho')

    num_coefficients = int(compression_ratio * len(audio_dct))

    if len(audio_data.shape) == 1:
        audio_dct_compressed = np.zeros_like(audio_dct)
        audio_dct_compressed[:num_coefficients] = audio_dct[:num_coefficients]
    else:
        audio_dct_compressed = np.zeros_like(audio_dct)
        audio_dct_compressed[:num_coefficients, :] = audio_dct[:num_coefficients, :]

    if len(audio_data.shape) == 1:
        audio_data_compressed = sf.idct(audio_dct_compressed, norm='ortho').astype(np.int16)
    else:
        audio_data_compressed = np.apply_along_axis(sf.idct, axis=0, arr=audio_dct_compressed, norm='ortho').astype(np.int16)

    return audio_data_compressed

def write_audio(file_path, data, sample_rate, format="mp3", bitrate="32k"):
    try:
        audio_segment = AudioSegment(
            data.tobytes(),
            frame_rate=sample_rate,
            sample_width=data.dtype.itemsize,
            channels=(1 if len(data.shape) == 1 else data.shape[1])
        )

        audio_segment.export(file_path, format=format, bitrate=bitrate)
        print(f"Compressed audio saved to {file_path}")
    except Exception as e:
        print(f"Error writing '{file_path}': {e}")

def compress_audio(input_audio_file, output_audio_file, compression_ratio, output_format="mp3", bitrate="32k"):
    sample_rate, audio_data = read_audio(input_audio_file)

    if audio_data is None:
        return

    compressed_data = dct_compression(audio_data, compression_ratio)

    write_audio(output_audio_file, compressed_data, sample_rate, format=output_format, bitrate=bitrate)


@app.route('/compress-audio', methods=['POST'])
# ------------------- DCT ALGORITHM
def compress_audio_dct():
    if 'files[]' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files[]')
    if not files:
        return jsonify({"error": "No selected files"}), 400
    
    for file in files: 
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_audio(file.filename):
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_AUDIO'], filename)
            file.save(temp_path)

            compression_ratio = 0.2
            bitrate = "32k"
            output_name = filename
            output_path = os.path.join(app.config['AFTER_AUDIO_DCT'], output_name)
            format = "mp3"

            compress_audio(temp_path, output_path, compression_ratio, output_format = "mp3", bitrate=bitrate)



            return jsonify({
                "dct_audio_url": f"/static/audio/dct/{output_name}"
            })

    return jsonify({"error": "No valid files processed"}), 400


# ------------- DWT ALGORITHM ----------------


if __name__ == '__main__':
    app.run(debug=True)