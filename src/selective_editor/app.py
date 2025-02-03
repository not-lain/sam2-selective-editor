import numpy as np
import torch
import supervision as sv
from loadimg import load_img
import gradio as gr
from gradio_client import Client, handle_file

from sam2.sam2_image_predictor import SAM2ImagePredictor


def process_selection(base_img, selected, legend, hidden_mask, evt: gr.SelectData):
    # process input
    label = 1 if selected == "add point" else 0
    if legend is None:
        legend = {
            "points": [],
            "labels": [],
            "scores": None,
            "logits": None,
        }

    legend["points"].append(evt.index)
    legend["labels"].append(label)
    mask_input = np.array(legend["logits"]) if legend["logits"] is not None else None

    # sam 2
    input_points = np.array(legend["points"])
    input_labels = np.array(legend["labels"])
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
        predictor.set_image(base_img)
        masks, scores, logits = predictor.predict(
            point_coords=input_points,
            point_labels=input_labels,
            mask_input=mask_input,
            multimask_output=False,
        )
    # update legend
    legend["scores"] = scores
    legend["logits"] = logits.tolist()
    # hidden mask
    hidden_mask = load_img(np.squeeze(masks * 255)).convert("L")
    # supervision for better visuals
    mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX)

    detections = sv.Detections(xyxy=sv.mask_to_xyxy(masks), mask=masks.astype(bool))
    annotated_frame = mask_annotator.annotate(
        scene=base_img.copy(), detections=detections
    )

    return annotated_frame, legend, hidden_mask


def inpaint(img, mask, prompt, num_inference_steps, guidance_scale):
    out = client.predict(
        image=handle_file(load_img(img, output_type="str")),
        mask=handle_file(load_img(mask, output_type="str")),
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        api_name="/inpaint",
    )
    out_img = load_img(out)
    return out_img


def upload(img):
    return img


def reset_fn(base_img, img, legend, hidden_mask):
    return base_img, base_img, None, None


# function for loading variables when called
# avoid calling this in the tests for now as it will require GPU
def get_app():
    global predictor, client

    with gr.Blocks(theme="ocean") as demo:
        predictor = SAM2ImagePredictor.from_pretrained("facebook/sam2.1-hiera-large")

        client = Client("not-lain/flux-inpainting")
        car = load_img(
            "https://raw.githubusercontent.com/facebookresearch/sam2/main/notebooks/images/truck.jpg"
        )
        with gr.Row():
            with gr.Column():
                base_img = gr.Image(
                    value=car, visible=False
                )  # invisible holder of original image before transformation
                hidden_mask = gr.Image(visible=False)  # invisible
                img = gr.Image(value=car, interactive=True)
                selected = gr.Radio(
                    ["add point", "avoid point"], value="add point", label="label"
                )
                with gr.Row():
                    prompt = gr.Text(label="inpaint_prompt")
                    num_inference_steps = gr.Number(30, label="num_inference_steps")
                    guidance_scale = gr.Number(28, label="guidance_scale")

                with gr.Row():
                    reset = gr.Button("Reset", variant="secondary")
                    btn = gr.Button("Inpaint", variant="primary")
                legend = gr.JSON(label="legend", visible=False)
            with gr.Column():
                out = gr.Image()

        img.upload(upload, [img], base_img)
        img.select(
            process_selection,
            [base_img, selected, legend, hidden_mask],
            [img, legend, hidden_mask],
        )
        btn.click(
            inpaint,
            inputs=[base_img, hidden_mask, prompt, num_inference_steps, guidance_scale],
            outputs=[out],
        )
        reset.click(
            reset_fn,
            [base_img, img, legend, hidden_mask],
            [base_img, img, legend, hidden_mask],
        )
    return demo


if __name__ == "__main__":
    demo = get_app()
    demo.launch(debug=True)
