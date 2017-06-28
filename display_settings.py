#CONFIGURATION FILE
#DISPLAY SETTINGS
#change values bellow to change game configuration (please avoid doing this at runtime)



#___BASIC OPTIONS___

FULLSCREEN = True #enable Fullscreen mode or not

RESIZABLE = True #enable the Window to be resizable or not

RESOLUTION_AUTO = True #let the application find the best resolution (current resolution of the monitor)

ALLOW_TILE_FOLLOW_CURSOR = True #ONLY WORKS IN FULLSCREEN (crash if cursor out of the game window)



#___CUSTOM RESOLUTIONS___

#IF RESOLUTION_AUTO SET TO FALSE :
HEIGH = 720 #heigh resolution of the window #COMMON VALUES 1080 or 720

WIDTH = round (HEIGH * (16/9.0) ) #width resolution of the window



#___ADVANCED OPTIONS___

DOUBLEBUF = True #enable double buffer (recommended for HWSURFACE or OPENGL)

HWSURFACE = True #hardware accelerated (only in FULLSCREEN)

#NOTE : DO NOT SUPPORT "OPENGL and NOFRAME arguments from Pygame API
