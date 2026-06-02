# Development notes

These notes are for contributors working on the site locally.

## Local static site preview

From the repository root:

```bash
cd public
python3 -m http.server 8080
```

Then open `http://localhost:8080` in a browser.

The public site is deployed through GitHub Pages from the `public/` directory. Keep public-facing README content focused on the project, governance, contribution process, and live deployment rather than local preview instructions.
