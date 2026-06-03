# ============================================================
# YANGS GARAGE - Vehicle Market Analyzer v0.8
# Author: Wencong Xie
# Company: ONIONS AUTO LLC
# Project Start: 2026
#
# Description:
# Internal development script for analyzing used vehicle
# inventory, projected profits, rental performance,
# depreciation, and market opportunity scoring.
#
# NOTE:
# This project is still under development.
# Some functions are experimental and may not be finalized.
# ============================================================

import csv
import random
import statistics
from datetime import datetime

# ------------------------------------------------------------
# Vehicle Inventory Dataset
# ------------------------------------------------------------

inventory = [
    {
        "vin": "5YJSA1E26HF000001",
        "brand": "Tesla",
        "model": "Model S",
        "year": 2017,
        "purchase_price": 23800,
        "current_market_price": 26400,
        "mileage": 91200,
        "monthly_bookings": 17,
        "rating": 4.91,
        "maintenance_cost": 1840
    },
    {
        "vin": "4T1BF1FK5HU000002",
        "brand": "Toyota",
        "model": "Camry",
        "year": 2019,
        "purchase_price": 15800,
        "current_market_price": 17950,
        "mileage": 74000,
        "monthly_bookings": 13,
        "rating": 4.88,
        "maintenance_cost": 620
    },
    {
        "vin": "JTDKARFU8K3000003",
        "brand": "Toyota",
        "model": "Prius",
        "year": 2019,
        "purchase_price": 14900,
        "current_market_price": 14100,
        "mileage": 102000,
        "monthly_bookings": 16,
        "rating": 4.80,
        "maintenance_cost": 2150
    },
    {
        "vin": "5YJXCDE22HF000004",
        "brand": "Tesla",
        "model": "Model X",
        "year": 2017,
        "purchase_price": 42900,
        "current_market_price": 47200,
        "mileage": 88300,
        "monthly_bookings": 21,
        "rating": 4.95,
        "maintenance_cost": 3270
    }
]

# ------------------------------------------------------------
# Market Score Calculation
# ------------------------------------------------------------

def calculate_market_score(vehicle):
    """
    Calculates an internal profitability score
    for evaluating fleet expansion opportunities.
    """

    booking_weight = vehicle["monthly_bookings"] * 12
    rating_weight = vehicle["rating"] * 100

    depreciation = (
        vehicle["purchase_price"]
        - vehicle["current_market_price"]
    )

    maintenance_penalty = vehicle["maintenance_cost"] * 0.45

    mileage_penalty = vehicle["mileage"] / 1000

    score = (
        booking_weight
        + rating_weight
        - depreciation
        - maintenance_penalty
        - mileage_penalty
    )

    return round(score, 2)

# ------------------------------------------------------------
# Future Value Projection
# ------------------------------------------------------------

def project_vehicle_value(vehicle, years=3):
    """
    Projects future resale value using simplified
    depreciation assumptions.
    """

    current_value = vehicle["current_market_price"]

    yearly_depreciation_rate = random.uniform(0.08, 0.17)

    projected_values = []

    for year in range(1, years + 1):

        current_value = current_value * (
            1 - yearly_depreciation_rate
        )

        projected_values.append({
            "year": year,
            "estimated_value": round(current_value, 2)
        })

    return projected_values

# ------------------------------------------------------------
# Fleet Analytics
# ------------------------------------------------------------

def generate_fleet_summary(data):

    total_inventory_value = sum(
        car["current_market_price"] for car in data
    )

    average_rating = round(
        statistics.mean(car["rating"] for car in data),
        2
    )

    average_bookings = round(
        statistics.mean(
            car["monthly_bookings"] for car in data
        ),
        2
    )

    return {
        "fleet_value": total_inventory_value,
        "avg_rating": average_rating,
        "avg_monthly_bookings": average_bookings,
        "vehicle_count": len(data)
    }

# ------------------------------------------------------------
# Opportunity Ranking Engine
# ------------------------------------------------------------

def rank_inventory(data):

    ranked = []

    for vehicle in data:

        score = calculate_market_score(vehicle)

        vehicle_copy = vehicle.copy()

        vehicle_copy["market_score"] = score

        ranked.append(vehicle_copy)

    ranked.sort(
        key=lambda x: x["market_score"],
        reverse=True
    )

    return ranked

# ------------------------------------------------------------
# CSV Export
# ------------------------------------------------------------

def export_analysis_to_csv(data, filename):

    fieldnames = [
        "brand",
        "model",
        "year",
        "market_score",
        "monthly_bookings",
        "rating",
        "mileage"
    ]

    with open(filename, "w", newline="") as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in data:

            writer.writerow({
                "brand": row["brand"],
                "model": row["model"],
                "year": row["year"],
                "market_score": row["market_score"],
                "monthly_bookings": row["monthly_bookings"],
                "rating": row["rating"],
                "mileage": row["mileage"]
            })

# ------------------------------------------------------------
# Internal Notes
# ------------------------------------------------------------

development_notes = """
TODO:
- Connect Turo API scraper
- Add California market heatmap
- Integrate dynamic pricing engine
- Add AI demand forecasting
- Compare Bay Area vs Austin utilization
- Add insurance risk scoring
- Improve Tesla battery degradation model
- Add auction price tracking
"""

# ------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("YANGS GARAGE - MARKET ANALYZER")
    print("=" * 60)

    print("\nGenerating Fleet Summary...\n")

    summary = generate_fleet_summary(inventory)

    print(f"Vehicle Count: {summary['vehicle_count']}")
    print(f"Fleet Value: ${summary['fleet_value']}")
    print(f"Average Rating: {summary['avg_rating']}")
    print(
        f"Average Monthly Bookings: "
        f"{summary['avg_monthly_bookings']}"
    )

    print("\nRanking Inventory...\n")

    ranked_inventory = rank_inventory(inventory)

    for idx, car in enumerate(ranked_inventory, start=1):

        print(
            f"{idx}. "
            f"{car['year']} "
            f"{car['brand']} "
            f"{car['model']}"
        )

        print(f"   Score: {car['market_score']}")
        print(f"   Mileage: {car['mileage']}")
        print(f"   Rating: {car['rating']}")
        print(f"   Monthly Bookings: {car['monthly_bookings']}")

        projections = project_vehicle_value(car)

        print("   Future Value Projection:")

        for projection in projections:

            print(
                f"      Year {projection['year']}: "
                f"${projection['estimated_value']}"
            )

        print("-" * 40)

    export_analysis_to_csv(
        ranked_inventory,
        "fleet_analysis.csv"
    )

    print("\nCSV export completed.")

    print("\nDevelopment Notes:")
    print(development_notes)

    print("\nExecution Timestamp:")
    print(datetime.now())

    print("\nSystem run completed.")
