# Gesture Alchemy - Sign Language Translator 🤟

A real-time, speech-to-sign language desktop application that helps bridge the communication gap for the hearing-impaired community. Speak into your microphone, and watch the words translate into visual sign language gestures!
🌟 Key Features

    🎤 Real-Time Speech Recognition: Utilizes Google's Speech Recognition API to instantly capture and convert spoken words into text.

    🎨 Dynamic Visual Translation: Translates recognized phrases into corresponding sign language GIFs for fluid, easy-to-understand communication.

    🔡 Letter-by-Letter Spelling: If a word isn't in the phrase library, the app automatically spells it out character by character, ensuring no word is left untranslated.

    🖥️ Simple & Intuitive GUI: Built with Tkinter, the interface is clean, straightforward, and easy for anyone to use.

    🚀 Responsive & Non-Blocking: Employs multithreading to handle the audio-listening process, so the UI remains smooth and responsive at all times.

🛠️ How It Works

The application follows a simple yet effective workflow:

    Listen: The app listens for audio input from the user's microphone.

    Recognize: The captured audio is sent to Google's Speech Recognition API, which processes it and returns the recognized text.

    Translate:

        The application's logic checks if the recognized text matches a known phrase (e.g., "Hello", "Thank You"). If it's a match, it displays the corresponding GIF.

        If the phrase is not found, the application breaks the word down and displays a sequence of images for each letter, spelling it out in sign language.

    Display: The final visual output (GIF or letter sequence) is rendered on the Tkinter GUI.
    📁 SignMedia Folder

For the application to work correctly, you must have a folder named SignMedia in the same directory as the script. This folder should contain:

    Phrase GIFs: Animated GIFs for common words or phrases (e.g., Hello.gif, HowAreYou.gif).

    Letter Images: Static images (JPG or PNG) for each letter of the alphabet (e.g., A.jpg, B.jpg).

    Initial Logo: A default image to display on startup (e.g., signlang.png).

💻 How to Use the App

    Launch the application.

    Click the "Start Listening" button.

    Speak clearly into your microphone.

    The application will display the sign language equivalent of what you said.

    To stop the application, say "Good Bye" or "Stop Listening".

🔧 Technologies Used

    Python: Core programming language.

    Tkinter: For the graphical user interface (GUI).

    SpeechRecognition: To capture microphone input and perform speech-to-text conversion.

    Pillow (PIL Fork): For handling and displaying images and GIFs.

    Google Speech Recognition API: The backend service for converting speech to text.
