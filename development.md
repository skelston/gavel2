# Development

Development happens in the `develop` branch, while the latest stable version is in the `master` branch.

## Setup

The easiest way to get started hacking on Gavel is to use [Docker](https://www.docker.com/). This will containerize the application and its dependencies, ensuring a consistent environment across all machines.

If you really want, you could also manually install stuff on your machine and get Gavel running there.

Also, if you need help with anything, feel free to ask in the [Gitter chat][gitter].

### Docker (Recommended)

Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine with Docker Compose) installed on your machine.

#### 1. Build and Run the Application

The `docker-compose.yml` file defines the application service. To start Gavel:

```bash
# Start the application in the foreground
docker-compose up

# Or, to start it in the background (detached mode)
docker-compose up -d

# Follow the logs if running in detached mode
docker-compose logs -f
```

This command will:
* Build the Docker image defined in the `Dockerfile`.
* Run the container, mapping port **5000** on your host machine to port **5000** inside the container.
* Start the application using the command in the `Dockerfile`.

Now, on your local machine, you should be able to navigate to `http://localhost:5000/` and see Gavel running!

#### 2. Initial Setup (First Time Run)

On the **first run only**, you need to initialize the database. You can do this by executing a command inside the running container:

1.  **Open a new shell** in your terminal.
2.  Find the name of your running container:
    ```bash
    docker-compose ps
    ```
    It will likely be something like `gavel2-web-1`.
3.  Run the initialization script inside the container:
    ```bash
    docker-compose exec web python initialize.py
    ```

You should now be able to go to `http://localhost:5000/admin` and log in with the username "admin" and the password "admin".

#### 3. Development Workflow

*   **Code Changes:** Since your project directory is mounted into the container using the `volumes` directive in `docker-compose.yml`, any changes you make to the source code on your host machine will be immediately reflected inside the container. The Gunicorn server will automatically reload on changes because of the `--reload` flag.
*   **Stopping the Application:**
    ```bash
    # If you started it in the foreground (docker-compose up), use Ctrl+C
    # Otherwise, stop the detached containers
    docker-compose down
    ```

#### 4. Running Commands

To run any other command (e.g., a shell) inside the application container:

```bash
# Get an interactive bash shell inside the running 'web' container
docker-compose exec web bash

# Run a one-off command, like pip install for a new dependency
docker-compose exec web pip install <new-package>

# After adding a new dependency to requirements.txt, rebuild the image
docker-compose build
```

### Manual Setup

This is not the recommended way to do things, so this section isn't super detailed.

* Be using Python 3.9 or later
* Install Postgres
* Do development inside a [virtualenv][virtualenv]
* `pip install -r requirements.txt`
* `cp config.template.yaml config.yaml`
* Edit config file for your setup (ensure it points to a local Postgres instance)
* `python initialize.py`
* `DEBUG=true python gavel.py`

## Tips

* While developing, it's helpful to set the environment variable `DEBUG=true` in your `docker-compose.yml` file to enable more verbose logging and automatic reloading.

* If Gavel's database schema is changed or if the database gets messed up in any way, you can reset everything by **recreating the Docker volumes**. **Warning: This will delete all data.**

    ```bash
    # Stop the containers and delete the persisted database volume
    docker-compose down --volumes

    # Then bring it back up and re-initialize
    docker-compose up -d
    docker-compose exec web python initialize.py
    ```

* This project uses [EditorConfig][editorconfig]. [Download][editorconfig-download] a plugin for your editor!

[gitter]: https://gitter.im/anishathalye/gavel
[virtualenv]: https://virtualenv.pypa.io/en/stable/
[editorconfig]: http://editorconfig.org/
[editorconfig-download]: http://editorconfig.org/#download

---