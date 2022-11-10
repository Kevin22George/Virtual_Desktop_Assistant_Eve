from flask import Flask, request, render_template
import webview
import speech_recognition as sr
import pywhatkit as pwk
import pyttsx3
import os
import webbrowser as wb
from googlesearch import search
import pyjokes
import random
import datetime
import wikipedia
from PyPDF2 import PdfFileReader

app = Flask(__name__)
window = webview.create_window('Eve', app)

@app.route('/')
def home():
    return render_template('signin.html')


@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    global greetings
    global info

    uname_info = request.form.get('uname')
    passw_info = request.form.get('passw')
    wrong_details_info = '* Incorrect username or password *'

    for line in open('Virtual Desktop Assistant - Eve/static/data/account_data.txt', 'r').readlines():
        info = line.split()

        if uname_info == info[1] and passw_info == info[2]:
            hour = int(datetime.datetime.now().hour)
            greetings = ['Good Morning,', 'Good Afternoon,', 'Good Evening,']
            
            if hour >= 0 and hour < 12:        
                return render_template('main.html', greetings = greetings[0], info = info[0].capitalize() + '!')

            elif hour >= 12 and hour < 5:                    
                return render_template('main.html', greetings = greetings[1], info = info[0].capitalize() + '!')

            else:                    
                return render_template('main.html', greetings = greetings[2], info = info[0].capitalize() + '!')

    if uname_info != info[1] == None or passw_info != info[2] == None:            
        return render_template('signin.html', wrong_details = wrong_details_info)

    return render_template('signin.html')


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    fname_info = request.form.get('fname')
    uname_info = request.form.get('uname')
    passw_info = request.form.get('passw')
    cpassw_info = request.form.get('cpassw')
    wrong_match_info = '* Password does not match *'

    if passw_info == cpassw_info and passw_info is not None and cpassw_info is not None:
        file = open('Virtual Desktop Assistant - Eve/static/data/account_data.txt', 'a')
        file.write(str(fname_info))
        file.write(' ')
        file.write(str(uname_info))
        file.write(' ')
        file.write(str(passw_info))
        file.write('\n')
        file.close()
        return render_template('success.html', fname = fname_info, uname = uname_info, passw = passw_info)
    
    elif passw_info != cpassw_info:
        return render_template('signup.html', wrong_match = wrong_match_info)

    return render_template('signup.html')


@app.route('/success', methods = ['POST', 'GET'])
def success():
    return render_template('success.html')


@app.route('/main', methods = ['POST', 'GET'])
def main():
    r = sr.Recognizer()
    m = sr.Microphone()
    va = pyttsx3.init()

    def speak(command):
        voice = va.getProperty('voices')
        va.setProperty('voice', voice[1].id)
        va.say(command)
        va.runAndWait()

    you = 'You:'
    eve = 'Eve:'
    question = 'How can I help you?'
    speak(question)

    try:
        with m as source:
            r.adjust_for_ambient_noise(source, duration = .2)
            audio = r.listen(source)            
            user = r.recognize_google(audio).lower()

            if 'open word' in user or 'open microsoft word' in user:
                question1 = 'Opening word...'
                speak(question1)

                os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010.lnk')       
            
                return render_template('main.html', question1 = f'{eve} {question1}', user = f'{you} {user.capitalize()}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')

            elif 'search' in user and 'youtube' in user:
                question1 = 'What would you like to search on youtube?'
                speak(question1)

                audio = r.listen(source)                
                user1 = r.recognize_google(audio).lower()
                user1 = user1.title()
                search = 'Searching for ' + user1
                speak(search)

                pwk.playonyt(user1)

                return render_template('main.html', search = f'{eve} {search}', question1 = f'{eve} {question1}', user = f'{you} {user.capitalize()}', user1 = f'{you} {user1}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')
            
            elif 'open google' in user:
                question1 = 'Opening google...'
                speak(question1)

                wb.open('https://www.google.com')

                return render_template('main.html', question1 = f'{eve} {question1}', user = f'{you} {user.capitalize()}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')

            elif 'open' in user and 'website' in user or 'website' in user:
                question1 = 'What website are you looking for?'
                speak(question1) 

                audio = r.listen(source)
                user1 = r.recognize_google(audio).lower()
                website = 'Opening ' + user1
                speak(website)

                for link in search(user1, num=1, stop=1):
                    wb.open(link)

                return render_template('main.html', question1 = f'{eve} {question1}', website = f'{eve} {website}', user = f'{you} {user.capitalize()}', user1 = f'{you} {user1}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')

            elif 'tell me a joke' in user or 'make me laugh' in user or 'funny' in user:
                joke = pyjokes.get_joke()
                speak(joke)

                review_list = ['Hope I made you laugh', 'Hope you liked that', 'This is one of my favorites', 'Hope it was a good one', 'Hope you enjoyed that one', '']
                review = random.choice(review_list)
                speak(review)

                return render_template('main.html', joke = f'{eve} {joke}', review = review, user = f'{you} {user.capitalize()}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')

            elif 'time' in user:                
                time = datetime.datetime.now().strftime('%I:%M %p')
                time_info = 'The time is ' + time
                speak(time_info)

                return render_template('main.html', time = f'{eve} {time_info}', user = f'{you} {user.capitalize()}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')

            elif 'question' in user or 'answer' in user:
                question1 = 'What is your question?'
                speak(question1)

                audio = r.listen(source)
                user1 = r.recognize_google(audio).lower()
                details = wikipedia.summary(user1, 1)
                speak(details)   

                return render_template('main.html', question1 = f'{eve} {question1}', details = f'{eve} {details}', user = f'{you} {user.capitalize()}', user1 = f'{you} {user1.capitalize()}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')

            elif 'pdf' in user:
                question1 = 'What pdf file are you looking for?'
                speak(question1)

                audio = r.listen(source)
                user1 = r.recognize_google(audio).lower()
                user1 = user1.capitalize()
                file = open('Virtual Desktop Assistant - Eve/static/pdf/' + user1 + '.pdf', 'rb')
                read = PdfFileReader(file)
                pages = read.numPages         
                pdf_info = user1 + ' consists of ' + str(pages) + ' pages. Which page would you like me to read?'
                speak(pdf_info)

                audio = r.listen(source)
                user2 = r.recognize_google(audio).lower()
                page = read.getPage(int(user2))
                text_info = page.extractText()
                speak(text_info)

                return render_template('main.html', question1 = f'{you} {question1}', pdf = f'{eve} {pdf_info}', text = f'{eve} {text_info}', user = f'{you} {user.capitalize()}', user1 = f'{you} {user1}', user2 = f'{you} {user2}', question = f'{eve} {question}', greetings = greetings[2], info = info[0].capitalize() + '!')            

            else: speak('invalid command')

    except sr.UnknownValueError: return render_template('main.html', greetings = greetings[2], info = info[0].capitalize() + '!')

    return render_template('main.html', question = question, greetings = greetings[2], info = info[0].capitalize() + '!')


if __name__ == '__main__':
    webview.start()
