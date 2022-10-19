import docker
import subprocess
import time


# https://docker-py.readthedocs.io/en/stable/containers.html
# https://github.com/docker/docker-py/blob/master/tests/unit/models_containers_test.py
# https://docker-py.readthedocs.io/en/stable/containers.html
# https://docs.docker.com/engine/reference/commandline/update/
# https://docs.docker.com/engine/api/sdk/examples/

class Dockermanager():
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.containers_list = []
        # client = docker.from_env()

    def containerlist(self):
        containers = self.client.containers.list(all=True)
        self.containers_list = [{'name': container.name, "image": container.image, 'status': container.status} for
                                container in
                                containers]

    def get_container_by_ID(self, id):
        return self.client.containers.get(id)

    def getcontainer(self, containername):
        return self.client.containers.get(containername)

    def containerlog(self, containername, timestamps=True, tail='all', since=None, until=None, ):

        container = self.getcontainer(containername)
        content = container.logs(timestamps=timestamps, tail=tail, since=since, until=until)
        return content

    def log_container(self, containername):
        # 实时读取日志
        pos = 0
        while 1:
            num = 0
            print('reading..........')
            out = subprocess.Popen('docker logs -t {}'.format(containername), shell=True, stdout=subprocess.PIPE)
            logs = out.stdout.readlines()[pos:]
            out.terminate()
            for i in logs:
                d = bytes.decode(i).replace('\r\n', '')
                if len(d) > 40:
                    print(d)
                num += 1
            pos += num
        #   time.sleep(1)

    def run_container(self, image, command=None, **kwargs):
        # client.containers.run('alpine', 'echo hello world')
        newcontainer = self.client.containers.run(image, command=None, **kwargs)

    def update_container(self, container_name, cpus):
        container = self.getcontainer(container_name)
        # container.update(cpu_shares=2, mem_limit="20MB", memswap_limit="20MB")

        # out = subprocess.Popen('docker update --cpus {} -m 4096M --memory-swap 4096M {}'.format(container_name), shell=True, stdout=subprocess.PIPE)
        out = subprocess.Popen('docker update --cpus {} {}'.format(cpus, container_name),
                               shell=True, stdout=subprocess.PIPE)

        print(out.stdout)

    def pause_container(self, containername):
        container = self.getcontainer(containername)
        container.pasue()

    def remove_container(self, containername):
        container = self.getcontainer(containername)
        container.remove()

    def stop_container(self, containername):
        container = self.getcontainer(containername)
        container.stop()

    def top_container(self, containername):
        container = self.getcontainer(containername)
        top = container.top()
        print(top)
        return top

    # def stats_container(self, containername):
    #     # Stream statistics for this container. Similar to the docker stats command.
    #     container = self.getcontainer(containername)
    #     stats = container.stats(decode=True)
    #     statsvalue = next(stats)
    #     timestamp = statsvalue['read'][:-11]
    #     pids_num = statsvalue['pids_stats']['current']
    #     networks = statsvalue['networks']['eth0']
    #     out = subprocess.Popen('docker stats {}'.format(containername), shell=True, stdout=subprocess.PIPE)
    #     for n, v in enumerate(out.stdout):
    #         if n == 1:
    #             stat_str = bytes.decode(v.strip())
    #             print(stat_str)
    #             value = stat_str.split(' ')
    #
    #             valuelist = [j for j in value if j != '' and j != '/']
    #             monitordict = dict(zip(
    #                 ['cpu_percentage', 'memory_useage', 'memory_total', 'memory_percentage', 'net_in', 'net_out',
    #                  'block_in', 'block_out'], valuelist[2:]))
    #
    #             out.terminate()
    #             break
    #     monitordict.update({'timestamp': timestamp, 'pids_num': pids_num, 'networks': networks})
    #     print(monitordict)
    #     return monitordict

    def stats_container(self, containername):
        # Stream statistics for this container. Similar to the docker stats command.
        container = self.getcontainer(containername)
        stats = container.stats(decode=True)
        statsvalue = next(stats)
        timestamp = statsvalue['read'][:-11]
        pids_num = statsvalue['pids_stats']['current']
        networks = statsvalue['networks']['eth0']
        out = subprocess.Popen('docker stats {}'.format(containername), shell=True, stdout=subprocess.PIPE)
        monitordict = None

        for n, v in enumerate(out.stdout):
            stat_str = bytes.decode(v.strip())
            print(stat_str)
            print("lele")
            # if n == 0:
            #     print("n==0")
            #     stat_str = bytes.decode(v.strip())
            #     print(stat_str)
            #     continue
            #
            # if n == 1:
            #     print("n==1")
            #     stat_str = bytes.decode(v.strip())
            #     print(stat_str)
            #     value = stat_str.split(' ')
            #
            #     valuelist = [j for j in value if j != '' and j != '/']
            #     monitordict = dict(zip(
            #         ['cpu_percentage', 'memory_useage', 'memory_total', 'memory_percentage', 'net_in', 'net_out',
            #          'block_in', 'block_out'], valuelist[2:]))
            #     continue
            #
            # if n == 2:
            #     print("n==2")
            #     stat_str = bytes.decode(v.strip())
            #     print(stat_str)
            #     value = stat_str.split(' ')
            #
            #     valuelist = [j for j in value if j != '' and j != '/']
            #     monitordict = dict(zip(
            #         ['cpu_percentage', 'memory_useage', 'memory_total', 'memory_percentage', 'net_in', 'net_out',
            #          'block_in', 'block_out'], valuelist[2:]))
            #     continue


            if n == 5:
                print("n==5")
                stat_str = bytes.decode(v.strip())
                print(stat_str)
                value = stat_str.split(' ')

                valuelist = [j for j in value if j != '' and j != '/']
                monitordict = dict(zip(
                    ['cpu_percentage', 'memory_useage', 'memory_total', 'memory_percentage', 'net_in', 'net_out',
                     'block_in', 'block_out'], valuelist[2:]))
                out.terminate()
                break
            # else:
            #     out.terminate()
            #     break
        if monitordict is None:
            return None

        monitordict.update({'timestamp': timestamp, 'pids_num': pids_num, 'networks': networks})
        # print(monitordict)
        return monitordict


