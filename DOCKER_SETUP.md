# Ipswich Retail — Docker development stage

## What this adds

- A Docker image based on supported Python 3.12 (Mac Python 3.9 is unchanged)
- Django 5.2 from the repository's `requirements.txt`
- A reproducible container that runs migrations and adds demo products
- A local HTTP `/health/` check visible through `docker compose ps`

**Not production-ready:** this setup intentionally uses Django `runserver`, DEBUG=true,
SQLite inside the container, and the starter's development secret. Do not deploy this
Compose configuration to a public host. Container replacement will reset SQLite data.

## Installation and usage on macOS

1. Install/start Docker Desktop or another compatible Docker Engine + Compose setup.
2. Put `Dockerfile`, `.dockerignore`, and `compose.yaml` in the same folder as `manage.py`.
3. In PyCharm Terminal, enter the Django project folder:

   ```bash
   cd /Users/edmund/Documents/Ipswich_Retail_Django
   docker --version
   docker compose version
   docker info
   ```

4. Check your earlier fix to `shop/tests.py` is present:

   ```python
   self.assertRedirects(
       self.client.post(checkout, data),
       reverse('shop:basket'),
       fetch_redirect_response=False,
   )
   ```

5. Build and run the development container:

   ```bash
   docker compose up --build
   ```

   Keep this terminal open. Visit http://localhost:8000/ and http://localhost:8000/health/.
   If your Mac Python server is still running on port 8000, stop it with Ctrl+C first.

6. In a **second** PyCharm Terminal (from the same folder):

   ```bash
   docker compose ps
   docker compose exec web python --version
   docker compose exec web python -m django --version
   docker compose exec web python manage.py check
   docker compose exec web python manage.py test
   docker compose logs --tail=50 web
   ```

7. Stop the running environment using Ctrl+C in the first Terminal, then:

   ```bash
   docker compose down
   ```

   Do not use `docker compose down -v` as a casual cleanup command on future projects
   with persistent volumes.

8. Once all tests succeed, commit these three files:

   ```bash
   git status
   git add Dockerfile .dockerignore compose.yaml
   git commit -m "Add reproducible Django Docker development environment"
   git push
   ```

## Screenshots for Component 2

- Docker build success from `docker compose up --build`
- App displayed at `http://localhost:8000`
- `docker compose ps` with service status `healthy` (wait ~30–60 seconds)
- `docker compose exec web python manage.py test` showing all 11 tests passing
- `/health/` JSON response

## Failure checklist

- `docker: command not found` → install Docker Desktop/Engine first
- `Cannot connect to the Docker daemon` → start Docker Desktop and retry `docker info`
- `port is already allocated` → stop the Mac Django server with Ctrl+C
- CI tests fail → check `shop/tests.py` has the redirect assertion fix
- `no such service: web` → run commands from the project folder containing `compose.yaml`
- `Django is not importable` **on Mac** → no impact on the Docker image: it installs Django inside Python 3.12
