"""Lightweight, explainable plant-health image inference."""

from datetime import datetime

import cv2
import numpy as np

from app.contracts.inference_contract import InferenceServiceContract
from app.domain.enums import PlantHealthStatus
from app.domain.inference_result import InferenceResult
from app.domain.preprocessing_result import PreprocessingResult
from app.utils.logger import logger


class InferenceService(InferenceServiceContract):
    """
    Handles AI inference.
    """

    def predict(
        self,
        preprocessing_result: PreprocessingResult,
    ) -> InferenceResult:
        """
        Classify the leaf canopy from its HSV colour distribution.

        This deterministic edge-friendly baseline works without a model file.
        A high proportion of yellow pixels relative to green pixels is treated
        as a possible nitrogen deficiency; images without enough vegetation are
        reported as unknown.
        """

        logger.info("5. Running AI inference...")

        image = cv2.imread(str(preprocessing_result.processed_image_path))
        if image is None:
            raise ValueError(
                "Unable to load processed image: "
                f"{preprocessing_result.processed_image_path}"
            )

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        green = cv2.inRange(
            hsv,
            np.array([35, 35, 25]),
            np.array([95, 255, 255]),
        )
        yellow = cv2.inRange(
            hsv,
            np.array([15, 40, 40]),
            np.array([34, 255, 255]),
        )

        pixel_count = float(image.shape[0] * image.shape[1])
        green_ratio = cv2.countNonZero(green) / pixel_count
        yellow_ratio = cv2.countNonZero(yellow) / pixel_count
        vegetation_ratio = green_ratio + yellow_ratio

        if vegetation_ratio < 0.02:
            prediction = PlantHealthStatus.UNKNOWN
            confidence = min(1.0, (0.05 - vegetation_ratio) / 0.05)
        else:
            yellow_share = yellow_ratio / vegetation_ratio
            if yellow_share >= 0.30:
                prediction = PlantHealthStatus.POSSIBLE_NITROGEN_DEFICIENCY
                confidence = min(1.0, 0.5 + yellow_share / 2)
            else:
                prediction = PlantHealthStatus.HEALTHY
                confidence = min(1.0, 0.7 + green_ratio * 0.3)

        logger.info(
            "Inference result: %s (confidence %.2f)",
            prediction.value,
            confidence,
        )

        return InferenceResult(
            prediction=prediction,
            confidence=round(confidence, 4),
            model_version="hsv-baseline-1.0",
            timestamp=datetime.now(),
        )
