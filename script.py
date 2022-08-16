from HAdockerPy.redisSetup import redisSetup
import argparse
import docker


def main():

    ######################################################################################
    ########################### Creating Parser and Subparsers ###########################
    ######################################################################################

    parser = argparse.ArgumentParser(
        description="Docker setup for redis high availability."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    ######################################################################################
    ############################ Implementing RUN subparser ##############################
    ######################################################################################

    run_parser = subparsers.add_parser(
        "run", help="Create a Docker container and start it"
    )
    run_parser.add_argument(
        "-n",
        "--name",
        dest="name",
        type=str,
        required=True,
        help="Specify the name of the setup. NOTE: The setup with the provided name must not exist",
    )
    run_parser.add_argument(
        "-p", "--port", type=int, default=[6379, 6380, 6381], dest="port", nargs="+"
    )
    run_parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="latest",
        dest="version",
        choices=(
            "7.0.4",
            "7.0",
            "7",
            "latest",
            "7.0.4-bullseye",
            "7.0-bullseye",
            "7-bullseye",
            "bullseye",
        ),
    )

    ######################################################################################
    ############################ Implementing START subparser ############################
    ######################################################################################

    start_parser = subparsers.add_parser("start", help="Start a Docker setup")

    start_parser.add_argument(
        "-n",
        "--name",
        dest="name",
        type=str,
        required=True,
        help="Specify the name of the setup to start",
    )

    ######################################################################################
    ############################ Implementing STOP subparser #############################
    ######################################################################################

    stop_parser = subparsers.add_parser(
        "stop", help="Stop redis setup. Check setups.json file for setups information."
    )
    stop_parser.add_argument(
        "-n",
        "--name",
        dest="name",
        type=str,
        required=True,
        help="Specify the name of the setup to stop",
    )

    ######################################################################################
    ############################ Implementing STATUS subparser ###########################
    ######################################################################################

    status_parser = subparsers.add_parser("status", help="Print status information.")

    ######################################################################################
    ###################### Parsing args and preparing for execution ######################
    ######################################################################################

    args = parser.parse_args()
    print(vars(args))

    client = docker.from_env()
    containers = client.containers

    ######################################################################################
    #################################### Execution #######################################
    ######################################################################################

    if args.command == "run":

        setupName = args.name
        redis_version = f"redis:{args.version}"

        if redisSetup.setupExists(setupName):
            raise Exception("Setup already exists. Pick another name.")
        redisSetup.createRedisSetup(redis_version, setupName, args.port)

    elif args.command == "start":
        setupName = args.name
        if redisSetup.setupExists(setupName):
            redisSetup.getSetup(setupName).startSetup()

    elif args.command == "stop":
        setupName = args.name
        if redisSetup.setupExists(setupName):
            redisSetup.getSetup(setupName).stopSetup()

    elif args.command == "status":
        print(redisSetup.getAllSetups())


if __name__ == "__main__":
    main()
