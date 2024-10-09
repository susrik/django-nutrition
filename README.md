# django-nutrition

django-nutrition is a Django app to track calories

## Quick start

1. Add "nutrition" to your INSTALLED_APPS setting like this:
   ```python
   INSTALLED_APPS = [
       ...,
       "django_nutrition",
   ]
   ```

2. Include the nutrition URLconf in your project urls.py like this
   ```python
   path("nutrition/", include("django_nutrition.urls")),
   ```
3. Run `python manage.py migrate` to create the models.

4. Start the development server and create one or more users.

5. Visit the `/nutrition/` URL to manage nutrition information.

## Dev Notes

to update the style bundle, from within the `django_nutrition` directory:
```bash
npm install
npm run build:css
```

then commit `django_nutrition/state/nutrition/styles.css`
