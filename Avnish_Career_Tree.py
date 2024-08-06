import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import openai
import os 


openai_api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_key = openai_api_key
print(openai_api_key)

# Store conversation history
conversation_history = []

# OpenAI API interaction
def chat_with_gpt(prompt):
    global conversation_history
    conversation_history.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    message_content = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": message_content})
    return message_content

# Step 1: Select location
def select_location():
    location = simpledialog.askstring("Input", "Please enter your location (e.g., Raleigh, NC):")
    if location:
        return location
    else:
        messagebox.showerror("Error", "Please enter a valid location.")
        return select_location()

# Step 2: Suggest universities based on location
def suggest_universities(location):
    universities_prompt = f"Based on {location}, suggest some universities (only include the names):"
    response = chat_with_gpt(universities_prompt)
    university_list = response.split('\n')  # Split universities by new line
    return [u.strip() for u in university_list if u.strip()]  # Strip and filter out empty lines

# Step 3: Get user interests
def get_user_interests():
    interests = simpledialog.askstring("Input", "What are you interested in? (e.g., Science, Arts, Sports)")
    return interests

# Step 4: Get user hobbies
def get_user_hobbies():
    hobbies = simpledialog.askstring("Input", "What are your hobbies? (e.g., Reading, Sports, Gaming)")
    return hobbies

# Step 5: Get user details and university selection
def get_user_details(location):
    education_level = simpledialog.askstring("Input", "What is your current education level? (e.g., 9th grade, 10th grade)")
    aptitude = simpledialog.askstring("Input", "What is your aptitude or skill level related to your interests? (e.g., Beginner, Intermediate, Advanced)")
    grades = simpledialog.askstring("Input", "What are your current grades or academic performance? (e.g., A, B, C)")

    universities = suggest_universities(location)
    
    # Display university selection list
    def select_university():
        selected_indices = listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            root.unbind("<Return>")  # Unbind the Enter key
            selection_window.destroy()
            selected_university.set(universities[selected_index])
        else:
            messagebox.showerror("Error", "Please select a university.")
    
    selection_window = tk.Toplevel(root)
    selection_window.title("Select a University")
    
    tk.Label(selection_window, text="Please select a university:").grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Create a frame to contain the Listbox for proper alignment
    listbox_frame = tk.Frame(selection_window)
    listbox_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE)
    for uni in universities:
        listbox.insert(tk.END, uni)
    
    # Align the Listbox with the frame
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    select_button = tk.Button(selection_window, text="Select", command=select_university)
    select_button.grid(row=2, column=0, padx=10, pady=5)

    selected_university = tk.StringVar()
    root.bind("<Return>", lambda event: select_university())

    selection_window.wait_window()
    return aptitude, grades, education_level, selected_university.get()


# Generate industry based on interests
def generate_industry_based_on_interests(interests):
    industry_prompt = f"Based on the interest in {interests}, suggest a suitable industry."
    industry_response = chat_with_gpt(industry_prompt)
    return industry_response

# Generate a summary based on user inputs
def generate_summary(location, interests, hobbies, aptitude, grades, education_level, industry):
    summary_prompt = (f"Provide a summary based on the following information:\n"
                      f"Location: {location}\n"
                      f"Interests: {interests}\n"
                      f"Hobbies: {hobbies}\n"
                      f"Aptitude: {aptitude}\n"
                      f"Grades: {grades}\n"
                      f"Education Level: {education_level}\n"
                      f"Industry: {industry}\n"
                      f"The summary should include two paragraphs, each being two to three sentences.")
    summary_response = chat_with_gpt(summary_prompt)
    return summary_response

# Generate advice based on user inputs
def generate_career_advice():
    # Provide concise advice based on user inputs
    advice_prompt = "Based on your interests and background, here's some advice for your career:"
    advice_response = chat_with_gpt(advice_prompt)
    # Limit advice to two paragraphs
    advice_paragraphs = advice_response.split('\n\n')[:2]  # Limit to first two paragraphs
    return '\n\n'.join(advice_paragraphs)

# Generate career options based on user inputs
def generate_career_options(interests):
    options_prompt = f"Suggest four to five career options based on the interest in {interests}. Include a brief one-sentence description for each career."
    options_response = chat_with_gpt(options_prompt)
    return options_response

# Generate salary information for career options
def generate_salary_info(career_options):
    salary_info = []
    for career in career_options.split('\n'):
        career = career.strip()
        if career:  # Avoid empty lines
            # Separate career name from the description
            parts = career.split(':')
            career_name = parts[0].strip()
            
            salary_prompt = (f"Provide the salary information for a career in {career_name}. "
                             f"Include low, median, and high salaries in the format:\n"
                             f"Low: Salary\n"
                             f"Median: Salary\n"
                             f"Highest: Salary\n"
                             f"Only provide the salary ranges, do not include any additional explanations.")
            salary_response = chat_with_gpt(salary_prompt)
            
            # Clean and format the salary response
            formatted_salary_response = ""
            for line in salary_response.split('\n'):
                if line.strip() and not any(keyword in line.lower() for keyword in ["factors", "location", "education", "experience", "organization"]):
                    formatted_salary_response += f"{line.strip()}\n"
                    
            salary_info.append((career_name, formatted_salary_response))
    
    # Format salary info with new lines between careers
    formatted_salary_info = '\n'.join(
        [f"- {career_name}:\n  Salary Info:\n  {salary}"
         for career_name, salary in salary_info]
    )
    return formatted_salary_info

