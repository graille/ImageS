# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:23:15 2015

@author: Thibault
"""

# Imports
import os
import sys

# Import HTMLParser
from HTMLParser import HTMLParser

class ISHTMLParser(HTMLParser):
    def __init__(self, website_path):
        self.reset()
        self.url_container = []
        self.img_container = []
        
        # Parsage de la page du site web
        url_temp = ""
        if website_path[0:7] == "http://": # Verification de l'entète pour savoir ou commencer la vérification
            depart = 7
        elif website_path[0:7] == "ftp://":
            depart = 6
        elif website_path[0:8] == "https://":
            depart = 8
        else:
            depart = 0
        
        for i in range(depart, len(website_path) - 1):
            if website_path[i] == "/":
                break
            else:
                url_temp = url_temp + website_path[i]

        self.website_path = website_path[0: depart] + url_temp
    
    def feed_website(self):
        self.feed(self.website_page)
    
    def URLParser(self, url):
        # Gestion de l'url
        if url[0] == "/": # Si c'est un lien relatif
            if "www" not in url[0:15] and "http" not in url[0:15]:
                url = self.website_path + url
            else:
                url = url[1:]
                return self.URLParser(url)
        elif "http" not in url and "www" not in url \
        and ".com" not in url and ".fr" not in url and ".net" not in url \
        and ".eu" not in url: # Si c'est un lien relatif direct
            url = self.website_path + "/" + url 
        elif url[0:4] == "www.": # Si c'est un lien sans http
            url = "http://" + url
        
        return url
        
    def handle_starttag(self, tag, attrs):
        if tag == "img": # Gestion des images
            for attr in attrs:
                if attr[0] == "src":
                    url = attr[1]
                    if len(url) > 0 and url[0] != "#":
                        self.img_container.append(self.URLParser(url))
        
        if tag == "a": # Gestion des liens
            for attr in attrs:
                if attr[0] == "href":
                    url = attr[1]
                    
                    if len(url) > 0 and url[0] != "#":
                        # Enregistrement de l'URL
                        if url[-4:].lower() in [".jpg", ".png", ".gif", ".bmp", ".svg", ".jpeg"]: # Si c'est un lien vers une image
                            self.img_container.append(self.URLParser(url))
                        elif url[-4:].lower() in [".css"] or url[-3:].lower() in [".js"]: # If is a CSS or a Javascript element
                            pass
                        else:
                            self.url_container.append(self.URLParser(url))
