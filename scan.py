import cv2
from flask import Flask, jsonify
from gpiozero import LED
import numpy as np
import os
from picamera2 import Picamera2
import threading


# Define ranks and suits for template matching
ranks = ["ace", "king", "queen", "jack", 10, 9, 8, 7, 6, 5, 4, 3, 2]
suits = ["spades", "hearts", "diamonds", "clubs"]
templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "cards")

ir_led = LED(18)


# Scan through templateDir
def readTemplates():
    templates = {}
    for suit in suits:
        for rank in ranks:
            path = f"{templateDir}/{rank}_of_{suit}.png"
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                templates[(rank, suit)] = img
    return templates

templates = readTemplates()


# Initialize video capture
picam = Picamera2()
config = picam.create_video_configuration(main={"size": (1280, 720)}, format="BGR888")
picam.configure(config)
picam.start()

picam.set_controls({"AnalogueGain": 10, "ExposureTime": 10000})

scannedCards = []

THRESHOLD = 0.80

cardPresent = False

def scanLoop():
    global cardPresent

    ir_led.on()

    while True:
        frame = picam.capture_array()
        if frame is None:
            break

        # Grayscale + blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)


        # Threshold + find card contours
        thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
          continue


        # Largest contour = the card
        cardContour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cardContour)
        cardRoi = gray[y : y + h, x : x + w]


        # Match template against card region
        bestScore = 0
        bestKey = None
        for (rank, suit), tmpl in templates.items():
            if tmpl.shape[0] > cardRoi.shape[0] or tmpl.shape[1] > cardRoi.shape[1]:
                    continue
            result = cv2.matchTemplate(cardRoi, tmpl, cv2.TM_CCOEFF_NORMED)
            _, maxVal, _, _ = cv2.minMaxLoc(result)
            if maxVal > bestScore:
                bestScore = maxVal
                bestKey = (rank, suit)


        # If adequately confident, record the card
        if bestKey and bestScore >= THRESHOLD:
            filename = f"{bestKey[0]}_of_{bestKey[1]}.png"
            if not cardPresent:
                scannedCards.append(filename)
                print(f"Scanned: {filename}")
            cardPresent = True
        else:
            cardPresent = False
    ir_led.off()
    picam.close()


app = Flask(__name__)

@app.route("/cards", methods=["GET"])
def apiGetCards():
    return jsonify({"cards": scannedCards, "total": len(scannedCards)})


@app.route("/reset", methods=["POST"])
def apiResetCards():
    scannedCards.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    t = threading.Thread(target=scanLoop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)