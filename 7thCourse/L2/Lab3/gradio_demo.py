import gradio as gr

def add_numbers(number1, number2):
    return number1 + number2

demo = gr.Interface(
    fn=add_numbers,
    inputs=[
        gr.Number(label='Insert the first number: '),
        gr.Number(label='Insert the second number: ')
    ],
    outputs=[gr.Number(label='The sum of the two numbers is: ')]
)
demo.launch(server_name='127.0.0.1', server_port=7680)