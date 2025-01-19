import speech_recognition as sr


def map_audio_to_function(audio_input: str, available_functions: list[str]) -> str:
    audio_input = audio_input.lower()
    
    # Define common command patterns and their corresponding keywords
    command_patterns = {
        'move': ['move', 'raise', 'lift', 'lower'],
        'left': ['left'],
        'right': ['right'],
        'arm': ['arm', 'hand'],
        'leg': ['leg', 'foot'],
    }
    
    detected_keywords = []
    for category, keywords in command_patterns.items():
        if any(keyword in audio_input for keyword in keywords):
            detected_keywords.append(category)
    
    if detected_keywords:
        potential_function = '_'.join(detected_keywords)
        
        for function in available_functions:
            if potential_function.lower() in function.lower():
                return function
    
    return None

def listen_and_process_command() -> tuple[str, str]:
    """
    Listen for voice command and map it to an available function.

    How to use:
    function_to_call = listen_and_process_command()
    eg: left_uppercut
    """

    # TODO: change function names
    available_functions = [
            "move_left_arm",
            "move_right_arm",
            "move_left_leg",
            "move_right_leg"
        ]
       
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            
            result = map_audio_to_function(command, available_functions)
            print(f"Command: '{command}' -> Function: {result}")
            return result
            
    except sr.WaitTimeoutError:
        print("No speech detected within timeout period")
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    
    return None, None

if __name__ == "__main__":
    listen_and_process_command()