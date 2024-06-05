#include <SFML/Graphics.h>

/**
 * ------------------------------------------------------------------------------
 * Window
 * ------------------------------------------------------------------------------
*/

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

int get_window_width(sfRenderWindow *window)
{
    return sfRenderWindow_getSize(window).x;
}

int get_window_height(sfRenderWindow *window)
{
    return sfRenderWindow_getSize(window).y;
}

void set_window_framerate(sfRenderWindow *window, int framerate)
{
    sfRenderWindow_setFramerateLimit(window, framerate);
}

/**
 * ------------------------------------------------------------------------------
 * Event
 * ------------------------------------------------------------------------------
*/

int quit_event(sfRenderWindow *window)
{
    sfEvent event;

    while (sfRenderWindow_pollEvent(window, &event))
    {
        if (event.type == sfEvtClosed) {
            sfRenderWindow_close(window);
            return (1);
        }
    }

    return (0);
}
/**
 * ------------------------------------------------------------------------------
 * Rectangle
 * ------------------------------------------------------------------------------
*/
void draw_rectangle(sfRenderWindow *window, sfRectangleShape *rectangle)
{
    sfRenderWindow_drawRectangleShape(window, rectangle, NULL);
}

sfRectangleShape *create_rectangle(int x, int y, int size_x, int size_y, int r, int g, int b, int a)
{
    sfRectangleShape *rectangle = sfRectangleShape_create();

    sfRectangleShape_setPosition(rectangle, (sfVector2f){x, y});
    sfRectangleShape_setSize(rectangle, (sfVector2f){size_x, size_y});
    sfRectangleShape_setFillColor(rectangle, (sfColor){r, g, b, a});

    return rectangle;
}

void destroy_rectangle(sfRectangleShape *rectangle)
{
    sfRectangleShape_destroy(rectangle);
}

void move_rectangle(sfRectangleShape *rectangle, int x, int y)
{
    sfRectangleShape_setPosition(rectangle, (sfVector2f){x, y});
}

/**
 * ------------------------------------------------------------------------------
 * Circle
 * ------------------------------------------------------------------------------
*/

void draw_circle(sfRenderWindow *window, sfCircleShape *circle)
{
    sfRenderWindow_drawCircleShape(window, circle, NULL);
}

sfCircleShape *create_circle(int x, int y, int radius, int r, int g, int b, int a)
{
    sfCircleShape *circle = sfCircleShape_create();

    sfCircleShape_setPosition(circle, (sfVector2f){x, y});
    sfCircleShape_setRadius(circle, radius);
    sfCircleShape_setFillColor(circle, (sfColor){r, g, b, a});

    return circle;
}

void destroy_circle(sfCircleShape *circle)
{
    sfCircleShape_destroy(circle);
}

void move_circle(sfCircleShape *circle, int x, int y)
{
    sfCircleShape_setPosition(circle, (sfVector2f){x, y});
}