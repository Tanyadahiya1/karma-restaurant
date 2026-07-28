from app import create_app

app = create_app()
client = app.test_client()
with client.session_transaction() as sess:
    sess['cart'] = {'1': 1}
resp = client.get('/checkout')
print('STATUS', resp.status_code)
data = resp.data.decode('utf-8', errors='replace')
print('LENGTH', len(data))
print('\n---START-HTML---\n')
print(data[:4000])
print('\n---END-HTML---\n')
