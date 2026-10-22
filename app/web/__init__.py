import json
from pathlib import Path

from flask import Flask, jsonify, render_template, send_file

from app.config.settings import settings


def create_app() -> Flask:
    """Create and configure the dashboard web application."""
    app = Flask(__name__)

    latest_result_path = (
        settings.storage.results_directory / "latest.json"
    )
    processed_images_dir = (
        settings.storage.processed_images_directory.resolve()
    )

    @app.get("/")
    def dashboard():
        """Render the monitoring dashboard."""
        return render_template("dashboard.html")

    @app.get("/health")
    def health_check():
        """Report whether the dashboard web server is responding."""
        return {"status": "ok"}

    @app.get("/api/latest")
    def latest_result():
        """Return the latest monitoring result as JSON."""
        if not latest_result_path.is_file():
            return jsonify({
                "error": "No monitoring result is available yet."
            }), 404

        try:
            with latest_result_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                result = json.load(file)
        except (json.JSONDecodeError, OSError):
            app.logger.exception(
                "Could not read latest monitoring result."
            )
            return jsonify({
                "error": "The latest monitoring result could not be read."
            }), 500

        return jsonify(result)

    @app.get("/plant-image")
    def plant_image():
        """Serve the latest processed plant image safely."""
        if not latest_result_path.is_file():
            return jsonify({
                "error": "No monitoring result is available yet."
            }), 404

        try:
            with latest_result_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                result = json.load(file)

            preprocessing = result.get("preprocessing") or {}
            image_path = preprocessing.get("processed_image_path")

            if not image_path:
                return jsonify({
                    "error": "No processed image is recorded."
                }), 404

            requested_path = Path(image_path).resolve()

            if not requested_path.is_relative_to(processed_images_dir):
                return jsonify({
                    "error": (
                        "Image path is outside the permitted directory."
                    )
                }), 403

            if not requested_path.is_file():
                return jsonify({
                    "error": "The processed image file was not found."
                }), 404

            return send_file(requested_path, mimetype="image/jpeg")

        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            app.logger.exception(
                "Could not serve the processed plant image."
            )
            return jsonify({
                "error": "The processed image could not be read."
            }), 500

    return app
