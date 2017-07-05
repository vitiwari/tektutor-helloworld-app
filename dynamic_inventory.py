#!/usr/bin/env python

import subprocess
import json
from os.path import expanduser

def docker_command(*args):
    return subprocess.check_output(["docker"] + list(args)).strip()

def docker_inspect(fmt, mcn):
    return docker_command("inspect", "-f", fmt, mcn)

def docker_port(command):
    output = docker_command("port", command, "22")
    return output[8:]

def extractDockerContainerFacts(container):
    home = expanduser("~")
    hosts = [docker_inspect("{{.NetworkSettings.IPAddress}}", container)]
    ssh_vars = {
         "ansible_ssh_port": docker_port(container),
         "ansible_ssh_host": "localhost",
         "ansible_ssh_private_key_file": home+ "/.ssh/" + "id_rsa",
         "ansible_ssh_user": "root",
         "ansible_ssh_password": "root",
         "ansible_become_user": "root",
         "ansible_become_password": "root"
    }
    data = {"hosts": hosts, "vars": ssh_vars}
    return data

class DockerMachineInventory(object):
      def __init__(self):
          containers = docker_command("ps", "-q").splitlines()
          json_data = {container: extractDockerContainerFacts(container) for container in containers }

          print json.dumps(json_data)

DockerMachineInventory() 
