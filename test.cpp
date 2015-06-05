#include "SDL.h"
#include "stdio.h"

int main ( int argc, char *argv[] )
{
    SDL_Init(SDL_INIT_EVERYTHING);
    SDL_WM_SetCaption("SDL Test", "SDL Test");
    SDL_Surface* screen = SDL_SetVideoMode(640, 480, 0, 0);
    SDL_Surface* temp = SDL_LoadBMP("sdl_logo.bmp");
    SDL_Surface* bg = SDL_DisplayFormat(temp);
    SDL_FreeSurface(temp);

    SDL_Event event;
    int gameover = 0;

    while (!gameover)
    {
        /* look for an event */
        if (SDL_PollEvent(&event)) {
            /* an event was found */
            switch (event.type) {
                /* close button clicked */
                case SDL_QUIT:
                    gameover = 1;
                    break;

                /* handle the keyboard */
                case SDL_KEYDOWN:
                    switch (event.key.keysym.sym) {
                        case SDLK_ESCAPE:
                        case SDLK_q:
                            gameover = 1;
                            break;
                            default:
                            printf( "Switch default.\n" );
                            break;
                    }
                    break;
            }
        }

        SDL_BlitSurface(bg, NULL, screen, NULL);
        SDL_UpdateRect(screen, 0, 0, 0, 0);
    }

    SDL_FreeSurface(bg);
    SDL_Quit();

    return 0;
}

