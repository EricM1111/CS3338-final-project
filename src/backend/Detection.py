"""
Copy-move forgery detection using OpenCV.

Algorithm (simple, beginner-friendly):
1. Detect "keypoints" in the image using ORB (Oriented FAST and Rotated BRIEF).
   Keypoints are distinctive locations like corners and edges.
2. For each keypoint, generate a "descriptor" (a numeric fingerprint).
3. Match every descriptor against every other descriptor in the same image.
4. If two keypoints are FAR apart but have VERY similar descriptors,
   the content at those locations is likely duplicated => copy-move forgery.
5. Draw the suspicious matches onto the image and return it.
"""

import base64
import cv2
import numpy as np


# Tunable detection parameters. Adjust these if results are too sensitive
# or not sensitive enough.
MAX_FEATURES = 2000          # how many keypoints to detect per image
MIN_SPATIAL_DIST_PX = 30     # ignore matches between points closer than this
MAX_DESCRIPTOR_DIST = 50     # how "similar" two descriptors must be to count
FORGERY_THRESHOLD = 10       # need this many suspicious matches to flag forgery


def detect_copy_move(image_path: str) -> dict:
    """
    Analyze an image for copy-move forgery.

    Args:
        image_path: path to the image file on disk

    Returns:
        dict with keys:
        - forgery_detected (bool)
        - match_count (int)        : number of suspicious matches found
        - result_image (str)       : base64-encoded PNG showing marked regions
        - error (str, optional)    : present if something went wrong
    """

    # Load the image. cv2.imread returns None if the file is invalid.
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not read image file"}

    # ORB works on grayscale. Convert before detection.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and compute descriptors.
    orb = cv2.ORB_create(nfeatures=MAX_FEATURES)
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    # If the image is too plain (blurry, low detail), there won't be enough
    # keypoints to make a confident judgment.
    if descriptors is None or len(descriptors) < 20:
        return {
            "forgery_detected": False,
            "match_count": 0,
            "reason": "Not enough distinctive features in image"
        }

    # For each descriptor, find the 2 nearest neighbors among all other
    # descriptors. The closest match will usually be the keypoint itself,
    # so we look at the 2nd closest.
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descriptors, descriptors, k=2)

    # Filter matches:
    # - skip if the match is a keypoint matching itself
    # - skip if the two points are too close (same region, not a copy)
    # - skip if descriptors aren't similar enough
    good_matches = []
    for match_pair in matches:
        if len(match_pair) < 2:
            continue

        # match_pair[0] is the closest (almost always self-match).
        # match_pair[1] is the 2nd closest — the candidate duplicate.
        candidate = match_pair[1]

        if candidate.queryIdx == candidate.trainIdx:
            continue  # skip self-matches

        pt1 = keypoints[candidate.queryIdx].pt
        pt2 = keypoints[candidate.trainIdx].pt

        # Spatial distance between the two keypoints (in pixels)
        spatial_dist = np.sqrt(
            (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2
        )

        if (
            spatial_dist > MIN_SPATIAL_DIST_PX
            and candidate.distance < MAX_DESCRIPTOR_DIST
        ):
            good_matches.append({
                "pt1": (int(pt1[0]), int(pt1[1])),
                "pt2": (int(pt2[0]), int(pt2[1])),
            })

    # Draw the suspicious matches onto a copy of the image
    output_img = img.copy()
    for match in good_matches:
        # Green dots on each matched keypoint
        cv2.circle(output_img, match["pt1"], 5, (0, 255, 0), -1)
        cv2.circle(output_img, match["pt2"], 5, (0, 255, 0), -1)
        # Red line connecting them
        cv2.line(output_img, match["pt1"], match["pt2"], (0, 0, 255), 1)

    # Encode the result image as PNG, then base64 so it can travel in JSON
    success, buffer = cv2.imencode(".png", output_img)
    if not success:
        return {"error": "Failed to encode result image"}

    img_base64 = base64.b64encode(buffer).decode("utf-8")

    forgery_detected = len(good_matches) >= FORGERY_THRESHOLD

    return {
        "forgery_detected": forgery_detected,
        "match_count": len(good_matches),
        "result_image": f"data:image/png;base64,{img_base64}",
    }
