#!/bin/bash
# Generate gym exercise images with Gemini
API_KEY="REDACTED"
MODEL="gemini-2.5-flash-image"
OUTPUT_DIR="/Users/bond/.openclaw/workspace/drafts/gym"

generate_image() {
  local num="$1"
  local prompt="$2"
  local filename="$3"
  
  echo "Генерирую: $filename..."
  
  response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}" \
    -H 'Content-Type: application/json' \
    -d "{
      \"contents\": [{
        \"parts\": [{\"text\": \"Generate a clear, professional photo-realistic image showing: ${prompt}. The image should be instructional, showing proper form and the gym equipment clearly. Clean gym background, good lighting. No text overlay.\"}]
      }],
      \"generationConfig\": {
        \"responseModalities\": [\"TEXT\", \"IMAGE\"]
      }
    }")
  
  # Extract base64 image
  echo "$response" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
try:
    for part in data['candidates'][0]['content']['parts']:
        if 'inlineData' in part:
            img_data = base64.b64decode(part['inlineData']['data'])
            with open('${OUTPUT_DIR}/${filename}', 'wb') as f:
                f.write(img_data)
            print('OK: ${filename}')
            break
    else:
        print('NO IMAGE in response')
        print(json.dumps(data.get('candidates',[{}])[0].get('content',{}).get('parts',[{}])[0].get('text','no text')[:200]))
except Exception as e:
    print(f'ERROR: {e}')
    print(str(data)[:300])
"
}

mkdir -p "$OUTPUT_DIR"

generate_image 1 "A muscular man performing BARBELL SQUATS in a squat rack at the gym. Standing position with barbell on shoulders, feet shoulder-width apart, demonstrating proper squat form going down. Side view angle" "01_squats.jpg"

generate_image 2 "A man using a LEG PRESS MACHINE at the gym. Seated in the leg press, pushing the platform with feet placed shoulder-width apart. Shows the full machine and proper body positioning. Side angle view" "02_leg_press.jpg"

generate_image 3 "A man using a LEG EXTENSION MACHINE at the gym. Seated in the machine, extending legs forward against the padded roller. Shows the machine clearly and proper form. Side angle" "03_leg_extension.jpg"

generate_image 4 "A man using a LYING LEG CURL MACHINE at the gym. Lying face down on the machine, curling legs up toward glutes against the padded roller. Shows the machine and proper form. Side angle" "04_leg_curl.jpg"

generate_image 5 "A man performing STANDING CALF RAISES on a calf raise machine at the gym. Standing on the platform edge with shoulders under pads, rising up on toes. Shows the machine and proper form" "05_calf_raise.jpg"

echo "Готово!"
