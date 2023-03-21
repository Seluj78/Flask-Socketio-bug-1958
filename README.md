# Steps to reproduce:

- Create a 3.11 venv
- Activate it
- `pip install requirements.txt`
- Run `python server.py`
- Open `client.html` in your browser and click `CONNECT`
  - If, inside `client.html`, the query params `token` is equal to `TOKEN`, then the `connect` will succeed (But the disconnect throws an error :/)
  - Else: You will have the OSError.