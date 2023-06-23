from flask import Flask, render_template, request, redirect
import json, sys
import urllib.request, requests

app = Flask(__name__)