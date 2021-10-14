from coronacheck_tools.api.denylist import denylist, proof as denylist_proof
from coronacheck_tools.clitools import parse_input, convert

input_path = 'test/testdata/qrtestrevoked.raw'
input_format = 'RAW'

blacklist = denylist()
print('Denylist:')
for k, v in blacklist.items():
    print(f'  {k} -> {v}')
print()

if input_path:
    input_data = parse_input(input_format, input_path)
    data = convert(input_format, input_data, 'JSON')

    if isinstance(data, list) and len(data) > 0:
        # only grab the first QR
        data = data[0]

    if not data or len(data) == 0:
        print(f'No valid QR code found in {input_path}')
    else:
        proof = denylist_proof(data)
        print(f'QR proof: {proof}')
        if proof in blacklist:
            print(f"QR Code present in proof identifier denylist")
        else:
            print(f"QR Code not present in proof identifier denylist")
