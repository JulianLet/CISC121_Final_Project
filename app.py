import gradio as gr
import random

#bubble sort state
state = {
    "lst": random.sample(range(1, 20), 8),  #initial list
    "i": 0,                  #start index
    "j": 0,                  #selected index
    "warning": False,        #if user wanted to continue but should have swapped
    "swapped": False,        #did it swap last iteration
    "finished": False        #is it finished
}

def render(state):
    lst = state["lst"]
    j = state["j"]
    i = state["i"]
    n = len(lst)

    #show final list if finished
    if state["finished"]:
        sorted_ok = all(lst[k] <= lst[k+1] for k in range(n-1))
        color = "#69dd79" if sorted_ok else "#dd6969"

        final_items = "".join(
            f'<div class="final">{v}</div>' for v in lst
        )

        html = f"""
        <style>
            .final {{
                width: 60px;
                height: 60px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: #888;
                border-radius: 50%;
                margin: 6px;
                font-size: 25px;
                font-weight: bold;
                color: white;
            }}
            .check {{
                padding: 10px;
                margin-top: 15px;
                background-color: {color};
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                width: 170px;
            }}
        </style>
        <h2>Final List</h2>
        <div>{final_items}</div>
        <div class="check">Sorted: {sorted_ok}</div>
        """
        return html

    #regular view
    circles = ""

    for idx in range(n):
        if idx == j or idx == j + 1: #selected turn red when warning is active
            color = "#dd6969" if state["warning"] else "#4a8cff"
            circles += f"""
            <div class="selected" style="background-color:{color}">{lst[idx]}</div>
            """
        elif idx >= n - i:  # completed sorted items
            circles += '<div class="sorted"></div>'
        else:
            circles += '<div class="circle"></div>'

    html = f"""
    <style>
        .circle {{
            width: 60px;
            height: 60px;
            background-color: gray;
            border-radius: 50%;
            display: inline-block;
            margin: 6px;
        }}
        .sorted {{
            width: 60px;
            height: 60px;
            background-color: yellow;
            border-radius: 50%;
            display: inline-block;
            margin: 6px;
        }}
        .selected {{
            width: 60px;
            height: 60px;
            color: white;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin: 6px;
            font-size: 25px;
            font-weight: bold;
            border: 3px solid #003f99;
        }}
    </style>

    <h3>Bubble Sort — Current View</h3>
    <div>{circles}</div>
    """

    return html


#swap button
def swap_pressed(state_in):
    s = state_in
    j = s["j"]
    s["lst"][j], s["lst"][j+1] = s["lst"][j+1], s["lst"][j]
    s["swapped"] = True
    return s, render(s)

#next button
def next_pressed(state_in):
    s = state_in
    j = s["j"]
    n = len(s["lst"])

    #if user should have swapped dont continue and warning
    if s["lst"][j] > s["lst"][j+1]:
        s["warning"] = True
        return s, render(s)

    s["warning"] = False
    s["j"] += 1

    #at the end of the iteration
    if s["j"] >= n - s["i"] - 1:

        #if user did not swap its finished
        if not s["swapped"]:
            s["finished"] = True
            return s, render(s)

        s["i"] += 1
        s["j"] = 0
        s["swapped"] = False

    return s, render(s)

#restart the programm
def restart_pressed():
    new_state = {
        "lst": random.sample(range(1, 20), 8),
        "i": 0,
        "j": 0,
        "swapped": False,
        "finished": False,
        "warning": False
    }
    return new_state, render(new_state)


with gr.Blocks() as demo:
    gr.Markdown("""
        ## Bubble Sort
       
        Sort this list in acending order. This app visualizes in a way the computer will see the current list and has to decide on what to do. \n
        # Jump In! Be the Computer! Sort this list!
    """)

    state_box = gr.State(state)

    html_area = gr.HTML(render(state))

    with gr.Row():
        swap_btn = gr.Button("Swap")
        next_btn = gr.Button("Next")
        restart_btn = gr.Button("Restart")


    swap_btn.click(swap_pressed, inputs=state_box, outputs=[state_box, html_area])
    next_btn.click(next_pressed, inputs=state_box, outputs=[state_box, html_area])
    restart_btn.click(restart_pressed, inputs=None, outputs=[state_box, html_area])

demo.launch()
