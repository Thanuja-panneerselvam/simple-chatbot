import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import re
import time
import threading

class SimpleChatbot:
    def __init__(self, name):
        self.name = name
        self.memory = {}
        
        # Define response patterns
        self.patterns = [
            (r'hi|hello|hey', self.greet),
            (r'what is your name', lambda _: f"My name is {self.name}!"),
            (r'how are you', lambda _: "I'm doing well, thank you! How about you?"),
            (r'my name is (.*)', self.remember_name),
            (r'what is my name', self.recall_name),
            (r'what time is it', lambda _: f"The current time is {time.strftime('%H:%M')}"),
            (r'what day is it', lambda _: f"Today is {time.strftime('%A, %B %d, %Y')}"),
            (r'bye|goodbye', lambda _: "Goodbye! It was nice chatting with you!"),
            (r'tell me a joke', self.tell_joke),
            (r'tell me a fact', self.tell_fact),
            (r'what can you do', self.capabilities),
            (r'who created you', lambda _: "I was created by a human using Python as a simple demonstration of rule-based chatbots."),
            (r'help', self.help_message),
            (r'thank you|thanks', lambda _: "You're welcome!"),
            (r'weather', lambda _: "I'm sorry, I don't have access to real-time weather data."),
            (r'how old are you', lambda _: "I'm just a simple program, so I don't have an age in the traditional sense."),
        ]
        
        # Default response
        self.default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting! Tell me more.",
            "I don't have a response for that yet.",
            "I'm still learning and don't know how to respond to that.",
            "Could you elaborate on that?"
        ]
    
    def greet(self, _):
        """Generate a greeting response"""
        greetings = [
            f"Hello! I'm {self.name}. How can I help you today?",
            f"Hi there! I'm {self.name}. Nice to meet you!",
            f"Hey! I'm {self.name}. What's on your mind?"
        ]
        return random.choice(greetings)
    
    def remember_name(self, message):
        """Remember the user's name"""
        name_match = re.search(r'my name is (.*)', message, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            self.memory['user_name'] = name
            return f"Nice to meet you, {name}! I'll remember your name."
        return "I didn't catch your name. Could you tell me again?"
    
    def recall_name(self, _):
        """Recall the user's name if stored in memory"""
        if 'user_name' in self.memory:
            return f"Your name is {self.memory['user_name']}!"
        return "I don't think you've told me your name yet."
    
    def tell_joke(self, _):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I'm reading a book on anti-gravity. It's impossible to put down!"
        ]
        return random.choice(jokes)
    
    def tell_fact(self, _):
        """Tell a random fact"""
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat.",
            "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
            "A group of flamingos is called a 'flamboyance'.",
            "The world's oldest known living tree is a Great Basin bristlecone pine tree in California, estimated to be over 5,000 years old.",
            "Octopuses have three hearts, nine brains, and blue blood."
        ]
        return random.choice(facts)
    
    def capabilities(self, _):
        """List what the chatbot can do"""
        return ("I can do several things:\n"
                "- Greet you and remember your name\n"
                "- Tell jokes and interesting facts\n"
                "- Tell you the current time and date\n"
                "- Respond to basic questions about myself\n"
                "- Have a simple conversation\n"
                "Just ask me something or type 'help' for guidance!")
    
    def help_message(self, _):
        """Provide help information"""
        return ("Here are some things you can ask me:\n"
                "- 'Hello' or 'Hi' to greet me\n"
                "- 'What is your name?'\n"
                "- 'My name is [your name]'\n"
                "- 'What is my name?'\n"
                "- 'Tell me a joke'\n"
                "- 'Tell me a fact'\n"
                "- 'What can you do?'\n"
                "- 'What time is it?'\n"
                "- 'What day is it?'\n"
                "- 'Goodbye' to end our conversation")
    
    def respond(self, message):
        """Generate a response based on the input message"""
        # Convert message to lowercase
        message = message.lower().strip()
        
        # Check for matching patterns
        for pattern, response_func in self.patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return response_func(message)
        
        # If no pattern matches, use a default response
        return random.choice(self.default_responses)


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.chatbot = SimpleChatbot("ChatPy")
        
        # Set window title and size
        self.root.title("ChatPy - Simple AI Chatbot")
        self.root.geometry("600x500")
        self.root.minsize(400, 400)
        
        # Create a frame for the chat display
        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a scrolled text widget for the chat history
        self.chat_history = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for the input area
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Create an entry widget for user input
        self.input_field = tk.Entry(self.input_frame)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        
        # Create a send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # Create a frame for additional buttons
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Create quick action buttons
        self.create_quick_buttons()
        
        # Set up fonts and colors
        self.setup_styles()
        
        # Display welcome message
        self.display_bot_message(self.chatbot.greet(""))
        
        # Focus on the input field
        self.input_field.focus_set()
    
    def setup_styles(self):
        # Configure text colors and tags
        self.chat_history.tag_configure("user", foreground="#0000FF")  # Blue for user
        self.chat_history.tag_configure("bot", foreground="#008000")   # Green for bot
        self.chat_history.tag_configure("system", foreground="#808080", font=("Arial", 9, "italic"))  # Gray for system
    
    def create_quick_buttons(self):
        # Create buttons for common actions
        actions = [
            ("Hello", "hello"),
            ("Tell a joke", "tell me a joke"),
            ("Tell a fact", "tell me a fact"),
            ("Help", "help"),
            ("Clear", self.clear_chat)
        ]
        
        for i, (text, action) in enumerate(actions):
            if callable(action):
                button = tk.Button(self.buttons_frame, text=text, command=action)
            else:
                button = tk.Button(self.buttons_frame, text=text, 
                                  command=lambda a=action: self.quick_action(a))
            button.pack(side=tk.LEFT, padx=5)
    
    def quick_action(self, action_text):
        """Handle quick action button clicks"""
        self.display_user_message(action_text)
        self.process_message(action_text)
    
    def send_message(self, event=None):
        """Handle sending a message"""
        message = self.input_field.get().strip()
        if message:
            self.display_user_message(message)
            self.input_field.delete(0, tk.END)
            
            # Process the message (with a small delay to make it feel more natural)
            threading.Thread(target=self.process_message, args=(message,)).start()
    
    def process_message(self, message):
        """Process user message and generate response"""
        # Add a small delay to make the interaction feel more natural
        time.sleep(0.5)
        
        # Get response from chatbot
        response = self.chatbot.respond(message)
        
        # Display the bot's response
        self.display_bot_message(response)
        
        # Check if the user said goodbye
        if re.search(r'bye|goodbye', message, re.IGNORECASE):
            # Add a small delay before showing the goodbye message box
            time.sleep(1)
            self.root.after(0, self.show_goodbye_message)
    
    def show_goodbye_message(self):
        """Show a goodbye message box"""
        messagebox.showinfo("Goodbye", "Thank you for chatting with ChatPy!")
    
    def display_user_message(self, message):
        """Display a user message in the chat history"""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "You: ", "user")
        self.chat_history.insert(tk.END, f"{message}\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)
    
    def display_bot_message(self, message):
        """Display a bot message in the chat history"""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{self.chatbot.name}: ", "bot")
        self.chat_history.insert(tk.END, f"{message}\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear the chat history"""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.display_bot_message(self.chatbot.greet(""))


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()