import tkinter as tk
from tkinter import *
import customtkinter
import os
import openai
from PIL import Image
from tkinter import messagebox

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("AMA_UI/custom.json")  # Themes: "blue" (standard), "green", "dark-blue"

# get absolute path of current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# dictionary mapping topics to image file names
TOPIC_IMAGES = {
    "Astronomy": os.path.join(current_dir, "AMA_UI", "3.png"),
    "Sneakers and Shoes": os.path.join(current_dir, "AMA_UI", "5.png"),
    "Dinosaurs": os.path.join(current_dir, "AMA_UI", "1.png"),
}


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.topic = ""  # initialize topic to empty string

        def update_image(event):
            selected_topic = self.subject_combobox.get()
            image_file = TOPIC_IMAGES.get(selected_topic, os.path.join(current_dir, "AMA_UI", "robo_AMA.png"))
            self.subject_image = customtkinter.CTkImage(Image.open(image_file), size=(240, 200))
            self.subject_image_label.configure(image=self.logo_image)


        ## initial logo image
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join("AMA_UI/robo_AMA.png")), size=(80, 100))

        # Function to create and update the history file based on the user's name and grade
        def update_history_file():
            name = app.name_entry.get().strip()
            grade = app.grade_combobox.get().strip()

            if name and grade:
                filename = f"{name}_{grade}_conversation_history.txt"
            else:
                filename = "conversation_history.txt"

            if os.path.exists(filename):
                with open(filename, "r") as f:
                    conversation_history = f.read().splitlines()
            else:
                with open(filename, 'w') as f:
                    conversation_history = []

            global history_file
            history_file = filename

            return conversation_history

        ### save history of the chat
        with open('conversation_history.txt', 'w') as f:
            pass
        # set up OpenAI API key
        openai.api_key = ""

        # initial conversation history
        conversation_history = []
        self.history_file = "conversation_history.txt"
        self.response_text = tk.StringVar()

        # def generate_response(user_input, age, topic):
        #     # clear conversation history
        #     conversation_history = []
        # 
        #     try:
        #         response = openai.ChatCompletion.create(
        #             model="gpt-3.5-turbo",
        #             messages=[
        #                 {"role": "system",
        #                  "content": f"You are an expert in {topic} and You are talking to a {age} year old student. "
        #                             f"Answer questions assuming this. If you are asked a question outside the realm of {topic}, "
        #                             f"please answer that you can only answer questions about {topic} and "
        #                             f"don't answer further for questions outside {topic} and avoid responding to off-topic queries.\n\n"},
        #                 {"role": "user", "content": user_input}
        #             ],
        #             temperature=0.7,
        #             max_tokens=1024,
        #             top_p=1,
        #             frequency_penalty=0,
        #             presence_penalty=0
        #         )
        #     except Exception as e:
        #         return f"Error in API call: {e}"
        # 
        #     # Check and extract GPT response
        #     if 'choices' in response and response['choices']:
        #         choice = response['choices'][0]
        #         if 'message' in choice and 'content' in choice['message']:
        #             message = choice['message']['content'].strip()
        #         else:
        #             message = "Response found, but 'content' key is missing."
        #     else:
        #         message = "No valid response found in 'choices'."
        # 
        #     with open(self.history_file, "r") as f:
        #         conversation_history = f.read().splitlines()
        # 
        #     # append user input and AI response to conversation history file
        #     conversation_history.append(user_input)
        #     conversation_history.append(message)
        # 
        #     # write conversation history to file
        #     with open(self.history_file, "w") as f:
        #         f.write('\n'.join(conversation_history))
        # 
        #     return message
        #  Sample of answer: sani (Grade 8): what is the best running shoes?
            # I apologize, but as an AI language model, I am programmed to provide information about Astronomy only. I am not capable of providing recommendations for running shoes or any other topics outside of Astronomy. Do you have any questions about Astronomy that I can help you with?
            # sani (Grade 8): What is the name of the tallest tree in the world?
            # I can only answer questions about Astronomy, unfortunately, I cannot answer that question as it is not related to Astronomy.
            # sani (Grade 8): how many seasons we have?
            # There are four seasons in a year, namely spring, summer, autumn, and winter. The change in seasons is caused by the tilt of the Earth's axis and its orbit around the sun.
            # sani (Grade 8): can you give me the name of red fruits?
            # I'm sorry, but as an AI language model, I can only answer questions about Astronomy. However, some examples of red fruits are apples, strawberries, cherries, and raspberries.

        
        # generate response using ChatGPT engine text-davinci-002-- shutdown in 01/04/2024 you could use the above function instead (openai.ChatCompletion.create). 
        def generate_response(user_input, age, topic):
            # clear conversation history for this user
            conversation_history = []
            # gpt-3.5-turbo  response variation
            # def generate_response(user_input, topic):
            #     response = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo",
            #         messages=[
            #             {"role": "system", "content": f"You are a expert in {topic} and You are talking to a 7 to 10 year old student. "
            #                                           f"Asnswer questions assuming this. If you asked a question outside the realm of {topic}, "
            #                                           f"please answer that you can only answer questions about {topic} and "
            #                                           f"don't answer further for questions outside {topic} and avoid responding to off-topic queries."},
            #             {"role": "user", "content": user_input}
            #         ],
            #         temperature=0.7,
            #         max_tokens=1024,
            #         top_p= 1,
            #         frequency_penalty=0,
            #         presence_penalty=0
            #     )
           
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=(
                    f"You are an expert in {topic} and You are talking to a {age} year old student. "
                    f"Answer questions assuming this. If you are asked a question outside the realm of {topic}, "
                    f"please answer that you can only answer questions about {topic} and "
                    f"don't answer further for questions outside {topic} and avoid responding to off-topic queries.\n\n"
                    f"User: {user_input}\nAssistant:"
                ),
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Extract response from the API response
            message = response['choices'][0]['text'].strip()

            # read conversation history from file
            with open(self.history_file, "r") as f:
                conversation_history = f.read().splitlines()

            # append user input and the corresponding response to conversation history file
            conversation_history.append(user_input)
            conversation_history.append(message)

            # write conversation history to file
            with open(self.history_file, "w") as f:
                f.write('\n'.join(conversation_history))

            return message

        def button_click():

            # Update conversation history file based on user's name and grade
            name = self.name_entry.get().strip()
            grade = self.grade_combobox.get().strip()
            # mandatory user name and grade filed
            if not name or not grade:
                messagebox.showerror("Error", "Please enter your name and grade.")
                return
            # Update conversation history based on user's name and grade
            conversation_history = update_history_file()

            # select age range
            age = self.age_combobox.get()

            #selecte topic
            current_topic = self.subject_combobox.get()

            # dynamic image updating functionality based on the selected topic
            image_file = TOPIC_IMAGES.get(current_topic, os.path.join(current_dir, "AMA_UI", "robo_AMA.png"))
            self.logo_image = customtkinter.CTkImage(Image.open(image_file), size=(240, 200))
            self.subject_image_label.configure(image=self.logo_image)  # changes subject image

            # if current topic is different than the stored topic, update the topic
            if self.topic != current_topic:
                self.topic = current_topic

            # get user input
            user_input = self.entry.get()

            # Add name and grade to user_input
            name = self.name_entry.get().strip()
            grade = self.grade_combobox.get().strip()
            user_input_with_name_grade = f"{name} (Grade {grade}): {user_input}"

            # generate response
            response = generate_response(user_input_with_name_grade, age, self.topic)

            # append user input and modified response to conversation history
            conversation_history.append(user_input_with_name_grade)
            conversation_history.append(response)

            # display response
            self.response_text.set(response)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, self.response_text.get())

            # write conversation history to file
            with open(history_file, "w") as f:
                f.write('\n'.join(conversation_history))

        def clear():
            # Clear response

            self.textbox.delete("1.0", tk.END)

            # Clear user query input
            self.entry.delete(0, tk.END)


        def reset():
            # Clear age and selected topic
            self.name_entry.delete(0, tk.END)
            self.age_combobox.set(" ")
            self.subject_combobox.set(" ")
            self.grade_combobox.set(" ")

            self.subject_image = customtkinter.CTkImage(Image.open(os.path.join("AMA_UI", "2.png")), size=(
            240, 200))  # changes the image back to transparent
            self.subject_image_label.configure(image=self.subject_image)

            # Clear conversation history for new user
            global conversation_history
            conversation_history = []

        # configure window
        self.title("Ask Me Anything")
        self.geometry(f"{1100}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # load image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "AMA_UI")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join("AMA_UI", "robo_AMA.png")), size=(80, 100))
        self.welcome_image = customtkinter.CTkImage(Image.open(os.path.join("AMA_UI", "welcome.png")), size=(250, 100))
        self.subject_image = customtkinter.CTkImage(Image.open(os.path.join("AMA_UI", "2.png")), size=(240, 220))

        # create sidebar frame with subframes (logo frame and input frame)
        self.sidebar_frame = customtkinter.CTkFrame(self, width=50, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=2)

        # logo frame
        self.logo_frame = customtkinter.CTkFrame(master=self.sidebar_frame, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsew")
        self.robo_image_label = customtkinter.CTkLabel(master=self.logo_frame, image=self.logo_image, compound="left",
                                                       text="")
        self.robo_image_label.grid(row=1, column=0)
        self.welcome_image_label = customtkinter.CTkLabel(master=self.logo_frame, image=self.welcome_image, text="")
        self.welcome_image_label.grid(row=1, column=1, sticky="n")

        # # #input frame
        self.input_frame = customtkinter.CTkFrame(master=self.sidebar_frame, fg_color="transparent")
        self.input_frame.grid(row=3, rowspan=2, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

        # input labels
        self.name_label = customtkinter.CTkLabel(master=self.input_frame, text=" Name:")
        self.name_label.grid(row=0, rowspan=1, column=0, padx=5, pady=5, sticky="w")

        self.grade_label = customtkinter.CTkLabel(master=self.input_frame, text=" Select Your Grade:")
        self.grade_label.grid(row=2, rowspan=1, column=0, padx=5, pady=5, sticky="w")

        self.age_label = customtkinter.CTkLabel(master=self.input_frame, text=" Select Your Age Range:")
        self.age_label.grid(row=4, rowspan=1, column=0, padx=5, pady=5, sticky="w")

        self.topic_label = customtkinter.CTkLabel(master=self.input_frame, text=" Select a Topic:")
        self.topic_label.grid(row=6, rowspan=1, column=0, padx=5, pady=5, sticky="w")

        # input widget
        self.name_entry = customtkinter.CTkEntry(master=self.input_frame, width=250)
        self.name_entry.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="e")
        self.grade_combobox = customtkinter.CTkComboBox(master=self.input_frame,
                                                        values=["3rd", "4th", "5th", "6th", "7th", "8th"])
        self.grade_combobox.grid(row=2, column=1, padx=20, pady=(10, 10))
        self.age_combobox = customtkinter.CTkComboBox(master=self.input_frame, values=["7-9", "9-11", "12-14"])
        self.age_combobox.grid(row=4, column=1, padx=20, pady=(10, 10))

        self.subject_combobox = customtkinter.CTkComboBox(master=self.input_frame,
                                                          values=["Astronomy", "Sneakers and Shoes", "Dinosaurs"])
        self.subject_combobox.grid(row=6, column=1, padx=20, pady=(10, 10))
        self.subject_combobox.bind("<<ComboboxSelected>>", update_image)

        self.subject_image_label = customtkinter.CTkLabel(master=self.input_frame, image=self.subject_image,
                                                          compound="left",
                                                          text="")  ## <-------- styling for subject/topic image ; seperate from robot logo
        self.subject_image_label.grid(row=8, rowspan=2, column=0, columnspan=2, padx=5, pady=20, sticky="n")

        self.resetbutton_frame = customtkinter.CTkButton(master=self.input_frame, text="Reset", command=reset)
        self.resetbutton_frame.grid(row=10, column=0, columnspan=2, padx=20, pady=20, sticky="ns")

        # create search frame
        self.search_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=1, column=1, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="nsew")

        self.prompt_text = tk.StringVar()
        self.prompt_text.set("Ready to explore! Choose a topic and ask your questions:")
        self.info_label = customtkinter.CTkLabel(master=self.search_frame, textvariable=self.prompt_text,
                                                 font=customtkinter.CTkFont(size=15, weight="normal"))
        self.info_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.entry = customtkinter.CTkEntry(master=self.search_frame, width=450)
        self.entry.grid(row=2, column=1, columnspan=3, padx=23, pady=15, sticky="w")

        self.main_button_1 = customtkinter.CTkButton(master=self.search_frame, text="Submit", command=button_click)
        self.main_button_1.grid(row=2, column=4, sticky="e")

        # create response frame
        self.response_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.response_frame.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        self.chatbot_label = customtkinter.CTkLabel(master=self.response_frame, text="Answer Box:",
                                                    font=customtkinter.CTkFont(size=15, weight="normal"))
        self.chatbot_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.textbox = customtkinter.CTkTextbox(master=self.response_frame, width=610, wrap=None)
        self.textbox.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="w")

        self.clearbutton_frame = customtkinter.CTkButton(master=self.response_frame, text="Clear", command=clear)
        self.clearbutton_frame.grid(row=8, column=3, sticky="nsew")
        ## clear button


if __name__ == "__main__":
    app = App()
    app.mainloop()
