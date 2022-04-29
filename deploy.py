#!/usr/bin/env python3
"""
Deploy simple-feed.cloud

1. Define files and dirs to make a package
2. define execution tasks
3. copy these files and dirs to the new location
4. execute tasks
    - run containers (postgres, pgadmin, webapi)
    - apply alembic migration (create database and table if needed)
"""
import os
import shutil
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import path
from os.path import basename
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import List, Dict, Any, Optional

import yaml

PATH = Path(__name__).resolve().parent
DEPLOY_PATH = PATH / 'deploy'
TARGET = "."
DB_PATH = "."
FILES_AND_DIRS = ['alembic', 'deploy/docker-compose.yml', 'deploy/Dockerfile',
                  'deploy/run.sh', 'deploy/env.yml', 'src', 'templates',
                  'alembic.ini', 'main.py', 'requirements.txt']
ENV_FILE = "env.yml"
DOCKER_ENV = ".env"


class DeployFeed:
    """Deploy simple-feed.cloud apps."""

    def __init__(self):
        """"""
        self.deploy_path = DEPLOY_PATH
        self._target: Optional[Path] = None
        self.db_path: str = DB_PATH
        self.files_and_dirs: List[str] = FILES_AND_DIRS
        self.env_file: str = ENV_FILE
        self.docker_env: str = DOCKER_ENV

    def asdict(self):
        self_as_dict = {}
        # Include properties
        self_as_dict.update({"target": str(self.target)})

        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                self_as_dict.update({k: v})

        return self_as_dict

    @property
    def target(self) -> Path:
        if self._target:
            return self._target
        else:
            return Path(TARGET)

    @target.setter
    def target(self, target: str):
        self._target = Path(target)

    def get_env(self, *args, **kwargs) -> Dict[str, str]:
        """
        Set environment variable.

        Returns:
            Environment variables
        """
        if 'local' in args:
            with open(str(self.deploy_path / self.env_file), 'r') as f:
                return yaml.load(f.read(), Loader=yaml.Loader)
        else:
            with open(str(self.target / self.env_file), 'r') as f:
                return yaml.load(f.read(), Loader=yaml.Loader)

    def set_environment(self, *args, **kwargs) -> None:
        """
        Set environment variable.

        Returns:
            Environment variables
        """
        for k, v in self.get_env(*args, **kwargs).items():
            os.environ[k] = str(v)

    def create_docker_env_file(self):
        """
        Create environment file.

        Returns:
            None
        """
        with open(str(self.target / self.docker_env), 'w') as f:
            for k, v in self.get_env().items():
                f.write(f"{k}={v}\n")

    @staticmethod
    def create_dir(dirname: Path):
        """
        Create a directory.

        Args:
            dirname: directory (full path)

        Returns:
            None
        """
        msg = f"Create directory '{dirname}'"
        try:
            dirname.mkdir(parents=True)
            print(f"SUCCESS {msg}")
        except PermissionError as exc:
            print(f"FAILED  {msg}, error => {exc}")
            sys.exit(1)

    @staticmethod
    def copy_dir(dirname: Path, target: Path):
        """
        Copy a directory.

        Args:
            dirname: directory (full path)
            target: target directory (full path)

        Returns:
            None
        """
        msg = f"Copy directory '{dirname}' to '{target}'"
        try:
            shutil.copytree(src=str(dirname), dst=str(target), symlinks=False,
                            ignore=None, copy_function=shutil.copy2,
                            ignore_dangling_symlinks=False,
                            dirs_exist_ok=True)
            print(f"SUCCESS {msg}")
        except PermissionError as exc:
            print(f"FAILED  {msg}, error => {exc}")
            sys.exit(1)

    @staticmethod
    def copy_file(filename: Path, target: Path):
        """
        Copy file.

        Args:
            filename: File name (full path)
            target: target directory + file name (full path)

        Returns:
            None
        """
        msg = f"Copy file '{filename}' to '{target}'"
        try:
            shutil.copy(src=str(filename), dst=str(target))
            print(f"SUCCESS {msg}")
        except FileNotFoundError as exc:
            print(f"FAILED  {msg}, error => {exc}")
            sys.exit(1)

    def prepare_copy_files_and_dirs(self) -> Dict[str, Any]:
        """Prepare Copy files and directories."""
        prepare_copy_files_and_dirs = {
            "create_dir": None,
            "files_dirs": {
                "copy_dir": [],
                "copy_file": []
            }
        }
        if not self.target.is_dir():
            prepare_copy_files_and_dirs["create_dir"] = self.target

        for item in self.files_and_dirs:
            path_item = PATH / item

            if path_item.is_dir():
                target_item = self.target / item
                prepare_copy_files_and_dirs["files_dirs"]["copy_dir"].append({
                    "dirname": path_item, "target": target_item})

            elif path.isfile(path_item):
                target_item = self.target
                prepare_copy_files_and_dirs["files_dirs"]["copy_file"].append({
                    "filename": path_item, "target": target_item})

            else:
                print(f"[!] not exist => {path_item}")

        return prepare_copy_files_and_dirs

    def copy_files_and_dirs(self, prepare_copy_files_and_dirs: Dict[str, Any]):
        """Copy files and directories."""
        if prepare_copy_files_and_dirs['create_dir'] is not None:
            self.create_dir(dirname=self.target)

        files_dirs_items = prepare_copy_files_and_dirs['files_dirs'].items()
        for files_dirs, values in files_dirs_items:
            for item in values:

                if files_dirs == "copy_dir":
                    path_item = item['dirname']
                    target_item = item['target']
                    self.copy_dir(dirname=path_item, target=target_item)

                elif files_dirs == 'copy_file':
                    path_item = item['filename']
                    target_item = item['target']
                    self.copy_file(filename=path_item, target=target_item)

    def set_cfg_properties(self, **kwargs):
        """Set properties from config file."""
        if Path(kwargs.get('config_file')).is_file():
            # config file
            with open(kwargs.get('config_file'), 'r') as f:
                data = yaml.load(f.read(), Loader=yaml.Loader)
                self.target = data['target'] \
                    if data.get('target') else self.target
                self.db_path = data['db_path'] \
                    if data.get('db_path') else self.db_path
                self.files_and_dirs = data['files_and_dirs'] \
                    if data.get('files_and_dirs') else self.files_and_dirs
                self.env_file = data['env_file'] \
                    if data.get('env_file') else self.env_file
                self.docker_env = data['docker_env'] \
                    if data.get('docker_env') else self.docker_env

    def set_env_properties(self):
        """Set properties from environment variables."""
        # Environment
        self.target = os.getenv("SIMPLEFEED_TARGET") \
            if os.getenv("SIMPLEFEED_TARGET") else self.target
        self.db_path = os.getenv("SIMPLEFEED_DB_PATH") \
            if os.getenv("SIMPLEFEED_DB_PATH") else self.db_path
        self.files_and_dirs = [
            val.strip()
            for val in os.getenv("SIMPLEFEED_FILES_AND_DIRS").split(',')] \
            if os.getenv("SIMPLEFEED_FILES_AND_DIRS") else self.files_and_dirs
        self.env_file = os.getenv("SIMPLEFEED_ENV_FILE") \
            if os.getenv("SIMPLEFEED_ENV_FILE") else self.env_file
        self.docker_env = os.getenv("SIMPLEFEED_DOCKER_ENV") \
            if os.getenv("SIMPLEFEED_DOCKER_ENV") else self.docker_env

    def set_cli_properties(self, **kwargs):
        """Set properties from CLI."""
        # CLI
        self.target = kwargs['target'] \
            if kwargs.get('target') else self.target
        self.db_path = kwargs['db_path'] \
            if kwargs.get('db_path') else self.db_path
        self.files_and_dirs = [
            val.strip() for val in kwargs['files_and_dirs'].split(',')] \
            if kwargs.get('files_and_dirs') else self.files_and_dirs
        self.docker_env = kwargs['docker_env'] \
            if kwargs.get('docker_env') else self.docker_env

    def set_properties(self, **kwargs):
        """
        Define properties depending on source.

        priorities:
            - cli (high priority)
            - environment
            - config file
            - config script (low priority)
        """
        # lowest priority
        self.set_cfg_properties(**kwargs)
        self.set_env_properties()
        # higher priority
        self.set_cli_properties(**kwargs)


