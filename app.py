import os
from flask import Flask, send_from_directory, abort  # pyright: ignore[reportMissingImports]

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def serve_index():
    # Halaman utama WebGIS Perkebunan Kopi Argopuro Walida
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    # Melayani file pendukung (gambar, GeoJSON, dsb.) jika nanti ditambahkan
    # di folder yang sama dengan app.py. Mencegah akses ke app.py itu sendiri.
    if filename in ('app.py',) or filename.startswith('.'):
        abort(404)

    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(BASE_DIR, filename)


@app.errorhandler(404)
def not_found(_):
    # Untuk SPA-like behavior, arahkan rute tidak dikenal kembali ke index.html
    return send_from_directory(BASE_DIR, 'index.html'), 200


if __name__ == '__main__':
    # PORT diambil dari environment (untuk hosting seperti Railway, Render, Heroku),
    # fallback ke 8000 saat dijalankan secara lokal (port 5000 dipakai AirPlay di macOS).
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
