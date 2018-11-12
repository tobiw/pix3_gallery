from pix3_gallery.pix import Pix


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [Pix().get_output().encode('utf-8')]
