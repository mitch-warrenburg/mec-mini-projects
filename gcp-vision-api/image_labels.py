from typing import Sequence

from google.cloud import vision


def analyze_image_from_uri(
        image_uri: str,
        feature_types: Sequence,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = image_uri
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)

    return response


def print_labels(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for label in response.label_annotations:
        print(
            f"{label.score:4.0%}",
            f"{label.description:5}",
            sep=" | ",
        )


def detect_labels():
    image_uri = "gs://cloud-samples-data/vision/label/setagaya.jpeg"
    features = [vision.Feature.Type.LABEL_DETECTION]

    response = analyze_image_from_uri(image_uri, features)
    print_labels(response)


def print_text(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for annotation in response.text_annotations:
        vertices = [f"({v.x},{v.y})" for v in annotation.bounding_poly.vertices]
        print(
            f"{repr(annotation.description):42}",
            ",".join(vertices),
            sep=" | ",
        )


def detect_text():
    image_uri = "gs://cloud-samples-data/vision/ocr/sign.jpg"
    features = [vision.Feature.Type.TEXT_DETECTION]

    response = analyze_image_from_uri(image_uri, features)
    print_text(response)


def print_landmarks(response: vision.AnnotateImageResponse, min_score: float = 0.5):
    print("=" * 80)
    for landmark in response.landmark_annotations:
        if landmark.score < min_score:
            continue
        vertices = [f"({v.x},{v.y})" for v in landmark.bounding_poly.vertices]
        lat_lng = landmark.locations[0].lat_lng
        print(
            f"{landmark.description:18}",
            ",".join(vertices),
            f"{lat_lng.latitude:.5f}",
            f"{lat_lng.longitude:.5f}",
            sep=" | ",
        )


def detect_landmarks():
    image_uri = "gs://cloud-samples-data/vision/landmark/eiffel_tower.jpg"
    features = [vision.Feature.Type.LANDMARK_DETECTION]

    response = analyze_image_from_uri(image_uri, features)
    print_landmarks(response)


def print_faces(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for face_number, face in enumerate(response.face_annotations, 1):
        vertices = ",".join(f"({v.x},{v.y})" for v in face.bounding_poly.vertices)
        print(f"# Face {face_number} @ {vertices}")
        print(f"Joy:     {face.joy_likelihood.name}")
        print(f"Exposed: {face.under_exposed_likelihood.name}")
        print(f"Blurred: {face.blurred_likelihood.name}")
        print("-" * 80)


def detect_faces():
    image_uri = "gs://cloud-samples-data/vision/face/faces.jpeg"
    features = [vision.Feature.Type.FACE_DETECTION]

    response = analyze_image_from_uri(image_uri, features)
    print_faces(response)


def print_objects(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for obj in response.localized_object_annotations:
        nvertices = obj.bounding_poly.normalized_vertices
        print(
            f"{obj.score:4.0%}",
            f"{obj.name:15}",
            f"{obj.mid:10}",
            ",".join(f"({v.x:.1f},{v.y:.1f})" for v in nvertices),
            sep=" | ",
        )


def detect_objects():
    image_uri = "gs://cloud-samples-data/vision/label/setagaya.jpeg"
    features = [vision.Feature.Type.OBJECT_LOCALIZATION]

    response = analyze_image_from_uri(image_uri, features)
    print_objects(response)


def detect_multiple_features():
    image_uri = "gs://cloud-samples-data/vision/label/setagaya.jpeg"
    features = [
        vision.Feature.Type.OBJECT_LOCALIZATION,
        vision.Feature.Type.FACE_DETECTION,
        vision.Feature.Type.LANDMARK_DETECTION,
        vision.Feature.Type.LOGO_DETECTION,
        vision.Feature.Type.LABEL_DETECTION,
        vision.Feature.Type.TEXT_DETECTION,
        vision.Feature.Type.DOCUMENT_TEXT_DETECTION,
        vision.Feature.Type.SAFE_SEARCH_DETECTION,
        vision.Feature.Type.IMAGE_PROPERTIES,
        vision.Feature.Type.CROP_HINTS,
        vision.Feature.Type.WEB_DETECTION,
        vision.Feature.Type.PRODUCT_SEARCH,
        vision.Feature.Type.OBJECT_LOCALIZATION,
    ]

    print(analyze_image_from_uri(image_uri, features))


detect_labels()
detect_text()
detect_landmarks()
detect_faces()
detect_objects()
detect_multiple_features()
