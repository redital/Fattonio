from telebot import types
from time import sleep
import telebot
from config import Token
import os

API_TOKEN = Token


bot = telebot.TeleBot(API_TOKEN)

intervallo= 1*60*60

os.chdir("assets")

fattoni={}
coglioni={}


@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardRemove()
    print(message.chat.type)

    
    
    if message.chat.type=="group":
        print(os.getcwd())
        open("Classifica dei fattoni in " + message.chat.title + ".txt","a")
        open("Classifica dei coglioni in " + message.chat.title + ".txt","a")
    
        lista_fattoni=open("Classifica dei fattoni in " + message.chat.title + ".txt","r").readlines()
        fattoni[message.chat.title]={}
        for i in lista_fattoni:
            fattoni[message.chat.title][i.split("\t",)[0]]=int(i.split("\t")[-1].replace("\n",""))
        print (fattoni[message.chat.title])
        lista_coglioni=open("Classifica dei coglioni in " + message.chat.title + ".txt","r").readlines()
        coglioni[message.chat.title]={}
        for i in lista_coglioni:
            coglioni[message.chat.title][i.split("\t",)[0]]=int(i.split("\t")[-1].replace("\n",""))
        print (coglioni[message.chat.title])
    
        bot.send_message( message.chat.id,
"""\
heylà
d'ora in poi farò un cannone ogni """ + converti_tempo(intervallo) +
""", oppure puoi farne uno tu quando vuoi, basta usare il comando /canna

""" , markup)
        i=0
        flag=True
        while flag:
            sleep(intervallo)
            bot.send_message( message.chat.id,"Oh ne ho girata una!\n\nChi fuma?", reply_markup=gen_markup(message))
            #i=i+1
            if i==2:
                flag=False

    else:
        bot.send_message( message.chat.id,
"""\
bro aggiungimi ad un gruppo e ti girerò qualche canna

""" , markup)


@bot.message_handler(commands=['canna'])
def canna(message):
    print(os.getcwd())
    markup=types.ReplyKeyboardRemove()
    if message.chat.type=="group":
        bot.send_message( message.chat.id,"Oh " + message.from_user.first_name + " ne ha girata una!\n\nChi fuma?", reply_markup=gen_markup(message))
        
    else:
        bot.send_message( message.chat.id,
"""\
bro aggiungimi ad un gruppo e te la giro io qualche canna

""" , markup)



@bot.message_handler(commands=['classifiche'])
def classifiche(message):
    print(os.getcwd())
    markup=types.ReplyKeyboardRemove()
    if message.chat.type=="group":
        controllo_fattoni="True"
        if message.chat.title not in fattoni.keys():
            fattoni[message.chat.title]={}
            lista_fattoni=open("Classifica dei fattoni in " + message.chat.title + ".txt","r").readlines()
            for i in lista_fattoni:
                fattoni[message.chat.title][i.split("\t",)[0]]=int(i.split("\t")[-1].replace("\n",""))
        if fattoni[message.chat.title]=={}:
            bot.send_message( message.chat.id,"La classifica fattoni è vuota qui, sarete mica degli sbirri?" , markup)
            controllo_fattoni=False
        if controllo_fattoni:
            classifica = sorted(fattoni[message.chat.title].items(), key=lambda x: x[1])
            text=""
            for key,value in classifica:
                text = key + "\t" + str(value) + "\n" + text
            bot.send_message( message.chat.id,"I PIU' FATTONI SONO\n------------------\n" + text,markup)

        controllo_coglioni="True"
        if message.chat.title not in coglioni.keys():
            coglioni[message.chat.title]={}
            lista_coglioni=open("Classifica dei coglioni in " + message.chat.title + ".txt","r").readlines()
            for i in lista_coglioni:
                coglioni[message.chat.title][i.split("\t",)[0]]=int(i.split("\t")[-1].replace("\n",""))
        if coglioni[message.chat.title]=={}:
            bot.send_message( message.chat.id,"La classifica coglioni è vuota qui, che palle, manco una risata mi fate fare" , markup)
            controllo_coglioni=False
        if controllo_coglioni:
            classifica = sorted(coglioni[message.chat.title].items(), key=lambda x: x[1])
            text=""
            for key,value in classifica:
                text = key + "\t" + str(value) + "\n" + text
            bot.send_message( message.chat.id,"I PIU' COGLIONI SONO\n------------------\n" + text,markup)
        
    else:
        bot.send_message( message.chat.id,"bro aggiungimi ad un gruppo e poi vediamo" , markup)




