__author__ = 'DusX'
from time import sleep
import random
import requests
import json
import glsl_parser # as found here: https://github.com/rougier/glsl-parser , as of May 10th 2015
import os,sys # OS and FileSystem

#  from bs4 import BeautifulSoup
# print 'sys.argv[0] =', sys.argv[0]
pathname = os.path.dirname(sys.argv[0])
# print 'path =', pathname
fullpath = os.path.abspath(pathname)
# print 'full path =', fullpath

# GLOBALS
# ==============
glslsandbox_url = "http://glslsandbox.com/item/"  # ID details: ...box.com/item/23833.0 , '.0' at end is not required
# live link : http://glslsandbox.com/e#23833
# code only : http://glslsandbox.com/item/23833
# code loading script: http://glslsandbox.com/js/helpers.js , find "$.getJSON('/item/'+hash, function(result)"

shadertoy_url = "none"
#  https://www.shadertoy.com/js/pgEmbed.js   function loadShader()   gShaderID     , this is load section.. seems to
# require a post request.

# Define system path to save downloaded files to.
savepath = fullpath + "\shaders\\"

def glsl_crawl(start_url, max_num=1) :
    """Program entry and routing logic

    route request based on URL, send along params

    Args:
    start_url -- string
    max_num -- int (1)
    Returns:
    0 = complete
    """
    pass


def glslsandbox(start_url, max_num) :
    """grab the data, url by url.

    process thru a range of URLS (constructed)
    for each: process the text in the data, down to valid GLSL
    save the data to a location as 'sandbox_license_type_pageID_parent.glsl' , this format sort alphabetically

    Args:
    start_url -- string
    max_num -- int (1)
    Returns:
    0 = complete
    """
    # total = 60
    total = max_num
    breaknum = max_num - total  # allow to test with smaller batches
    current = max_num
    while current > breaknum :
        id = str(current).zfill(5)
        url = start_url + id
        if current != max_num :
            ptime = random.randrange(25, 300) / 100.0
            print "sleep: " + str(ptime)
            sleep(ptime)
        print "\n" + url


        try:
            webdata = requests.get(url).text  # should be valid JSON
        except:
            print "error with get GET"
            webdata = '{code: "// item not found", user: false, parent: "BAD"}'


        try:
            webdata = json.loads(webdata)
        except:
            print "error with get JSON"
            webdata = '{code: "// item not found", user: false, parent: "BAD2"}'
            webdata = json.loads(webdata)

        # addtional Hacks to fix 'errors' from glsl_parser , these error types still contain running GLSL code,
        # so I am continuing.

        try:
            source_user = str(webdata['user'])
        except:
            source_user = False

        try:
            source_parent = webdata['parent']
        except:
            source_parent = False

        try:
            try:
                source_code = str(webdata['code'])
            except:
                source_code = webdata['code'].encode("utf-8")
                source_parent = str(source_parent) + "_utf-8_"
        except:
            # break
            source_code = "---"  # try to fail parsing.

        print source_user + " " + str(source_parent)
        try :
            glslcode, _ = glsl_parser.resolve(source_code)
        except ZeroDivisionError, e:
            print "==================="
            print e.args
            print "NameError - " + url
            print "==================="
            source_parent = str(source_parent) + "_0divE_"
        except NameError, e:
            print "==================="
            print e.args
            print "NameError - " + url
            print "==================="
            source_parent = str(source_parent) + "_NE_"
        except SyntaxError, e:
            print "==================="
            print e.args
            print "SyntaxError - " + url
            print "==================="
            source_parent = str(source_parent) + "_SE_"
        finally:
            # process the txt and save to file
            save_code(source_code, id, source_parent, url)

        current -= 1  # de-increment


def save_code(code, id, parentID, url) :
    # call functions to return license info and format 'code'
    # sandbox_license_type_pageID_parent.glsl
    filename = "sandbox_"
    lcode = code.lower()

    # add code to auto insert Isadora GLSL variable headers into Commercial use friendly scripts

    if "license" in lcode:
        filename += "Licensed_"
    if "Creative Commons".lower() in lcode or "CreativeCommons".lower() in lcode \
            or "Creative_Commons".lower() in lcode or "Creative-Commons".lower() in lcode:
        filename += "CC_"
    if " MIT ".lower() in lcode:
        filename += "MIT_"
    if "NonCommercial".lower() in lcode or "Non Commercial".lower() in lcode \
            or "Non_Commercial".lower() in lcode or "Non-Commercial".lower() in lcode:
        filename += "NONcommercial_"

    filename = filename + str(id) + "_"

    if parentID:
        # need to remove leading /
        parentID = parentID[1:]
        filename = filename + parentID + "_"

    print code
    filepath = savepath + filename + ".glsl"
    print filepath

    url = "//  " + url
    output_code = str(url) + "\n\n" + str(code) # be sure its not the lowercase version for tests

    try :
        with open(filepath, "w") as text_file:
            text_file.write(output_code)
    except:
        print "==================="
        e = sys.exc_info()[0]
        print "Error: %s" % e
        print "==================="


if __name__ == '__main__' :
    """ sudo code
    implement glsl_crawl, to route logic for differenet source sites.
    """

    # quick hack to run code as is for glslSandbox , note 2nd param is the max number of ID, it counts down.
    # just change the MAX ID, and run script as is.
    print "--start"
    glslsandbox(glslsandbox_url, 16630)
    print "\n--end"
