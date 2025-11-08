import subprocess

def get_gemini_response(prompt: str) -> str:
    command = ["gemini", "-p", prompt]
    try:
        result = subprocess.run(
            command,
            capture_output=True,  # Capture stdout and stderr
            text=True,            # Decode output as a string (not bytes)
            check=True            # Raise an error if the command fails
        )
        
        # 3. The successful output is stored in result.stdout
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        # Handle cases where the 'gemini' command fails (e.g., authentication error)
        error_output = f"GEMINI CLI Error: {e.stderr.strip()}"
        print(error_output)
        return f"Error: Failed to get response from Gemini CLI. Check terminal for details.\n{error_output}"
    
    except FileNotFoundError:
        # Handle cases where the 'gemini' command is not found
        return "Error: 'gemini' command not found. Ensure the Gemini CLI is installed and in your system's PATH."


# --- Example Usage ---
user_prompt = "What are the three most popular Python GUI libraries for creating a chat interface?"
print(f"Sending prompt to Gemini CLI: '{user_prompt}'\n")

# Call the function to get the response
gemini_output = get_gemini_response(user_prompt)

# Print the captured output
print("--- Gemini CLI Response ---")
print(gemini_output)
print("---------------------------")