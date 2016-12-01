#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Enable occurence of utf-8 in source code, done in the two lines aboves

# Module to do http requests
import requests

# Module to parse html
from BeautifulSoup import BeautifulSoup

# Module to print errors/exceptions properly
import traceback, sys, subprocess, os

# Module for timeing
import time

# Imports customized tool to (store/read) serialized python objects from mypkl.py
import mypkl as pkl

# Imports bot functions from bot.py
import bot

# Imports configs from conf.py
import conf

# inserts a char(char) into string(s) at position(pos)
def insert_char(s,char,pos):
    ns = s[:pos]+char+s[pos:]
    # important comment !!!!
    # @jf - ns is a very useful variable name, it obviously stands for new_string
    return ns
    
def wait_before_next_request():
    sleep_minutes = conf.minutes_between_requests
    sleep_seconds = 60*sleep_minutes
    time.sleep(sleep_seconds)
    
    # fix - to avoid too many request to server
    time.sleep(0.3)

def visit_site():
 
    # If plan_changes.pkl file exists load content to plan_changes_prev
    try:
        plan_changes_prev = pkl.read("plan_changes.pkl")  
    except IOError as e:
        if e.errno == 2:
            plan_changes_prev = None  
        else:
            raise e
    
    # read url of course table from file 
    lines = open("link.txt","r").readlines()
    # clean url
    lines = [x.strip() for x in lines]
    link = "".join(lines)
    link = link.replace("__var_link_type_id__",conf.link_type_id)
    print link[:50]
    
    if 1:
        # get content from link
        r = requests.request(method='GET', url=link)
        content = r.content
        
        #{"vorlesungen":"
        content = content.replace('{"vorlesungen":"',"").replace('"}','"')
        #content = content.replace('\\"','"')
        content = content.decode('string_escape')
        content = content.replace("\\/","/")
        
        # print first 50 chars of content, useful for debugging
        print content[:50]
        
        # for debugging purposes write content to temp.html
        open( "temp.html","w").write(content)
    else:
        # for debugging purposes read data from temp.html, reduces requests to website
        content = open( "temp.html","r").read()
        
    if 1:
        #######################################
        # Parse content from response, store events, professors in  "output" variable
        #######################################
        
        # create BeautifulSoup tree for parsing
        tree = BeautifulSoup(content)
        #attrs={'class': "twelve columns nop"}): #"b", { "class" : "lime" }

        # load cnt from file
        try:
            cnt_pkl = open("cnt.pkl","r").read()
            cnt_pkl = int(cnt_pkl)
            cnt_pkl += 1
        except IOError as e:
            if e.errno == 2:
                cnt_pkl = 1
            else:
                raise e
        # safe cnt incremented
        open("cnt.pkl","w").write(str(cnt_pkl))
        
        # contains changes to the Stundenplan
        plan_changes = []
        
        for node in tree.findAll("div", { "class" : "twelve columns nop" }):
            # for debugging
            if 0:
                # print node.contents
                print "---"
                print cnt_pkl
                print "---"
                print str(node)[:50]
            
            rows = node.find('table').findAll('tr')

            # iterate over table cells, store them in output
            for row in rows:
                cells = row.findAll('td')

                output = []

                for i, cell in enumerate(cells):
                    if i == 0:
                        output.append(cell.text.strip())
                    if i > 0:
                        output.append(cell.text.strip())
                        #print "--",cell.text.strip()
                    """
                    elif cell.find('img'):
                        output.append(cell.find('img')['title'])
                    elif cell.find('input'):
                        output.append(cell.find('input')['value'])
                    """
                #print output
                plan_changes.append(output)
                    
            #tname = "table_previous.pkl"
            #pkl.write( (plan_changes,cnt_pkl),tname)
            #plan_changes_prev,cnt_pkl_prev = pkl.read(tname)
        
        if len(plan_changes) > 0: #bug ??, not recognize entfall ?
            pkl.write(plan_changes,"plan_changes.pkl")   
        
        #open("file_plan.html","w").write(str(plan_changes))
        #open("file_plan_prev.html","w").write(str(plan_changes_prev))
        
    # init this code block with intention to always send new updates,
    # then later on check if there really is a change
    # <-- that's reason for website_changed = 1
    website_changed = 1
    if plan_changes == plan_changes_prev:
        website_changed = 0
    else:        
        # If there are no plan_changes, dont resize hash ?
        # if len(plan_changes) #bug ??, not recognize entfall ?
        if len(plan_changes) > 0:
            website_changed = 1
        else:
            website_changed = 0
            
    print "website_changed", website_changed
    
    # Formatting and Builder of bot message
    
    line_pad = 20
    line_pad_short = 14
    line_pad_short_half = (line_pad_short)/2

    msg = u""
    msg += "#stundenplan"
    msg += "\n"
    msg += "="*line_pad
    ch = "\n"
    
    for change in plan_changes:
        if 0:
            print ".........."
            print change
            print len(change)
            print ".........."
            
        if len(change)>0:
            for n,e in enumerate(change):
                # text from table cell for title
                if n == 1:
                    try:
                        e = e[:e.index("(")]
                    except ValueError:
                        print " ( substring not found - ValueError" 
                        # e is not changed
                    # replace titles that are too long, with a substitution
                    #   [ "title_to_be_replace", "substitution_of_title" ]
                    names = [ 
                              ["Formale Sprachen","FS"], 
                              ["Praktikum Software Entwicklung","PSE"], 
                              ["Sport und Gesundheit","Sport"],
                              ["Oracle 11g Release 2 - Administration Workshop","Oracle"],
                              ["Webtechnologie und Webmarketing in der Cloud","Cloudmarketing"],
                            ]
                    for name in names:
                        e = e.replace(name[0],name[1])
                        
                    msg += "\n"
                    msg += e
                    msg += "    "
                    
                # text from table cell for professor
                if n == 2:
                    e = e.replace("Prof.","").replace("Dr.","")
                    e = e.strip()
                    msg += ""
                    msg += e
                    msg += "\n"
                    msg += "-"*line_pad_short_half
                    msg += "------------------"
                    msg += "-"*line_pad_short_half
                    
                # text from table cell for entfällt
                if n == 3:
                    msg += "\n"
                    s = list(e)
                    e = "".join(s)
                    e = insert_char(e," ",10)
                    e = insert_char(e," ",10)
                    e = insert_char(e," ",10)
                    e = insert_char(e," ",22)
                    e = insert_char(e,"-",22)
                    e = insert_char(e,ch,22)
                    msg += e
                    msg += "\n"
                    msg += "-"*line_pad_short_half
                    msg += " Vertretung "
                    msg += "-"*line_pad_short_half
                    
                # text from table cell for vertreten
                if n == 4:
                    #print e
                    if len(e.strip())>0:
                        msg += "\n"
                        s = list(e)
                        e = "".join(s)
                        e = insert_char(e," ",10)
                        e = insert_char(e," ",10)
                        e = insert_char(e," ",10)
                        e = insert_char(e," ",22)
                        e = insert_char(e,"-",22)
                        e = insert_char(e,ch,22)
                        msg += e

            msg += "\n"
            msg += "="*line_pad
                     
    if website_changed:
        endpoints = conf.endpoints
        bot.send_msg(msg, endpoints = endpoints)
        
def main():
    while 1:
        try:
            visit_site()
            
        except Exception as e:
        
            # if there is an exception/error happending, send message to admin
            
            try:
                exc_info_123 = sys.exc_info() # just a reference/func pointer, not a string
            except Exception as e_:
                print "exc_info show failed with", str(e_)
            finally:
                # Display the *original* exception
                print "--tb--"
                traceback_msg = traceback.print_exception(*exc_info_123)
                print traceback_msg
                print traceback_msg
                #traceback_msg = "msg"+str(e)
                #return_code = subprocess.call("tail nohup.out", shell=True)  
                return_code = os.popen("tail nohup.out").readlines()
                return_code_clean = []
                for line in return_code:
                    if "urllib3.connectionpool" in line:
                        pass
                    else:
                        return_code_clean.append(line)
                
                time.sleep(0.3) #bug
                traceback_msg = "".join(return_code_clean[-6:])
                
                del exc_info_123
                
            msg = " open.py - error:  "
            msg += "\n"
            msg += str(traceback_msg)
            print "-"*30
            print msg
            print "-"*30
            bot.send_msg(msg, flag_notify_admin_only = 1)
                    
        print "=="*30
        
        wait_before_next_request()
        
main()











