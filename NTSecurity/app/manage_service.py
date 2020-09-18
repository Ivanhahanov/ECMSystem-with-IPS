import docker
import os
import glob



client = docker.from_env()


def build_container(build_args=None):
    image, build_logs = client.images.build(path='./sandbox', tag='sandbox', buildargs=build_args)
    for iter in build_logs:
        print(iter)


def run_container(docker_env=None):
    print(client.containers.run(image='sandbox',
                                remove=True,
                                environment=docker_env,
                                volumes={f'{PWD}/static_sandbox/yara/rules': {'bind': '/rules', 'mode': 'ro'},
                                         f'{PWD}/static_sandbox/yara/mallware': {'bind': '/malware', 'mode': 'ro'},
                                         f'{PWD}/static_sandbox/files': {'bind': '/files', 'mode': 'ro'}},
                                command=['/rules/test.yar', '/files/1']))
# docker run --rm
# -v /home/ivan/Documents/Learn/ECM_elastic_fastapi_vue/NTSecurity/app/sandbox/yara/rules:/rules:ro
# -v /home/ivan/Documents/Learn/ECM_elastic_fastapi_vue/NTSecurity/app/sandbox/yara/mallware:/malware:ro
# -v /home/ivan/Documents/Learn/ECM_elastic_fastapi_vue/NTSecurity/app/sandbox/files:/files
# sandbox /rules/test.yar /files/1

def rm_files():
    files = glob.glob('sandbox/files/*')
    for f in files:
        os.remove(f)


def send_files():
    pass

if __name__ == '__main__':
    build_args = {'OS': 'Windows'}
    docker_env = {'OS': 'Windows'}
    PWD = os.getcwd()
    print(PWD)
    # build_container()
    run_container(docker_env)
    #rm_files()
