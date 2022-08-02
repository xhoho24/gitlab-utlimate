from cgitb import html
from pyobigram.utils import sizeof_fmt
import datetime
import time
import os

def text_progres(index,max):
	try:
		if max<1:
			max += 1
		porcent = index / max
		porcent *= 100
		porcent = round(porcent)
		make_text = ''
		index_make = 1
		make_text += '\n['
		while(index_make<21):
			if porcent >= index_make * 5: make_text+='●'
			else: make_text+='○'
			index_make+=1
		make_text += ']\n'
		return make_text
	except Exception as ex:
			return ''

def porcent(index,max):
    porcent = index / max
    porcent *= 100
    porcent = round(porcent)
    return porcent

def createDownloading(filename,totalBits,currentBits,speed,time,tid=''):
    msg = '📥Descargando... \n\n'
    msg+= '🔖Nombre: ' + str(filename)+'\n'
    msg+= '🗂Tamaño Total: ' + str(sizeof_fmt(totalBits))+'\n'
    msg+= '🗂Descargado: ' + str(sizeof_fmt(currentBits))+'\n'
    msg+= '📶Velocidad: ' + str(sizeof_fmt(speed))+'/s\n'
    msg+= '🕐Tiempo: ' + str(datetime.timedelta(seconds=int(time))) +'\n'
    msg = '📡 Descargando Archivo....\n'
    msg += '➤ Archivo: '+filename+'\n'
    msg += text_progres(currentBits,totalBits)+'\n'
    msg += '➤ Porcentaje: '+str(porcent(currentBits,totalBits))+'%\n'
    msg += '➤ Total: '+sizeof_fmt(totalBits)+'\n'
    msg += '➤ Descargado: '+sizeof_fmt(currentBits)+'\n'
    msg += '➤ Velocidad: '+sizeof_fmt(speed)+'/s\n'
    msg += '➤ Tiempo de Descarga: '+str(datetime.timedelta(seconds=int(time)))+'s\n'
    if tid!='':
        msg+= '/cancel_' + tid
    return msg
def createUploading(filename,totalBits,currentBits,speed,time,originalname=''):
    msg = '⏫Subiendo A La Nube☁... \n'
    msg+= '🔖Nombre: ' + str(filename)+'\n'
    if originalname!='':
        msg = str(msg).replace(filename,originalname)
        msg+= '⏫Subiendo: ' + str(filename)+'\n'
    msg+= '🗂Tamaño Total: ' + str(sizeof_fmt(totalBits))+'\n'
    msg+= '🗂Subido: ' + str(sizeof_fmt(currentBits))+'\n'
    msg+= '📶Velocidad: ' + str(sizeof_fmt(speed))+'/s\n'
    msg+= '🕐Tiempo: ' + str(datetime.timedelta(seconds=int(time))) +'\n'

    msg = '⏫ Subiendo A La Nube☁...\n'
    msg += '➤ Nombre: '+filename+'\n'
    if originalname!='':
        msg = str(msg).replace(filename,originalname)
        msg+= '➤ Nombre: ' + str(filename)+'\n'
    msg += text_progres(currentBits,totalBits)+'\n'
    msg += '➤ Porcentaje: '+str(porcent(currentBits,totalBits))+'%\n'
    msg += '➤ Total: '+sizeof_fmt(totalBits)+'\n'
    msg += '➤ Descargado: '+sizeof_fmt(currentBits)+'\n'
    msg += '➤ Velocidad: '+sizeof_fmt(speed)+'/s\n'
    msg += '➤ Tiempo de Descarga: '+str(datetime.timedelta(seconds=int(time)))+'s\n\n'

    return msg
def createCompresing(filename,filesize,splitsize):
    msg = '📚Comprimiendo... \n\n'
    msg+= '🔖Nombre: ' + str(filename)+'\n'
    msg+= '🗂Tamaño Total: ' + str(sizeof_fmt(filesize))+'\n'
    msg+= '📂Tamaño Partes: ' + str(sizeof_fmt(splitsize))+'\n'
    msg+= '💾Cantidad Partes: ' + str(round(int(filesize/splitsize)+1,1))+'\n\n'
    return msg
def createFinishUploading(filename,filesize,split_size,current,count,findex):
    msg = '📌Proceso Finalizado📌\n\n'
    msg+= '🔖Nombre: ' + str(filename)+'\n'
    msg+= '🗂Tamaño Total: ' + str(sizeof_fmt(filesize))+'\n'
    msg+= '📂Tamaño Partes: ' + str(sizeof_fmt(split_size))+'\n'
    msg+= '📤Partes Subidas: ' + str(current) + '/' + str(count) +'\n\n'
    msg+= '**-----------------**\n'
    msg+= '🗑Borrar Archivo: \n'
    msg+= '/borrar_'+str(findex)
    return msg

