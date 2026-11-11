# Evidence checklist for Component 2 (capture your own work)

These are **suggested** screenshots to take **after you have run and implemented the steps yourself**. Do not claim that future DevOps features are already implemented.

1. **Home page** — `http://127.0.0.1:8000/`: show a polished storefront with featured products.
2. **Django product catalogue** — `/shop/`: search, category filtering and the list of products.
3. **Django MVT** — open `shop/models.py`, `shop/views.py` and `shop/templates/shop/` in your editor; combine as one clearly labelled screenshot if useful.
4. **Product details** — `/shop/slow-morning-mug/`: product description, price, stock and Add to Basket.
5. **Basket** — `/basket/`: items, totals and simulated checkout form.
6. **Demo order persisted** — `/admin/shop/order/` (after creating a superuser and placing a test order): show the created record **without revealing customer personal data**.
7. **Automated tests** — capture `python manage.py test shop` after running them on your Mac; include the command, outcome and test count.
8. **Health endpoint** — `/health/`: show the JSON response.
9. **GitHub (next phase)** — repository, branches, pull requests and review history after you create the repo.
10. **CI/CD, container and monitoring (later phases)** — capture successful and intentionally failing steps only after they really exist.

Save these in a dedicated evidence folder on your Mac. Include dates, tool versions, any errors you encountered and how you resolved them in your lab journal/report notes.
