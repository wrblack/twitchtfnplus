import PySimpleGUI as sg

colorValues = [
    "Blue",
    "Coral",
    "DodgerBlue",
    "SpringGreen",
    "YellowGreen",
    "Green",
    "OrangeRed",
    "Red",
    "GoldenRod",
    "HotPink",
    "CadetBlue",
    "SeaGreen",
    "Chocolate",
    "BlueViolet",
    "Firebrick"
]

inputLangs = ['ja', 'en']
outputLangs = ['en', 'ja']

layout = [
    [sg.Text("Your Twitch Channel:"), sg.Input(key="Twitch_Channel")],
    [sg.Text("Your Translator Account:"), sg.Input(key="Trans_Username")],
    [sg.Text("Your Twitch Access Token:"), sg.Input(password_char="*", key="Trans_ACCESS_TOKEN")],
    [sg.Text("Translation Text Color:"), sg.Listbox(values=colorValues, key="Trans_TextColor")],
    [sg.Text("Input Language"), sg.Listbox(values=inputLangs, key="lang_TransToHome")],
    [sg.Text("Output Language"), sg.Listbox(values=outputLangs, key="lang_HomeToOther")],
    [sg.Submit(), sg.Button('Exit'), sg.Button('Show')],
    [sg.Text("Testing:")], [sg.Text(size=(15,1), key="-OUTPUT-")]
]

window = sg.Window('TwitchTFN+', layout)
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "Show":
        window['-OUTPUT-'].update(values)
window.close()