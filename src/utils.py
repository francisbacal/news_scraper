import pymongo
import newspaper
import json
import csv
import colorama
import os
import dotenv
import unidecode
from os.path import join
from os.path import dirname
from pymongo import MongoClient
from src.news import News
from src.helpers import bcolors
from colorama import Fore
from dotenv import load_dotenv