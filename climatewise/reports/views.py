from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from .utils.parser import run_parser

def run_parser_api(request):
    if request.method == "POST":
        result = run_parser()
        return JsonResponse(result)
    return JsonResponse({"error":"Only POST allowed"},status=405)


def mongo_reports_api(request):
    client = MongoClient("mongodb+srv://abdoulbin38:w0bsa0IXB7mk2xcH@cluster0.5n02s7c.mongodb.net/climateReportSystemdb?retryWrites=true&w=majority&authSource=admin")
    db = client["climateReportSystem"]
    collection = db["Incoming Messages"]
    collection_2 = db["Processed Messages"]

    reports = []
    for doc in collection.find({"latitude":{"$ne": None}
                                 ,"longitude":{"$ne":None}}):
        reports.append(
                {
                "location":doc.get("location"),
                "incident_type":doc.get("issueType"),
                "time":doc.get("date"),
                "latitude":doc.get("latitude"),
                "longitude":doc.get("longitude")
                }
            )
    return JsonResponse({"reports": reports})

def map_view(request):
    return render(request,'map.html')
'''AIzaSyAsR2JOO3qPTFHVpKUxY-aPWDF2rJ92z-s'''
