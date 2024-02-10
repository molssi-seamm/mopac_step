FROM molssi/mamba141

COPY ./environment.yml /root/environment.yml

RUN mamba env update -f /root/environment.yml

WORKDIR /home
CMD ["mopac", "mopac.dat"]
