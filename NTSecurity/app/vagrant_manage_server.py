import vagrant
from fabric.api import env, execute, task, run

@task
def mytask():
    run('echo $USER')
    run('uname -a')


vagrantfile = '/home/ivan/Documents/Learn/ECM_elastic_fastapi_vue/NTSecurity/app/dynamic_sandbox/alpine/'
v = vagrant.Vagrant(vagrantfile)
v.up()
env.hosts = [v.user_hostname_port()]
env.key_filename = v.keyfile()
env.disable_known_hosts = True # useful for when the vagrant box ip changes.
execute(mytask) # run a fabric task on the vagrant host.