def gen_markup(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Il puma!", callback_data="Il puma!")
    markup.add(item1)
    item2 = types.InlineKeyboardButton("Io!", callback_data="Io!")
    markup.add(item2)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    markup=types.ReplyKeyboardRemove()
    
    bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,None)

    #print("ha detto il puma!")
    print(call.data)
    #print(call)
    #print(call.message.text + "\n" + str(call.message.id))
    #bot.send_message( call.message.chat.id,call.from_user.first_name + " ha detto il puma!", markup)
        
    if call.data == "Il puma!":
        print("ha detto il puma!")
        bot.send_message( call.message.chat.id,call.from_user.first_name + " l'ha detto per primo! Passategli un cannone", markup)
        
        if call.message.chat.title not in fattoni.keys():
            fattoni[call.message.chat.title]={}
        if call.from_user.first_name in fattoni[call.message.chat.title].keys():
            fattoni[call.message.chat.title][call.from_user.first_name]=int(fattoni[call.message.chat.title][call.from_user.first_name])+1
            
            lista_fattoni=open("Classifica dei fattoni in " + call.message.chat.title + ".txt","r").readlines()
            text=""
            for i in lista_fattoni:
                fattoni[call.message.chat.title][i.split("\t",)[0]]=int(i.split("\t")[-1].replace("\n",""))
                if i.split("\t",)[0]==call.from_user.first_name:
                    i=call.from_user.first_name + "\t" + str(fattoni[call.message.chat.title][call.from_user.first_name]+1) + "\n"
                print(i)
                text=text+i
            open("Classifica dei fattoni in " + call.message.chat.title + ".txt","w").write(text)
        else:
            fattoni[call.message.chat.title][call.from_user.first_name]=1
            stringa=call.from_user.first_name + "\t" + str(fattoni[call.message.chat.title][call.from_user.first_name]) + "\n"
            open("Classifica dei fattoni in " + call.message.chat.title + ".txt","a").write(stringa)

        

        

        

    if call.data == "Io!":
        print("è un coglione")
        bot.send_message( call.message.chat.id,call.from_user.first_name + " è un coglione", markup)
        bot.edit_message_reply_markup(call.message.chat.id,call.message.id,call.inline_message_id,gen_markup(call.message))

        if call.message.chat.title not in coglioni.keys():
            coglioni[call.message.chat.title]={}
        if call.from_user.first_name in coglioni[call.message.chat.title].keys():
            coglioni[call.message.chat.title][call.from_user.first_name]=int(coglioni[call.message.chat.title][call.from_user.first_name])+1

            lista_coglioni=open("Classifica dei coglioni in " + call.message.chat.title + ".txt","r").readlines()
            text=""
            for i in lista_coglioni:
                coglioni[call.message.chat.title][i.split("\t",)[0]]=int(i.split("\t")[-1].replace("\n",""))
                if i.split("\t",)[0]==call.from_user.first_name:
                    i=call.from_user.first_name + "\t" + str(coglioni[call.message.chat.title][call.from_user.first_name]+1) + "\n"
                print(i)
                text=text+i
            open("Classifica dei coglioni in " + call.message.chat.title + ".txt","w").write(text)
        else:
            coglioni[call.message.chat.title][call.from_user.first_name]=1
            stringa=call.from_user.first_name + "\t" + str(coglioni[call.message.chat.title][call.from_user.first_name]) + "\n"
            open("Classifica dei coglioni in " + call.message.chat.title + ".txt","a").write(stringa)
            

def converti_tempo(intervallo):
    ore=int(intervallo/(60*60))
    minuti=int((intervallo%(60*60))/60)
    secondi=(intervallo%(60*60))%60
    tempo = ""
    if ore > 0:
        if ore > 1:
            tempo = tempo + str(ore) + " ore "
        else :
            tempo = tempo + "ora "
    if minuti > 0:
        if ore > 0:
            if secondi > 0:
                tempo = tempo + ", "
            else:
                tempo = tempo + "e "
        if minuti > 1:
            tempo = tempo + str(minuti) + " minuti "
        else :
            if ore > 0:
                tempo = tempo + "un "
            tempo = tempo + "minuto "
    if secondi > 0:
        if ore > 0 or minuti > 0:
            tempo = tempo + "e "
        tempo = tempo + str(secondi) + " secondi"

    return tempo
    
tempo=converti_tempo(intervallo)
print("lo fa ogni " + tempo)
print("fatto")


bot.polling()






































