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
import subprocess
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import path
from os.path import basename
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import List, Dict
from alembic.config import Config
from alembic import command

import yaml

PATH = Path(__name__).resolve().parent


class DeployFeed:
    """Deploy simple-feed.cloud apps."""

    target = None
    customize = {
        "bundle": ['alembic', 'deploy/docker-compose.yml', 'deploy/Dockerfile',
                   'deploy/run.sh', 'deploy/env.yml', 'src', 'templates',
                   'alembic.ini', 'main.py', 'requirements.txt'],
        "exec": [],
        "env": "env.yml",
        "docker_env": ".env"
    }

    def create_migration(self):
        """"""
        alembic_cfg = Config("/path/to/yourapp/alembic.ini")

    def get_env(self) -> Dict[str, str]:
        """
        Set environment variable.

        Returns:
            Environment variables
        """
        with open(str(self.target / self.customize['env']), 'r') as f:
            return yaml.load(f.read(), Loader=yaml.Loader)

    def set_environment(self) -> None:
        """
        Set environment variable.

        Returns:
            Environment variables
        """
        for k, v in self.get_env().items():
            os.environ[k] = str(v)

    def create_docker_env_file(self):
        """
        Create environment file.

        Returns:
            None
        """
        with open(str(self.target / self.customize['docker_env']), 'w') as f:
            for k, v in self.get_env().items():
                f.write(f"{k}={v}\n")

    @staticmethod
    def run_task(tasks: List[str]):
        """
        Run tasks

        Args:
            tasks: a List of arg

        Returns:
            None
        """
        try:
            r = subprocess.run(tasks)
            if r.returncode != 0:
                raise FileNotFoundError(f"{tasks}: No such file or directory, "
                                        f"err: {r.returncode}")
        except FileNotFoundError as exc:
            print(f"[!] {exc}")
            sys.exit(2)

    def run_tasks(self):
        for task in self.customize['exec']:
            tasks = []
            if task.get('pre', None):
                tasks.append(task['pre'])

            tasks.append(task['task'])

            print(f"exec task {tasks}")
            self.run_task(tasks=tasks)

    @staticmethod
    def create_dir(dirname: Path):
        """
        Create a directory.

        Args:
            dirname: directory (full path)

        Returns:
            None
        """
        try:
            print(f"create directory '{dirname}'")
            dirname.mkdir(parents=True)
            print(f"successfully created!")
        except PermissionError as exc:
            print(f"[!] Unable to create directory '{dirname}' {exc}")
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
        try:
            print(f"copy directory '{dirname}' to '{target}'")
            shutil.copytree(src=str(dirname), dst=str(target), symlinks=False,
                            ignore=None, copy_function=shutil.copy2,
                            ignore_dangling_symlinks=False,
                            dirs_exist_ok=True)
            print(f"successfully copied!")
        except PermissionError as exc:
            print(f"[!] Unable to copy directory '{dirname}' to '{target}' "
                  f"{exc}")
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
        try:
            print(f"copy file '{filename}' to '{target}'")
            shutil.copy(src=str(filename), dst=str(target))
            print(f"successfully copied!")
        except FileNotFoundError as exc:
            print(f"[!] Unable to copy file '{filename}' to '{target}' {exc}")
            sys.exit(1)

    def copy_files_and_dirs(self):
        """Copy files and directories."""
        if not self.target.is_dir():
            self.create_dir(dirname=self.target)

        for item in self.customize['bundle']:

            path_item = PATH / item

            if path_item.is_dir():
                target_item = self.target / item
                self.copy_dir(dirname=path_item, target=target_item)

            elif path.isfile(path_item):
                target_item = self.target
                self.copy_file(filename=path_item, target=target_item)

            else:
                print(f"[!] not exist => {path_item}")


def main() -> None:
    """Main function."""
    args = Parser()()
    deploy_feed = DeployFeed()

    if args.path:
        deploy_feed.target = Path(args.path[0])

    # Execute tasks
    deploy_feed.copy_files_and_dirs()
    deploy_feed.run_tasks()
    deploy_feed.set_environment()
    deploy_feed.create_docker_env_file()
    deploy_feed.create_migration()


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
            'path', nargs='+', type=str, help='Path where to create bundle')

    def __call__(self):
        """Parse arguments."""
        args = self.parser.parse_args()
        return args


if __name__ == '__main__':
    main()
