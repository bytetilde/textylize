import httpx
import os
import json
KEY = os.environ.get('POLLINATIONS_TOKEN')
HEADERS = {
  'Authorization': f'Bearer {KEY}',
  'Content-Type': 'application/json',
  'User-Agent': 'bytetilde/send 1.0'
}
def send(hist, model='llama-scout', maxtks=0, temperature=1.0, stream=False):
  data = {'model': model, 'messages': hist, 'stream': stream}
  if(maxtks > 0): data['max_tokens'] = maxtks
  data['temperature'] = temperature
  ret = httpx.post('https://gen.pollinations.ai/v1/chat/completions', headers=HEADERS, json=data)
  try: ret.raise_for_status()
  except Exception as e:
    try: print(ret.json())
    except: pass
    raise e
  if(stream): return _parse_stream(ret.iter_lines())
  ret = ret.json()
  resp = ret.get('choices', [{}])[0].get('message', {}).get('content', '')
  if('usage' in ret): print(f'used {ret["usage"].get("total_tokens", 0)} tokens')
  return resp.strip()
def _parse_stream(lines):
  for line in lines:
    if(not line.startswith('data: ')): continue
    payload = line[6:]
    if(payload == '[DONE]'): break
    try:
      chunk = json.loads(payload)
      delta = chunk.get('choices', [{}])[0].get('delta', {})
      content = delta.get('content', '')
      if(content): yield content
    except json.JSONDecodeError: pass
