# ♻️ Kachra2Cash

**India's waste economy engine.** Turn household recyclables into pooled, lane-level income, in the user's own language.

🔗 **Live demo:** [ADD YOUR LIVE LINK]
🎥 **Demo video:** [ADD YOUR YOUTUBE LINK]

## Problem
Waste isn't only a collection problem, it's an **incentive problem**. Kabadiwalas skip small loads, people don't know the right bin or the value of what they throw, and hazardous items (batteries, CFLs, medicines) end up in normal bins.

## Solution
1. **Smart lookup** (type or voice) for common Indian household items in **English, Hindi and Tamil**: correct bin colour, ₹/kg value, CO₂ saved, reuse tip.
2. **City price radar**: rates scale for Coimbatore, Chennai, Delhi NCR, Mumbai, Bengaluru, Hyderabad, Kolkata, Jaipur.
3. **Lane Pool planner**: pool recyclables with neighbours to cross a pickup minimum, forecast monthly lane earnings, and send a one-tap WhatsApp pickup request.
4. **Which-bin game** to build segregation habits, with levels and daily streaks.
5. **Impact dashboard**: kg diverted, ₹ recovered, CO₂ saved, car-km avoided, 7-day chart, WhatsApp share.

## Why it works across India
Single HTML file, no login, no install, works **offline**, runs on low-end phones, data stays on device, uses WhatsApp for sharing.

## Tech
Vanilla HTML/CSS/JS, localStorage, Web Speech API (voice). No backend, no tracking.

## Run locally
Open `index.html` in any browser.

## Limitations (honest)
- Rates are indicative averages, not live market prices.
- Leaderboard lanes and lane forecasts are sample/estimated data.
- Text and voice lookup only, no photo recognition yet.

## Roadmap
Photo recognition with a vision model, live rates from partner kabadiwalas, real society accounts, more regional languages, municipal dashboard.

## AWS architecture
Browser (static app on **AWS Amplify Hosting**) → **Amazon API Gateway (HTTP API)** → **AWS Lambda (Python)** → **Amazon Bedrock** (photo-based waste recognition) and **Amazon DynamoDB** (lane leaderboard). Infrastructure is defined as code in `template.yaml` and deployed with the open-source **AWS SAM CLI**; Lambda uses the open-source **boto3** SDK. API throttling is enabled to control cost.

### Deploy backend
```bash
sam build && sam deploy --guided --region us-east-1
# copy the ApiUrl output into `const API=""` in index.html, then push
```
