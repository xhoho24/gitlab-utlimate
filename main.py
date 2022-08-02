from distutils.log import info
from fileinput import filename
from pyobigram.utils import sizeof_fmt,get_file_size,createID
from pyobigram.client import ObigramClient,inlineQueryResultArticle
import requests
import config
from base64 import b64encode
import gitlab
import re

from JDatabase import JsonDatabase
import zipfile
import os
import infos
import xdlink
import acortar
import mediafire
import datetime
import time
import youtube

from pydownloader.downloader import Downloader
from ProxyCloud import ProxyCloud
import ProxyCloud
import socket
import tlmedia
import S5Crypto
import json
LOG_ID = -1001611044759
BOT_NAME = '@ShellHelp_robot'
jsonfile = 'listdownload.json'


def downloadFile(downloader,filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        thread = args[2]
        if thread.getStore('stop'):
            downloader.stop()
        downloadingInfo = infos.createDownloading(filename,totalBits,currentBits,speed,time,tid=thread.id)
        bot.editMessageText(message,downloadingInfo)
    except Exception as ex: print(str(ex))
    pass

def delete(filename, update, bot, message):
    username = update.message.sender.username
    jdb = JsonDatabase('database')
    jdb.check_create()
    jdb.load()
    user_info = jdb.get_user(username)  
    gl = gitlab.Gitlab(str(user_info['host']), private_token=str(user_info['private_token']))
    project = gl.projects.get(str(user_info['project']))
    project.files.delete(file_path=filename, commit_message='Delete '+filename, branch=str(user_info["dir"]))
    infotext='🗑️ Archivo '+filename+' ha sido borrado 🗑️\n'
    bot.editMessageText(message,infotext, parse_mode="markdown")

def uploadFile(filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        originalfile = args[2]
        thread = args[3]
        downloadingInfo = infos.createUploading(filename,totalBits,currentBits,speed,time,originalfile)
        bot.editMessageText(message,downloadingInfo)
    except Exception as ex: print(str(ex))
    pass

def processUploadFiles(filename,update,bot,message):
    username = update.message.sender.username
    jdb = JsonDatabase('database')
    jdb.check_create()
    jdb.load()
    user_info = jdb.get_user(username)
    branch = str(user_info["dir"])
    filedelete = filename
    size = os.path.getsize(filename)
    #proxy = ProxyCloud.parse(user_info['proxy'])
    bot.editMessageText(message,'🕐Preparando para subir {0}☁...'.format(filename))
    gl = gitlab.Gitlab(str(user_info['host']), private_token=str(user_info['private_token']))
    project = gl.projects.get(str(user_info['project']))
    with open(filename, 'rb') as f:
        bin_content = f.read()
    b64_content = b64encode(bin_content).decode('utf-8')
    # b64_content must be a string!
    filename = re.sub(r"[^a-zA-Z0-9.-_]","",filename)
    filename = filename.replace('_','-')
    print(f'Subiendo '+filename)
    bot.editMessageText(message,'⏫Subiendo {} de {}☁'.format(filename, sizeof_fmt(size)))
    header = {'file_path': filename,'branch': branch,'content': b64_content,'author_email': 'matador@gmail.com','author_name': 'username','encoding': 'base64','commit_message': 'create'}
    f = project.files.create(header)
    infotext = infos.createFinish(filename)
    logtext = infos.logFinish(filename,username)
    print(f)
    print(logtext)
    url = user_info['host']
    urlfilter = url.split('.')[-1]
    urlfilter = urlfilter.replace('/','')
    if urlfilter == 'cu':
        link = url+'api/v4/projects/'+str(user_info['project'])+'/repository/files/'+filename+'/raw?ref='+str(user_info["dir"])
    else:
        urlhost = url.replace('https://','http://nexus.uclv.edu.cu/repository/')
        link = urlhost+'api/v4/projects/'+str(user_info['project'])+'/repository/files/'+filename+'/raw?ref='+str(user_info["dir"])
    bot.sendMessage(chat_id=LOG_ID, text=logtext, parse_mode="markdown")
    sendTxt(filename,link,update,bot)
    bot.editMessageText(message,infotext, parse_mode="markdown")
    os.unlink(filedelete)

def sendTxt(file_name,link,update,bot):
    name = file_name+'.txt'
    txt = open(name,'w')
    separator= '\n'
    txt.write(link+separator)
    txt.close()
    bot.sendFile(update.message.chat.id,name)
    print(name)
    os.unlink(name)

def ddl(update,bot,message,url,file_name='',thread=None,jdb=None):
    downloader = Downloader()
    file = downloader.download_url(url,progressfunc=downloadFile,args=(bot,message,thread))
    if not downloader.stoping:
        processUploadFiles(file,update,bot,message)

def onmessage(update,bot:ObigramClient):
    try:
        thread = bot.this_thread
        username = update.message.sender.username
        tl_admin_user = os.environ.get('tl_admin_user')

        #set in debug
        tl_admin_user = 'ElJoker63'

        jdb = JsonDatabase('database')
        jdb.check_create()
        jdb.load()

        user_info = jdb.get_user(username)

        if username == tl_admin_user or user_info :  # validate user
            if user_info is None:
                if username == tl_admin_user:
                    jdb.create_admin(username)
                else:
                    jdb.create_user(username)
                user_info = jdb.get_user(username)
                jdb.save()
        else:return

        msgText = ''
        try: msgText = update.message.text
        except:pass

        # comandos de admin
        if '/adduser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_user(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora tiene acceso al bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                    bot.sendMessage(chat_id=LOG_ID, text='<b>BOT:</b> '+BOT_NAME+'\n<b>💢@'+username+'</b> ha añadido a <b>@'+user+'</b> como usuario💢', parse_mode="html")
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /adduser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/addadmin' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_admin(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora es admin del bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                    username = update.message.sender.username
                    bot.sendMessage(chat_id=LOG_ID, text='<b>BOT:</b> '+BOT_NAME+'\n<b>💢@'+username+'</b> ha añadido a <b>@'+user+'</b> como admin💢', parse_mode="html")
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /addadmin username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/banuser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    if user == username:
                        bot.sendMessage(update.message.chat.id,'❌No Se Puede Banear Usted❌')
                        return
                    jdb.remove(user)
                    jdb.save()
                    msg = '🦶Fuera @'+user+' Baneado❌'
                    bot.sendMessage(update.message.chat.id,msg)
                    username = update.message.sender.username
                    bot.sendMessage(chat_id=LOG_ID, text='<b>BOT:</b> '+BOT_NAME+'\n<b>💢@'+username+'</b> ha baneado a <b>@'+user+'</b>💢', parse_mode="html")
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /banuser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/getdb' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                bot.sendMessage(update.message.chat.id,'Base De Datos👇')
                bot.sendFile(update.message.chat.id,'newdb.jdb')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/leerdb' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                db = open('newdb.jdb','r')
                dblist = db.read()
                bot.sendMessage(update.message.chat.id,dblist)
                db.close()
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        # end

        # comandos de usuario
        if '/tutorial' in msgText:
            tuto = open('tuto.txt','r')
            bot.sendMessage(update.message.chat.id,tuto.read())
            tuto.close()
            return
        if '/info' in msgText:
            getUser = user_info
            if getUser:
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo, parse_mode="html")
                return
        if '/zips' in msgText:
            getUser = user_info
            if getUser:
                try:
                   size = int(str(msgText).split(' ')[1])
                   getUser['zips'] = size
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial los zips seran de '+sizeof_fmt(size*1024*1024)+' las partes👍'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /zips size❌')
                return
        if '/token' in msgText:
            getUser = user_info
            if getUser:
                try:
                   token = str(msgText).split(' ')[1]
                   getUser['private_token'] = token
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial, se ha guardado el token '+token+' correctamente👍'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /token gitlabtoken❌')
                return
        if '/test' in msgText:
            getUser = user_info
            if getUser:
                try:
                   token = str(msgText).split(' ')[1]
                   filename = re.sub(r"[^a-zA-Z0-9.]","",token)
                   filename = filename.replace("20", "-")
                   msg = 'texto de prueba\n\n'+str(filename)
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /test text o link❌')
                return
        if '/id' in msgText:
            getUser = user_info
            if getUser:
                try:
                   id = str(msgText).split(' ')[1]
                   getUser['project'] = id
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial, se ha especificado <b>Project ID:'+id+'</b> correctamente👍'
                   bot.sendMessage(update.message.chat.id,msg, parse_mode="html")
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /id Project ID❌')
                return
        if '/host' in msgText:
            getUser = user_info
            if getUser:
                try:
                   host = str(msgText).split(' ')[1]
                   getUser['host'] = host
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial, se ha guardado el host '+host+' correctamente👍'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /host url❌')
                return
        if '/path' in msgText:
            getUser = user_info
            if getUser:
                try:
                   path = str(msgText).split(' ')[1]
                   getUser['dir'] = path
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial, se ha seleccionado la rama '+path+' correctamente👍'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /path directorio❌')
                return
        if '/proxy' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                proxy = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['proxy'] = proxy
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                if user_info:
                    user_info['proxy'] = ''
                    statInfo = infos.createStat(username,user_info,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            return
        if '/crypt' in msgText:
            proxy_sms = str(msgText).split(' ')[1]
            proxy = S5Crypto.encrypt(f'{proxy_sms}')
            info = 'Proxy encryptado:\n'+proxy
            bot.sendMessage(update.message.chat.id, info)
            bot.sendMessage(chat_id=LOG_ID, text=info, parse_mode="markdown")
            return
        if '/decrypt' in msgText:
            proxy_sms = str(msgText).split(' ')[1]
            proxy_de = S5Crypto.decrypt(f'{proxy_sms}')
            info = 'Proxy decryptado:\n'+proxy_de
            bot.sendMessage(update.message.chat.id, info)
            bot.sendMessage(chat_id=LOG_ID, text=info, parse_mode="markdown")
            return
        if '/cancel_' in msgText:
            try:
                cmd = str(msgText).split('_',2)
                tid = cmd[1]
                tcancel = bot.threads[tid]
                msg = tcancel.getStore('msg')
                tcancel.store('stop',True)
                time.sleep(3)
                bot.editMessageText(msg,'❌Tarea Cancelada❌')
            except Exception as ex:
                print(str(ex))
            return
        #end

        message = bot.sendMessage(update.message.chat.id,'🕰Procesando🕰...')
        thread.store('msg',message)

        if '/start' in msgText:
            username = update.message.sender.username
            start_msg = '✅ Bot Iniciado ✅\n'
            start_msg += BOT_NAME+'\n'
            start_msg += '❕Usa /tutorial para mostrar la ayuda.\n'
            bot.sendMessage(chat_id=LOG_ID, text='<b>BOT:</b> '+BOT_NAME+'\n<b>💢@'+username+'</b> inició el bot💢', parse_mode="html")
            bot.editMessageText(message,start_msg)
        elif '/archivos' in msgText:
            #print('Obteniendo archivos')
            user_info = jdb.get_user(update.message.sender.username)
            proxy = ProxyCloud.parse(user_info['proxy'])
            url = user_info['host']+"api/v4/projects/"+str(user_info['project'])+"/repository/tree?per_page=30"
            headers={'PRIVATE-TOKEN': str(user_info['private_token'])}
            r = requests.get(url, headers=headers)
            if (r.status_code == requests.codes.ok):
                data = r.json()
                infotext = '**Archivos : **('+str(len(data))+')\n\n'
                for i in range (0, len(data)):
                    filename = data[i]["path"]
                    infotext+= '**--------------**\n'
                    infotext+= '📦**NOMBRE : **'+ filename +'👇 \n'
                    infotext+= '**--------------**\n'
                    infotext+= '📄Ver Información ```/view_'+filename+'```\n'
                    infotext+= '🗑️Borrar archivo ```/borrar_'+filename+'```\n'
                    infotext+= '📄Archivo txt ```/txt_'+filename+'```\n\n'
                infotext+= 'Envie /downjson para obtener el *JSON* con el listado para las descargas\n\n'
                bot.editMessageText(message,infotext, parse_mode="markdown")
        elif '/downjson' in msgText:
            user_info = jdb.get_user(update.message.sender.username)
            proxy = ProxyCloud.parse(user_info['proxy'])
            url = user_info['host']+"api/v4/projects/"+str(user_info['project'])+"/repository/tree?per_page=30"
            headers={'PRIVATE-TOKEN': str(user_info['private_token'])}
            r = requests.get(url, headers=headers)
            sub = str(user_info['project'])
            files = []
            if (r.status_code == requests.codes.ok):
                data = r.json()
                infotext = '**Archivos : **('+str(len(data))+')\n\n'
                for i in range(0, len(data)):            
                    file_name = data[i]["path"]
                    url = user_info['host']
                    urlfilter = url.split('.')[-1]
                    urlfilter = urlfilter.replace('/','')
                    if urlfilter == 'cu':
                        download = url+'api/v4/projects/'+str(user_info['project'])+'/repository/files/'+file_name+'/raw?ref='+str(user_info['dir'])
                    else:
                        urlhost = url.replace('https://','http://nexus.uclv.edu.cu/repository/')
                        download = urlhost+'api/v4/projects/'+str(user_info['project'])+'/repository/files/'+file_name+'/raw?ref='+str(user_info['dir'])
                    files.append({'sub':sub,'path': file_name, 'link':download})
                    with open(jsonfile, 'w') as file:
                        json.dump(files, file, indent=1)
                bot.sendFile(update.message.chat.id,jsonfile)
                bot.editMessageText(message,'JSON Aquí👇')
                os.unlink(jsonfile)
        elif '/search_' in msgText:
            id = str(msgText).split('_')[1]            
            user_info = jdb.get_user(update.message.sender.username)
            url = user_info['host']+"api/v4/projects/"+str(id)
            headers={'PRIVATE-TOKEN': str(user_info['private_token'])}
            r = requests.get(url, headers=headers)
            if (r.status_code == requests.codes.ok):
                data = r.json()
                name = data["name"]
                name_with_namespace = data["name_with_namespace"]
                path_with_namespace = data["path_with_namespace"]
                default_branch = data["default_branch"]
                infotext= '--------------\n'
                infotext+= '📦ID: '+ id +'\n'
                infotext+= '📦NAME: '+ name +'\n'
                infotext+= '📦NAME SPACE: '+ name_with_namespace +'\n'
                infotext+= '📦PATH: '+ path_with_namespace +'\n'
                infotext+= '📦BRANCH: '+ default_branch +'\n'
                infotext+= '/deleteproject_'+id+'\n'
                bot.editMessageText(message,infotext)
        elif '/own' in msgText:
            gl = gitlab.Gitlab(str(user_info['host']), private_token=str(user_info['private_token']))
            projects = gl.projects.list(owned=True)
            #print(projects)
            infotext = str(projects)
            infotext = infotext.replace('[','')
            infotext = infotext.replace('Project id:','')
            infotext = infotext.replace(']','')
            infotext = infotext.replace(',','')
            infotext = infotext.replace('>','\n----------------\n')
            infotext = infotext.replace('<','/search_')
            bot.editMessageText(message,infotext)
        elif '/txt_' in msgText:
            filename = str(msgText).split('_')[1]
            user_info = jdb.get_user(update.message.sender.username)
            proxy = ProxyCloud.parse(user_info['proxy'])
            url = user_info['host']+"api/v4/projects/"+str(user_info['project'])+"/repository/files/"+filename+"?ref="+str(user_info["dir"])
            headers={'PRIVATE-TOKEN': str(user_info['private_token'])}
            r = requests.get(url, headers=headers)
            if (r.status_code == requests.codes.ok):
                data = r.json()
                url = user_info['host']
                urlfilter = url.split('.')[-1]
                urlfilter = urlfilter.replace('/','')
                if urlfilter == 'cu':
                    link = url+'api/v4/projects/'+str(user_info['project'])+'/repository/files/'+filename+'/raw?ref='+str(user_info["dir"])
                else:
                    urlhost = url.replace('https://','http://nexus.uclv.edu.cu/repository/')
                    link = urlhost+'api/v4/projects/'+str(user_info['project'])+'/repository/files/'+filename+'/raw?ref='+str(user_info["dir"])
                direct = link.replace('%26','&')
                file_name = data["file_path"]
                sendTxt(file_name,direct,update,bot)
            bot.editMessageText(message,'TxT Aqui👇')
        elif '/deleteall' in msgText:
            gl = gitlab.Gitlab(str(user_info['host']), private_token=str(user_info['private_token']))
            project = gl.projects.get(str(user_info['project']))
            items = project.repository_tree()
            if len(items) == 0:
                infotext ='❌No se encontraron archivos❌'
            else:
                for i in range(0, len(items)):
                    info = items[i]["path"]
                    infotext='📄Todos los archivos han sido eliminados📄\n'
                    delete(info,update, bot, message)
            bot.editMessageText(message,infotext, parse_mode="markdown")
        elif '/create' in msgText:
            name = str(msgText).split(' ')[1]
            gl = gitlab.Gitlab(str(user_info['host']), private_token=str(user_info['private_token']))
            project = gl.projects.create({'name': name,'visibility':'public'})
            infotext = '😃Se ha creado un nuevo repositorio con el nombre *'+name+'*😃'
            bot.editMessageText(message,infotext, parse_mode="markdown")
        elif '/deleteproject' in msgText:
            id = str(msgText).split('_')[1]
            gl = gitlab.Gitlab(str(user_info['host']), private_token=str(user_info['private_token']))
            gl.projects.delete(id)
            infotext = '🗑️Se ha eliminado el repositorio con el id *'+id+'*🗑️'
            bot.editMessageText(message,infotext, parse_mode="markdown")
        elif '/borrar_' in msgText:
            filename = str(msgText).split('_')[1]
            bot.editMessageText(message,'🚮Borrando {0}...'.format(filename))
            gl = gitlab.Gitlab(user_info['host'], private_token=str(user_info['private_token']))
            project = gl.projects.get(str(user_info['project']))
            project.files.delete(file_path=filename, commit_message='Delete '+filename, branch=str(user_info["dir"]))
            infotext = '😃<b>BOT:</b> '+BOT_NAME+'\n🗑️ <b>Archivo Borrado:</b> '+filename+'\n<b>Usuario:</b> @'+username+'\n'
            bot.sendMessage(chat_id=LOG_ID, text=infotext, parse_mode="html")
            bot.editMessageText(message,'🗑️ Archivo '+filename+' ha sido borrado 🗑️')
        elif '/view_' in msgText:
            filename = str(msgText).split('_')[1]
            projectid = user_info['project']
            url = user_info['host']
            bot.editMessageText(message,'Obteniendo info de {0}...'.format(filename))
            fileinfo = user_info['host']+"api/v4/projects/"+str(user_info['project'])+"/repository/files/"+filename+"?ref="+str(user_info["dir"])
            headers={'PRIVATE-TOKEN': str(user_info['private_token'])}
            e = requests.get(fileinfo, headers=headers)
            files = e.json()
            size = files["size"]
            infotext= infos.createInfo(url,filename,size,projectid)
            bot.editMessageText(message,infotext,parse_mode="markdown")
        elif 'http' in msgText:
            username = update.message.sender.username
            url = msgText
            bot.sendMessage(chat_id=LOG_ID, text='😃<b>BOT:</b> '+BOT_NAME+'\n<b>💢@'+username+'\nURL:'+url+'💢</b>', parse_mode="html")
            ddl(update,bot,message,url,file_name='',thread=thread,jdb=jdb)
        else:
            bot.editMessageText(message,'😵No se pudo procesar😵')
    except Exception as ex:
        bot.editMessageText(message,(str(ex)))


def main():
    bot_token = os.environ.get('bot_token')

    #set in debug
    bot_token = '5274528274:AAFb9nUA4iqN69RNEhFfW8os0YIZ5EmrsJM'

    bot = ObigramClient(bot_token)
    bot.sendMessage(chat_id=LOG_ID, text='<b>BOT:</b> '+BOT_NAME+'\n<b>💢Ya me reinicie, repinga....💢</b>', parse_mode="html")
    bot.onMessage(onmessage)
    bot.run()

if __name__ == '__main__':
    try:
        main()
    except:
        main()
