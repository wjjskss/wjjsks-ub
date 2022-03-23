from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from meval import meval
import logging
from traceback import format_exc
import tracemalloc
import os

tracemalloc.start()

logging.basicConfig(level=logging.INFO)

api_id = input('Enter your api_id: ')
api_hash = input('Enter your api_hash: ')

app = Client('ub-session', api_id, api_hash)

@app.on_message(filters.command([' e'], prefixes='.') & filters.me)
async def evaluate_code(_, msg):
    try:
        text = msg.text.split('. e ')
        e = await meval(text[1], globals())
        txt = f'<strong>📄Input:</strong>\n<code>{text[1]}</code>\n<strong>📃Output:</strong>\n<code>{e}</code>'
        await msg.edit(txt)
    
    except MessageTooLong:
        f = open('evaluate.txt', 'a')
        f.write(e)
        f.close()
        
        await msg.edit('<strong>📃 The result of code will be written to file</strong>')
        await app.send_document(msg.from_user.id, r'C:\Users\user\Desktop\python\evaluate.txt')
        
        os.remove(r'C:\Users\user\Desktop\python\evaluate.txt')

    except Exception:
        txt1 = f'<strong>📄 Input:</strong>\n<code>{text[1]}</code>\n\n<strong>🚫 Error:</strong>\n<code>{format_exc()}</code>'
        await msg.edit(txt1)

import sqlite3 as sql
con = sql.connect('test1.db')
cur = con.cursor()

@app.on_message(filters.command([' note'], prefixes='.') & filters.me)
async def notes_sql(_, msg):
    try:
        if not msg.reply_to_message:
            text = msg.text.split('. note ')
            a = text[1]
            with con:
                cur.execute("INSERT INTO notes VALUES(?)", (a,))
                con.commit()
                await msg.edit(f'<strong>Note has been added...</strong>')
    
        else:
            txt = msg.reply_to_message.text
            with con:
                cur.execute("INSERT INTO notes VALUES(?)", (txt,))
                con.commit()
                await msg.edit(f'<strong>Note has been added...</strong>')
    except:
        pass
    
@app.on_message(filters.command([' mynotes'], prefixes='.') & filters.me)
async def mynotes_sql(_, msg):
        cur.execute("SELECT * FROM notes")
        n = cur.fetchall()
        con.commit()
        lst = [str('<code>'+x[0]+'</code>') for x in n]
        a = '\n\n'.join(lst)
        
        try:
            await msg.edit(f'{a}')
        
        except MessageEmpty:
            await msg.edit('<strong>No notes</strong>')

@app.on_message(filters.command([' delallnotes'], prefixes='.') & filters.me)
async def delallnotes(_, msg):
     with con:
        cur.execute("DELETE FROM notes")
        con.commit()
        await msg.edit('<strong>All notes have been deleted...</strong>')

@app.on_message(filters.command([' delnote'], prefixes='.') & filters.me)
async def delnotes(_, msg):
    text = msg.text.split('. delnote ')
    a = text[1]
    with con:
        cur.execute("DELETE FROM notes WHERE note=(?)", (a,))
        con.commit()
        await msg.edit(f'<strong>Note <code>{text[1]}</code> has been deleted...</strong>')

app.run()
