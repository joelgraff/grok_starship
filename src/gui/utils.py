# src/gui/utils.py
def update_button_style(button, checked, color):
    if checked:
        button.setStyleSheet(f"background-color: {color}; color: white; border: 1px solid gray;")
    else:
        button.setStyleSheet(f"background-color: gray; color: black; border: 1px solid gray;")