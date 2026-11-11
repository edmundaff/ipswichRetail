# Ipswich Retail - GitHub Actions CI setup

## Before enabling CI

Ensure the checkout redirect test is fixed in `shop/tests.py` by replacing:

```python
self.assertRedirects(self.client.post(checkout, data), reverse('shop:basket'))
```

with:

```python
self.assertRedirects(
    self.client.post(checkout, data),
    reverse('shop:basket'),
    fetch_redirect_response=False,
)
```

The original test follows the redirect and consumes the one-time session confirmation before the subsequent assertion. Save the source file and rebuild the Docker image:

```bash
cd /Users/edmund/Documents/Ipswich_Retail_Django
docker compose up -d --build
docker compose exec web python manage.py test
```

Expected: 11 tests run; OK.

## Install the workflow into the existing project

Extract the ZIP **directly into the Django project root**, beside `manage.py`. After extraction the workflow must be at:

```
Ipswich_Retail_Django/.github/workflows/ci.yml
```

Verify:

```bash
ls -la .github/workflows/ci.yml
```

## Commit application, Docker, and CI files

Don't stage missing `START_ON_MAC.command` or an unnecessary duplicate `Docker_Files/` folder.

```bash
cd /Users/edmund/Documents/Ipswich_Retail_Django
git rev-parse --show-toplevel
git add shop/ docs/ README.md Dockerfile .dockerignore compose.yaml DOCKER_SETUP.md .github/workflows/ci.yml
git status
git diff --cached --stat
```

Check you are not staging `.venv/`, `.env`, `db.sqlite3`, secrets or duplicate `Docker_Files/`.

```bash
git commit -m "Add storefront, Docker setup, and GitHub Actions CI"
git push
```

## Inspect results

Open `https://github.com/edmundaff/ipswichRetail/actions`, select **Ipswich Retail CI** and open the latest run.

Expected green jobs: `Django checks and unit tests`; `Build and smoke-test Docker image`.

Take screenshots of the workflow overview, completed jobs, tests and Docker checks.

## Troubleshooting

* `ModuleNotFoundError: No module named shop`: ensure `shop/` was committed and pushed.
* `Dockerfile: no such file`: ensure `Dockerfile`, `.dockerignore`, and `requirements.txt` are committed in repository root.
* Checkout test assertion fails: apply the change above, save `shop/tests.py`, then commit and push the fix.
* Workflow not showing: verify `.github/workflows/ci.yml` exists on GitHub's `main` branch and repository Actions are enabled.

Note: This is **continuous integration (CI)**. It does **not** automatically deploy a production application. Production deployment/CD is a separate stage.
