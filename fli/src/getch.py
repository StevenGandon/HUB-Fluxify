from sys import platform

if (platform == 'win32'):
    from msvcrt import getch

else:
    from tty import setraw
    from termios import tcsetattr, tcgetattr, TCSADRAIN
    from sys import stdin

    def getch():
        fd: int = stdin.fileno()
        defaut_settings = tcgetattr(fd)

        try:
            setraw(fd)
            ch = stdin.read(1)
        finally:
            tcsetattr(fd, TCSADRAIN, defaut_settings)
        return ch.encode()