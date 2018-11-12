#!/usr/bin/env python3

import cgi
import sys
import pix3_gallery as pix

if __name__ == '__main__':
    print('Content-type:text/html\n')  # newline separates CGI header from HTML
    try:
        fs = cgi.FieldStorage()
        if len(sys.argv) == 3:
            admin_action = sys.argv[1]
            album = sys.argv[2]
            pic = ''
         else:
            album = getArg(fs, 'album')
            pic = getArg(fs, 'pic')
            control = getArg(fs, 'control')
            admin_action = getArg(fs, 'admin')

        p = pix.Pix()
        print('<html><head><title>{title:s}</title></head><body>{body:s}</body></html>'.format(title=p.get_site_title(), body=p.get_body())
    except Exception as data:
        print('<pre><h1>')
        print('Fatal server error' 
        print('</h1>')
        print(str(data))
        print('</pre>')
