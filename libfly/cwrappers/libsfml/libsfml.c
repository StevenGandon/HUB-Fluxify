#include <SFML/Graphics.h>

sfRenderWindow *init_window(int width, int height, char *title)
{
    sfVideoMode mode = {width, height, 32};
    sfRenderWindow *window = sfRenderWindow_create(mode, title, sfDefaultStyle, NULL);

    return window;
}

void destroy_window(sfRenderWindow *window)
{
    sfRenderWindow_destroy(window);
}

void clear_window(sfRenderWindow *window)
{
    sfColor color = {0, 0, 0, 255};

    sfRenderWindow_clear(window, color);
}

void display_window(sfRenderWindow *window)
{
    sfRenderWindow_display(window);
}
