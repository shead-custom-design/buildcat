# Copyright 2018 Timothy M. Shead
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
import os
import pprint
import shutil
import signal
import subprocess
import sys
import time
import uuid

import arrow
import blessings
import buildcat
import rq
import tqdm


class FramesAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed.")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        ranges = values.split(",")
        ranges = [range.split(":") for range in ranges]
        ranges = [[item.split("-") for item in range] for range in ranges]
        ranges = [(int(range[0][0]), int(range[0][-1])+1, int(range[1][0]) if len(range) > 1 else 1) for range in ranges]
        print(ranges)

        setattr(namespace, self.dest, ranges)


parser = argparse.ArgumentParser(description="Command line client for Buildcat: the portable, lightweight render farm.")
parser.add_argument("--debug", action="store_true", help="Verbose logging output.")
subparsers = parser.add_subparsers(title="commands (choose one)", dest="command")

# certificate-info
subparser = subparsers.add_parser("certificate-info", help="Display information about a TLS certificate.")
subparser.add_argument("path", help="Path to the certificate file.")

# client-keygen
subparser = subparsers.add_parser("client-keygen", help="Generate client key and certificate for TLS encryption.")
subparser.add_argument("--country", default="US", help="Certificate country. Default: %(default)s")
subparser.add_argument("--days", type=int, default=365, help="Length of time the certificate will be valid. Default: %(default)s")
subparser.add_argument("--email", default=None, help="Certificate email. Default: %(default)s")
subparser.add_argument("--locality", default="Albuquerque", help="Certificate locality. Default: %(default)s")
subparser.add_argument("--name", default="*", help="Client name. Default: %(default)s")
subparser.add_argument("--organization", default="Buildcat", help="Certificate organization. Default: %(default)s")
subparser.add_argument("--state", default="New Mexico", help="Certificate state. Default: %(default)s")
subparser.add_argument("--unit", default=None, help="Certificate organizational unit. Default: %(default)s")

# client-tunnel
subparser = subparsers.add_parser("client-tunnel", help="Create a forwarding TLS tunnel for Buildcat workers and clients.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--identity", default=os.path.expanduser("~/.buildcat/client.pem"), help="Client private key and certificate. Default: %(default)s")
subparser.add_argument("--peer", default=os.path.expanduser("~/.buildcat/server.cert"), help="Server certificate. Default: %(default)s")
subparser.add_argument("--port", type=int, default=4443, help="Server port. Default: %(default)s")
subparser.add_argument("--tunnel-port", type=int, default=6379, help="Listening port. Default: %(default)s")

# eta
subparser = subparsers.add_parser("eta", help="Estimate when a queue will empty.")
subparser.add_argument("--count", type=int, default=60, help="Number of intervals to retain for the moving average. Default: %(default)s")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--interval", type=float, default=5, help="Update interval in seconds. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue to ping. Default: %(default)s")

# houdini-info
subparser = subparsers.add_parser("houdini-info", help="Retrieve Houdini information from a worker.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue to ping. Default: %(default)s")

