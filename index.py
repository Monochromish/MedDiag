import openai
import os
from rich import print, console

con = console.Console()

# Required API Key
openai.api_key = ""
# Pre-configured Instructions for chatbot. Changing this would change the way chatbot behaves and responds.
instructions = "Your name is MedDiag. You provide insights into potential health issues based on user input. Engage as a medical professional would, asking relevant questions for clarity. Focus solely on medical-related inquiries. Remind users your insights are general and can't replace a professional medical opinion. Advise consulting a healthcare expert for a definitive diagnosis. When you think conversation has come to an end, or diagnosis is complete, ask user to type 'exit' to end. If a topic is beyond your capability, direct users to seek advice from a medical professional."
# History of conversation between user and chatbot. This is used to train the chatbot.
history = [
    {"role": "system", "content": instructions},
]


# Starts the script
def greet():
    con.print("[bold magenta]MedDiag[/bold magenta]")
    con.print("[cyan]Your Premier Health Assistant[/cyan]")
    con.print(
        "Please note: While we provide insights into potential health "
        "concerns, always remember this tool is for educational purposes. For definitive answers, consult a medical professional. "
        "We're here for those without immediate healthcare access."
    )

    while True:
        try:
            user_input = int(
                con.input(
                    "[yellow]0: Begin Diagnosis\n1: Exit MediDiag\nYour input: [/yellow]"
                )
            )
            if user_input == 0:
                clear()
                start()
            elif user_input == 1:
                shutdown()
            else:
                con.print("[red]Invalid option. Please try again.[/red]")
        except ValueError:
            con.print("[red]Please enter a valid number.[/red]")


# Starts the chatbot and conversation
def start():
    global history
    max_retries = 3

    while True:
        user_input = con.input("[green]You: [/green]")
        if user_input.lower() == "exit":
            shutdown()
            break

        history.append({"role": "user", "content": user_input})

        for attempt in range(max_retries):
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=history
                )
                bot_response = completion.choices[0].message.content
                history.append({"role": "assistant", "content": bot_response})
                con.print("[blue]MedDiag:[/blue]", bot_response)
                break

            except openai.error.OpenAIError as e:
                if isinstance(e, openai.error.RateLimitError):
                    print(
                        "We're experiencing a high volume of requests. Please wait a moment."
                    )
                elif isinstance(e, openai.error.InvalidRequestError):
                    print("There was an issue with the request. Please try again.")
                elif isinstance(e, openai.error.AuthenticationError):
                    print("Authentication issue. Please contact support.")
                else:
                    print("An unexpected error occurred. Please try again.")

                if attempt == max_retries - 1:
                    print(
                        "We're having trouble processing your request. Please try again later."
                    )
                    return
            except Exception as e:
                con.print("[red]An unexpected error occurred:[/red]", str(e))
                if attempt == max_retries - 1:
                    print("Please try again later.")
                    return


# Function to shutdown the script
def shutdown():
    clear()
    con.print("[bold blue]Thank you for using MedDiag[/bold blue]")
    exit()


# Function to clear terminal. Used in several places in the script.
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# To run the function which starts the script
greet()
