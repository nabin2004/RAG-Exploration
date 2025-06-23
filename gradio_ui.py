import gradio as gr
import time

def alternating_response(message, history):
    assistant_turns = len([h for h in history if h['role'] == "assistant"])
    
    if assistant_turns % 2 == 0:
        # Stream slow echo
        for i in range(len(message)):
            time.sleep(0.2)
            yield "You typed: " + message[:i+1]
    else:
        # Immediate reply (no streaming)
        yield "I don't think so"

chat = gr.ChatInterface(
    fn=alternating_response,
    type="messages"
)

chat.launch()
