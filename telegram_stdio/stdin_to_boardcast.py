from telegram.ext import Updater, CommandHandler
import argparse
import json
import sys
import traceback

def start(bot, update):
    try:
        setting = bot.ahjzfags['setting']
        data = bot.ahjzfags['data']
    
        if 'whitelist' in setting:
            username = update.message.from_user.username
            if username not in setting['whitelist']:
                update.message.reply_text('BLOCKED')
                return
    
        chat_id = update.message.chat_id
        #print(chat_id)
        if chat_id not in data['chat_id_list']:
            data['chat_id_list'].append(update.message.chat_id)
            save(bot)
        update.message.reply_text('OK')
    except:
        traceback.print_exc()

def load_json(fn):
    with open(fn,'r') as fin:
        return json.load(fin)

def dump_json(fn, data):
    with open(fn,'w') as fout:
        json.dump(data, fout, indent=2)

def save(bot):
    dump_json(bot.ahjzfags['setting']['data'],bot.ahjzfags['data'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='stdin to boardcast')
    parser.add_argument('setting_fn', type=str)
    args = parser.parse_args()

    setting = load_json(args.setting_fn)
    try:
        data = load_json(setting['data'])
    except:
        data = {}
    if 'chat_id_list' not in data:
        data['chat_id_list'] = []
        
    ahjzfags = {} # runtime data
    ahjzfags['setting'] = setting
    ahjzfags['data'] = data
    
    updater = Updater(setting['token'])
    bot = updater.bot
    bot.ahjzfags = ahjzfags

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    #updater.idle()
    
    try:
        for line in sys.stdin:
            if line == None:
                break
            l = line.rstrip('\n')
            #sender.message(l)
            for chat_id in updater.bot.ahjzfags['data']['chat_id_list']:
                bot.send_message(chat_id, text=l)
    except:
        pass
    
    updater.stop()
