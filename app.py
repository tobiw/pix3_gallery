from pix3_gallery.pix import Pix


p = Pix()


def application(env, start_response):
    ret_code, content = p.get_output(env['REQUEST_URI'])
    start_response(ret_code, [('Content-Type', 'text/html')])
    return [content.encode('utf-8')]
