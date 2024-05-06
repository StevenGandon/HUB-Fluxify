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
RUN apt install valgrind -y
RUN apt install libc6 -y
RUN apt install python3 -y
RUN apt install pip -y
RUN apt install gcc -y
RUN apt install make -y
RUN apt install man -y
RUN apt install nano -y

#        * Install fluxify *
RUN mkdir /tmp/fluxify
WORKDIR /tmp/fluxify
RUN git clone https://github.com/StevenGandon/HUB-Fluxify.git
WORKDIR /tmp/fluxify/HUB-Fluxify
RUN make
RUN mkdir /var/lib/fcc
RUN cp ./vm/fvm /bin
RUN cp ./compiler/fcc /var/lib/fcc/
RUN cp -r ./compiler/src /var/lib/fcc/
RUN ln -s /var/lib/fcc/fcc /bin/fcc
RUN cp ./docs/man/* /usr/share/man/ -r

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
