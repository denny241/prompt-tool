import gradio as gr
import openai

data_placeholder_txt = "The tuesday meeting has to be rescheduled\n I will be late by around 15 minutes on Thursday\n Friday I will bring my own lunch"
placeholder_txt = "Turn the above information into a formal mail."
alternate_placeholder_txt = "Turn the above information into a formal mail. Keep it short."

##Functions
def save_api_key(key):
    openai.api_key = key

def test_api_key():
    try:
        openai.Model.list()
        status = "API key is working!"
    except:
        status = "Incorrect API key!"
    return status

def request_chat_completion(data,prompt):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "{}\n{}".format(data,prompt)}], temperature=0.2)
    print(chat_completion)
    return chat_completion["choices"][0]["message"]["content"]

def request_chat_completion_compare(data,prompt_a,prompt_b):
    return request_chat_completion(data,prompt_a), request_chat_completion(data,prompt_b)

def copy(src):
    return src

#UI Setup
with gr.Blocks() as settings:
    with gr.Row():
        api_key_box = gr.Textbox(label="OpenAI API Key")
        confirm_button = gr.Button(value="Save")
        confirm_button.click(save_api_key,inputs=api_key_box)
    with gr.Row():
        confirm_button = gr.Button(value="Test if key is working")
        output_box = gr.Textbox(label="Result")
        confirm_button.click(test_api_key,outputs=output_box)


with gr.Blocks() as use:
    with gr.Column():
        prompt_data_use = gr.Textbox(label="data",placeholder=data_placeholder_txt,lines=5)
        prompt_instruction_use = gr.Textbox(label="instruction",placeholder=alternate_placeholder_txt,lines=5)
        with gr.Row():
            prompt_dropdown_load_use = gr.Dropdown(choices=["mail_prompt","other_prompt"],label="")
            prompt_dropdown_load_btn_use = gr.Button("Load instruction")
        send_btn_use = gr.Button("Send")
        output_box_use = gr.Textbox(label="result",lines=5,interactive=False)
        send_btn_use.click(request_chat_completion,inputs=[prompt_data_use,prompt_instruction_use],outputs=output_box_use)

with gr.Blocks() as compare:
    with gr.Column():
        prompt_data = gr.Textbox(label="data",placeholder=data_placeholder_txt,lines=5)
        with gr.Row():
            with gr.Column(scale=1, min_width=300):
                prompt_instruction_left = gr.Textbox(label="instruction",placeholder=placeholder_txt,lines=5)
                copy_btn_left = gr.Button("Copy ->")
                output_box_left = gr.Textbox(label="result",lines=5,interactive=False)
                with gr.Row():
                    prompt_name_left = gr.Textbox(label="",placeholder="mail_prompt",lines=1)
                    prompt_name_save_btn_left = gr.Button("Save instruction")
                with gr.Row():
                    prompt_dropdown_left = gr.Dropdown(choices=["mail_prompt","other_prompt"],label="")
                    prompt_dropdown_load_btn_left = gr.Button("Load instruction")
            with gr.Column(scale=1, min_width=300):
                prompt_instruction_right = gr.Textbox(label="alternate instruction",placeholder=alternate_placeholder_txt,lines=5)
                copy_btn_right = gr.Button("<- Copy")
                output_box_right = gr.Textbox(label="result",lines=5,interactive=False)
                with gr.Row():
                    prompt_name_right = gr.Textbox(label="",placeholder="mail_prompt",lines=1)
                    prompt_name_save_btn_right = gr.Button("Save instruction")
                with gr.Row():
                    prompt_dropdown_right = gr.Dropdown(choices=["mail_prompt","other_prompt"],label="")
                    prompt_dropdown_load_btn_right = gr.Button("Load instruction")
        copy_btn_left.click(copy,inputs=prompt_instruction_left,outputs=prompt_instruction_right)
        copy_btn_right.click(copy,inputs=prompt_instruction_right,outputs=prompt_instruction_left)
        submit_both_btn = gr.Button("Send")
        submit_both_btn.click(request_chat_completion_compare,inputs=[prompt_data,prompt_instruction_left,prompt_instruction_right],outputs=[output_box_left,output_box_right])
demo = gr.TabbedInterface([settings,compare, use],["Settings","Compare", "Use"])
demo.launch()