# PickMyTech

A minimal gadget decision app for Malaysia. Buildless HTML, CSS and JavaScript; no dependencies or account required.

Run `npm start`, then open http://127.0.0.1:4173. Run `npm run check` to check JavaScript and the recommendation engine.

## Google Cloud Run

The container runs as an unprivileged user and serves only `dist/`. It listens on Cloud Run's `PORT` and shuts down on SIGTERM. No database, API keys or environment secrets are needed.

Deploy with `./scripts/deploy-cloud-run.ps1 -ProjectId workshop-513307`. The script uses service `pickmytech`, region `asia-southeast1` (Singapore), 256 MiB memory, minimum zero instances and maximum two. Public access is enabled so visitors can open the app. Source deployment uses Cloud Build and Artifact Registry; their usage and Cloud Run requests may incur Google Cloud charges. Scaling limits reduce capacity but do not set a spending cap.

Required Google Cloud APIs: Cloud Run (`run.googleapis.com`), Cloud Build (`cloudbuild.googleapis.com`), and Artifact Registry (`artifactregistry.googleapis.com`). Authenticate with the Google Cloud CLI before deploying. Cloud hosting metadata and local credentials are excluded from Git and the deployment upload.

Features: laptops and smartphones, hard RM budget limit, purpose matching, optional brand preference and strict RAM/storage/OS filters, sorting, browser-local saved choices, comparison of up to three devices, English/Bahasa Melayu, larger text, responsive layout and keyboard-accessible native controls.

## Catalogue and pricing

This is a curated catalogue, not a live price or stock feed. Listings were researched on 31 October 2026. Do not imply real-time stock, market-wide coverage, benchmark scores, or the lowest price in Malaysia. Source links are stored on each product in `dist/catalog.mjs`. Update that file and the checked date when refreshing prices. Unconfirmed RAM/storage are `null` and excluded by strict spec filters. Brand preference affects ranking without overriding budget or strict filters. Gaming and coding use minimum suitability requirements. Suitability ratings are editorial.

Sources: [Acer Malaysia laptops](https://store.acer.com/en-my/laptops), [Acer 16GB Aspire range](https://store.acer.com/en-my/laptops/aspire/memory_standard-16_gb), [Apple Malaysia store](https://www.apple.com/my/store), [Apple Malaysia iPhones](https://www.apple.com/my/shop/buy-iphone), [Senheng Galaxy A17](https://www.senheng.com.my/product/samsung-galaxy-a17-5g-8256gb/), [Connect First Xiaomi retailer](https://www.connectfirst-my.com/).

No backend, analytics or personal profiles. Saved choices and language/text preferences stay in localStorage on the current browser. Retailer links open externally. Prices exclude any unverified delivery fees, accessories or conditional discounts.

`scripts/fetch-assets.py` fetches product photographs from the corresponding public product/retailer pages. Images retain their source ownership.
