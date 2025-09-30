import gradio as gr

def combine_sentences(stc1, stc2):
    return ''.join([stc1, ' ', stc2])

gradio_itf = gr.Interface(
    fn=combine_sentences,
    inputs=[
        gr.Textbox(label='Insert the first sentence: '),
        gr.Textbox(label='Insert the second sentence: ')
    ],
    outputs = gr.Textbox(label='The combined sentence is: ')
)

gradio_itf.launch(server_name='127.0.0.1', server_port=7680)