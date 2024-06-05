FROM debian:bullseye

#    *-----*\ Root jobs /*-----*
USER root

#        * Preparing env *
ENV DEBIAN_FRONTEND=noninteractive

#        * Prologue Installation *
RUN apt update
RUN apt upgrade -y
RUN apt dist-upgrade -y

#        * Install Bins & Deps *
RUN apt install git -y
# RUN apt install valgrind -y
RUN apt install libc6 -y
RUN apt install python3 -y
RUN apt install pip -y
RUN apt install gcc -y
RUN apt install make -y
RUN apt install man -y
RUN apt install nano -y

RUN mkdir /usr/lib64
RUN cp /lib/x86_64-linux-gnu/libc.so.6 /usr/lib64/

#        * Install fluxify *
RUN mkdir /tmp/fluxify
WORKDIR /tmp/fluxify
RUN git clone https://github.com/StevenGandon/HUB-Fluxify.git
WORKDIR /tmp/fluxify/HUB-Fluxify

RUN make

RUN mkdir /var/lib/fcc
RUN mkdir /var/lib/fli
RUN mkdir /var/lib/flo_to_exe

RUN cp ./vm/fvm /bin

RUN cp ./compiler/fcc /var/lib/fcc/
RUN cp -r ./compiler/src /var/lib/fcc/
RUN ln -s /var/lib/fcc/fcc /bin/fcc

RUN cp ./docs/man/* /usr/share/man/ -r

RUN cp ./vm/lib/libfloff.a /lib/
RUN cp ./vm/lib/libfluxify.a /lib/

RUN cp ./vm/lib/floff/floff.h /usr/include/
RUN cp ./vm/lib/fluxify/fluxify.h /usr/include/

RUN cp ./fli/fli /var/lib/fli/
RUN cp -r ./fli/src /var/lib/fli/
RUN ln -s /var/lib/fli/fli /bin/fli

RUN cp ./flo_to_exe/flo_to_exe /var/lib/flo_to_exe/
RUN cp -r ./flo_to_exe/src /var/lib/flo_to_exe/
RUN cp -r ./flo_to_exe/assets /var/lib/flo_to_exe/
RUN ln -s /var/lib/flo_to_exe/flo_to_exe /bin/flo_to_exe

RUN chmod +x /bin/fvm
RUN chmod +x /var/lib/fcc/fcc
RUN chmod +x /var/lib/fli/fli
RUN chmod +x /var/lib/flo_to_exe/flo_to_exe

#        * Create user *
RUN useradd fluxify

#        * Prepare workdir *
RUN mkdir /app
RUN chown -R fluxify: /app
RUN chmod u+w /app

#        * Clean *
RUN make fclean
WORKDIR /
RUN apt clean
RUN apt autoremove
RUN apt autoclean
RUN rm -rf /tmp/fluxify

#    *-----*\ Fluxify jobs /*-----*
USER fluxify

#        * Switching working dir *
WORKDIR /app

CMD ["/bin/bash"]
