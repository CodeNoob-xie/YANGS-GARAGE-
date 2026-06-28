"""
==============================================================
YANGS GARAGE
Vehicle Purchase Decision Engine
Version: 0.2.0 (Development)

Author: Vincent
Company: ONIONS AUTO LLC

Description:
Internal tool used for evaluating auction vehicles before
purchase. The scoring model estimates profitability,
utilization potential and investment risk.

Status:
[IN DEVELOPMENT]
Several scoring parameters are still being calibrated.
==============================================================
"""

from datetime import datetime
import statistics

# -------------------------------------------------------------
# Sample Inventory Candidates
# TODO:
# Connect with future auction scraper
# -------------------------------------------------------------

auction_inventory = [

    {
        "stock_id": "A1001",
        "brand": "Toyota",
        "model": "Mirai",
        "year": 2021,
        "auction_price": 6900,
        "estimated_market_value": 11200,
        "mileage": 67000,
        "expected_monthly_bookings": 23,
        "hydrogen_incentive": True
    },

    {
        "stock_id": "A1002",
        "brand": "Tesla",
        "model": "Model 3",
        "year": 2020,
        "auction_price": 21900,
        "estimated_market_value": 25700,
        "mileage": 81000,
        "expected_monthly_bookings": 19,
        "hydrogen_incentive": False
    },

    {
        "stock_id": "A1003",
        "brand": "Toyota",
        "model": "Camry",
        "year": 2021,
        "auction_price": 14800,
        "estimated_market_value": 18100,
        "mileage": 52000,
        "expected_monthly_bookings": 16,
        "hydrogen_incentive": False
    },

    {
        "stock_id": "A1004",
        "brand": "Hyundai",
        "model": "Nexo",
        "year": 2022,
        "auction_price": 8300,
        "estimated_market_value": 13800,
        "mileage": 49000,
        "expected_monthly_bookings": 20,
        "hydrogen_incentive": True
    }

]

# -------------------------------------------------------------
# Profit Estimation
# -------------------------------------------------------------

def estimate_profit(vehicle):

    gross_margin = (
        vehicle["estimated_market_value"]
        - vehicle["auction_price"]
    )

    return gross_margin


# -------------------------------------------------------------
# Utilization Score
# -------------------------------------------------------------

def utilization_score(vehicle):

    score = (
        vehicle["expected_monthly_bookings"] * 5
    )

    if vehicle["mileage"] < 60000:
        score += 15

    if vehicle["hydrogen_incentive"]:
        score += 12

    return score


# -------------------------------------------------------------
# Risk Model
# -------------------------------------------------------------

def investment_risk(vehicle):

    risk = 100

    if vehicle["mileage"] > 90000:
        risk -= 25

    if vehicle["auction_price"] > 20000:
        risk -= 18

    if vehicle["expected_monthly_bookings"] > 20:
        risk += 10

    return risk


# -------------------------------------------------------------
# Overall Purchase Score
# -------------------------------------------------------------

def calculate_purchase_score(vehicle):

    profit = estimate_profit(vehicle)

    utilization = utilization_score(vehicle)

    risk = investment_risk(vehicle)

    score = (
        profit * 0.03
        + utilization
        + risk
    )

    return round(score,2)


# -------------------------------------------------------------
# Ranking Engine
# -------------------------------------------------------------

ranked = []

for car in auction_inventory:

    car["estimated_profit"] = estimate_profit(car)

    car["purchase_score"] = calculate_purchase_score(car)

    ranked.append(car)

ranked.sort(
    key=lambda x: x["purchase_score"],
    reverse=True
)


# -------------------------------------------------------------
# Statistics
# -------------------------------------------------------------

scores = [
    x["purchase_score"]
    for x in ranked
]

average_score = round(
    statistics.mean(scores),
    2
)

best_vehicle = ranked[0]


# -------------------------------------------------------------
# Console Output
# -------------------------------------------------------------

print("="*60)
print("YANGS GARAGE PURCHASE ENGINE")
print("="*60)

print()

for car in ranked:

    print(
        f"{car['brand']} {car['model']} ({car['year']})"
    )

    print(
        f" Auction Price : ${car['auction_price']}"
    )

    print(
        f" Market Value  : ${car['estimated_market_value']}"
    )

    print(
        f" Expected Profit : ${car['estimated_profit']}"
    )

    print(
        f" Purchase Score : {car['purchase_score']}"
    )

    print("-"*50)

print()

print("Average Score:", average_score)

print(
    "Top Recommendation:",
    best_vehicle["brand"],
    best_vehicle["model"]
)

print()

print("Execution Time:", datetime.now())

# -------------------------------------------------------------
# Development Notes
# -------------------------------------------------------------

"""
TODO LIST

[ ] Connect Copart auction API
[ ] Connect Manheim inventory
[ ] Add battery degradation prediction
[ ] Add Toyota hydrogen incentive database
[ ] Add Carfax history parser
[ ] Add AI purchase recommendation model
[ ] Export recommendation to CSV
[ ] Integrate future pricing engine

Known Issues

- Mileage weighting needs adjustment
- Risk score currently hard coded
- Future rental income estimation unfinished

Next Sprint

Develop automated resale analysis module.
"""