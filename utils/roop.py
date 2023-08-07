import insightface
from PIL import Image
import cv2


def get_face_single(img_data, face_index=0, det_size=(640, 640)):
    face_analyser = insightface.app.FaceAnalysis(name="buffalo_l")
    face_analyser.prepare(ctx_id=0, det_size=det_size)
    face = face_analyser.get(img_data)

    if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
        det_size_half = (det_size[0] // 2, det_size[1] // 2)
        return get_face_single(img_data, face_index=face_index, det_size=det_size_half)
    try:
        return sorted(face, key=lambda x: x.bbox[0])[face_index]
    except IndexError:
        return None
    

def getFaceSwapModel(model_path):
    model = insightface.model_zoo.get_model(model_path)
    return model


def main(source_img, target_img, model, faces_index={0}):
    result_image = target_img
    if model is not None:
        source_face = get_face_single(source_img, face_index=0)
        if source_face is not None:
            result = target_img
            for face_num in faces_index:
                target_face = get_face_single(target_img, face_index=face_num)
                if target_face is not None:
                    result = model.get(result, target_face, source_face)
                else:
                    print(f"No target face found for {face_num}")

            result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        else:
            print("No source face found")
    return result_image
