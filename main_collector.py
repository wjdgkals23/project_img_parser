from bing_image import BingCollector
from class_google import Collector

collector = BingCollector()
keyword = input("Please input keyword : ")
collector.collectImage(str(keyword))