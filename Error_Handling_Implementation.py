# Ezekiel's part:
# Algorithm customization, error handling, and edge cases

class RouteError(Exception):
    pass


def validate_network_data(network):
    """
    Check if the network data is valid before route search starts.
    Raises RouteError if there is a serious problem.
    """
    if network is None:
        raise RouteError("Network is not loaded.")

    if len(network.stops) == 0:
        raise RouteError("Network has no stops.")

    if len(network.segments) == 0:
        raise RouteError("Network has no segments.")

    for segment in network.segments:
        if segment.duration < 0:
            raise RouteError("Segment has negative duration.")
        if segment.cost < 0:
            raise RouteError("Segment has negative cost.")
        if segment.from_stop not in network.stops:
            raise RouteError("Segment has unknown starting stop.")
        if segment.to_stop not in network.stops:
            raise RouteError("Segment has unknown ending stop.")


def validate_route_query(network, origin, destination, preference):
    """
    Validate user query before generating journeys.
    """
    if origin not in network.stops:
        raise RouteError("Unknown origin stop.")

    if destination not in network.stops:
        raise RouteError("Unknown destination stop.")

    if origin == destination:
        raise RouteError("Origin and destination cannot be the same.")

    valid_preferences = ["cheapest", "fastest", "fewest"]
    if preference not in valid_preferences:
        raise RouteError("Invalid preference mode.")


def validate_custom_settings(settings):
    """
    Validate optional customization settings.
    Example settings:
    {
        'avoid_modes': ['Walk'],
        'max_budget': 20,
        'max_segments': 4,
        'preferred_modes': ['MTR']
    }
    """
    if not isinstance(settings, dict):
        raise RouteError("Customization settings must be a dictionary.")

    if "max_budget" in settings:
        if settings["max_budget"] < 0:
            raise RouteError("max_budget cannot be negative.")

    if "max_segments" in settings:
        if settings["max_segments"] <= 0:
            raise RouteError("max_segments must be at least 1.")

    if "avoid_modes" in settings:
        if not isinstance(settings["avoid_modes"], list):
            raise RouteError("avoid_modes must be a list.")

    if "preferred_modes" in settings:
        if not isinstance(settings["preferred_modes"], list):
            raise RouteError("preferred_modes must be a list.")


def journey_matches_settings(journey, settings):
    """
    Return True if a journey satisfies user customization settings.
    """
    if "max_budget" in settings:
        if journey.total_cost() > settings["max_budget"]:
            return False

    if "max_segments" in settings:
        if journey.number_of_segments() > settings["max_segments"]:
            return False

    if "avoid_modes" in settings:
        for segment in journey.segments:
            if segment.mode in settings["avoid_modes"]:
                return False

    return True


def apply_custom_filter(journeys, settings):
    """
    Keep only journeys that satisfy the user's custom conditions.
    """
    filtered = []

    for journey in journeys:
        if journey_matches_settings(journey, settings):
            filtered.append(journey)

    return filtered


def customization_bonus(journey, settings):
    """
    Lower score is better.
    This function adjusts ranking without replacing the base preference.
    Example: reward routes that use preferred modes.
    """
    bonus = 0

    if "preferred_modes" in settings:
        for segment in journey.segments:
            if segment.mode in settings["preferred_modes"]:
                bonus -= 0.5

    return bonus


def route_score_with_customization(journey, preference, settings):
    """
    Combined scoring:
    - base score depends on user preference
    - then adjusted by customization bonus
    """
    if preference == "cheapest":
        base = journey.total_cost()
    elif preference == "fastest":
        base = journey.total_duration()
    elif preference == "fewest":
        base = journey.number_of_segments()
    else:
        raise RouteError("Invalid preference during scoring.")

    return base + customization_bonus(journey, settings)


def rank_journeys_with_customization(journeys, preference, settings):
    """
    Rank only the valid journeys after filtering.
    """
    valid_journeys = apply_custom_filter(journeys, settings)

    ranked = valid_journeys[:]
    ranked.sort(key=lambda j: route_score_with_customization(j, preference, settings))
    return ranked


def remove_duplicate_journeys(journeys):
    """
    Remove duplicate routes based on stop path.
    """
    unique = []
    seen_paths = []

    for journey in journeys:
        path = tuple(journey.stops_path())
        if path not in seen_paths:
            seen_paths.append(path)
            unique.append(journey)

    return unique


def safe_generate_and_rank(network, origin, destination, preference, settings, generator_function):
    """
    Main wrapper for Ezekiel's part.
    Handles validation, filtering, ranking, and algorithm-related errors.
    """
    try:
        validate_network_data(network)
        validate_route_query(network, origin, destination, preference)
        validate_custom_settings(settings)

        journeys = generator_function(network, origin, destination)

        if len(journeys) == 0:
            return {
                "success": False,
                "message": "No journey found between the selected stops.",
                "journeys": []
            }

        journeys = remove_duplicate_journeys(journeys)
        ranked = rank_journeys_with_customization(journeys, preference, settings)

        if len(ranked) == 0:
            return {
                "success": False,
                "message": "Journeys exist, but none match the customization settings.",
                "journeys": []
            }

        return {
            "success": True,
            "message": "Journeys ranked successfully.",
            "journeys": ranked
        }

    except RouteError as error:
        return {
            "success": False,
            "message": str(error),
            "journeys": []
        }