import sys

if __name__ == '__main__':
    list_of_arguments = sys.argv
    if len(list_of_arguments) < 6:
        print(
            "please input the primary_docker_name, secondary_docker_name, cpu_lower_bound, cpu_upper_bound, update_cpus")
        print("e.g. hadoop-slave3 hadoop-slave8 10 40 30")
        exit(0)

    primary_docker_name = list_of_arguments[1]
    secondary_docker_name = list_of_arguments[2]
    cpu_lower_bound = float(list_of_arguments[3]) * 100
    cpu_upper_bound = float(list_of_arguments[4]) * 100
    update_cpus = int(list_of_arguments[5])
    c = Dockermanager()
    # c.log_container('stupefied_roentgen')
    # docker that we can squeeze resource from
    # primary_docker_name = "hadoop-slave3.1.eagvhbu0ae603s2oy8e31cc65"
    # secondary_docker_name = "hadoop-slave8.1.3526fg6b92pnp0jso4ayf677x"

    while True:
        monitordict = c.stats_container(primary_docker_name)
        if monitordict == None:
            time.sleep(1)
            continue

        cpu_percentage = monitordict['cpu_percentage']
        # cpu_percentage_float is the CPU usage of monitored docker
        cpu_percentage_float = float(cpu_percentage.replace("%", ""))
        # print(cpu_percentage_float)
        hos_cpu_map = {'q15_500': 40}

        print("CPU utilization is {} for primary_docker_name {} ".format(cpu_percentage_float, primary_docker_name))
        if cpu_percentage_float <= cpu_lower_bound:
            # secondary container name
            print(" cpu_percentage_float {} <= cpu_lower_bound {}".format(cpu_percentage_float, cpu_lower_bound))
            update_cpus = int(cpu_lower_bound/100 - cpu_percentage_float/100)
            print("update the cpu cores of the secondary docker {} to {}".format(secondary_docker_name, update_cpus))
            c.update_container(secondary_docker_name, update_cpus)
        elif cpu_percentage_float >= cpu_upper_bound:
            print(" cpu_percentage_float {} >= cpu_upper_bound {}".format(cpu_percentage_float, cpu_upper_bound))
            print("update the cpu cores of the secondary docker {} to 5".format(secondary_docker_name))
            c.update_container(secondary_docker_name, 5)
        else:
            # cpu_lower_bound <= cpu_percentage_float <= cpu_upper_bound
            print("cpu_lower_bound {} <= cpu_percentage_float <= cpu_upper_bound {}".format(cpu_lower_bound,
                                                                                            cpu_upper_bound))
            print("update the cpu cores of the secondary docker {} to 5".format(secondary_docker_name))
            c.update_container(secondary_docker_name, 5)

        time.sleep(1)
