from django_nutrition.models import Preferences


def preferences(request):
    # print(Preferences.current_preferences(request))
    return {"preferences": Preferences.current_preferences(request)}