def createFinish(filename):
    msg = '📌Proceso Finalizado📌\n'
    msg+= '🔖Nombre:' + str(filename)+'\n'
    msg+= '**-----------------**\n'
    msg+= '📄Ver Información\n```/view_'+filename+'```\n'
    msg+= '🗑️Borrar archivo\n```/borrar_'+filename+'```\n'
    msg+= '📄Archivo txt\n```/txt_'+filename+'```\n\n'
    return msg

def createB64(filename,link):
    msg = '📌Proceso Finalizado📌\n'
    msg+= '🔖Nombre:' + str(filename)+'\n'
    msg+= '🔖Enlace:' + str(link)+'\n'
    file = link.replace('http://api.aewhitedevs.ml/bot/','')
    msg+= '🗑Borrar Archivo: \n```/delete_'+str(file)+'```'
    return msg

def createInfo(url,filename,size,projectid):
    msg = '📌Información del archivo📌\n'
    msg+= '🔖Nombre: ' + str(filename)+'\n'
    msg+= '🗂Tamaño: ' + str(sizeof_fmt(size))+'\n'
    urlfilter = url.split('.')[-1]
    urlfilter = urlfilter.replace('/','')
    if urlfilter == 'cu':
        msg+= '🗂LINK: '+url+'api/v4/projects/'+str(projectid)+'/repository/files/'+filename+'/raw?ref=main'
    else:
        msg+= '🗂LINK: http://nexus.uclv.edu.cu/repository/gitlab.com/api/v4/projects/'+str(projectid)+'/repository/files/'+filename+'/raw?ref=main'
    msg+= '\n📑Archivo txt : \n```/txt_'+str(filename)+'```\n'
    msg+= '\n🗑Borrar Archivo: \n```/borrar_'+str(filename)+'```'
    return msg

def createLink(filename,size,id, projectid):
    msg = '📌Información del archivo📌\n'
    msg+= '🔖Nombre: ' + str(filename)+'\n'
    msg+= '🗂Tamaño: ' + str(sizeof_fmt(size))+'\n'
    msg+= '🗂LINK: http://nexus.uclv.edu.cu/repository/gitlab.com/api/v4/projects/'+str(projectid)+'/repository/archive?sha='+str(id)+'\n'
    msg+= '\n🗑Borrar Archivo: \n```/borrar_'+str(filename)+'```'
    return msg

def logFinish(filename,username):
    msg = '📌Proceso Finalizado📌\n'
    msg+= '🔖Nombre: @'+str(username)+'\n'
    msg+= '🔖Archivo: '+str(filename)+'\n'
    return msg

def createFileMsg(filename,files):
    import urllib
    if len(files)>0:
        msg= '<b>🖇Enlaces🖇</b>\n'
        for f in files:
            url = urllib.parse.unquote(f['directurl'],encoding='utf-8', errors='replace')
            #msg+= '<a href="'+f['url']+'">🔗' + f['name'] + '🔗</a>'
            msg+= "<a href='"+url+"'>🔗"+f['name']+'🔗</a>\n'
        return msg
    return ''

def createStat(username,userdata,isadmin):
    from pyobigram.utils import sizeof_fmt
    max_file_size = 1024 * 1024 * userdata['zips']
    msg = '⚙️Configuración de Usuario⚙️\n\n'
    msg+= '🔖<b>Nombre:</b> @' + str(username)+'\n'
    msg+= '📑<b>Project:</b> ' + str(userdata['project'])+'\n'
    msg+= '🗳<b>Token:</b> ' + str(userdata['private_token'])+'\n'
    msg+= '📡<b>Host:</b> ' + str(userdata['host'])+'\n'
    msg+= '📂<b>Rama :</b> ' + str(userdata['dir'])+'\n'
    msg+= '📚<b>Zips :</b> ' + str(sizeof_fmt(max_file_size))+'\n'
    msgAdmin = '❌'
    if isadmin:
        msgAdmin = '✅'
    msg+= '🦾<b>Admin :</b> ' + msgAdmin + '\n'
    proxy = '❌'
    if userdata['proxy'] !='':
       proxy = '✅'
    tokenize = '❌'
    if userdata['tokenize']!=0:
       tokenize = '✅'
    msg+= '🔌<b>Proxy :</b> ' + proxy + '\n'
    msg+= '🔮Tokenize : ' + tokenize + '\n\n'
    #msg+= '⚙️Configurar Moodle⚙️\n🤜Ejemplo /account user,password👀'
    return msg