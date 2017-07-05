FROM ubuntu:16.04

RUN apt-get update && apt-get install -y openssh-server && apt-get install -y python
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd

#RUN echo 'jenkins:jenkins' | chpasswd
#RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN mkdir -p /root/.ssh
COPY authorized_keys /root/.ssh/authorized_keys

RUN mkdir -p /root/hello
copy . /root/hello

EXPOSE 22
EXPOSE 80
CMD ["/usr/sbin/sshd", "-D"] 

