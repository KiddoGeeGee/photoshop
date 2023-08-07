import gradio as gr
import requests
import cv2
from PIL import Image
from utils.utils import convert_to_b64_list, decode_base64_to_image


def req(source_img, target_img):
    source = convert_to_b64_list([Image.fromarray(source_img)])[0].decode("utf-8")
    target = convert_to_b64_list([Image.fromarray(target_img)])[0].decode("utf-8")
    response = requests.post("http://localhost:8000/v1/main",
                              json={"source_img": source, "target_img": target}).json()
    return cv2.cvtColor(decode_base64_to_image(response), cv2.COLOR_BGR2RGB)


def search(query):
    response = requests.get("http://localhost:8000/v1/search", params={"query": query}).json()
    return response

def selected(gallery, evt: gr.SelectData):
    return gallery[evt.index]["name"]

with gr.Blocks() as demo:
    with gr.Tab("选底图"):
        with gr.Row():
            query = gr.Textbox(label="search", scale=5)
            search_btn = gr.Button(value="search", scale=1)
        gallery = gr.Gallery(label="gallery").style(grid=4)
        

    with gr.Tab("生成"):
        with gr.Row():
            source = gr.Image(label="source")
            target = gr.Image(label="target")
        result = gr.Image(label="result")
        btn = gr.Button("Run")
        
    btn.click(req, [source, target], [result])
    gallery.select(selected, gallery, target)
    search_btn.click(search, [query], [gallery])
    

demo.queue(concurrency_count=3).launch(server_name="0.0.0.0", share=True)
