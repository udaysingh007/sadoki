from guizero import App, Picture
import logging
from constants import const as cn

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

app = App(title=cn.GUI_TITLE)
	
def launchDisplay():
	logging.debug("Launching display window")
	picture = Picture(app, image=cn.LOGO_IMAGE)
	app.display()

def cleanup():
	logging.debug("Closing windows")
	app.destroy()
	
