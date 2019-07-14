import time

import redis
import rq

import buildcat


class Job(object):
    def __init__(self, job):
        self._job = job

    @property
    def result(self):
        return self._job.result

    def wait(self):
        while True:
            if self._job.is_failed:
                raise buildcat.Error("Job failed.", "")
            if self._job.result is not None:
                return self._job.result
            time.sleep(0.5)


class Queue(object):
    def __init__(self, queue="default", host="127.0.0.1", port=6379, timeout=5):
        if not host:
            raise buildcat.Error(
                message="Server host not specified.",
                description="You must specify the IP address or hostname of the Buildcat server.",
                )
        try:
            self._connection = redis.Redis(host, socket_timeout=timeout)
            self._connection.ping()
        except redis.exceptions.TimeoutError:
            raise buildcat.Error(
                message="Couldn't connect to server.",
                description="Verify that the Buildcat server is listening at {} port {}.".format(host, port),
                )
        except Exception as e:
            raise buildcat.Error(
                message="Couldn't connect to server.",
                description=str(e),
                )

        if not queue:
            raise buildcat.Error(
                message="Server queue not specified.",
                description="You must specify the name of a Buildcat queue.",
                )

#        buildcat_root = node.evalParm("buildcat_root")
#        if not buildcat_root:
#            return error("Buildcat Root not set.", "You must specify the path to the Buildcat shared storage directory for this machine.")
#
#        if not (os.path.exists(buildcat_root) and os.path.isdir(buildcat_root)):
#            return error("Buildcat Root path does not exist.", "The Buildcat shared storage location must be an existing directory.")
#
#        if not os.path.isabs(buildcat_root):
#            return error("Buildcat Root must be absolute.", "The Buildcat Root path must be an absolute (not relative) path.")
#
#        hipfile = hou.hipFile.path()
#        if not os.path.isabs(hipfile):
#            return error("Internal error.", "The hipfile path must be an absolute (not relative) path.")
#
#        if not hipfile.startswith(buildcat_root):
#            return error("HIP file stored outside Buildcat Root.", "This file and its assets must be saved to the Buildcat shared storage location to be rendered.")
#        hipfile = os.path.join("$BUILDCAT_ROOT", os.path.relpath(hipfile, buildcat_root))
#
#        start = int(node.evalParm("f1"))
#        end = int(node.evalParm("f2")) + 1 # Buildcat uses half-open ranges
#        increment = int(node.evalParm("f3"))

        self._queue = rq.Queue(queue, connection=self._connection)

    def submit(self, command, *args, **kwargs):
        if not command:
            raise buildcat.Error(
                message="Command not specified.",
                description="You must specify the name of a Buildcat command.",
                )

        return Job(self._queue.enqueue(command, *args, **kwargs))
