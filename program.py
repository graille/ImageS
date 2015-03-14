# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:26:14 2015

@author: Thibault
"""
import os
import sys
import hashlib
reload(sys)  
sys.setdefaultencoding('utf8')
current_dir = os.getcwd()
sys.path.append(current_dir + "\\lib")
sys.path.append(current_dir + "\\src")

# Import files
import urllib2 as urllib
from ISHtmlParser import ISHTMLParser
from PIL import Image

class Url():
    def __init__(self, url = '', deep = 1):
        self.url = url
        self.deep = deep
    
class File():
    def __init__(self):
        self.file = []
        self.nb_elements = 0
        
    def take(self):
        if self.length() > 0:
            self.nb_elements -= 1
            return self.file.pop(0)
        
    def add(self, p):
        self.file.append(p)
        self.nb_elements += 1
    
    def length(self):
        return self.nb_elements
        
class Program():
    def __init__(self, register_path = "", max_pages = 15):
        self.url_visited = []
        self.url_waiting = File()
        
        self.register_path = register_path
        
        self.img_visited = []
        self.img_waiting = File()
        
        self.max_pages = max_pages
		
		# Counters
        self.nb_pages = 0
        self.nb_images = 0
    
    def explore_img(self):
        print("")
        print("Telechargement des images")
        while self.img_waiting.length() > 0:
            try:
                url = self.img_waiting.take()
                
                # Récupération de l'image
                extension = url[-4:] if url[-4] == "." else url[-5:]
                if extension[0] == "." and extension not in [".exe", ".com", ".html", ".htm", ".css", ".less", ".net"]:
                    path_img = self.register_path + str(self.nb_images) + extension

                    f = open(path_img, 'wb')
                    f.write(urllib.urlopen(url).read())
                    f.close()
                    
                    print("Download : " + url)  
                    # Ajout de l'image dans la bibliothèque
                    self.img_visited.append(self.md5(url))

                    # Vérification de l'image                
                    if(self.verif_img(path_img)):
                        self.nb_images += 1
                    else:
                        print("No download : " + url)
                        os.remove(path_img) # On supprime l'image
                    
            except urllib.HTTPError:
                pass
            except urllib.URLError:
                pass
            except ValueError:
                pass
    
    def verif_img(self, path_img):
        try:
            im = Image.open(path_img)
            (l, h) = im.size
            if l > 1200: # Image en HD
                return True
            else:
                return False
        except Exception:
            return False
    
    def main(self, main_url):
        if main_url != None:
            self.url_waiting.add(main_url)
            
            while self.nb_pages < self.max_pages \
                and self.url_waiting.length() > 0:
                
                url = self.url_waiting.take()
                
                print("Exploration de : " + url)
                result = self.visite(url)
                
                # Exploration des images référencés
                self.explore_img()
                
                # Si on a explorer l'url sans encombre, on peu passer a la suivante
                self.nb_pages += 1 if result else 0
                
            print("Done !")
        else:
            print("No arguments specified")
    
    def visite(self, website):
        try:
            # Parsage de la page
            parser = ISHTMLParser(website)
            source = urllib.urlopen(website).read()
            parser.feed(source)
            
            # Ajout du lien dans la bibliothèque
            self.url_visited.append(self.md5(website))
            
            # Recupération des URL
            for url in parser.url_container:
                if self.nb_pages < self.max_pages:
                    if self.md5(url) not in self.url_visited \
                    and url not in self.url_waiting.file:
                        self.url_waiting.add(url)
            
            # Récupération des images
            for img in parser.img_container:
                if self.md5(img) not in self.img_visited \
                and img not in self.img_waiting.file:
                    self.img_waiting.add(img)
            
            return True
        except urllib.HTTPError:
            return False
        except urllib.URLError:
            return False
        except ValueError:
            return False
            
    def md5(self, text):
        return hashlib.md5(text).hexdigest()
    
# Récupération des arguments consoles            
argv = sys.argv
register_path = argv[2] if len(argv) >= 3 else "images/"
main_url = argv[1] if len(argv) >= 2 else None
nb_pages = argv[3] if len(argv) >= 3 else 15

# Récupération de images
main = Program(register_path, nb_pages)
main.main(main_url)