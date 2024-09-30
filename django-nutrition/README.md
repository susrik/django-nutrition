================
django-nutrition
================

django-nutrition is a Django app to track calories

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "nutrition" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_nutrition",
    ]

2. Include the nutrition URLconf in your project urls.py like this::

    path("nutrition/", include("django_nutrition.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and create one or more users.

5. Visit the ``/nutrition/`` URL to manage nutrition information.

to update the style bundle:
npm install
npm run build:css

then commit state/nutrition/styles.css
