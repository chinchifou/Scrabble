#CONFIGURATION FILE
#change values bellow to change game configuration (avoid doing this at runtime)

#BASIC OPTIONS
FULLSCREEN = True #enable Fullscreen mode or not

HEIGH = 1080 #heigh resolution of the window #COMMON VALUES 1080 or 720
WIDTH = round (HEIGH * (16/9) ) #width resolution of the window

#ADVANCED OPTIONS
RESIZABLE = True #enable the Window to be resizable or not

DOUBLEBUF = True #enable double buffer (recommended for HWSURFACE or OPENGL)
HWSURFACE = True #hardware accelerated (only in FULLSCREEN)


#NOTE : DO NOT SUPPORT "OPENGL and NOFRAME argument sfrom Pygame API

# /// DO NOT REMOVE ///
#force coherence of local configuration
RESIZABLE = False if FULLSCREEN == True else RESIZABLE
HWSURFACE = False if FULLSCREEN == False else HWSURFACE
