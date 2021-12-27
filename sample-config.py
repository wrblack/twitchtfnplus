######################################################
# PLEASE CHANGE FOLLOWING CONFIGS ####################
Twitch_Channel          = '<your twitch channel>'
Trans_Username          = '<your twitch channel>'
Trans_ACCESS_TOKEN      = '<your access token>'
#######################################################
# OPTIONAL CONFIGS ####################################
Trans_TextColor         = 'GoldenRod'
# Blue, Coral, DodgerBlue, SpringGreen, YellowGreen, Green, OrangeRed, Red, GoldenRod, HotPink, CadetBlue, SeaGreen, Chocolate, BlueViolet, and Firebrick

lang_TransToHome        = 'ja' # will output to this language
lang_HomeToOther        = 'en' # will translate TransToHome to this language

Show_ByName             = True
Show_ByLang             = True

Ignore_Lang             = ['']
Ignore_Users            = ['Nightbot', 'BikuBikuTest']
Ignore_Line             = ['http', 'BikuBikuTest', '888', '８８８']
Delete_Words            = ['saatanNooBow', 'BikuBikuTest']

# Any environment, set it to `True`, then text will be read by TTS voice!
# gTTS_In:User Input Text, gTTS_Out:Bot Output Text
gTTS_In                 = True
gTTS_Out                = True

# if you make TTS for only few lang, please add langID in the list
# for example, ['ja'] means Japanese only, ['ko','en'] means Korean and English are TTS!
ReadOnlyTheseLang       = ['en']

# Select the translate engine ('deepl' or 'google')
Translator              = 'deepl'

# Use Google Apps Script for tlanslating
# e.g.) GAS_URL         = 'https://script.google.com/macros/s/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/exec'
GAS_URL                 = ''

# If you meet any bugs, You can check some error message using Debug mode (Debug = True)
Debug                   = True