# houdini-render-ifd
subparser = subparsers.add_parser("houdini-render-ifd", help="Submit Houdini .ifd render jobs.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="server queue to use for rendering. default: %(default)s")
subparser.add_argument("--timeout", type=int, default=15 * 60, help="Job timeout in seconds. default: %(default)s")
subparser.add_argument("ifdfile", nargs="+", help="Houdini .ifd file(s) to render with mantra.")

# houdini-render-hip
subparser = subparsers.add_parser("houdini-render-hip", help="Submit a Houdini .hip render job.")
subparser.add_argument("--frames", action=FramesAction, default="1", help="Frame(s) to render.  Default: %(default)s")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue to use for rendering. Default: %(default)s")
subparser.add_argument("--rop", default="/out/mantra_ipr", help="ROP to use for rendering. Default: %(default)s")
subparser.add_argument("--timeout", type=int, default=15 * 60, help="Job timeout in seconds. default: %(default)s")
subparser.add_argument("hipfile", help="Houdini .hip file to render.")

# modo-info
subparser = subparsers.add_parser("modo-info", help="Retrieve Modo information from a worker.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue to ping. Default: %(default)s")

# modo-render
subparser = subparsers.add_parser("modo-render", help="Submit a Modo render job.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue to ping. Default: %(default)s")
subparser.add_argument("--start", type=int, default=0, help="First frame to render. Default: %(default)s")
subparser.add_argument("--step", type=int, default=1, help="Interval between rendered frames. Default: %(default)s.")
subparser.add_argument("--stop", type=int, default=1, help="One past the last frame to render. Default: %(default)s")
subparser.add_argument("--timeout", type=int, default=15 * 60, help="Job timeout in seconds. default: %(default)s")
subparser.add_argument("lxofile", help="Modo .lxo file to render.")

# redshift-info
subparser = subparsers.add_parser("redshift-info", help="Retrieve Redshift information from a worker.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue to ping. Default: %(default)s")

# redshift-render
subparser = subparsers.add_parser("redshift-render", help="Submit a Redshift render job.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue to use for rendering. Default: %(default)s")
subparser.add_argument("--timeout", type=int, default=15 * 60, help="Job timeout in seconds. default: %(default)s")
subparser.add_argument("rsfile", help="Redshift .rs file to render.")

# server
subparser = subparsers.add_parser("server", help="Start a Buildcat server.")
subparser.add_argument("--bind", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--storage", default="buildcat.aof", help="Persistent storage location. Default: %(default)s")

# server-keygen
subparser = subparsers.add_parser("server-keygen", help="Generate server key and certificate for TLS encryption.")
subparser.add_argument("--country", default="US", help="Certificate country. Default: %(default)s")
subparser.add_argument("--days", type=int, default=365, help="Length of time the certificate will be valid. Default: %(default)s")
subparser.add_argument("--email", default=None, help="Certificate email. Default: %(default)s")
subparser.add_argument("--locality", default="Albuquerque", help="Certificate locality. Default: %(default)s")
subparser.add_argument("--name", default="127.0.0.1", help="Server name. Default: %(default)s")
subparser.add_argument("--organization", default="Buildcat", help="Certificate organization. Default: %(default)s")
subparser.add_argument("--state", default="New Mexico", help="Certificate state. Default: %(default)s")
subparser.add_argument("--unit", default=None, help="Certificate organizational unit. Default: %(default)s")

# server-tunnel
subparser = subparsers.add_parser("server-tunnel", help="Create a listening TLS tunnel for the Buildcat server.")
subparser.add_argument("--identity", default=os.path.expanduser("~/.buildcat/server.pem"), help="Server private key and certificate. Default: %(default)s")
subparser.add_argument("--peers", default=os.path.expanduser("~/.buildcat/client.cert"), help="Allowed client certificates. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--tunnel-port", type=int, default=4443, help="Listening port. Default: %(default)s")

# worker
subparser = subparsers.add_parser("worker", help="Start a Buildcat worker.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--max-jobs", default=None, type=int, help="Maximum number of jobs to execute. Default: unlimited")
subparser.add_argument("--no-fork", action="store_true", help="Use a non-forking worker for collecting code coverage.")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--redshift-gpu", action="append", help="Specify GPU indices to use for Redshift rendering. Default: use all GPUs.")
subparser.add_argument("queues", default=["default"], nargs="*", help="Server queues to handle. Default: %(default)s")

# workers
subparser = subparsers.add_parser("workers", help="Start multiple Buildcat workers.")
subparser.add_argument("--count", "-n", type=int, default=1, help="Number of workers to start. Default: %(default)s")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--max-jobs", default=None, type=int, help="Maximum number of jobs to execute. Default: unlimited")
subparser.add_argument("--no-fork", action="store_true", help="Use non-forking workers for collecting code coverage.")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--redshift-gpu", action="append", help="Specify GPU indices to use for Redshift rendering. Default: use all GPUs.")
subparser.add_argument("--session-name", "-s", default="buildcat-workers", help="tmux session name.  Default: %(default)s")
subparser.add_argument("queues", default=["default"], nargs="*", help="Server queues to handle. Default: %(default)s")

# worker-info
subparser = subparsers.add_parser("worker-info", help="Retrieve information about a worker.")
subparser.add_argument("--host", default="127.0.0.1", help="Server address. Default: %(default)s")
subparser.add_argument("--port", type=int, default=6379, help="Server port. Default: %(default)s")
subparser.add_argument("--queue", default="default", help="Server queue. Default: %(default)s")

# version
subparser = subparsers.add_parser("version", help="Print the version of this client.")

def main():
    arguments = parser.parse_args()

    if arguments.command is None:
        parser.print_help()

    logging.basicConfig(level=logging.DEBUG if arguments.debug else logging.INFO)
    log = logging.getLogger()
    log.name = os.path.basename(sys.argv[0])

    # certificate-info
    if arguments.command == "certificate-info":
        buildcat.check_call(["openssl", "x509", "-in", arguments.path, "-text"])

    # client-keygen
    if arguments.command == "client-keygen":
        subj = ""
        subj += f"/C={arguments.country}" if arguments.country else ""
        subj += f"/ST={arguments.state}" if arguments.state else ""
        subj += f"/L={arguments.locality}" if arguments.locality else ""
        subj += f"/O={arguments.organization}" if arguments.organization else ""
        subj += f"/OU={arguments.unit}" if arguments.unit else ""
        subj += f"/emailAddress={arguments.email}" if arguments.email else ""
        subj += f"/CN={arguments.name}"

        buildcat.check_call(["openssl", "genrsa", "-out", "client.key", "2048"])
        buildcat.check_call(["openssl", "req", "-new", "-key", "client.key", "-x509", "-subj", subj, "-out", "client.cert", "-days", str(arguments.days)])
        with open("client.pem", "wb") as output:
            with open("client.key", "rb") as input:
                output.write(input.read())
            with open("client.cert", "rb") as input:
                output.write(input.read())


    # client-tunnel
    if arguments.command == "client-tunnel":
        command = [
            "socat",
            f"TCP4-LISTEN:{arguments.tunnel_port},bind=127.0.0.1,reuseaddr,fork",
            f"OPENSSL:{arguments.host}:{arguments.port},cert={arguments.identity},cafile={arguments.peer}",
            ]
        try:
            process = subprocess.Popen(command)
            log.info(f"Connections to 127.0.0.1:{arguments.tunnel_port} will be forwarded to the server at {arguments.host}:{arguments.port}.")
            process.wait()
        except KeyboardInterrupt:
            process.wait()


    # eta
    if arguments.command == "eta":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        term = blessings.Terminal()

        with term.fullscreen():
            try:
                samples = []
                samples.append((len(queue), time.time()))
                count, timestamp = samples[-1]

                line = term.clear()
                line += f" queue: {term.bold_bright_green}{arguments.queue}{term.normal}"
                line += f" jobs: {term.bold_bright_white}{count}{term.normal}"
                print(line)

                while True:
                    time.sleep(arguments.interval)

                    samples.append((len(queue), time.time()))
                    samples = samples[-arguments.count:]
                    start_count, start_timestamp = samples[0]
                    count, timestamp = samples[-1]

                    rate = (start_count - count) / (timestamp - start_timestamp) # "jobs per second"

                    line = term.clear()
                    line += f" queue: {term.bold_bright_green}{arguments.queue}{term.normal}"
                    line += f" jobs: {term.bold_bright_white}{count}{term.normal}"

                    if rate > 0:
                        line += f" ({term.bold_bright_white}-{abs(rate):.2f}{term.normal} jobs/sec)"
                    else:
                        line += f" ({term.bold_bright_red}+{abs(rate):.2f}{term.normal} jobs/sec)"

                    if rate > 0:
                        eta = arrow.now().shift(seconds=count / rate).format("YYYY-MM-DD HH:mm:ss ZZ")
                        line += f" ETA: {term.bold_bright_red}{eta}{term.normal}"
                    else:
                        line += f" ETA: {term.bold_bright_red}unknown{term.normal}"

                    print(line)

            except KeyboardInterrupt:
                pass


    # houdini-info
    if arguments.command == "houdini-info":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        job = buildcat.submit(queue, "buildcat.hou.info")
        pprint.pprint(buildcat.wait(connection=connection, job=job))


    # houdini-render-ifd
    if arguments.command == "houdini-render-ifd":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        ifdfiles = [buildcat.require_relative_path(ifdfile, "Houdini .ifd file must be a relative path.") for ifdfile in arguments.ifdfile]
        for ifdfile in tqdm.tqdm(ifdfiles, unit="frame"):
            job = buildcat.submit(queue, "buildcat.hou.render_ifd", ifdfile, job_timeout=arguments.timeout)
        print(f"Submitted {len(ifdfiles)} job(s).")


    # houdini-render-hip
    if arguments.command == "houdini-render-hip":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        hipfile = buildcat.require_relative_path(arguments.hipfile, "Houdini .hip file must be a relative path.")
        job = buildcat.submit(queue, "buildcat.hou.render_hip", hipfile=hipfile, rop=arguments.rop, frames=arguments.frames, job_timeout=arguments.timeout)
        print(f"Submitted job {job.id}")


    # modo-info
    if arguments.command == "modo-info":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        job = buildcat.submit(queue, "buildcat.modo.info")
        pprint.pprint(buildcat.wait(connection=connection, job=job))


    # modo-render
    if arguments.command == "modo-render":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        lxofile = buildcat.require_relative_path(arguments.lxofile, "Modo .lxo file must be a relative path.")
        job = buildcat.submit(queue, "buildcat.modo.split_frames", lxofile, (arguments.start, arguments.stop, arguments.step), job_timeout=arguments.timeout)
        print(f"Submitted job {job.id}")


    # redshift-info
    if arguments.command == "redshift-info":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        job = buildcat.submit(queue, "buildcat.redshift.info")
        pprint.pprint(buildcat.wait(connection=connection, job=job))


    # redshift-render
    if arguments.command == "redshift-render":
        rsfile = buildcat.require_relative_path(arguments.rsfile, "Redshift .rs file must be a relative path.")
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        job = buildcat.submit(queue, "buildcat.redshift.render", rsfile, job_timeout=arguments.timeout)
        print(f"Submitted job {job.id}")


    # server
    if arguments.command == "server":
        storage_dir, storage_file = os.path.split(arguments.storage)
        storage_dir = storage_dir or "."

        command = [
            "redis-server",
            "--bind", arguments.bind,
            "--port", str(arguments.port),
            "--appendonly", "yes",
            "--appendfilename", storage_file,
            "--dir", storage_dir,
            ]
        try:
            process = subprocess.Popen(command)
            process.wait()
        except KeyboardInterrupt:
            process.send_signal(signal.SIGINT)
            process.wait()


    # server-keygen
    if arguments.command == "server-keygen":
        subj = ""
        subj += f"/C={arguments.country}" if arguments.country else ""
        subj += f"/ST={arguments.state}" if arguments.state else ""
        subj += f"/L={arguments.locality}" if arguments.locality else ""
        subj += f"/O={arguments.organization}" if arguments.organization else ""
        subj += f"/OU={arguments.unit}" if arguments.unit else ""
        subj += f"/emailAddress={arguments.email}" if arguments.email else ""
        subj += f"/CN={arguments.name}"

        buildcat.check_call(["openssl", "genrsa", "-out", "server.key", "2048"])
        buildcat.check_call(["openssl", "req", "-new", "-key", "server.key", "-x509", "-subj", subj, "-out", "server.cert", "-days", str(arguments.days)])
        with open("server.pem", "wb") as output:
            with open("server.key", "rb") as input:
                output.write(input.read())
            with open("server.cert", "rb") as input:
                output.write(input.read())


    # server-tunnel
    if arguments.command == "server-tunnel":
        command = [
            "socat",
            f"OPENSSL-LISTEN:{arguments.tunnel_port},cert={arguments.identity},cafile={arguments.peers},reuseaddr,fork",
            f"TCP4:127.0.0.1:{arguments.port}",
            ]
        try:
            process = subprocess.Popen(command)
            log.info(f"Connections to 0.0.0.0:{arguments.tunnel_port} will be forwarded to the server at 127.0.0.1:{arguments.port}.")
            process.wait()
        except KeyboardInterrupt:
            process.wait()


    # worker
    if arguments.command == "worker":
        if arguments.redshift_gpu:
            os.environ["BUILDCAT_REDSHIFT_GPU"] = " ".join(arguments.redshift_gpu)

        connection = buildcat.connect(host=arguments.host, port=arguments.port)
        if arguments.no_fork:
            worker = rq.SimpleWorker(arguments.queues, connection=connection, serializer=buildcat.Serializer)
        else:
            worker = rq.Worker(arguments.queues, connection=connection, serializer=buildcat.Serializer)
        worker.work(max_jobs=arguments.max_jobs)


    # workers
    if arguments.command == "workers":
        command = []
        for rank in range(arguments.count):
            if rank == 0:
                command += ["tmux", "new-session", "-s", arguments.session_name]
            else:
                command += [";", "new-window", "-d"]

            command += ["-n", f"worker-{rank}"]

            command += ["buildcat", "worker", "--host", arguments.host, "--port", str(arguments.port)]
            if arguments.max_jobs is not None:
                command += ["--max-jobs", arguments.max_jobs]
            if arguments.no_fork:
                command += ["--no-fork"]
            command += arguments.queues
        buildcat.check_call(command)


    # worker-info
    if arguments.command == "worker-info":
        connection, queue = buildcat.queue(queue=arguments.queue, host=arguments.host, port=arguments.port)
        job = buildcat.submit(queue, "buildcat.worker.info")
        pprint.pprint(buildcat.wait(connection=connection, job=job))


    # version
    if arguments.command == "version":
        print(buildcat.__version__)

