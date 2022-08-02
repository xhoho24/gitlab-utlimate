def generate(url,token):
    url = str(url).replace('pluginfile.php','webservice/pluginfile.php')
    return url+'&token='+token