import json
import os


def sahi_to_coco(file_sahi, directory_input, directory_output, dataset_base):

    with open(os.path.join(directory_input, dataset_base), "r") as f:
        dataset_completo = json.load(f)

    with open(os.path.join(directory_input,file_sahi), "r") as f:
        dati = json.load(f)

    annotation_key_field = ["image_id", "category_id", "segmentation", "area", "bbox", "iscrowd"]

    final_annotation = [{key: annotation[key] for key in annotation if key in annotation_key_field}
                        for annotation in dati]

    dataset_completo["annotations"].extend(final_annotation)
    dataset_completo["annotations"].sort(key=lambda x: x["image_id"])
    id_counter = 1
    current_image_id = None

    for annotation in dataset_completo["annotations"]:
        if annotation["image_id"] != current_image_id:
            current_image_id = annotation["image_id"]
            id_counter = 1
            annotation["attributes"] = {"occluded": False}

        annotation["id"] = id_counter
        id_counter += 1
        annotation["attributes"] = {"occluded": False}


    annotation_by_images = {}
    for annotation in dataset_completo["annotations"]:
        image_id = annotation["image_id"]
        if image_id not in annotation_by_images:
            annotation_by_images[image_id] = []
        annotation_by_images[image_id].append(annotation)

    for image_id, annotation in annotation_by_images.items():
        image_data = next((img for img in dataset_completo["images"] if img["id"] == image_id), None)
        image_file_name = image_data["file_name"]
        output_file = f"{os.path.splitext(image_file_name)[0]}.json"
        data_image = {"licenses": dataset_completo["licenses"],
            "info": dataset_completo["info"],
            "categories": dataset_completo["categories"],
            "images": [image_data],
            "annotations": annotation

        }
        with open(os.path.join(directory_output,output_file), "w") as f:
            json.dump(data_image, f)
