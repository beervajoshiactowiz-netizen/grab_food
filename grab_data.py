import json,re
from datetime import datetime
from pydantic import BaseModel
from typing import Dict,List,Any

def load_file(file):
    with open(file,"rb") as f:
        data=json.loads(f.read().decode())
        return data


def parser(data):
    all=[]
    merchant = data.get("merchant", {})

    # Main dictionary
    result = {
        "merchant_id": merchant.get("ID"),
        "name": merchant.get("name"),
        "cuisine": merchant.get("cuisine"),
        "timingEveryday":merchant.get("openingHours").get("sun"),
        "distance": merchant.get("distanceInKm"),
        "ETA": merchant.get("ETA"),
        "rating": merchant.get("rating"),
        "DeliveryBy":merchant.get("deliverBy"),
        "DeliveryOption":merchant.get("deliveryOptions"),
        "VoteCount": merchant.get("voteCount"),
        "Tips": [merchant.get("sofConfiguration").get("tips")],
        "BuisinessType":merchant.get("businessType"),
        "Offers":[],
        "menu": []
    }
    for offers in merchant.get("offerCarousel").get("offerHighlights",[]):
        off={
                "Title": offers.get("highlight").get("title"),
                "SubTitle":offers.get("highlight").get("subtitle")
        }
        result["Offers"].append(off)

    # Build Menu List Category Wise
    for category in merchant.get("menu", {}).get("categories", []):

        category_block = {
            "category_name": category.get("name"),
            "items": []
        }

        for item in category.get("items", []):

            item_block = {
                "item_id": item.get("ID"),
                "name": item.get("name"),
                "description": item.get("description"),
                "price_display": float(item.get("priceV2", {}).get("amountDisplay")),
                "available": item.get("available"),
                "images": item.get("imgHref"),
            }

            category_block["items"].append(item_block)

        result["menu"].append(category_block)
        all.append(result)
    return all
def data_extracted(extracted_data):
    with open(f"Grab_food_{datetime.now().date()}.json","wb") as f:
        f.write(json.dumps(extracted_data, indent=4,ensure_ascii=False).encode())


file_name="grabfood.json"
file_data=load_file(file_name)
extracted=parser(file_data)
data_extracted(extracted)