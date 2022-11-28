from docker import from_env


containers = from_env().containers
package_name = "HAredisPy"


class redisSetup:
    def __init__(self, containers):
        self.containers = containers

    @staticmethod
    def createRedisSetup(redisV, name, ports):
        for i in range(3):
            contName = f"{name}_{package_name}_redis_{i}"
            port = {"6379/tcp": ports[i]}
            containers.run(image=redisV, name=contName, detach=True, ports=port)

    @staticmethod
    def getAllSetups():

        # get all containers from docker daemon
        allContainers = containers.list(all=True)

        containerSetups = dict()

        # for each container run the code below
        for container in allContainers:

            # if there's no HAdockerPy in the name of the container
            # then skip this container since it was not created by this script
            if container.name.split("_")[1] != package_name:
                continue

            # get the name of the container
            containerName = str(container.name.split("_")[0])

            # if container name already exists in containerSetups dictionary
            # then add a container to the dictionary
            if containerName in containerSetups.keys():
                containerSetups[containerName].add(container)

            # else create a key value pair in the dictionary
            # where key is name of the setup and value is a set of three containers.
            else:
                containerSetups[containerName] = set()
                containerSetups[containerName].add(container)

        # substitute the set of three containers
        # by the redisSetup object which contains all three containers.
        for key, value in containerSetups.items():
            containerSetups[key] = redisSetup(value)

        # return dictionary where key is name of the setup and value is a redisSetup object.
        return containerSetups

    @staticmethod
    def getContPort(container):
        return container.attrs.get('HostConfig').get('PortBindings').get('6379/tcp')[0].get('HostPort')

    @staticmethod
    def getSetupPorts(setupName):
        # get containers
        setupConts = redisSetup.getSetup(setupName).getContainers()
        # get ports used by the setup
        setupPorts = [redisSetup.getContPort(container) for container in setupConts]
        return setupPorts
    
    @staticmethod
    def getOccupiedPorts():
        runningContainers = containers.list()
        occPorts = [redisSetup.getContPort(container) for container in runningContainers]
        return occPorts

    @staticmethod
    def checkPortsValidity(ports):
        for port in ports:
            if port in redisSetup.getOccupiedPorts():
                print("Ports are already in use")
                return False
        return True
    
    @staticmethod
    def getSetup(name):
        return redisSetup.getAllSetups().get(name)

    @staticmethod
    def setupExists(name):
        return name in redisSetup.getAllSetups().keys()

    def getContainers(self):
        return self.containers
    
    def startSetup(self):
        for container in self.containers:
            container.start()

    def stopSetup(self):
        for container in self.containers:
            container.stop()

    def setupRemove(self):
        for container in self.containers:
            container.kill()
            container.remove()