# Generate degree requirements for career options
def generate_degree_requirements(career_options):
    degree_requirements = []
    for career in career_options.split('\n'):
        career = career.strip()
        if career:  # Avoid empty lines
            # Separate career name from the description
            parts = career.split(':')
            career_name = parts[0].strip()
            
            degree_prompt = (f"Provide the degree requirements for a career in {career_name}. "
                             f"Include the type of degree(s) required and any additional requirements in the format:\n"
                             f"Degree(s) Required: Degree\n"
                             f"Additional Requirements: Requirements\n"
                             f"Only provide the degree requirements, do not include any additional explanations.")
            degree_response = chat_with_gpt(degree_prompt)
            
            # Clean and format the degree response
            formatted_degree_response = ""
            for line in degree_response.split('\n'):
                if line.strip() and not any(keyword in line.lower() for keyword in ["factors", "location", "education", "experience", "organization"]):
                    formatted_degree_response += f"{line.strip()}\n"
                    
            degree_requirements.append((career_name, formatted_degree_response))
    
    # Format degree requirements info with new lines between careers
    formatted_degree_requirements = '\n'.join(
        [f"- {career_name}:\n  Degree Requirements:\n  {requirements}"
         for career_name, requirements in degree_requirements]
    )
    return formatted_degree_requirements

# Function to handle user input and GPT response in GUI
def handle_input(event=None):
    user_input = user_entry.get()
    if user_input.lower() in ["quit", "exit", "bye"]:
        root.quit()
    else:
        response = chat_with_gpt(user_input)
        response_text.insert(tk.END, f"\nYou: {user_input}\n", 'blue')  # User input color
        response_text.insert(tk.END, f"Chatbot:\n{response}\n", 'white')  # Chatbot response color
        response_text.see(tk.END)
    user_entry.delete(0, tk.END)

# Ask user if they want to display salaries and degree requirements
def ask_display_options():
    show_salaries = messagebox.askyesno("Display Salaries", "Do you want to display salaries for each career listed?")
    show_requirements = messagebox.askyesno("Display Degree Requirements", "Do you want to display degree requirements for each career listed?")
    return show_salaries, show_requirements

# Main program execution
def main():
    location = select_location()
    universities = suggest_universities(location)

    interests = get_user_interests()
    hobbies = get_user_hobbies()
    aptitude, grades, education_level, selected_university = get_user_details(location)

    industry = generate_industry_based_on_interests(interests)
    
    if selected_university:
        response_text.insert(tk.END, f"\nWelcome to {selected_university.split('.')[1].strip()}!\n", 'white')

    summary = generate_summary(location, interests, hobbies, aptitude, grades, education_level, industry)
    response_text.insert(tk.END, f"\nSummary:\n{summary}\n", 'white')
    
    prompt = (f"You are interested in {interests} and enjoy {hobbies}. Your aptitude in {aptitude} combined with "
              f"your current grades of {grades} and education level of {education_level} suggests a strong foundation "
              f"for a career in {industry}. Selected University: {selected_university}")
    response = chat_with_gpt(prompt)
    
    career_options = generate_career_options(interests)
    
    show_salaries, show_requirements = ask_display_options()
    
    salary_info = generate_salary_info(career_options) if show_salaries else ""
    degree_requirements = generate_degree_requirements(career_options) if show_requirements else ""
    
    response_text.insert(tk.END, f"\nCareer Advice:\n{generate_career_advice()}\n", 'white')
    response_text.insert(tk.END, f"\nCareer Options:\n{career_options}\n", 'white')
    if show_salaries:
        response_text.insert(tk.END, f"\nSalary Information:\n{salary_info}\n", 'white')
    if show_requirements:
        response_text.insert(tk.END, f"\nDegree Requirements:\n{degree_requirements}\n", 'white')

# GUI setup
root = tk.Tk()
root.title("Career Information Tool")
root.configure(background='gray')  # Gray background 

# Outer frame with gray background and black border
outer_frame = tk.Frame(root, bd=5, relief=tk.FLAT, background='gray', highlightbackground='black', highlightcolor='black', highlightthickness=2)  # Gray background with black border
outer_frame.pack(padx=5, pady=5)

# Inner frame with gray background
inner_frame = tk.Frame(outer_frame, bd=2, background='gray')  # Gray background
inner_frame.pack(padx=5, pady=5)

# Define font size for ScrolledText
font = ('Helvetica', 20)  # Font name and size

# Chatbot response box with gray background, white text, and black border
response_text = scrolledtext.ScrolledText(inner_frame, wrap=tk.WORD, width=100, height=30, background='gray', foreground='white', highlightbackground='black', highlightcolor='black', highlightthickness=2)  # Gray background with white text and black border
response_text.pack(padx=10, pady=10)

# Configure tags for text color and font
response_text.tag_configure('blue', foreground='blue', font=font)  # User input color and font size
response_text.tag_configure('white', foreground='white', font=font)  # Chatbot response color and font size

user_entry = tk.Entry(inner_frame, width=100, background='gray', foreground='white')  # Gray background with white text
user_entry.pack(padx=10, pady=10)
user_entry.bind("<Return>", handle_input)

submit_button = tk.Button(inner_frame, text="Submit", command=handle_input, background='gray', foreground='black', bd=2, relief=tk.RAISED, highlightbackground='blue', highlightcolor='blue', highlightthickness=2)  # Blue border with gray background and black text
submit_button.pack(padx=10, pady=10)

start_button = tk.Button(inner_frame, text="Start", command=main, background='gray', foreground='black', bd=2, relief=tk.RAISED, highlightbackground='blue', highlightcolor='blue', highlightthickness=2)  # Blue border with gray background and black text
start_button.pack(padx=10, pady=10)

# Introduction message
messagebox.showinfo("Welcome", "Welcome to the Career Information Tool! This tool will help you explore career options based on your interests and preferences. Let's get started!")

root.mainloop()
 
