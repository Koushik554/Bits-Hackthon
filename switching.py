def decide(demand_kw: float, hour: int) -> dict:
    is_evening = (18 <= hour <= 22)
    is_critical = (demand_kw >= 200)
    if demand_kw > 160 or is_evening:
        mode = "Renewable Storage Mode"
    else:
        mode = "Main Grid Mode"
    return {"mode": mode, "overload": is_critical}

if __name__ == "__main__":
    assert decide(160, 10)["mode"] == "Main Grid Mode"
    assert decide(160.01, 10)["mode"] == "Renewable Storage Mode"
    assert decide(100, 18)["mode"] == "Renewable Storage Mode"
    assert decide(100, 22)["mode"] == "Renewable Storage Mode"
    assert decide(100, 23)["mode"] == "Main Grid Mode"
    assert decide(199.9, 10)["overload"] is False
    assert decide(200, 10)["overload"] is True
    print("all good")
