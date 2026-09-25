def bmi_calculator(weight, height):
    if height <= 0:
        return 0

    bmi = weight / ((height / 100) ** 2)
    return round(bmi, 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"


def bmr_calculator(gender, age, weight, height):
    gender = gender.lower()

    if gender == "male":
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )

    elif gender == "female":
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    else:
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
        )

    return round(bmr, 2)


def tdee_calculator(bmr, activity_level):
    activity_level = activity_level.lower()

    multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }

    multiplier = multipliers.get(activity_level, 1.2)

    return round(bmr * multiplier, 2)


def calorie_target(tdee, goal):
    goal = goal.lower()

    if goal == "lose weight":
        target = tdee - 500

    elif goal == "gain weight":
        target = tdee + 300

    else:
        target = tdee

    return round(target, 2)


def protein_target(weight, goal):
    """
    General wellness estimate.
    Not a medical prescription.
    """

    if goal.lower() == "gain weight":
        multiplier = 1.6

    elif goal.lower() == "lose weight":
        multiplier = 1.6

    else:
        multiplier = 1.2

    return round(weight * multiplier, 1)