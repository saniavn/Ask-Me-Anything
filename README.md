# Ask-Me-Anything-chatbot-for-kids
<p align="justify"> Ask Me Anthing is a child-friendly chatbot that is specialized in three topics: Astronomy, Sneakers and Shoes, and Dinosaurs. It sends the user's query to the OpenAI API's ChatGPT model 3 and retrieves a response based on the user's age and topic selection. User input and AI-generated responses are then added to a conversation history file based on the user name and grade. </p>

## Features: 
Implemented dynamic image updating functionality: 
1. **The displayed image changes as the user selects a topic from the dropdown menu, providing a visual cue.**
2. **Added functionality to the Submit, Clear, and Reset buttons:**
- Submit: Based on the user's selected age range and topic, this retrieves the user's input and generates an AI response using the OpenAI API. The AI response is then displayed in the Answer Box.
- Clear: The input field and the AI response in the Answer Box are cleared when this button is clicked.
- Reset: Input fields Name, Grade, Age Range, and Topic are reset to their default values, as well as the subject image.

## Libraries and Dependencies:
Ask Me Anything requires the following libraries : 
- **customtkinter**: An enhanced version of tkinter with custom widgets. [More info](https://pypi.org/project/customtkinter/).
- **openai**: The OpenAI Python client library for interacting with the OpenAI API. [More info](https://github.com/openai/openai-python).
- **Pillow (PIL)**: The Python Imaging Library, used for image processing tasks. [More info](https://pillow.readthedocs.io/en/stable/).

### Installing Dependencies

To install these dependencies, you can typically use a package manager like pip for Python projects. 
- **pip install customtkinter**

