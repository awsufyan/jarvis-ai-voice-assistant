import speech_recognition as sr
import pyttsx3
import datetime
import requests
from bs4 import BeautifulSoup
import time

# Initialize the speech engine
engine = pyttsx3.init()

# Function to speak the text
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to take voice command with retries
def take_command(retries=3):
    r = sr.Recognizer()
    while retries > 0:
        try:
            with sr.Microphone() as source:
                print("🎤 Speak now... (You have 5 seconds)")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                print("🧠 Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"✅ You said: {query}")
                return query.lower()
        except sr.WaitTimeoutError:
            print("⏱️ Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("❌ Could not understand your speech. Try again.")
        except sr.RequestError as e:
            print(f"🌐 Could not connect to the speech recognition service: {e}")
        except Exception as e:
            print(f"⚠️ Unknown error: {e}")

        retries -= 1
        if retries > 0:
            print(f"🔁 Retrying... {retries} attempts left.")
            time.sleep(2)
    
    return input("⌨️ Couldn't understand. Type your command: ").lower()

# Function to fetch current Prime Minister of India from Wikipedia
def get_current_prime_minister():
    url = "https://en.wikipedia.org/wiki/Prime_Minister_of_India"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find infobox table
        infobox = soup.find("table", {"class": "infobox"})
        if infobox:
            # Find the row that contains 'Incumbent'
            rows = infobox.find_all("tr")
            for row in rows:
                header = row.find("th")
                if header and "Incumbent" in header.text:
                    # The name should be in the next <td>
                    incumbent_td = row.find("td")
                    if incumbent_td:
                        # Clean the name text (remove references and footnotes)
                        name = incumbent_td.get_text(separator=" ", strip=True)
                        return name
        return "Sorry, I couldn't fetch the current Prime Minister's name."
    except Exception as e:
        return f"Error fetching Prime Minister data: {e}"

# Function to fetch current President of India from Wikipedia
def get_current_president():
    url = "https://en.wikipedia.org/wiki/President_of_India"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        infobox = soup.find("table", {"class": "infobox"})
        if infobox:
            rows = infobox.find_all("tr")
            for row in rows:
                header = row.find("th")
                if header and "Incumbent" in header.text:
                    incumbent_td = row.find("td")
                    if incumbent_td:
                        name = incumbent_td.get_text(separator=" ", strip=True)
                        return name
        return "Sorry, I couldn't fetch the current President's name."
    except Exception as e:
        return f"Error fetching President data: {e}"

# Wikipedia summary fallback (optional)
def get_wikipedia_summary(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['extract']
        else:
            return "Sorry, I couldn't find relevant information."
    except requests.exceptions.RequestException as e:
        return "Sorry, I couldn't connect to the internet."

# Main function
def main():
    print("✅ Jarvis is starting...")
    speak("Hello, I am Jarvis. How can I help you?")

    while True:
        query = take_command()
        print(f"🎤 You said: {query}")

        if "search" in query:
            search_query = query.replace("search", "").strip()
            speak(f"Searching Wikipedia for: {search_query}")
            answer = get_wikipedia_summary(search_query)
            speak(answer)

        elif "who are you" in query or "your name" in query:
            speak("I am Jarvis, your personal assistant.")

        elif "time" in query:
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time_str}")

        elif "prime minister of india" in query:
            speak("Let me fetch the current Prime Minister of India for you.")
            answer = get_current_prime_minister()
            speak(answer)

        elif "president of india" in query:
            speak("Let me fetch the current President of India for you.")
            answer = get_current_president()
            speak(answer)

        elif "exit" in query or "quit" in query or "bye" in query:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()
