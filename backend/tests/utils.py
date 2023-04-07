from time import sleep
from typing import Callable

import docker
from docker.models.containers import Container


class Storage:
    """Storage for passing objects between functions."""

    confirm_link = "No link"


class Users:
    """Samples of different types of users."""

    user_1 = {
        "email": "user1@mail.ru",
        "password": "password1",
    }
    user_2 = {
        "email": "user2@mail.ru",
        "password": "password2",
        "user_type": 1,
    }
    owner_1 = {
        "email": "teacher1@gmail.com",
        "password": "password1",
        "user_type": 2,
    }
    owner_2 = {
        "email": "teacher2@gmail.com",
        "password": "password2",
        "user_type": 2,
    }


class Docker:
    """Running and managing Docker containers for testing."""

    def __init__(
        self,
        redis_name: str = "redis_test",
        redis_port: int = 6379,
        postgres_name: str = "postgres_test",
        postgres_port: int = 5432,
        postgres_user: str = "postgres",
        postgres_password: str = "postgres",
    ) -> None:
        self.redis_name = redis_name
        self.redis_port = redis_port
        self.postgres_name = postgres_name
        self.postgres_port = postgres_port
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.containers: list[Container] = []
        self.client = docker.from_env()

        for _ in range(5):
            if self.client.ping():
                break
            sleep(1)
        else:
            raise ConnectionError("no connection to docker")

        for container in self.client.containers.list():
            container: Container
            if container.name == redis_name or container.name == postgres_name:
                container.stop()
                container.wait()

    def _check_running_container(self, container: Container) -> None:
        """Make sure the container status is running.
        Time limit for checking is near `1.5 sec`.

        #### Args:
        - container (Container):
            Container for checking.

        #### Raises:
        - ConnectionError:
            Time limit for checking is out.
        """
        for _ in range(5):
            if container.status == "running":
                break
            sleep(0.3)
            container.reload()
        else:
            raise ConnectionError(f"{container.name} is not running")
        return None

    def _check_running_containers(self) -> None:
        """Check the status of all containers."""
        for container in self.containers:
            self._check_running_container(container)
        return None

    def _run_redis(self) -> None:
        """Run container with `Redis` database.."""
        redis: Container = self.client.containers.run(
            image="redis:7.0-alpine",
            name=self.redis_name,
            ports={6379: self.redis_port},
            auto_remove=True,
            detach=True,
        )
        self.containers.append(redis)
        return None

    def _run_postgres(self) -> None:
        """Run container with `Postgres` database.."""
        postgres: Container = self.client.containers.run(
            image="postgres:15-alpine",
            name=self.postgres_name,
            environment={"POSTGRES_PASSWORD": self.postgres_password},
            ports={5432: self.postgres_port},
            auto_remove=True,
            detach=True,
        )
        self.containers.append(postgres)
        return None

    def stop_all(self) -> None:
        """Stop all containers associated with the `Doker` instance."""
        for container in self.containers:
            container.stop()
            container.wait()
        return None

    def run_all(self) -> None:
        """Run all containers associated with the `Doker` instance."""
        self.stop_all()
        self._run_postgres()
        self._run_redis()
        self._check_running_containers()
        return None


def mock_send_confirm_link() -> Callable:
    """Replacing the app function for sending emails with confirmation links.

    #### Returns:
    - Callable:
        Mock function for sending emails with confirmation links.
    """

    def save_confirm_link(email: str, confirm_link: str) -> None:
        Storage.confirm_link = confirm_link

    return save_confirm_link
