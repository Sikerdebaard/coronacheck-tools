from coronacheck_tools.verification.idemix import calc_timebased_challenge
from coronacheck_tools import decode_qr
from common import TESTQRPATH



data = decode_qr(TESTQRPATH, 'dict')

print(data)

timestamp = data[0]['aDisclosed']['validFrom']

res = calc_timebased_challenge(timestamp)

print(res)
