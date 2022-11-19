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
import pyscreenshot as pyshot
import time as t

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
            r.adjust_for_ambient_noise(source, duration = 1)
            audio = r.listen(source)            
            user = r.recognize_google(audio).lower()

            if 'open word' in user or 'open microsoft word' in user:
                question1 = 'Opening word...'
                speak(question1)

                os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010.lnk')                        

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + question1))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            elif 'search' in user and 'youtube' in user:
                question1 = 'What would you like to search on youtube?'
                speak(question1)

                audio = r.listen(source)                
                user1 = r.recognize_google(audio).lower()
                user1 = user1.title()
                search = 'Searching for ' + user1
                speak(search)

                pwk.playonyt(user1)  

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + question1))
                convo.write('\n')
                convo.write(str(you + ' ' + user1.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + search))
                convo.write('\n')
                convo.write('\n')
                convo.close()              
            
            elif 'open google' in user:
                question1 = 'Opening google...'
                speak(question1)

                wb.open('https://www.google.com')      

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + question1))
                convo.write('\n')
                convo.write('\n')
                convo.close()          

            elif 'website' in user:
                question1 = 'What website are you looking for?'
                speak(question1) 

                audio = r.listen(source)
                user1 = r.recognize_google(audio).lower()
                website = 'Opening ' + user1
                speak(website)

                for link in search(user1, num=1, stop=1):
                    wb.open(link)

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + question1))
                convo.write('\n')
                convo.write(str(you + ' ' + user1.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + website))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            elif 'tell me a joke' in user or 'make me laugh' in user or 'funny' in user:
                joke = pyjokes.get_joke()
                speak(joke)

                review_list = ['Hope I made you laugh', 'Hope you liked that', 'This is one of my favorites', 'Hope it was a good one', 'Hope you enjoyed that one', '']
                review = random.choice(review_list)
                speak(review)

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + joke + ' ' + review))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            elif 'time' in user:                
                time = datetime.datetime.now().strftime('%I:%M %p')
                time_info = 'The time is ' + time
                speak(time_info)

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + time_info))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            elif 'question' in user or 'answer' in user:
                question1 = 'What is your question?'
                speak(question1)

                audio = r.listen(source)
                user1 = r.recognize_google(audio).lower()
                details = wikipedia.summary(user1, 1)
                speak(details)

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + question1))
                convo.write('\n')
                convo.write(str(you + ' ' + user1.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + details))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            elif 'pdf' in user:
                question1 = 'What pdf file are you looking for?'
                speak(question1)

                audio = r.listen(source)
                user1 = r.recognize_google(audio).lower()
                user1 = user1.capitalize()
                file = open('Virtual Desktop Assistant - Eve/static/pdf/' + user1 + '.pdf', 'rb')

                question2 = 'Would you like to open ' + user1 + '?'
                speak(question2)

                audio = r.listen(source)
                user2 = r.recognize_google(audio).lower()                                

                if 'yes' in user2:
                    pdf_open = ('Opening ' + user1)
                    speak(pdf_open)
                    os.startfile('Virtual Desktop Assistant - Eve\\static\\pdf\\' +  user1 + '.pdf')
                
                elif 'no' in user2:
                    pass

                read = PdfFileReader(file)
                pages = read.numPages
                pdf_info = user1 + ' consists of ' + str(pages) + ' pages. Which page would you like me to read?'
                speak(pdf_info)

                audio = r.listen(source)
                user3 = r.recognize_google(audio).lower()
                page = read.getPage(int(user3))
                text_info = page.extractText()
                speak(text_info)

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + question1))
                convo.write('\n')
                convo.write(str(you + ' ' + user1.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + question2))
                convo.write('\n')
                convo.write(str(you + ' ' + user2.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + pdf_open + ' ' + pdf_info))
                convo.write('\n')
                convo.write(str(you + ' ' + user3))
                convo.write('\n')
                convo.write(str(eve + ' ' + text_info))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            elif 'google search' in user or 'google' in user:                          
                user = user.replace('google search', '')
                user = user.replace('google', '')
                pwk.search(user)

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            elif '' in user:
                statement = 'Alright'
                speak(statement)
                user = user.replace('take', '')
                user = user.replace('screenshots', '')
                user = user.replace('to', '2')
                user = user.replace('two', '2')
                for i in range(int(user)):
                    t.sleep(4)
                    screenshot = ('Taking screenshot')
                    speak(screenshot)
                    t.sleep(1.5)
                    image_name = 'screenshot-' + str(datetime.datetime.now())
                    image_name = image_name.replace(":", "")
                    screenshot = pyshot.grab()
                    filepath = 'Virtual Desktop Assistant - Eve/static/screenshots/' + image_name + '.png'
                    screenshot.save(filepath)
                    screenshot1 = 'Screenshot taken'
                    speak(screenshot1)

                convo = open('Virtual Desktop Assistant - Eve/static/data/conversation_record.txt', 'a')
                convo.write(str(eve + ' ' + question))
                convo.write('\n')
                convo.write(str(you + ' ' + user.capitalize()))
                convo.write('\n')
                convo.write(str(eve + ' ' + statement))
                convo.write('\n')
                convo.write(str(eve + ' ' + screenshot))
                convo.write('\n')
                convo.write(str(eve + ' ' + screenshot1))
                convo.write('\n')
                convo.write('\n')
                convo.close()

            else: speak('invalid command')

    except sr.UnknownValueError: return render_template('main.html', greetings = greetings[2], info = info[0].capitalize() + '!')

    return render_template('main.html', greetings = greetings[2], info = info[0].capitalize() + '!')


if __name__ == '__main__':
    webview.start()
    # app.run(debug=True)
