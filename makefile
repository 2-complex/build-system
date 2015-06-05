
SDL_INCLUDE_PATH = /usr/local/Cellar/sdl/1.2.15/include/SDL
SDL_LIB_PATH = /usr/local/Cellar/sdl/1.2.15/lib

SDL_LIBS = \
	$(SDL_LIB_PATH)/libSDL.a \
	$(SDL_LIB_PATH)/libSDLmain.a \
	-framework Cocoa \
	-framework OpenGL \
	-framework AudioUnit \
	-framework IOKit \
	-framework Carbon

run: test
	./test

test: test.cpp
	c++ test.cpp -I$(SDL_INCLUDE_PATH) $(SDL_LIBS) -o test

