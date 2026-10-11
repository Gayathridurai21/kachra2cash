import json, os, base64, boto3

br = boto3.client("bedrock-runtime")
tbl = boto3.resource("dynamodb").Table(os.environ["TABLE"])
KEYS = "news card pet hard pouch iron alu copper glass cloth book tetra steel phone appl batt bulb med paint food flower shell pad".split()


def res(code, body):
    return {"statusCode": code, "body": json.dumps(body, default=int), "headers": {"Content-Type": "application/json"}}


def handler(event, _):
    path = event.get("rawPath", "")
    try:
        body = json.loads(event.get("body") or "{}")
        if path.endswith("/scan"):
            return scan(body)
        if path.endswith("/lane"):
            return lane(body)
        if path.endswith("/leaderboard"):
            return board()
    except Exception as e:
        print("error", e)
        return res(500, {"error": "failed"})
    return res(404, {})


def scan(b):
    img = base64.b64decode(b["image"])
    if len(img) > 3_000_000:
        return res(413, {"error": "image too large"})
    prompt = ("Identify the main household waste item in this photo. Reply with ONLY JSON like "
              '{"key":"<one of %s, or unknown>"}' % KEYS)
    r = br.converse(
        modelId=os.environ["MODEL_ID"],
        messages=[{"role": "user", "content": [{"image": {"format": "jpeg", "source": {"bytes": img}}}, {"text": prompt}]}],
        inferenceConfig={"maxTokens": 50, "temperature": 0},
    )
    txt = r["output"]["message"]["content"][0]["text"]
    try:
        k = json.loads(txt[txt.index("{"):txt.rindex("}") + 1]).get("key")
    except Exception:
        k = None
    return res(200, {"key": k if k in KEYS else "unknown"})


def lane(b):
    tbl.put_item(Item={"lane": str(b["lane"])[:40], "pts": min(int(b.get("pts", 0)), 100000), "hh": min(int(b.get("hh", 1)), 1000)})
    return res(200, {"ok": True})


def board():
    items = sorted(tbl.scan(Limit=100)["Items"], key=lambda i: -i["pts"])
    return res(200, [{"lane": i["lane"], "pts": int(i["pts"])} for i in items[:10]])
