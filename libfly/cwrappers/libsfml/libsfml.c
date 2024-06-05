#include <SFML/Graphics.h>

sfRenderWindow *init_window(int width, int height, char *title)
{
    sfVideoMode mode = {width, height, 32};
    sfRenderWindow *window = sfRenderWindow_create(mode, title, sfDefaultStyle, NULL);

    return window;
}
