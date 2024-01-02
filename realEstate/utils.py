def m2_to_pyung(area):
    """Convert square meters to pyeong"""
    return round(area / 3.305785, 1)


def add_pyung_unit(area):
    """Add '평' to area value"""
    return f"{area}평"
