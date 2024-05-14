FROM molssi/mamba141

COPY ./mopac_step/data/seamm-mopac.yml /root/environment.yml

RUN mamba env update -f /root/environment.yml

WORKDIR /home
CMD ["mopac", "mopac.dat"]
