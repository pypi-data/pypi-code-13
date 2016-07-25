# import alooma_pysdk
#
# INPUT_TOKEN='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnROYW1lIjoic2hlbmRldiIsImlucHV0TGFiZWwiOiJhc2Rhc2QiLCJpbnB1dFR5cGUiOiJQWVRIT05fU0RLIn0.mfQWcDSPb9vswsX4N5LuMvw3tqWG1goBzgXgneClws8'
# alooma_sdk = alooma_pysdk.PythonSDK(INPUT_TOKEN, servers='inputs-dev.alooma.com',
#                                     blocking=True)
#
# for i in range(1000000):
#     alooma_sdk.report({'num':i, 'text': str(i), 'batch': 0})
#
# import time
# time.sleep(100)
#
# for i in range(1000000):
#     alooma_sdk.report({'num':i, 'text': str(i), 'batch': 1})
