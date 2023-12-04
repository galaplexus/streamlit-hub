import subprocess
import dataclasses


@dataclasses.dataclass
class RunningProcess:
    link: str


@dataclasses.dataclass
class LocalProcess(RunningProcess):
    port: str
    process: subprocess.Popen