def main() -> None:
    """Main function."""
    args = Parser()()
    deploy_feed = DeployFeed()

    # Set environment variable only
    if args.set_env:
        deploy_feed.set_environment('local')
        sys.exit(0)

    # Execute tasks
    if not args.target:
        print("! 'target' path not provided, --target must be set")
        sys.exit(1)

    deploy_feed.set_properties(**args.__dict__)
    prepare_copy = deploy_feed.prepare_copy_files_and_dirs()
    deploy_feed.copy_files_and_dirs(prepare_copy_files_and_dirs=prepare_copy)
    deploy_feed.set_environment()
    deploy_feed.create_docker_env_file()


class Parser:
    """Parser class."""

    def __init__(self):
        """Init."""
        self.exe = basename(argv[0])
        self.parser = ArgumentParser(
            formatter_class=RawDescriptionHelpFormatter,
            description="Deploy tool for simplefeed.cloud.",
            epilog=dedent(f'''\
                examples:
                  Define a path where to copy required data to run apps
                  
                    {self.exe} <path>
            ''')
        )

        self.parser.add_argument(
            '-t', '--target', help='Path where to create bundle')

        self.parser.add_argument(
            '-db', '--db_path',
            help='path where the database file are stored.')

        self.parser.add_argument(
            '-c', '--config_file', default=".",
            help='Define properties in a yaml file.')

        self.parser.add_argument(
            '-fd', '--files_and_dirs', help='List of files and dirs to copy')

        self.parser.add_argument(
            '-e', '--env_file', help='An environment file.')

        self.parser.add_argument(
            '-de', '--docker_env', help='Docker environment file.')

        self.parser.add_argument(
            '--set_env', const=True, nargs='?',
            help='Set environment variables.')

    def __call__(self):
        """Parse arguments."""
        args = self.parser.parse_args()
        return args


if __name__ == '__main__':
    main()
